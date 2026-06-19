#!/usr/bin/env python3
"""Build an editable DOCX version of docs/final_report_ge.md.

This intentionally uses only the Python standard library so the report can be
generated in a clean checkout without installing document dependencies.
"""

from __future__ import annotations

import argparse
import html
import re
import struct
import zipfile
from datetime import datetime, timezone
from pathlib import Path


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}

EMU_PER_INCH = 914400
MAX_IMAGE_WIDTH_EMU = int(6.5 * EMU_PER_INCH)


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def run(text: str, *, bold: bool = False, italic: bool = False, code: bool = False) -> str:
    if not text:
        return ""
    props = []
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    if code:
        props.append('<w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/>')
        props.append("<w:sz w:val=\"20\"/>")
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    space = ' xml:space="preserve"' if text[:1].isspace() or text[-1:].isspace() else ""
    return f"<w:r>{rpr}<w:t{space}>{esc(text)}</w:t></w:r>"


def inline_runs(text: str) -> str:
    parts: list[str] = []
    pattern = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`)")
    pos = 0
    for match in pattern.finditer(text):
        if match.start() > pos:
            parts.append(run(text[pos : match.start()]))
        token = match.group(0)
        if token.startswith("**"):
            parts.append(run(token[2:-2], bold=True))
        elif token.startswith("`"):
            parts.append(run(token[1:-1], code=True))
        pos = match.end()
    if pos < len(text):
        parts.append(run(text[pos:]))
    return "".join(parts)


def paragraph(
    text: str = "",
    *,
    style: str | None = None,
    num_id: int | None = None,
    level: int = 0,
    keep_next: bool = False,
    direct_runs: str | None = None,
) -> str:
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if num_id is not None:
        ppr.append(
            f"<w:numPr><w:ilvl w:val=\"{level}\"/><w:numId w:val=\"{num_id}\"/></w:numPr>"
        )
    if keep_next:
        ppr.append("<w:keepNext/>")
    ppr_xml = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    content = direct_runs if direct_runs is not None else inline_runs(text)
    return f"<w:p>{ppr_xml}{content}</w:p>"


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as image:
        header = image.read(24)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Only PNG screenshots are supported: {path}")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def image_paragraph(image_path: Path, relationship_id: str, doc_property_id: int) -> str:
    width_px, height_px = png_dimensions(image_path)
    width_emu = MAX_IMAGE_WIDTH_EMU
    height_emu = int(width_emu * height_px / width_px)
    filename = esc(image_path.name)
    return f"""
<w:p>
  <w:pPr><w:spacing w:before="80" w:after="180"/></w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{width_emu}" cy="{height_emu}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{doc_property_id}" name="{filename}"/>
        <wp:cNvGraphicFramePr>
          <a:graphicFrameLocks noChangeAspect="1"/>
        </wp:cNvGraphicFramePr>
        <a:graphic>
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic>
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="{filename}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{relationship_id}"/>
                <a:stretch><a:fillRect/></a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="{width_emu}" cy="{height_emu}"/>
                </a:xfrm>
                <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
"""


def table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    cols = max(len(row) for row in rows)
    width = 9360
    col_width = width // cols
    grid = "".join(f'<w:gridCol w:w="{col_width}"/>' for _ in range(cols))
    body = []
    for row_index, row in enumerate(rows):
        cells = []
        for col_index in range(cols):
            value = row[col_index].strip() if col_index < len(row) else ""
            shade = '<w:shd w:fill="F2F4F7"/>' if row_index == 0 else ""
            bold = row_index == 0
            tc_pr = (
                f'<w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/>'
                f"{shade}"
                "<w:tcMar><w:top w:w=\"80\" w:type=\"dxa\"/>"
                "<w:left w:w=\"120\" w:type=\"dxa\"/>"
                "<w:bottom w:w=\"80\" w:type=\"dxa\"/>"
                "<w:right w:w=\"120\" w:type=\"dxa\"/></w:tcMar></w:tcPr>"
            )
            cells.append(f"<w:tc>{tc_pr}{paragraph(direct_runs=run(value, bold=bold))}</w:tc>")
        body.append(f"<w:tr>{''.join(cells)}</w:tr>")
    return (
        "<w:tbl>"
        "<w:tblPr>"
        '<w:tblW w:w="9360" w:type="dxa"/>'
        '<w:tblInd w:w="120" w:type="dxa"/>'
        '<w:tblLayout w:type="fixed"/>'
        '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="BFC7D5"/>'
        '<w:left w:val="single" w:sz="4" w:color="BFC7D5"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="BFC7D5"/>'
        '<w:right w:val="single" w:sz="4" w:color="BFC7D5"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="BFC7D5"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="BFC7D5"/></w:tblBorders>'
        "</w:tblPr>"
        f"<w:tblGrid>{grid}</w:tblGrid>"
        f"{''.join(body)}"
        "</w:tbl>"
    )


def parse_markdown(md: str, screenshot_1: Path | None = None) -> list[str]:
    blocks: list[str] = []
    lines = md.splitlines()
    i = 0
    in_code = False
    code_lines: list[str] = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        if line.startswith("```"):
            if in_code:
                for code_line in code_lines:
                    blocks.append(paragraph(code_line, style="CodeBlock"))
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(raw)
            i += 1
            continue

        if not line.strip():
            blocks.append(paragraph())
            i += 1
            continue

        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$", lines[i + 1]):
            table_rows: list[list[str]] = []
            table_rows.append([cell.strip().rstrip(":") for cell in line.strip("|").split("|")])
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                table_rows.append([cell.strip() for cell in lines[i].strip("|").split("|")])
                i += 1
            blocks.append(table(table_rows))
            continue

        if line.startswith("# "):
            blocks.append(paragraph(line[2:].strip(), style="Title"))
        elif line.startswith("## "):
            blocks.append(paragraph(line[3:].strip(), style="Heading1", keep_next=True))
        elif line.startswith("### "):
            blocks.append(paragraph(line[4:].strip(), style="Heading2", keep_next=True))
        elif line.startswith("- "):
            blocks.append(paragraph(line[2:].strip(), style="ListParagraph", num_id=1))
        elif re.match(r"^\d+\.\s+", line):
            blocks.append(paragraph(re.sub(r"^\d+\.\s+", "", line).strip(), style="ListParagraph", num_id=2))
        elif line.startswith("**სქრინშოთი"):
            clean = line.replace("**", "")
            blocks.append(paragraph(clean, style="ScreenshotNote"))
            if clean.startswith("სქრინშოთი 1") and screenshot_1 and screenshot_1.exists():
                blocks.append(image_paragraph(screenshot_1, "rId5", 1))
        else:
            blocks.append(paragraph(line.replace("  ", " ").strip(), style="Normal"))
        i += 1

    return blocks


def styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:color w:val="111111"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="120" w:line="264" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="0" w:after="180"/></w:pPr><w:rPr><w:b/><w:color w:val="0B2545"/><w:sz w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="0"/><w:spacing w:before="320" w:after="160"/></w:pPr><w:rPr><w:b/><w:color w:val="2E74B5"/><w:sz w:val="32"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="1"/><w:spacing w:before="240" w:after="120"/></w:pPr><w:rPr><w:b/><w:color w:val="2E74B5"/><w:sz w:val="26"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph"><w:name w:val="List Paragraph"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:after="80"/></w:pPr></w:style>
  <w:style w:type="paragraph" w:styleId="CodeBlock"><w:name w:val="Code Block"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="40" w:after="80"/><w:shd w:fill="F7F9FC"/></w:pPr><w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/><w:sz w:val="20"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="ScreenshotNote"><w:name w:val="Screenshot Note"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="80" w:after="120"/><w:ind w:left="240"/><w:shd w:fill="FFF4CC"/></w:pPr><w:rPr><w:b/><w:color w:val="7A5A00"/></w:rPr></w:style>
</w:styles>"""


def numbering_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:abstractNum w:abstractNumId="0"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>
  <w:abstractNum w:abstractNumId="1"><w:multiLevelType w:val="singleLevel"/><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/><w:pPr><w:tabs><w:tab w:val="num" w:pos="720"/></w:tabs><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>
  <w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
  <w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>
</w:numbering>"""


def document_xml(blocks: list[str]) -> str:
    body = "".join(blocks)
    sect_pr = (
        "<w:sectPr>"
        '<w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>'
        "</w:sectPr>"
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f"<w:body>{body}{sect_pr}</w:body></w:document>"
    )


def latest_desktop_screenshot() -> Path | None:
    desktop = Path.home() / "Desktop"
    screenshots = sorted(desktop.glob("Screenshot *.png"), key=lambda item: item.stat().st_mtime, reverse=True)
    return screenshots[0] if screenshots else None


def write_docx(markdown_path: Path, output_path: Path, screenshot_1: Path | None = None) -> None:
    markdown = markdown_path.read_text(encoding="utf-8")
    blocks = parse_markdown(markdown, screenshot_1=screenshot_1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    image_content_type = '<Default Extension="png" ContentType="image/png"/>'
    image_relationship = ""
    if screenshot_1 and screenshot_1.exists():
        image_relationship = '<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/screenshot-1.png"/>'
    files = {
        "[Content_Types].xml": f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>{image_content_type}<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/><Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/><Override PartName="/word/fontTable.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.fontTable+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>""",
        "_rels/.rels": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>""",
        "word/_rels/document.xml.rels": f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/><Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable" Target="fontTable.xml"/>{image_relationship}</Relationships>""",
        "word/document.xml": document_xml(blocks),
        "word/styles.xml": styles_xml(),
        "word/numbering.xml": numbering_xml(),
        "word/settings.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:compat/><w:defaultTabStop w:val="720"/></w:settings>""",
        "word/fontTable.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:font w:name="Calibri"/><w:font w:name="Courier New"/></w:fonts>""",
        "docProps/core.xml": f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>გულ-სისხლძარღვთა დაავადებების ადრეული დიაგნოსტიკის დამხმარე სისტემა</dc:title><dc:creator>ნინო ჯინჭარაძე</dc:creator><cp:lastModifiedBy>Codex</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>""",
        "docProps/app.xml": """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Codex</Application></Properties>""",
    }
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as docx:
        for name, content in files.items():
            docx.writestr(name, content)
        if screenshot_1 and screenshot_1.exists():
            docx.write(screenshot_1, "word/media/screenshot-1.png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="docs/final_report_ge.md")
    parser.add_argument("--output", default="output/documents/Nino_Jincharadze_Final_Report.docx")
    parser.add_argument(
        "--screenshot-1",
        default=None,
        help="PNG image to insert under the first screenshot placeholder. Defaults to the newest Desktop screenshot.",
    )
    args = parser.parse_args()
    screenshot_1 = Path(args.screenshot_1) if args.screenshot_1 else latest_desktop_screenshot()
    write_docx(Path(args.input), Path(args.output), screenshot_1=screenshot_1)
    print(args.output)


if __name__ == "__main__":
    main()
