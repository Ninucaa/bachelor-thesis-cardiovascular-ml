from __future__ import annotations


EXPANDED_DIAGNOSIS_TARGETS = {
    "target_myocardial_infarction": {
        "label_ge": "მიოკარდიუმის ინფარქტი",
        "label_en": "Myocardial infarction",
        "icd9": ("410",),
        "icd10": ("I21", "I22"),
    },
    "target_heart_failure": {
        "label_ge": "გულის უკმარისობა",
        "label_en": "Heart failure",
        "icd9": ("428",),
        "icd10": ("I50",),
    },
    "target_subarachnoid_hemorrhage": {
        "label_ge": "სუბარაქნოიდული სისხლჩაქცევა",
        "label_en": "Subarachnoid hemorrhage",
        "icd9": ("430",),
        "icd10": ("I60",),
    },
    "target_intracerebral_hemorrhage": {
        "label_ge": "ინტრაცერებრული სისხლჩაქცევა",
        "label_en": "Intracerebral hemorrhage",
        "icd9": ("431",),
        "icd10": ("I61",),
    },
    "target_ischemic_stroke": {
        "label_ge": "იშემიური ინსულტი / ცერებრული ინფარქტი",
        "label_en": "Ischemic stroke / cerebral infarction",
        "icd9": ("433", "434", "436"),
        "icd10": ("I63", "I64"),
    },
    "target_other_cerebrovascular_disease": {
        "label_ge": "სხვა ცერებროვასკულური დაავადება",
        "label_en": "Other cerebrovascular disease",
        "icd9": ("432",),
        "icd10": ("I62", "I65", "I66", "I67", "I68", "I69"),
    },
    "target_av_conduction_block": {
        "label_ge": "AV ბლოკადა / გამტარობის დარღვევა",
        "label_en": "AV block / conduction disorder",
        "icd9": ("426",),
        "icd10": ("I44", "I45"),
    },
    "target_cardiac_arrest": {
        "label_ge": "გულის გაჩერება",
        "label_en": "Cardiac arrest",
        "icd9": ("4275",),
        "icd10": ("I46",),
    },
    "target_paroxysmal_tachycardia": {
        "label_ge": "პაროქსიზმული ტაქიკარდია",
        "label_en": "Paroxysmal tachycardia",
        "icd9": ("4270", "4271", "4272"),
        "icd10": ("I47",),
    },
    "target_atrial_fibrillation_flutter": {
        "label_ge": "წინაგულთა ფიბრილაცია / flutter",
        "label_en": "Atrial fibrillation / flutter",
        "icd9": ("42731", "42732"),
        "icd10": ("I48",),
    },
    "target_other_arrhythmia": {
        "label_ge": "სხვა გულის არითმია",
        "label_en": "Other cardiac arrhythmia",
        "icd9": ("427",),
        "icd10": ("I49",),
        "exclude_icd9": ("4270", "4271", "4272", "42731", "42732", "4275"),
    },
    "target_primary_hypertension": {
        "label_ge": "პირველადი ჰიპერტენზია",
        "label_en": "Primary hypertension",
        "icd9": ("401",),
        "icd10": ("I10",),
    },
    "target_hypertensive_heart_disease": {
        "label_ge": "ჰიპერტენზიული გულის დაავადება",
        "label_en": "Hypertensive heart disease",
        "icd9": ("402",),
        "icd10": ("I11",),
    },
    "target_hypertensive_kidney_disease": {
        "label_ge": "ჰიპერტენზიული თირკმლის დაავადება",
        "label_en": "Hypertensive kidney disease",
        "icd9": ("403",),
        "icd10": ("I12",),
    },
    "target_hypertensive_heart_kidney_disease": {
        "label_ge": "ჰიპერტენზიული გულის და თირკმლის დაავადება",
        "label_en": "Hypertensive heart and kidney disease",
        "icd9": ("404",),
        "icd10": ("I13",),
    },
    "target_hypertensive_crisis": {
        "label_ge": "ჰიპერტენზიული კრიზი",
        "label_en": "Hypertensive crisis",
        "icd9": (),
        "icd10": ("I16",),
    },
    "target_angina_pectoris": {
        "label_ge": "სტენოკარდია",
        "label_en": "Angina pectoris",
        "icd9": ("413",),
        "icd10": ("I20",),
    },
    "target_acute_ischemic_heart_disease": {
        "label_ge": "მწვავე იშემიური გულის დაავადება",
        "label_en": "Acute ischemic heart disease",
        "icd9": ("411",),
        "icd10": ("I24",),
    },
    "target_chronic_ischemic_heart_disease": {
        "label_ge": "ქრონიკული იშემიური გულის დაავადება",
        "label_en": "Chronic ischemic heart disease",
        "icd9": ("412", "414"),
        "icd10": ("I25",),
    },
}


EXPANDED_CLINICAL_CHECKS = {
    "target_myocardial_infarction": ["ECG/ST-T ცვლილებები", "Troponin T-ის დინამიკა", "გულმკერდის ტკივილის შეფასება"],
    "target_heart_failure": ["NT-proBNP/BNP", "შეშუპება/ქოშინი", "ექოკარდიოგრაფიის განხილვა"],
    "target_subarachnoid_hemorrhage": ["ნევროლოგიური სტატუსი", "თავის ტვინის CT/MRI", "მწვავე თავის ტკივილის ისტორია"],
    "target_intracerebral_hemorrhage": ["ნევროლოგიური სტატუსი", "არტერიული წნევის კონტროლი", "თავის ტვინის CT/MRI"],
    "target_ischemic_stroke": ["ნევროლოგიური სტატუსი", "CT/MRI და ვასკულარული შეფასება", "ინსულტის დროის ფანჯარა"],
    "target_other_cerebrovascular_disease": ["ნევროლოგიური სიმპტომები", "ვიზუალიზაციის საჭიროება", "რისკ-ფაქტორების შეფასება"],
    "target_av_conduction_block": ["ECG გამტარობის ინტერვალები", "ბრადიკარდიის/სინკოპეს შეფასება", "მედიკამენტებისა და ელექტროლიტების გადამოწმება"],
    "target_cardiac_arrest": ["რეანიმაციის/არესტის ისტორია", "ECG rhythm strip", "ელექტროლიტები და Troponin"],
    "target_paroxysmal_tachycardia": ["ECG rhythm strip", "პალპიტაცია/სინკოპე", "ელექტროლიტები და გულისცემა"],
    "target_atrial_fibrillation_flutter": ["ECG rhythm strip", "ინსულტის რისკის შეფასება", "გულისცემის კონტროლი"],
    "target_other_arrhythmia": ["ECG rhythm strip", "ელექტროლიტები", "სიმპტომებთან კავშირის შეფასება"],
    "target_primary_hypertension": ["წნევის განმეორებითი გაზომვა", "ჰიპერტენზიის ისტორია", "თირკმლის ფუნქცია"],
    "target_hypertensive_heart_disease": ["წნევის კონტროლი", "გულის უკმარისობის ნიშნები", "ექოკარდიოგრაფიის განხილვა"],
    "target_hypertensive_kidney_disease": ["კრეატინინი/eGFR", "წნევის კონტროლი", "თირკმლის ქრონიკული დაავადების ისტორია"],
    "target_hypertensive_heart_kidney_disease": ["კრეატინინი/eGFR", "გულის უკმარისობის ნიშნები", "წნევის კონტროლი"],
    "target_hypertensive_crisis": ["წნევის გადაუდებელი შეფასება", "ორგანული დაზიანების ნიშნები", "ნევროლოგიური/კარდიოლოგიური შეფასება"],
    "target_angina_pectoris": ["ტკივილის დატვირთვასთან კავშირი", "ECG", "ლიპიდური პროფილი და რისკ-ფაქტორები"],
    "target_acute_ischemic_heart_disease": ["ECG", "Troponin T-ის დინამიკა", "მწვავე იშემიური სიმპტომები"],
    "target_chronic_ischemic_heart_disease": ["იშემიური სიმპტომები", "ლიპიდური პროფილი", "კარდიოლოგიური შეფასება"],
}

