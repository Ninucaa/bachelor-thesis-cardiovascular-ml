from __future__ import annotations

import html
import zipfile
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_DIR / "docs"
DOCX_PATH = DOCS_DIR / "sabakalavro_project_draft_ge.docx"
MD_PATH = DOCS_DIR / "sabakalavro_project_draft_ge.md"


METRICS = [
    ("საერთო გულ-სისხლძარღვთა რისკი", "0.8874", "0.9168", "0.8323", "0.8139", "0.8515"),
    ("მიოკარდიუმის ინფარქტი", "0.9337", "0.6079", "0.3296", "0.8054", "0.2072"),
    ("გულის უკმარისობა", "0.8801", "0.5971", "0.5266", "0.8087", "0.3905"),
    ("ინსულტი / ცერებროვასკულური დაავადება", "0.8182", "0.3415", "0.2263", "0.7149", "0.1344"),
    ("გულის არითმია", "0.8188", "0.5266", "0.5228", "0.7841", "0.3921"),
    ("ჰიპერტენზიული დაავადება", "0.8472", "0.8319", "0.7804", "0.8148", "0.7487"),
    ("კორონარული არტერიის დაავადება", "0.8458", "0.5714", "0.5415", "0.8082", "0.4071"),
]


SECTIONS = [
    (
        "შესავალი",
        [
            "პროექტის მიზანია გულ-სისხლძარღვთა დაავადებების რისკის პროგნოზირების მხარდამჭერი სისტემის შექმნა, რომელიც პაციენტის კლინიკურ მონაცემებზე დაყრდნობით აფასებს როგორც საერთო გულ-სისხლძარღვთა რისკს, ასევე კონკრეტული დაავადებების ქვეტიპების ალბათობას.",
            "სისტემა განკუთვნილია როგორც კლინიკური გადაწყვეტილების დამხმარე პროტოტიპი. მისი ამოცანა არ არის საბოლოო დიაგნოზის დასმა; მოდელი აჩვენებს, რამდენად ჰგავს ახალი პაციენტის მონაცემები იმ პაციენტების პროფილს, რომლებსაც სასწავლო მონაცემებში შესაბამისი გულ-სისხლძარღვთა დიაგნოზი ჰქონდათ დაფიქსირებული.",
        ],
    ),
    (
        "გამოყენებული მონაცემები",
        [
            "მონაცემთა წყაროდ გამოყენებულია MIMIC-IV ბაზიდან მიღებული ცხრილები. პროექტში გამოყენებული ძირითადი ფაილებია: admissions.csv.gz, patients.csv.gz, diagnoses_icd.csv.gz, edstays.csv.gz, triage.csv.gz, omr.csv.gz, labevents.csv.gz, chartevents.csv.gz, d_labitems.csv.gz და d_items.csv.gz.",
            "მონაცემები გაერთიანდა hospital admission-ის დონეზე. საბოლოო time-aware dataset შეიცავს 546,028 ჩანაწერს და 151 სვეტს. საერთო გულ-სისხლძარღვთა დადებითი კლასი ფიქსირდება 326,296 ჩანაწერში, რაც მთლიანი მონაცემების 59.76%-ია.",
            "მონაცემები გაიყო train, validation და test ნაწილებად პაციენტის დონეზე, subject_id-ის მიხედვით. ამ მიდგომით თავიდან იქნა აცილებული ერთი და იგივე პაციენტის სხვადასხვა admission-ის მოხვედრა სხვადასხვა split-ში. train/test/validation overlap ყველა შემთხვევაში ნულის ტოლია.",
        ],
    ),
    (
        "მონაცემების წინასწარი დამუშავება",
        [
            "მოდელის სასწავლო ცხრილი შეიქმნა time-aware პრინციპით: ლაბორატორიული ანალიზები და vital signs აიღება მხოლოდ admission-ის პირველი 24 საათის ფარგლებში. ეს ამცირებს მონაცემთა გაჟონვის რისკს, რადგან მოდელი არ იყენებს ისეთ ინფორმაციას, რომელიც პაციენტის შეფასების მომენტში ჯერ ცნობილი არ იქნებოდა.",
            "დემოგრაფიული ცვლადებიდან გამოყენებულია ასაკი და სქესი. დიაგნოზების ისტორიიდან გამოიყო prior history ცვლადები: დიაბეტი, თირკმლის ქრონიკული დაავადება, სიმსუქნე და თამბაქო/ნიკოტინი. ეს ისტორიული ცვლადები დათვლილია მხოლოდ წინა admission-ებიდან.",
            "Emergency department მონაცემებიდან გამოყენებულია triage vital signs, ტკივილის შეფასება, ambulance arrival და chief complaint-იდან მიღებული სიმპტომები: გულმკერდის ტკივილი, ქოშინი, გულის ფრიალი, სინკოპე, თავბრუსხვევა და შეშუპება.",
            "ლაბორატორიული მახასიათებლები მოიცავს კრეატინინს, გლუკოზას, ჰემოგლობინს, თრომბოციტებს, ტროპონინ T-ს, NT-proBNP-ს, საერთო ქოლესტერინს, HDL/LDL-ს და ტრიგლიცერიდებს. ICU/chartevents მონაცემებიდან გამოყენებულია გულისცემა, წნევა, სუნთქვის სიხშირე, SpO2, ტემპერატურა, წონა და სიმაღლე.",
            "აკლებული მნიშვნელობებისთვის დაემატა 67 missing indicator სვეტი. რიცხვითი მნიშვნელობები შეივსო training split-ის median-ით. არარეალისტური ან out-of-range მნიშვნელობები ჩანაცვლდა missing მნიშვნელობებად და შემდეგ დამუშავდა იგივე წესით.",
        ],
    ),
    (
        "სამიზნე ცვლადები",
        [
            "ძირითადი სამიზნე ცვლადია target_cvd, რომელიც აღნიშნავს, ფიქსირდება თუ არა admission-ში რომელიმე გულ-სისხლძარღვთა დიაგნოზი ICD კოდების მიხედვით.",
            "დამატებით აშენდა ექვსი subtype სამიზნე: მიოკარდიუმის ინფარქტი, გულის უკმარისობა, ინსულტი/ცერებროვასკულური დაავადება, გულის არითმია, ჰიპერტენზიული დაავადება და კორონარული არტერიის დაავადება. ეს subtype მოდელები ეხმარება სისტემას, მხოლოდ target_cvd=1 არ აჩვენოს, არამედ უფრო კონკრეტულად მიუთითოს, რომელ დაავადებასთან ხედავს ყველაზე მაღალ რისკს.",
        ],
    ),
    (
        "მოდელის აგება",
        [
            "პროგნოზირებისთვის გამოყენებულია XGBoost classifier. XGBoost შეირჩა იმიტომ, რომ კარგად მუშაობს tabular clinical data-ზე, ამუშავებს არახაზოვან კავშირებს და შეუძლია სხვადასხვა კლინიკური მახასიათებლის კომბინაციური ეფექტის სწავლა.",
            "გაიწვრთნა ერთი ძირითადი მოდელი საერთო გულ-სისხლძარღვთა რისკისთვის და ექვსი ცალკე მოდელი კონკრეტული ქვეტიპებისთვის. საბოლოო production web/API ამჟამად იყენებს models/time_aware საქაღალდეში შენახულ time-aware მოდელებს.",
            "მოდელის training-დან ამოღებულია ისეთი სვეტები, რომლებიც ახალი პაციენტის შეფასების მომენტში არ უნდა იყოს ცნობილი, მათ შორის subject_id, hadm_id და hospital_expire_flag.",
        ],
    ),
    (
        "შედეგების ინტერპრეტაცია",
        [
            "ძირითადი მოდელის test AUC-ROC არის 0.8874, რაც მიუთითებს, რომ მოდელი კარგად განასხვავებს მაღალი და დაბალი გულ-სისხლძარღვთა რისკის მქონე პროფილებს. Recall 0.8139 ნიშნავს, რომ დადებითი შემთხვევების დიდი ნაწილი სწორად ფიქსირდება.",
            "Subtype მოდელებიდან განსაკუთრებით ძლიერი შედეგი აქვს მიოკარდიუმის ინფარქტის მოდელს, test AUC-ROC 0.9337. გულის უკმარისობის მოდელის AUC არის 0.8801, ხოლო ჰიპერტენზიული დაავადების მოდელის AUC არის 0.8472.",
            "ზოგიერთ იშვიათ subtype-ზე precision შედარებით დაბალია, რაც მოსალოდნელია კლასების დისბალანსის პირობებში. ამ შემთხვევაში მოდელის გამოყენება უფრო მიზანშეწონილია როგორც screening signal და არა როგორც დამოუკიდებელი დიაგნოსტიკური ინსტრუმენტი.",
        ],
    ),
    (
        "ვებაპლიკაციის აღწერა",
        [
            "პროექტის frontend შექმნილია ქართულ ენაზე. მომხმარებელს შეუძლია შეიყვანოს პაციენტის ასაკი, სქესი, BMI, წონა, სიმაღლე, წნევა, ისტორიული დაავადებები, სიმპტომები, ლაბორატორიული მაჩვენებლები და გადაუდებელი განყოფილების vital signs.",
            "სისტემა აბრუნებს ყველაზე სავარაუდო რისკს კონკრეტული დაავადების მიხედვით, პროცენტულ მაჩვენებელს, რისკის დონეს და მოკლე განმსაზღვრელ ფაქტორებს. დამატებით ჩანს subtype risk-ების სრული სია.",
            "ვებაპლიკაციაში დაემატა მოდელის სანდოობის სექცია, სადაც ნაჩვენებია AUC, Recall და Precision. ასევე ავტომატურად გენერირდება პაციენტის ანგარიში ქართულად, რომელიც შეიძლება გამოყენებულ იქნას პროექტის დემონსტრაციაში ან ნაშრომის მაგალითის ნაწილში.",
        ],
    ),
    (
        "შეზღუდვები",
        [
            "სისტემა წარმოადგენს კლინიკური გადაწყვეტილების დამხმარე პროტოტიპს და არ ცვლის ექიმის შეფასებას. შედეგი არის რისკის პროგნოზი და არა საბოლოო დიაგნოზი.",
            "MIMIC-IV წარმოადგენს hospital-based მონაცემთა ბაზას, ამიტომ შედეგები შეიძლება განსხვავდებოდეს სხვა პოპულაციაში ან ამბულატორიულ გარემოში.",
            "მიმდინარე ვერსიაში ECG და რადიოლოგიური სურათები საბოლოო time-aware მოდელში არ არის გამოყენებული. ასეთი მონაცემების დამატება მომავალში გაზრდიდა მოდელის კლინიკურ სიზუსტეს, განსაკუთრებით არითმიის, ინფარქტისა და გულის უკმარისობის შეფასებისას.",
            "მოდელი სწავლობს მონაცემებში არსებულ სტატისტიკურ კავშირებს და კორელაციებს. ის არ ამტკიცებს მიზეზ-შედეგობრივ სამედიცინო კავშირს. საბოლოო გამოყენებამდე საჭიროა დამატებითი კლინიკური ვალიდაცია.",
        ],
    ),
    (
        "დასკვნა",
        [
            "პროექტის ფარგლებში შეიქმნა time-aware მანქანური სწავლების სისტემა, რომელიც პაციენტის ადრეულ კლინიკურ მონაცემებზე დაყრდნობით აფასებს გულ-სისხლძარღვთა დაავადების საერთო და subtype-ების რისკს.",
            "სისტემის მთავარი უპირატესობა არის ის, რომ იგი არ შემოიფარგლება მხოლოდ target_cvd=1/0 კლასით; იგი ექიმისთვის გასაგებად აჩვენებს კონკრეტული დაავადებების რისკებს და მოკლე ინტერპრეტაციას, რაც ზრდის მოდელის პრაქტიკულ მნიშვნელობას.",
        ],
    ),
]


def p(text: str, style: str | None = None) -> str:
    style_xml = f'<w:pStyle w:val="{style}"/>' if style else ""
    return (
        "<w:p><w:pPr>"
        f"{style_xml}"
        "</w:pPr><w:r><w:rPr><w:rFonts w:ascii=\"Arial\" w:hAnsi=\"Arial\" w:cs=\"Arial\"/></w:rPr>"
        f"<w:t>{html.escape(text)}</w:t></w:r></w:p>"
    )


def table(rows: list[list[str]]) -> str:
    table_rows = []
    for row in rows:
        cells = []
        for value in row:
            cells.append(
                "<w:tc><w:tcPr><w:tcW w:w=\"2400\" w:type=\"dxa\"/></w:tcPr>"
                f"{p(value)}</w:tc>"
            )
        table_rows.append(f"<w:tr>{''.join(cells)}</w:tr>")
    return (
        "<w:tbl><w:tblPr><w:tblW w:w=\"0\" w:type=\"auto\"/>"
        "<w:tblBorders><w:top w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"A0A0A0\"/>"
        "<w:left w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"A0A0A0\"/>"
        "<w:bottom w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"A0A0A0\"/>"
        "<w:right w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"A0A0A0\"/>"
        "<w:insideH w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"A0A0A0\"/>"
        "<w:insideV w:val=\"single\" w:sz=\"4\" w:space=\"0\" w:color=\"A0A0A0\"/>"
        "</w:tblBorders></w:tblPr>"
        f"{''.join(table_rows)}</w:tbl>"
    )


def document_xml() -> str:
    body = [
        p("გულ-სისხლძარღვთა დაავადებების რისკის პროგნოზირება მანქანური სწავლების გამოყენებით", "Title"),
        p("საბაკალავრო პროექტის სამუშაო ტექსტი", "Subtitle"),
        p("ავტორი: ნინო ჯინჭარაძე"),
        p("შენიშვნა: ეს ტექსტი არის სამუშაო draft და შესაძლებელია მისი პირდაპირი ჩასმა/რედაქტირება საბოლოო ნაშრომში."),
    ]
    for title, paragraphs in SECTIONS:
        body.append(p(title, "Heading1"))
        for paragraph in paragraphs:
            body.append(p(paragraph))
        if title == "შედეგების ინტერპრეტაცია":
            rows = [["მოდელი", "AUC-ROC", "Avg Precision", "F1", "Recall", "Precision"]]
            rows.extend([list(row) for row in METRICS])
            body.append(table(rows))

    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{''.join(body)}"
        '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1440" '
        'w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
        "</w:body></w:document>"
    )


def styles_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:sz w:val="22"/></w:rPr>
    <w:pPr><w:spacing w:after="160" w:line="276" w:lineRule="auto"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="32"/></w:rPr>
    <w:pPr><w:spacing w:after="240"/></w:pPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Subtitle">
    <w:name w:val="Subtitle"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:i/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:sz w:val="28"/></w:rPr>
    <w:pPr><w:spacing w:before="260" w:after="160"/></w:pPr>
  </w:style>
</w:styles>"""


def write_docx(path: Path) -> None:
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
    document_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/_rels/document.xml.rels", document_rels)
        docx.writestr("word/document.xml", document_xml())
        docx.writestr("word/styles.xml", styles_xml())


def markdown_text() -> str:
    lines = [
        "# გულ-სისხლძარღვთა დაავადებების რისკის პროგნოზირება მანქანური სწავლების გამოყენებით",
        "",
        "ავტორი: ნინო ჯინჭარაძე",
        "",
    ]
    for title, paragraphs in SECTIONS:
        lines.extend([f"## {title}", ""])
        for paragraph in paragraphs:
            lines.extend([paragraph, ""])
        if title == "შედეგების ინტერპრეტაცია":
            lines.extend(
                [
                    "| მოდელი | AUC-ROC | Avg Precision | F1 | Recall | Precision |",
                    "|---|---:|---:|---:|---:|---:|",
                ]
            )
            for row in METRICS:
                lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} |")
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    write_docx(DOCX_PATH)
    MD_PATH.write_text(markdown_text(), encoding="utf-8")
    print(f"Wrote {DOCX_PATH}")
    print(f"Wrote {MD_PATH}")


if __name__ == "__main__":
    main()
