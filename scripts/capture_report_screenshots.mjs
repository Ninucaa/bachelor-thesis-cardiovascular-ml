#!/usr/bin/env node
import fs from "node:fs/promises";

const OUTPUT_DIR = new URL("../docs/screenshots/", import.meta.url);
const FRONTEND_URL = "http://127.0.0.1:5173/";
const SWAGGER_URL = "http://127.0.0.1:8765/docs";
const CDP_PAGE_LIST_URL = "http://127.0.0.1:9222/json/list";

let nextId = 1;

async function connectCdp() {
  const pages = await fetch(CDP_PAGE_LIST_URL).then((response) => response.json());
  const page = pages.find((item) => item.type === "page");
  if (!page?.webSocketDebuggerUrl) throw new Error("No Chrome page target found");
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  const pending = new Map();

  ws.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (!message.id) return;
    const callbacks = pending.get(message.id);
    if (!callbacks) return;
    pending.delete(message.id);
    if (message.error) callbacks.reject(new Error(message.error.message));
    else callbacks.resolve(message.result);
  });

  await new Promise((resolve, reject) => {
    ws.addEventListener("open", resolve, { once: true });
    ws.addEventListener("error", reject, { once: true });
  });

  return {
    send(method, params = {}) {
      const id = nextId++;
      ws.send(JSON.stringify({ id, method, params }));
      return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
    },
    close() {
      ws.close();
    },
  };
}

async function wait(ms) {
  await new Promise((resolve) => setTimeout(resolve, ms));
}

async function evaluate(cdp, expression, awaitPromise = true) {
  const result = await cdp.send("Runtime.evaluate", {
    expression,
    awaitPromise,
    returnByValue: true,
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.text || "Runtime evaluation failed");
  }
  return result.result?.value;
}

async function waitFor(cdp, expression, timeoutMs = 15000) {
  const startedAt = Date.now();
  while (Date.now() - startedAt < timeoutMs) {
    const ok = await evaluate(cdp, expression);
    if (ok) return;
    await wait(250);
  }
  throw new Error(`Timed out waiting for: ${expression}`);
}

async function navigate(cdp, url) {
  await cdp.send("Page.navigate", { url });
  await waitFor(cdp, "document.readyState === 'complete'");
  await wait(800);
}

async function screenshot(cdp, filename) {
  const data = await cdp.send("Page.captureScreenshot", {
    format: "png",
    captureBeyondViewport: false,
  });
  await fs.writeFile(new URL(filename, OUTPUT_DIR), Buffer.from(data.data, "base64"));
}

async function main() {
  await fs.mkdir(OUTPUT_DIR, { recursive: true });
  const cdp = await connectCdp();
  try {
    await cdp.send("Page.enable");
    await cdp.send("Runtime.enable");
    await cdp.send("Emulation.setDeviceMetricsOverride", {
      width: 1440,
      height: 1100,
      deviceScaleFactor: 1,
      mobile: false,
    });

    await navigate(cdp, FRONTEND_URL);
    await waitFor(cdp, "Boolean(document.querySelector('#predict-button'))");
    await waitFor(cdp, "document.querySelector('#ecg-note')?.value?.length > 0");
    await evaluate(cdp, "window.scrollTo(0, 0)");
    await wait(300);
    await screenshot(cdp, "01-main-frontend.png");

    await evaluate(cdp, "document.querySelector('#ecg-note')?.scrollIntoView({ block: 'center' })");
    await wait(300);
    await screenshot(cdp, "02-filled-form-ecg-temperature.png");

    await evaluate(cdp, "document.querySelector('#predict-button')?.click()");
    await waitFor(cdp, "Boolean(document.querySelector('.patient-report'))", 30000);
    await evaluate(cdp, "window.scrollTo(0, 0)");
    await wait(500);
    await screenshot(cdp, "03-prediction-result.png");

    await evaluate(cdp, "document.querySelector('#toggle-diagnoses-button')?.click()");
    await evaluate(cdp, "document.querySelector('.diagnosis-list')?.scrollIntoView({ block: 'center' })");
    await wait(500);
    await screenshot(cdp, "04-diagnosis-cards.png");

    await evaluate(cdp, "document.querySelector('#lab-reference-button')?.click()");
    await waitFor(cdp, "Boolean(document.querySelector('.reference-window'))");
    await wait(300);
    await screenshot(cdp, "05-lab-bmi-reference.png");
    await evaluate(cdp, "document.querySelector('#close-lab-reference')?.click()");
    await wait(300);

    await evaluate(cdp, "document.querySelector('#model-trust-button')?.click()");
    await waitFor(cdp, "Boolean(document.querySelector('#model-trust-overlay .reference-window'))");
    await wait(300);
    await screenshot(cdp, "06-model-technical-evaluation.png");

    await navigate(cdp, SWAGGER_URL);
    await waitFor(cdp, "document.body.innerText.includes('FastAPI') || document.body.innerText.includes('/predict')");
    await wait(1000);
    await screenshot(cdp, "07-swagger-docs.png");
  } finally {
    cdp.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
