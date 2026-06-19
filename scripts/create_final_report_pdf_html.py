#!/usr/bin/env python3
"""Build a print-ready HTML version of the final Georgian report.

The HTML is used as a deterministic intermediate for Chrome PDF export and
page-by-page visual QA when DOCX rendering is unavailable.
"""

from __future__ import annotations

import html
import re
from pathlib import Path


SCREENSHOT_FILES = {
    1: "01-main-frontend.png",
    2: "02-filled-form-ecg-temperature.png",
    3: "03-prediction-result.png",
    4: "04-diagnosis-cards.png",
    5: "05-lab-bmi-reference.png",
    6: "06-model-technical-evaluation.png",
    7: "07-swagger-docs.png",
}


def inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def render_table(lines: list[str]) -> str:
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    if len(rows) < 2:
        return ""
    header = rows[0]
    body = rows[2:]
    parts = ["<table>", "<thead><tr>"]
    for cell in header:
        parts.append(f"<th>{inline(cell)}</th>")
    parts.append("</tr></thead><tbody>")
    for row in body:
        parts.append("<tr>")
        for cell in row:
            parts.append(f"<td>{inline(cell)}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)


def render_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    blocks: list[str] = []
    i = 0
    in_code = False
    code_lines: list[str] = []
    list_items: list[str] = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            blocks.append("<ul>" + "".join(f"<li>{item}</li>" for item in list_items) + "</ul>")
            list_items = []

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            blocks.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
            code_lines = []

    while i < len(lines):
        line = lines[i].rstrip()

        if line.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_list()
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not line.strip():
            flush_list()
            i += 1
            continue

        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$", lines[i + 1]):
            flush_list()
            table_lines = [line, lines[i + 1]]
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                table_lines.append(lines[i])
                i += 1
            blocks.append(render_table(table_lines))
            continue

        if line.startswith("# "):
            flush_list()
            blocks.append(f"<h1>{inline(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            flush_list()
            blocks.append(f"<h2>{inline(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            flush_list()
            blocks.append(f"<h3>{inline(line[4:].strip())}</h3>")
        elif line.startswith("- "):
            list_items.append(inline(line[2:].strip()))
        elif re.match(r"^\d+\.\s+", line):
            flush_list()
            text = re.sub(r"^\d+\.\s+", "", line).strip()
            blocks.append(f"<p>{inline(text)}</p>")
        elif line.startswith("**სქრინშოთი"):
            flush_list()
            clean = line.replace("**", "")
            blocks.append(f"<p class=\"figure-caption\">{inline(clean)}</p>")
            match = re.match(r"სქრინშოთი\s+(\d+)", clean)
            if match:
                number = int(match.group(1))
                filename = SCREENSHOT_FILES.get(number)
                if filename:
                    blocks.append(
                        f"<figure><img src=\"../../../docs/screenshots/{filename}\" alt=\"სქრინშოთი {number}\"></figure>"
                    )
        else:
            flush_list()
            blocks.append(f"<p>{inline(line.strip())}</p>")
        i += 1

    flush_list()
    flush_code()
    return "\n".join(blocks)


def build_html(markdown_path: Path, output_path: Path) -> None:
    body = render_markdown(markdown_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        f"""<!doctype html>
<html lang="ka">
<head>
  <meta charset="utf-8">
  <title>ნინო ჯინჭარაძე - საბოლოო ტექნიკური დოკუმენტაცია</title>
  <style>
    @page {{ size: A4; margin: 18mm 16mm; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
      color: #112433;
      font-size: 10.5pt;
      line-height: 1.42;
      max-width: 980px;
      margin: 0 auto;
    }}
    h1 {{ font-size: 23pt; line-height: 1.15; color: #0b2d42; margin: 0 0 18px; }}
    h2 {{ font-size: 16pt; color: #0b6f84; margin: 24px 0 9px; break-after: avoid; }}
    h3 {{ font-size: 12.5pt; color: #15475d; margin: 18px 0 6px; break-after: avoid; }}
    p {{ margin: 0 0 8px; }}
    ul {{ margin: 4px 0 12px 22px; padding: 0; }}
    li {{ margin: 0 0 4px; }}
    code {{ font-family: "SFMono-Regular", Consolas, monospace; font-size: 9.5pt; background: #eef3f6; padding: 1px 4px; border-radius: 3px; }}
    pre {{ background: #f4f7f9; border: 1px solid #d9e5ec; border-radius: 6px; padding: 10px; overflow-wrap: anywhere; white-space: pre-wrap; }}
    table {{ border-collapse: collapse; width: 100%; margin: 8px 0 14px; break-inside: avoid; }}
    th, td {{ border: 1px solid #cbd9e1; padding: 7px 8px; vertical-align: top; }}
    th {{ background: #edf4f7; text-align: left; color: #0b2d42; }}
    .figure-caption {{ margin-top: 16px; padding: 8px 10px; background: #fff7dd; color: #755400; border-left: 4px solid #d69b00; font-weight: 700; break-after: avoid; }}
    figure {{ margin: 8px 0 18px; break-inside: avoid; }}
    img {{ width: 100%; border: 1px solid #cad9df; border-radius: 5px; display: block; }}
  </style>
</head>
<body>
{body}
</body>
</html>
""",
        encoding="utf-8",
    )


def main() -> None:
    build_html(Path("docs/final_report_ge.md"), Path("output/documents/final_report_html/final_report.html"))
    print("output/documents/final_report_html/final_report.html")


if __name__ == "__main__":
    main()
