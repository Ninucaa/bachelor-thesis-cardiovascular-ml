import "./styles.css";

const API_BASE = "http://127.0.0.1:8765";

const editableFields = [
  { key: "age", label: "ასაკი", min: 18, max: 91, step: 1, unit: "წელი" },
  {
    key: "gender_male",
    label: "სქესი",
    type: "select",
    options: [
      { value: 0, label: "მდედრობითი" },
      { value: 1, label: "მამრობითი" },
    ],
  },
  { key: "omr_bmi_mean", label: "BMI", unit: "kg/m2", optional: true, type: "computed" },
  { key: "omr_weight_lbs_mean", label: "წონა", min: 23, max: 363, step: 0.1, unit: "კგ", optional: true, displayUnit: "kg" },
  { key: "omr_height_inches_mean", label: "სიმაღლე", min: 91, max: 244, step: 0.1, unit: "სმ", optional: true, displayUnit: "cm" },
  { key: "omr_sbp_mean", label: "ამბულატორიული სისტოლური წნევა", min: 40, max: 300, step: 1, unit: "mmHg", optional: true },
  { key: "omr_dbp_mean", label: "ამბულატორიული დიასტოლური წნევა", min: 20, max: 200, step: 1, unit: "mmHg", optional: true },
  { key: "history_diabetes", label: "დიაბეტის ისტორია", type: "boolean" },
  { key: "history_chronic_kidney_disease", label: "თირკმლის ქრონიკული დაავადება", type: "boolean" },
  { key: "history_obesity", label: "სიმსუქნის ისტორია", type: "boolean" },
  { key: "history_tobacco_or_nicotine", label: "თამბაქო / ნიკოტინი", type: "boolean" },
  { key: "symptom_chest_pain", label: "გულმკერდის ტკივილი", type: "boolean" },
  { key: "symptom_shortness_of_breath", label: "ქოშინი / სუნთქვის გაძნელება", type: "boolean" },
  { key: "symptom_palpitations", label: "გულის ფრიალი", type: "boolean" },
  { key: "symptom_syncope", label: "გულის წასვლა / სინკოპე", type: "boolean" },
  { key: "symptom_dizziness", label: "თავბრუსხვევა", type: "boolean" },
  { key: "symptom_edema", label: "შეშუპება", type: "boolean" },
  { key: "triage_pain_mean", label: "ტკივილის შეფასება", min: 0, max: 10, step: 0.5, unit: "0-10", optional: true },
  { key: "lab_creatinine_mean", label: "კრეატინინი", min: 0.1, max: 10, step: 0.01, unit: "mg/dL", precision: 2 },
  { key: "lab_hemoglobin_mean", label: "ჰემოგლობინი", min: 3, max: 20, step: 0.1, unit: "g/dL" },
  { key: "lab_glucose_mean", label: "გლუკოზა", min: 40, max: 400, step: 0.01, unit: "mg/dL", precision: 2 },
  { key: "lab_ntprobnp_mean", label: "NT-proBNP (გულის დატვირთვის მარკერი)", min: 0, max: 100000, step: 1, unit: "pg/mL", optional: true },
  { key: "lab_troponin_t_mean", label: "Troponin T", min: 0, max: 100, step: 0.001, unit: "ng/mL", optional: true },
  { key: "lab_chol_total_mean", label: "საერთო ქოლესტერინი", min: 20, max: 500, step: 1, unit: "mg/dL", optional: true },
  { key: "lab_hdl_mean", label: "HDL ქოლესტერინი", min: 1, max: 200, step: 1, unit: "mg/dL", optional: true },
  { key: "lab_ldl_calc_mean", label: "LDL ქოლესტერინი", min: 1, max: 400, step: 1, unit: "mg/dL", optional: true },
  { key: "lab_triglycerides_mean", label: "ტრიგლიცერიდები", min: 1, max: 2000, step: 1, unit: "mg/dL", optional: true },
  { key: "lab_platelets_mean", label: "თრომბოციტები", min: 1, max: 1500, step: 1, unit: "K/uL", optional: true },
  { key: "ed_triage_heart_rate_mean", label: "გულისცემა გადაუდებელში", min: 30, max: 180, step: 1, unit: "bpm", optional: true },
  { key: "ed_triage_sbp_mean", label: "სისტოლური წნევა", min: 60, max: 240, step: 1, unit: "mmHg", optional: true },
  { key: "ed_triage_dbp_mean", label: "დიასტოლური წნევა", min: 30, max: 140, step: 1, unit: "mmHg", optional: true },
  { key: "ed_triage_resp_rate_mean", label: "სუნთქვის სიხშირე", min: 4, max: 80, step: 1, unit: "breaths/min", optional: true },
  { key: "ed_triage_spo2_mean", label: "SpO2", min: 50, max: 100, step: 1, unit: "%", optional: true },
  { key: "ed_triage_temperature_f_mean", label: "ტემპერატურა", min: 26.7, max: 43.3, step: 0.1, unit: "°C", optional: true, displayUnit: "celsius" },
  { key: "ed_triage_acuity_mean", label: "triage სიმძიმე", min: 1, max: 5, step: 1, unit: "1-5", optional: true },
  { key: "ed_arrived_by_ambulance", label: "სასწრაფოთი მოყვანა", type: "boolean" },
];

const formSections = [
  {
    title: "დემოგრაფია და ფიზიკური მონაცემები",
    description: "BMI ავტომატურად ითვლება წონისა და სიმაღლის მიხედვით.",
    keys: [
      "age",
      "gender_male",
      "omr_bmi_mean",
      "omr_weight_lbs_mean",
      "omr_height_inches_mean",
      "omr_sbp_mean",
      "omr_dbp_mean",
    ],
  },
  {
    title: "სამედიცინო ისტორია",
    description: "წინა დიაგნოზები და რისკ-ფაქტორები.",
    keys: [
      "history_diabetes",
      "history_chronic_kidney_disease",
      "history_obesity",
      "history_tobacco_or_nicotine",
    ],
  },
  {
    title: "სტრუქტურირებული სიმპტომები",
    description: "მონიშნეთ მხოლოდ ამჟამინდელი, პაციენტთან აქტუალური ჩივილები.",
    keys: [
      "symptom_chest_pain",
      "symptom_shortness_of_breath",
      "symptom_palpitations",
      "symptom_syncope",
      "symptom_dizziness",
      "symptom_edema",
      "triage_pain_mean",
    ],
  },
  {
    title: "ლაბორატორიული მაჩვენებლები",
    description: "არასავალდებულო ანალიზები ცარიელი დატოვეთ, თუ პასუხი არ არის ცნობილი.",
    reference: "labs",
    keys: [
      "lab_creatinine_mean",
      "lab_hemoglobin_mean",
      "lab_glucose_mean",
      "lab_ntprobnp_mean",
      "lab_troponin_t_mean",
      "lab_chol_total_mean",
      "lab_hdl_mean",
      "lab_ldl_calc_mean",
      "lab_triglycerides_mean",
      "lab_platelets_mean",
    ],
  },
  {
    title: "გადაუდებელი განყოფილების მაჩვენებლები",
    description: "triage მონაცემები და შემოსვლის კონტექსტი.",
    keys: [
      "ed_triage_heart_rate_mean",
      "ed_triage_sbp_mean",
      "ed_triage_dbp_mean",
      "ed_triage_resp_rate_mean",
      "ed_triage_spo2_mean",
      "ed_triage_temperature_f_mean",
      "ed_triage_acuity_mean",
      "ed_arrived_by_ambulance",
    ],
  },
];

const ecgOptions = [
  { value: "not_available", label: "არ არის ხელმისაწვდომი", severity: "neutral" },
  { value: "normal", label: "ნორმალური ECG", severity: "low" },
  { value: "st_elevation", label: "ST elevation / მწვავე ინფარქტის ეჭვი", severity: "high" },
  { value: "st_depression", label: "ST depression / იშემიის ეჭვი", severity: "medium" },
  { value: "arrhythmia", label: "არითმიის ნიშნები", severity: "medium" },
  { value: "atrial_fibrillation", label: "წინაგულთა ფიბრილაციის ნიშნები", severity: "medium" },
  { value: "wide_qrs", label: "QRS გაფართოება", severity: "medium" },
  { value: "long_qt", label: "QT გახანგრძლივება", severity: "medium" },
  { value: "other_abnormal", label: "სხვა პათოლოგიური ცვლილება", severity: "medium" },
];

const editableFieldByKey = Object.fromEntries(editableFields.map((field) => [field.key, field]));

const labReferenceRanges = [
  { key: "lab_creatinine_mean", label: "კრეატინინი", low: 0.6, high: 1.3, unit: "mg/dL" },
  { key: "lab_hemoglobin_mean", label: "ჰემოგლობინი", low: 12, high: 17.5, unit: "g/dL" },
  { key: "lab_glucose_mean", label: "გლუკოზა", low: 70, high: 140, unit: "mg/dL" },
  { key: "lab_ntprobnp_mean", label: "NT-proBNP (გულის დატვირთვის მარკერი)", low: 0, high: 450, unit: "pg/mL" },
  { key: "lab_troponin_t_mean", label: "Troponin T", low: 0, high: 0.01, unit: "ng/mL" },
  { key: "lab_chol_total_mean", label: "საერთო ქოლესტერინი", low: 0, high: 200, unit: "mg/dL" },
  { key: "lab_hdl_mean", label: "HDL ქოლესტერინი", low: 40, high: 1000, unit: "mg/dL", lowLabel: "დაბალი" },
  { key: "lab_ldl_calc_mean", label: "LDL ქოლესტერინი", low: 0, high: 100, unit: "mg/dL" },
  { key: "lab_triglycerides_mean", label: "ტრიგლიცერიდები", low: 0, high: 150, unit: "mg/dL" },
  { key: "lab_platelets_mean", label: "თრომბოციტები", low: 150, high: 450, unit: "K/uL" },
];

const bmiReference = { key: "omr_bmi_mean", label: "BMI", low: 18.5, high: 24.9, unit: "kg/m2" };

const samplePatientOptions = [
  { value: "demo-1", label: "პაციენტი 1 - გულის უკმარისობა" },
  { value: "demo-2", label: "პაციენტი 2 - ინფარქტი" },
  { value: "demo-3", label: "პაციენტი 3 - არითმია" },
  { value: "demo-4", label: "პაციენტი 4 - დაბალი რისკი" },
  { value: "demo-5", label: "პაციენტი 5 - ჰიპერტენზიული გული" },
  { value: "demo-6", label: "პაციენტი 6 - ჰიპერტენზიული კრიზი" },
  { value: "demo-7", label: "პაციენტი 7 - ქრონიკული იშემია" },
  { value: "demo-8", label: "პაციენტი 8 - ინსულტი" },
];

const featureLabels = {
  age: "ასაკი",
  gender_male: "სქესი",
  omr_bmi_mean: "BMI",
  omr_weight_lbs_mean: "წონა",
  omr_height_inches_mean: "სიმაღლე",
  omr_sbp_mean: "ამბულატორიული სისტოლური წნევა",
  omr_dbp_mean: "ამბულატორიული დიასტოლური წნევა",
  history_diabetes: "დიაბეტის ისტორია",
  history_chronic_kidney_disease: "თირკმლის ქრონიკული დაავადების ისტორია",
  history_obesity: "სიმსუქნის ისტორია",
  history_tobacco_or_nicotine: "თამბაქოს/ნიკოტინის ისტორია",
  triage_pain_mean: "ტკივილის შეფასება გადაუდებელში",
  symptom_chest_pain: "გულმკერდის ტკივილის ჩივილი",
  symptom_shortness_of_breath: "ქოშინის/სუნთქვის გაძნელების ჩივილი",
  symptom_palpitations: "გულის ფრიალის ჩივილი",
  symptom_syncope: "გულის წასვლის/სინკოპეს ჩივილი",
  symptom_dizziness: "თავბრუსხვევის ჩივილი",
  symptom_edema: "შეშუპების ჩივილი",
  interaction_age_omr_sbp: "ასაკისა და სისტოლური წნევის კომბინაცია",
  interaction_bmi_omr_sbp: "BMI-ისა და სისტოლური წნევის კომბინაცია",
  interaction_glucose_bmi: "გლუკოზისა და BMI-ის კომბინაცია",
  interaction_ntprobnp_age: "NT-proBNP-ისა და ასაკის კომბინაცია",
  lab_creatinine_mean: "კრეატინინის საშუალო მაჩვენებელი",
  lab_hemoglobin_mean: "ჰემოგლობინის საშუალო მაჩვენებელი",
  lab_glucose_mean: "გლუკოზის საშუალო მაჩვენებელი",
  lab_ntprobnp_mean: "NT-proBNP (გულის დატვირთვის მარკერი)",
  lab_troponin_t_mean: "Troponin T",
  lab_chol_total_mean: "საერთო ქოლესტერინი",
  lab_hdl_mean: "HDL ქოლესტერინი",
  lab_ldl_calc_mean: "LDL ქოლესტერინი",
  lab_triglycerides_mean: "ტრიგლიცერიდები",
  lab_hdl_count: "HDL ანალიზის რაოდენობა",
  lab_chol_total_mean_missing: "საერთო ქოლესტერინის მნიშვნელობა აკლდა",
  lab_platelets_mean: "თრომბოციტები",
  ed_arrived_by_ambulance: "სასწრაფო დახმარებით მიყვანა",
  ed_triage_temperature_f_mean: "triage ტემპერატურა",
  ed_triage_resp_rate_mean: "triage სუნთქვის სიხშირე",
  ed_triage_heart_rate_mean: "triage გულისცემის საშუალო მაჩვენებელი",
  ed_triage_sbp_mean: "triage სისტოლური წნევის საშუალო მაჩვენებელი",
  ed_triage_dbp_mean: "triage დიასტოლური წნევის საშუალო მაჩვენებელი",
  ed_triage_spo2_mean: "triage SpO2",
  ed_triage_acuity_mean: "triage სიმძიმე",
  icu_sbp_mean: "ICU სისტოლური წნევის საშუალო მაჩვენებელი",
  icu_vital_count: "ICU vital ჩანაწერების რაოდენობა",
  icu_spo2_mean_missing: "ICU SpO2 მნიშვნელობა აკლდა",
  icu_vital_count_missing: "ICU vital ჩანაწერები აკლდა",
};

const optionalDefaults = {
  omr_bmi_mean: 27.7,
  omr_weight_lbs_mean: 171.08,
  omr_height_inches_mean: 66,
  omr_sbp_mean: 127.5,
  omr_dbp_mean: 73,
  triage_pain_mean: 3.5,
  lab_ntprobnp_mean: 2081.5,
  lab_troponin_t_mean: 0.075,
  lab_chol_total_mean: 160,
  lab_hdl_mean: 46,
  lab_ldl_calc_mean: 86,
  lab_triglycerides_mean: 106,
  lab_platelets_mean: 250,
  ed_triage_heart_rate_mean: 80,
  ed_triage_sbp_mean: 120,
  ed_triage_dbp_mean: 80,
  ed_triage_resp_rate_mean: 18,
  ed_triage_spo2_mean: 98,
  ed_triage_temperature_f_mean: 98.6,
  ed_triage_acuity_mean: 3,
};

const modelMetrics = [
  { label: "საერთო გულ-სისხლძარღვთა დიაგნოსტიკური სიგნალი", auc: "0.8871", recall: "0.8134", precision: "0.8511" },
  { label: "მიოკარდიუმის ინფარქტი", auc: "0.9337", recall: "0.8054", precision: "0.2072" },
  { label: "გულის უკმარისობა", auc: "0.8801", recall: "0.8087", precision: "0.3905" },
  { label: "სუბარაქნოიდული სისხლჩაქცევა", auc: "0.9275", recall: "0.7867", precision: "0.0256" },
  { label: "ინტრაცერებრული სისხლჩაქცევა", auc: "0.9107", recall: "0.7675", precision: "0.0574" },
  { label: "იშემიური ინსულტი / ცერებრული ინფარქტი", auc: "0.8600", recall: "0.7159", precision: "0.0780" },
  { label: "სხვა ცერებროვასკულური დაავადება", auc: "0.7988", recall: "0.7290", precision: "0.0674" },
  { label: "AV ბლოკადა / გამტარობის დარღვევა", auc: "0.7709", recall: "0.7162", precision: "0.0639" },
  { label: "გულის გაჩერება", auc: "0.8950", recall: "0.7508", precision: "0.0349" },
  { label: "პაროქსიზმული ტაქიკარდია", auc: "0.7866", recall: "0.7232", precision: "0.0518" },
  { label: "წინაგულთა ფიბრილაცია / flutter", auc: "0.8410", recall: "0.8334", precision: "0.3173" },
  { label: "სხვა გულის არითმია", auc: "0.7247", recall: "0.6436", precision: "0.0627" },
  { label: "პირველადი ჰიპერტენზია", auc: "0.7929", recall: "0.8020", precision: "0.5496" },
  { label: "ჰიპერტენზიული გულის დაავადება", auc: "0.8507", recall: "0.8127", precision: "0.0842" },
  { label: "ჰიპერტენზიული თირკმლის დაავადება", auc: "0.9363", recall: "0.9001", precision: "0.4041" },
  { label: "ჰიპერტენზიული გულის და თირკმლის დაავადება", auc: "0.9430", recall: "0.9062", precision: "0.1642" },
  { label: "ჰიპერტენზიული კრიზი", auc: "0.8946", recall: "0.7663", precision: "0.0257" },
  { label: "სტენოკარდია", auc: "0.8042", recall: "0.6868", precision: "0.0174" },
  { label: "მწვავე იშემიური გულის დაავადება", auc: "0.8769", recall: "0.7764", precision: "0.0429" },
  { label: "ქრონიკული იშემიური გულის დაავადება", auc: "0.8457", recall: "0.8092", precision: "0.3977" },
];

const metricDescriptions = [
  { key: "auc", label: "გარჩევის უნარი", technical: "AUC", note: "რამდენად კარგად არჩევს შესაბამის და არაშესაბამის შემთხვევებს" },
  { key: "recall", label: "აღმოჩენის უნარი", technical: "Recall", note: "დაავადებული შემთხვევებიდან რამდენს პოულობს" },
  { key: "precision", label: "დადებითი პასუხის სიზუსტე", technical: "Precision", note: "დადებითი პასუხებიდან რამდენია უფრო სარწმუნო" },
];

const modelTrustNotes = [
  {
    title: "რა აჩვენებს ეს ნაწილი",
    text: "ეს არის მოდელის შემოწმება უკვე ცნობილ test პაციენტებზე. აქ ჩანს, რამდენად კარგად არჩევდა სისტემა შესაბამის დიაგნოზის ჯგუფებს ისტორიულ მონაცემებში.",
  },
  {
    title: "როგორ წავიკითხოთ",
    text: "გარჩევის უნარი აჩვენებს საერთო ხარისხს, აღმოჩენის უნარი - რამდენ შემთხვევას პოულობს, დადებითი პასუხის სიზუსტე - რამდენად სანდოა დადებითი სიგნალი.",
  },
  {
    title: "კლინიკური შეზღუდვა",
    text: "ეს რიცხვები არ ნიშნავს, რომ მოდელი ექიმზე უკეთ სვამს დიაგნოზს. ისინი აჩვენებს prototype-ის ტექნიკურ ხარისხს კონკრეტულ dataset-ზე.",
  },
];

const symptomTextRules = [
  {
    key: "symptom_chest_pain",
    label: "გულმკერდის ტკივილი",
    patterns: [
      /გულმკერდ(ის)?\s*ტკივილ/i,
      /მკერდ(ის)?\s*ტკივილ/i,
      /chest pain|chest pressure|\bcp\b/i,
    ],
  },
  {
    key: "symptom_shortness_of_breath",
    label: "ქოშინი / სუნთქვის გაძნელება",
    patterns: [
      /ქოშინ/i,
      /სუნთქვ(ის)?\s*(გაძნელ|უკმარ|პრობლემ)/i,
      /ჰაერ(ი)?\s*არ\s*ყოფნ/i,
      /shortness of breath|\bsob\b|dyspnea|difficulty breathing|trouble breathing/i,
    ],
  },
  {
    key: "symptom_palpitations",
    label: "გულის ფრიალი",
    patterns: [/გულის\s*ფრიალ/i, /პალპიტაცი/i, /palpitation/i],
  },
  {
    key: "symptom_syncope",
    label: "გულის წასვლა / სინკოპე",
    patterns: [/გულის\s*წასვლ/i, /გონებ(ის)?\s*დაკარგ/i, /სინკოპ/i, /syncope|faint|passed out/i],
  },
  {
    key: "symptom_dizziness",
    label: "თავბრუსხვევა",
    patterns: [/თავბრუსხვ/i, /დizziness|dizzy|lightheaded|light headed/i],
  },
  {
    key: "symptom_edema",
    label: "შეშუპება",
    patterns: [/შეშუპ/i, /ფეხ(ების)?\s*შეშუპ/i, /edema|swelling|leg swelling/i],
  },
];

const dataQualityGroups = [
  {
    title: "დემოგრაფია",
    keys: ["age", "gender_male"],
    weight: 2,
    fix: "დაადასტურეთ ასაკი და სქესი.",
  },
  {
    title: "ფიზიკური მონაცემები",
    keys: ["omr_bmi_mean", "omr_sbp_mean", "omr_dbp_mean"],
    weight: 1.5,
    fix: "შეავსეთ BMI ან წონა/სიმაღლე და ამბულატორიული წნევა, თუ ცნობილია.",
  },
  {
    title: "სიმპტომები",
    keys: [
      "symptom_chest_pain",
      "symptom_shortness_of_breath",
      "symptom_palpitations",
      "symptom_syncope",
      "symptom_dizziness",
      "symptom_edema",
      "triage_pain_mean",
    ],
    weight: 1,
    fix: "დაამატეთ ამჟამინდელი ჩივილები ან მიუთითეთ, რომ სიმპტომები არ არის.",
  },
  {
    title: "ლაბორატორია",
    keys: ["lab_creatinine_mean", "lab_hemoglobin_mean", "lab_glucose_mean", "lab_ntprobnp_mean", "lab_troponin_t_mean"],
    weight: 2,
    fix: "გადაამოწმეთ ძირითადი ანალიზები, განსაკუთრებით Troponin T და NT-proBNP კარდიოლოგიური ეჭვისას.",
  },
  {
    title: "გადაუდებელი vital ნიშნები",
    keys: [
      "ed_triage_heart_rate_mean",
      "ed_triage_sbp_mean",
      "ed_triage_dbp_mean",
      "ed_triage_resp_rate_mean",
      "ed_triage_spo2_mean",
      "ed_triage_temperature_f_mean",
      "ed_triage_acuity_mean",
    ],
    weight: 2,
    fix: "შეავსეთ triage vital ნიშნები: წნევა, პულსი, SpO2, სუნთქვა და ტემპერატურა.",
  },
  {
    title: "ECG კონტექსტი",
    customPresent: () => ecgFinding !== "not_available" || Boolean(ecgNote.trim()),
    weight: 1.5,
    fix: "დაამატეთ ECG შეფასება ან მოკლე ECG აღწერა, თუ პასუხი არსებობს.",
  },
];

const negationPatterns = [
  /არ\s+(აქვს|აღენიშნება|უჩივის|აფიქსირებს|არის|ქონდა|ჰქონდა)/i,
  /უარყოფს/i,
  /without|denies|denied|no evidence of|negative for|not complaining of/i,
];

const historicalPatterns = [
  /წარსულში|ადრე|ანამნეზში|ბავშვობაში|რამდენიმე\s+წლის\s+წინ|ოჯახურ\s+ისტორიაში/i,
  /history of|prior|previous|previously|years ago|family history/i,
];

const uncertaintyPatterns = [
  /შესაძლოა|შეიძლება|სავარაუდოდ|ეჭვი|კითხვის\s*ნიშნით/i,
  /possible|possibly|probable|questionable|suspected|rule out|r\/o/i,
];

const currentTimePatterns = [
  /ახლა|ამჟამად|დღეს|მიმართვისას|ბოლო\s+\d+\s*(საათ|დღ)/i,
  /now|currently|today|acute|presenting|last\s+\d+\s*(hour|day)/i,
];

const severePatterns = [
  /ძლიერი|მძიმე|მწვავე|აუტანელი|გამოხატული|მკვეთრი/i,
  /severe|acute|crushing|marked|significant/i,
];

let sample = null;
let features = null;
let result = null;
let statusText = "იტვირთება სატესტო პაციენტი...";
let isPredicting = false;
let symptomText = "";
let ecgFinding = "not_available";
let ecgNote = "";
let baselineSbp = "";
let baselineDbp = "";
let isLabReferenceOpen = false;
let isModelTrustOpen = false;
let isAllDiagnosesOpen = false;
let clearedFieldKeys = new Set();
let selectedSampleId = "demo-1";

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function riskLabel(level) {
  if (level === "high") return "ძლიერი საერთო დიაგნოსტიკური სიგნალი";
  if (level === "medium") return "საშუალო საერთო დიაგნოსტიკური სიგნალი";
  return "დაბალი საერთო დიაგნოსტიკური სიგნალი";
}

function diseaseRiskLabel(level) {
  if (level === "high") return "მაღალი რისკი";
  if (level === "medium") return "საშუალო რისკი";
  return "დაბალი რისკი";
}

function diagnosisConfidenceLabel(confidence) {
  if (confidence === "high") return "ძლიერი სავარაუდო დიაგნოზი";
  if (confidence === "diagnostic_signal") return "სავარაუდო დიაგნოზის ჯგუფი";
  if (confidence === "borderline") return "სუსტი/საზღვრული სიგნალი";
  return "დაბალი მხარდაჭერა";
}

function confidenceClass(confidence) {
  if (confidence === "high") return "confidence-high";
  if (confidence === "diagnostic_signal") return "confidence-signal";
  if (confidence === "borderline") return "confidence-borderline";
  return "confidence-low";
}

function supportClass(level) {
  if (level === "strong") return "support-strong";
  if (level === "partial") return "support-partial";
  return "support-weak";
}

function supportLabel(level) {
  if (level === "strong") return "ძლიერი კლინიკური მხარდაჭერა";
  if (level === "partial") return "ნაწილობრივი კლინიკური მხარდაჭერა";
  return "სუსტი კლინიკური მხარდაჭერა";
}

function formatPercent(value) {
  return `${Math.round(value * 1000) / 10}%`;
}

function clampPercent(value) {
  return Math.max(0, Math.min(100, Math.round(value * 1000) / 10));
}

function displayFeatureName(feature) {
  if (featureLabels[feature]) return featureLabels[feature];
  if (feature.endsWith("_missing")) {
    const baseFeature = feature.replace("_missing", "");
    return `${featureLabels[baseFeature] || baseFeature} აკლდა`;
  }
  return feature;
}

function isOptionalMissing(field) {
  return Boolean(field.optional && Number(features?.[`${field.key}_missing`]) === 1);
}

function hasBlockingClearedFields() {
  return editableFields.some((field) => !field.optional && field.type !== "computed" && clearedFieldKeys.has(field.key));
}

function inputValue(field) {
  if (!features) return "";
  if (clearedFieldKeys.has(field.key)) return "";
  if (isOptionalMissing(field)) return "";
  let value = Number(features[field.key]);
  if (Number.isNaN(value)) return "";
  if (field.displayUnit === "kg") value /= 2.20462;
  if (field.displayUnit === "cm") value *= 2.54;
  if (field.displayUnit === "celsius") value = (value - 32) * (5 / 9);
  if (field.precision !== undefined) return value.toFixed(field.precision);
  if (field.step && Number(field.step) < 1) return String(Math.round(value * 10) / 10);
  return String(Math.round(value));
}

function labStatus(reference) {
  if (!features || Number(features[`${reference.key}_missing`] ?? 0) === 1) {
    return { label: "არ არის შეყვანილი", className: "missing" };
  }
  const value = Number(features[reference.key]);
  if (Number.isNaN(value)) return { label: "არ არის შეყვანილი", className: "missing" };
  if (value < reference.low) return { label: reference.lowLabel || "დაბალი", className: "low" };
  if (value > reference.high) return { label: "მაღალი", className: "high" };
  return { label: "ნორმაში", className: "normal" };
}

function labDisplayValue(reference) {
  if (!features || Number(features[`${reference.key}_missing`] ?? 0) === 1) return "—";
  const value = Number(features[reference.key]);
  if (Number.isNaN(value)) return "—";
  if (reference.key === "lab_creatinine_mean" || reference.key === "lab_glucose_mean") {
    return value.toFixed(2);
  }
  if (reference.key === "lab_troponin_t_mean") return value.toFixed(3);
  return String(Math.round(value * 10) / 10);
}

function labRangeText(reference) {
  if (reference.low === 0) return `≤ ${reference.high} ${reference.unit}`;
  if (reference.high >= 1000) return `≥ ${reference.low} ${reference.unit}`;
  return `${reference.low}-${reference.high} ${reference.unit}`;
}

function fieldStatus(field) {
  if (!features || field.type === "boolean" || field.type === "select" || field.type === "computed") return null;
  if (Number(features[`${field.key}_missing`] ?? 0) === 1 || clearedFieldKeys.has(field.key)) return null;
  const reference =
    labReferenceRanges.find((item) => item.key === field.key) ||
    [
      { key: "omr_sbp_mean", low: 90, high: 120 },
      { key: "omr_dbp_mean", low: 60, high: 80 },
      { key: "ed_triage_sbp_mean", low: 90, high: 120 },
      { key: "ed_triage_dbp_mean", low: 60, high: 80 },
      { key: "ed_triage_heart_rate_mean", low: 60, high: 100 },
      { key: "ed_triage_resp_rate_mean", low: 12, high: 20 },
      { key: "ed_triage_spo2_mean", low: 95, high: 100, lowLabel: "დაბალი" },
      { key: "ed_triage_temperature_f_mean", low: 97, high: 99.5 },
    ].find((item) => item.key === field.key);
  if (!reference) return null;
  const value = Number(features[field.key]);
  if (!Number.isFinite(value)) return null;
  if (value < reference.low) return { label: reference.lowLabel || "დაბალი", className: "field-low" };
  if (value > reference.high) return { label: "საყურადღებო", className: "field-high" };
  return { label: "ნორმაში", className: "field-normal" };
}

function bmiStatus() {
  if (!features || Number(features.omr_bmi_mean_missing ?? 0) === 1) {
    return { label: "არ არის გამოთვლილი", className: "missing" };
  }
  const value = Number(features.omr_bmi_mean);
  if (value < bmiReference.low) return { label: "დაბალი", className: "low" };
  if (value > bmiReference.high) return { label: "მაღალი", className: "high" };
  return { label: "ნორმაში", className: "normal" };
}

function splitSymptomSentences(text) {
  return text
    .split(/[.!?\n;]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function patternMatches(patterns, text) {
  return patterns.some((pattern) => pattern.test(text));
}

function symptomStatusForSentence(sentence) {
  if (patternMatches(negationPatterns, sentence)) return "negated";
  if (patternMatches(historicalPatterns, sentence) && !patternMatches(currentTimePatterns, sentence)) return "historical";
  if (patternMatches(uncertaintyPatterns, sentence)) return "uncertain";
  return "present";
}

function severityForSentence(sentence) {
  return patternMatches(severePatterns, sentence) ? "high" : "not_specified";
}

function parseSymptomTextDetailed(text) {
  const sentences = splitSymptomSentences(text);
  const details = {};
  symptomTextRules.forEach((rule) => {
    details[rule.key] = {
      key: rule.key,
      label: rule.label,
      status: "absent",
      severity: "not_specified",
      evidence: "",
    };
  });

  sentences.forEach((sentence) => {
    symptomTextRules.forEach((rule) => {
      if (!patternMatches(rule.patterns, sentence)) return;
      const status = symptomStatusForSentence(sentence);
      const severity = severityForSentence(sentence);
      const current = details[rule.key];
      const statusRank = { absent: 0, historical: 1, negated: 2, uncertain: 3, present: 4 };
      if (statusRank[status] >= statusRank[current.status]) {
        details[rule.key] = {
          ...current,
          status,
          severity,
          evidence: sentence,
        };
      }
    });
  });

  return details;
}

function parseSymptomText(text) {
  const details = parseSymptomTextDetailed(text);
  return Object.fromEntries(
    Object.entries(details).map(([key, value]) => [key, value.status === "present" ? 1 : 0]),
  );
}

function detectedSymptomLabels() {
  const details = parseSymptomTextDetailed(symptomText);
  return Object.values(details)
    .filter((item) => item.status === "present")
    .map((item) => item.label);
}

function selectedEcgOption() {
  return ecgOptions.find((option) => option.value === ecgFinding) || ecgOptions[0];
}

function ecgClinicalText() {
  const selected = selectedEcgOption();
  const note = ecgNote.trim();
  if (selected.value === "not_available" && !note) return "ECG პასუხი არ არის მითითებული";
  if (selected.value === "normal" && !note) return "ECG მითითებულია როგორც ნორმალური";
  return [selected.label, note].filter(Boolean).join(" - ");
}

function ecgClinicalChecks() {
  const selected = selectedEcgOption();
  if (selected.value === "not_available" || selected.value === "normal") return [];
  const checksByFinding = {
    st_elevation: ["ECG ცვლილების გადამოწმება ექიმის მიერ და მწვავე კორონარული სინდრომის გამორიცხვა", "Troponin T-ის დინამიკა და საჭიროების შემთხვევაში გადაუდებელი კარდიოლოგიური შეფასება"],
    st_depression: ["იშემიური ცვლილებების კლინიკურ სურათთან შედარება", "Troponin T, სიმპტომები და არტერიული წნევის დინამიკა"],
    arrhythmia: ["რიტმის ტიპის დადასტურება ECG ჩანაწერით", "ელექტროლიტების, გულისცემის და ჰემოდინამიკის შეფასება"],
    atrial_fibrillation: ["წინაგულთა ფიბრილაციის დადასტურება და ინსულტის რისკის შეფასება", "გულისცემის კონტროლისა და ანტიკოაგულაციის საჭიროების განხილვა ექიმის მიერ"],
    wide_qrs: ["გამტარობის დარღვევის ან ბლოკადის შეფასება", "QRS ცვლილების შედარება წინა ECG-სთან, თუ ხელმისაწვდომია"],
    long_qt: ["QT-ის გახანგრძლივების მიზეზების შეფასება", "მედიკამენტების და ელექტროლიტების გადამოწმება"],
    other_abnormal: ["ECG-ის პათოლოგიური აღწერის ექიმის მიერ ინტერპრეტაცია", "ECG ცვლილებების შედარება სიმპტომებთან და ლაბორატორიულ პასუხებთან"],
  };
  return checksByFinding[selected.value] || checksByFinding.other_abnormal;
}

function numericFeature(key, defaultValue = 0) {
  if (!features || Number(features[`${key}_missing`] ?? 0) === 1) return defaultValue;
  const value = Number(features[key]);
  return Number.isFinite(value) ? value : defaultValue;
}

function booleanFeature(key) {
  return numericFeature(key) >= 0.5;
}

function baselineBpValues() {
  const sbp = Number(String(baselineSbp).replace(",", "."));
  const dbp = Number(String(baselineDbp).replace(",", "."));
  return {
    hasBaseline: Number.isFinite(sbp) && Number.isFinite(dbp) && sbp > 0 && dbp > 0,
    sbp,
    dbp,
  };
}

function currentBpValues() {
  return {
    sbp: Math.max(numericFeature("omr_sbp_mean"), numericFeature("ed_triage_sbp_mean")),
    dbp: Math.max(numericFeature("omr_dbp_mean"), numericFeature("ed_triage_dbp_mean")),
  };
}

function baselineBpAssessment() {
  const current = currentBpValues();
  const baseline = baselineBpValues();
  const absoluteHigh = current.sbp >= 180 || current.dbp >= 120;
  const high = current.sbp >= 140 || current.dbp >= 90;

  if (!baseline.hasBaseline) {
    return {
      className: high ? "caution" : "neutral",
      label: "ჩვეულებრივი წნევა არ არის მითითებული",
      text: high
        ? "წნევა მაღალია ზოგად კლინიკურ დიაპაზონთან შედარებით; შეადარეთ პაციენტის ჩვეულებრივ მაჩვენებელს, თუ ეს მოგვიანებით გახდება ცნობილი."
        : "შეფასება ეფუძნება ზოგად კლინიკურ დიაპაზონს, რადგან პაციენტის ჩვეულებრივი წნევა მითითებული არ არის.",
      reason: high ? `წნევა ზოგად ზღვართან შედარებით მაღალია (${Math.round(current.sbp)}/${Math.round(current.dbp)} mmHg)` : "",
      absoluteHigh,
      aboveBaseline: false,
    };
  }

  const sbpDelta = current.sbp - baseline.sbp;
  const dbpDelta = current.dbp - baseline.dbp;
  const aboveBaseline = sbpDelta >= 20 || dbpDelta >= 10;
  const nearBaseline = Math.abs(sbpDelta) < 15 && Math.abs(dbpDelta) < 8;

  return {
    className: absoluteHigh || aboveBaseline ? "caution" : "neutral",
    label: "შედარებულია პაციენტის ჩვეულებრივ წნევასთან",
    text: nearBaseline
      ? `მიმდინარე წნევა ახლოსაა პაციენტის ჩვეულებრივ მაჩვენებელთან (${Math.round(baseline.sbp)}/${Math.round(baseline.dbp)} mmHg).`
      : `მიმდინარე წნევა პაციენტის ჩვეულებრივ მაჩვენებელთან შედარებით შეცვლილია: ${sbpDelta >= 0 ? "+" : ""}${Math.round(sbpDelta)}/${dbpDelta >= 0 ? "+" : ""}${Math.round(dbpDelta)} mmHg.`,
    reason: aboveBaseline
      ? `წნევა პაციენტის ჩვეულებრივ მაჩვენებელზე მაღალია (${sbpDelta >= 0 ? "+" : ""}${Math.round(sbpDelta)}/${dbpDelta >= 0 ? "+" : ""}${Math.round(dbpDelta)} mmHg)`
      : "",
    absoluteHigh,
    aboveBaseline,
  };
}

function ecgAlignment(risk) {
  const selected = selectedEcgOption();
  const target = risk?.target_name || "";
  const ischemicTargets = new Set([
    "target_myocardial_infarction",
    "target_acute_ischemic_heart_disease",
    "target_angina_pectoris",
    "target_chronic_ischemic_heart_disease",
  ]);
  const arrhythmiaTargets = new Set([
    "target_atrial_fibrillation_flutter",
    "target_paroxysmal_tachycardia",
    "target_other_arrhythmia",
    "target_av_conduction_block",
  ]);
  const strokeTargets = new Set([
    "target_ischemic_stroke",
    "target_other_cerebrovascular_disease",
    "target_subarachnoid_hemorrhage",
    "target_intracerebral_hemorrhage",
  ]);

  if (selected.value === "not_available") {
    return {
      className: "neutral",
      label: "ECG არ არის მითითებული",
      text: "ECG პასუხი არ არის შეყვანილი, ამიტომ მთავარი სავარაუდო მიმართულება ECG-ით ვერ მყარდება.",
    };
  }

  if (selected.value === "normal") {
    if (ischemicTargets.has(target) || arrhythmiaTargets.has(target)) {
      return {
        className: "caution",
        label: "ECG პირდაპირ არ ამყარებს",
        text: "ნორმალური ECG ამ ეტაპზე არ ამყარებს მწვავე იშემიურ ან რიტმის სიგნალს, თუმცა დიაგნოზს სრულად არ გამორიცხავს.",
      };
    }
    return {
      className: "neutral",
      label: "ECG ნეიტრალურია",
      text: "ნორმალური ECG მთავარ სავარაუდო მიმართულებას მკვეთრად არც ამყარებს და არც გამორიცხავს.",
    };
  }

  if (["st_elevation", "st_depression"].includes(selected.value)) {
    if (ischemicTargets.has(target)) {
      return {
        className: "match",
        label: "ECG ემთხვევა მთავარ მიმართულებას",
        text: "ST ცვლილება აძლიერებს იშემიური/კორონარული მიმართულების კლინიკურ გადამოწმებას.",
      };
    }
    return {
      className: "caution",
      label: "ECG სხვა მიმართულებასაც აძლიერებს",
      text: "ST ცვლილება მოითხოვს იშემიური მიზეზის პარალელურ გამორიცხვას, თუნდაც მთავარი მოდელური მიმართულება სხვა იყოს.",
    };
  }

  if (["arrhythmia", "atrial_fibrillation", "wide_qrs", "long_qt"].includes(selected.value)) {
    if (arrhythmiaTargets.has(target) || (selected.value === "atrial_fibrillation" && strokeTargets.has(target))) {
      return {
        className: "match",
        label: "ECG ემთხვევა მთავარ მიმართულებას",
        text: "რიტმის/გამტარობის ცვლილება ამყარებს შესაბამის კარდიოლოგიურ ან ინსულტის რისკის გადამოწმებას.",
      };
    }
    return {
      className: "caution",
      label: "ECG დამატებით გადასამოწმებელია",
      text: "რიტმის/გამტარობის ცვლილება შეიძლება იყოს თანმხლები პრობლემა და ექიმმა ცალკე უნდა შეაფასოს.",
    };
  }

  return {
    className: "caution",
    label: "ECG პათოლოგიურია",
    text: "პათოლოგიური ECG აღწერა უნდა შეედაროს სიმპტომებს, ლაბორატორიას და მთავარ სავარაუდო დიაგნოზს.",
  };
}

function urgencyAssessment(risk) {
  const reasons = [];
  const probability = Number(risk?.diagnosis_probability ?? risk?.risk_probability ?? 0);
  const supportScore = Number(risk?.clinical_support_score ?? 0);
  const ecg = selectedEcgOption().value;
  const troponin = numericFeature("lab_troponin_t_mean");
  const ntprobnp = numericFeature("lab_ntprobnp_mean");
  const spo2 = numericFeature("ed_triage_spo2_mean", 100);
  const heartRate = numericFeature("ed_triage_heart_rate_mean");
  const respRate = numericFeature("ed_triage_resp_rate_mean");
  const bp = currentBpValues();
  const bpAssessment = baselineBpAssessment();
  const acuity = numericFeature("ed_triage_acuity_mean", 5);

  if (["st_elevation", "st_depression"].includes(ecg)) reasons.push("ECG-ზე არის ST ცვლილება");
  if (troponin > 0.01) reasons.push("Troponin T მომატებულია");
  if (spo2 < 90) reasons.push(`SpO2 დაბალია (${Math.round(spo2)}%)`);
  if (bpAssessment.absoluteHigh) reasons.push(`წნევა ძალიან მაღალია (${Math.round(bp.sbp)}/${Math.round(bp.dbp)} mmHg)`);
  else if (bpAssessment.reason) reasons.push(bpAssessment.reason);
  if (heartRate >= 130 || heartRate <= 45) reasons.push(`გულისცემა უკიდურესია (${Math.round(heartRate)} bpm)`);
  if (respRate >= 28) reasons.push(`სუნთქვის სიხშირე მაღალია (${Math.round(respRate)} / min)`);
  if (acuity <= 2) reasons.push(`triage სიმძიმე მაღალია (${Math.round(acuity)} / 5)`);
  if (ntprobnp > 1800 && (booleanFeature("symptom_shortness_of_breath") || booleanFeature("symptom_edema"))) {
    reasons.push("NT-proBNP და გულის უკმარისობის სიმპტომები გამოკვეთილია");
  }

  if (reasons.length >= 2 || (probability >= 0.75 && supportScore >= 70)) {
    return {
      className: "urgent",
      label: "გადაუდებელი შეფასება",
      text: "პაციენტის პროფილში ჩანს ნიშნები, რომლებიც საჭიროებს სწრაფ კლინიკურ გადამოწმებას.",
      reasons: reasons.slice(0, 4),
    };
  }
  if (reasons.length === 1 || probability >= 0.5 || supportScore >= 40) {
    return {
      className: "soon",
      label: "სწრაფი კარდიოლოგიური გადამოწმება",
      text: "მოდელის პასუხი და კლინიკური ნიშნები საჭიროებს მიზანმიმართულ, მაგრამ არა ავტომატურად საბოლოო დიაგნოზად გამოყენებულ შეფასებას.",
      reasons: reasons.length ? reasons.slice(0, 4) : ["მოდელის ან კლინიკური მხარდაჭერის სიგნალი საშუალო დონეზეა"],
    };
  }
  return {
    className: "routine",
    label: "გეგმიური გადამოწმება",
    text: "ამ მონაცემებით მწვავე სიგნალი მკვეთრად არ ჩანს, თუმცა შედეგი დაავადებას სრულად არ გამორიცხავს.",
    reasons: reasons.length ? reasons.slice(0, 4) : ["მწვავე vital/ECG/ბიომარკერის სიგნალი არ ჩანს"],
  };
}

function missingForBetterAssessment(risk) {
  const target = risk?.target_name || "";
  const items = [];
  const addIfMissing = (key, text) => {
    if (!isFeaturePresent(key)) items.push(text);
  };

  if (["target_myocardial_infarction", "target_acute_ischemic_heart_disease", "target_angina_pectoris"].includes(target)) {
    addIfMissing("lab_troponin_t_mean", "Troponin T უკეთ ამყარებს ან ასუსტებს კორონარულ/ინფარქტის ეჭვს.");
    if (selectedEcgOption().value === "not_available" && !ecgNote.trim()) items.push("ECG საჭიროა იშემიური ცვლილებების შესადარებლად.");
    addIfMissing("symptom_chest_pain", "გულმკერდის ტკივილის არსებობა/უარყოფა მნიშვნელოვანია.");
  }
  if (target === "target_heart_failure") {
    addIfMissing("lab_ntprobnp_mean", "NT-proBNP უკეთ აფასებს გულის დატვირთვას/უკმარისობის ეჭვს.");
    addIfMissing("ed_triage_spo2_mean", "SpO2 და სუნთქვის მაჩვენებლები საჭიროა სიმძიმის შესაფასებლად.");
  }
  if (target.includes("hypertensive")) {
    if (!baselineBpValues().hasBaseline) items.push("პაციენტის ჩვეულებრივი არტერიული წნევა დაეხმარება მიმდინარე წნევის სწორად შეფასებას.");
    addIfMissing("lab_creatinine_mean", "კრეატინინი საჭიროა თირკმლის დაზიანების/ჰიპერტენზიული გართულების შესაფასებლად.");
  }
  if (target.includes("arrhythmia") || target.includes("fibrillation") || target.includes("tachycardia") || target.includes("conduction")) {
    if (selectedEcgOption().value === "not_available" && !ecgNote.trim()) items.push("ECG rhythm strip საჭიროა რიტმის/გამტარობის დასადასტურებლად.");
    addIfMissing("ed_triage_heart_rate_mean", "გულისცემის მაჩვენებელი საჭიროა რიტმის სიმძიმის შესაფასებლად.");
  }
  if (!baselineBpValues().hasBaseline && (numericFeature("ed_triage_sbp_mean") >= 140 || numericFeature("omr_sbp_mean") >= 140)) {
    items.push("თუ ცნობილია, დაამატეთ პაციენტის ჩვეულებრივი წნევა, რათა მაღალი წნევა baseline-ს შევადაროთ.");
  }

  return uniqueItems(items).slice(0, 4);
}

function uniqueItems(items) {
  const seen = new Set();
  return items
    .map((item) => String(item || "").replace(/\s+/g, " ").trim())
    .filter(Boolean)
    .filter((item) => {
      const key = item.toLowerCase();
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
}

function isFeaturePresent(key) {
  if (!features || clearedFieldKeys.has(key)) return false;
  if (Number(features[`${key}_missing`] ?? 0) === 1) return false;
  const value = features[key];
  if (value === null || value === undefined || value === "") return false;
  if (typeof value === "number" && !Number.isFinite(value)) return false;
  return true;
}

function dataQualitySummary() {
  if (!features) {
    return {
      score: 0,
      label: "მონაცემები არ არის ჩატვირთული",
      className: "low",
      missingGroups: dataQualityGroups,
      presentGroups: [],
      recommendation: "ჩატვირთეთ სატესტო პაციენტი ან შეავსეთ ფორმა.",
    };
  }

  const groupResults = dataQualityGroups.map((group) => {
    const presentRatio = group.customPresent
      ? group.customPresent()
        ? 1
        : 0
      : group.keys.filter((key) => isFeaturePresent(key)).length / group.keys.length;
    return { ...group, presentRatio };
  });
  const totalWeight = groupResults.reduce((sum, group) => sum + group.weight, 0);
  const weightedScore = groupResults.reduce((sum, group) => sum + group.weight * group.presentRatio, 0);
  const score = Math.round((weightedScore / totalWeight) * 100);
  const missingGroups = groupResults.filter((group) => group.presentRatio < 0.75);
  const presentGroups = groupResults.filter((group) => group.presentRatio >= 0.75);

  let label = "საკმარისი მონაცემები";
  let className = "good";
  if (score < 55) {
    label = "სუსტი მონაცემები";
    className = "low";
  } else if (score < 80) {
    label = "ნაწილობრივ სრული მონაცემები";
    className = "medium";
  }

  return {
    score,
    label,
    className,
    missingGroups,
    presentGroups,
    recommendation: missingGroups.length
      ? missingGroups[0].fix
      : "მონაცემები საკმარისად სრულად გამოიყურება; ახლა მთავარი ყურადღება კლინიკურ დადასტურებაზე გადადის.",
  };
}

function clinicalActionGroups(risk) {
  const quality = dataQualitySummary();
  const urgency = urgencyAssessment(risk);
  const ecg = ecgAlignment(risk);
  const diagnosisChecks = uniqueItems([...(risk?.suggested_clinical_checks || []).slice(0, 4), ...ecgClinicalChecks()]);
  const dataChecks = uniqueItems([...missingForBetterAssessment(risk), ...quality.missingGroups.slice(0, 3).map((group) => group.fix)]);
  const safetyChecks = [
    `${urgency.label}: ${urgency.text}`,
    ecg.text,
    "ეს პასუხი გამოიყენეთ როგორც კლინიკური დამხმარე სიგნალი; საბოლოო დიაგნოზი და მკურნალობა ექიმმა უნდა განსაზღვროს.",
  ];

  return [
    {
      title: "დიაგნოზის გადამოწმება",
      items: diagnosisChecks.length ? diagnosisChecks : ["მთავარი სავარაუდო მიმართულება შეადარეთ პაციენტის ჩივილებს, ანამნეზს და ფიზიკურ გასინჯვას."],
    },
    {
      title: "მონაცემების შევსება",
      items: dataChecks.length ? dataChecks : ["მონაცემების ძირითადი ჯგუფები შევსებულია; გადაამოწმეთ მხოლოდ საეჭვო ან უკიდურესი მნიშვნელობები."],
    },
    {
      title: "უსაფრთხოების შეზღუდვა",
      items: safetyChecks,
    },
  ];
}

function applySymptomText(nextFeatures, text) {
  const detected = parseSymptomText(text);
  Object.entries(detected).forEach(([key, value]) => {
    nextFeatures[key] = value;
    if (`${key}_missing` in nextFeatures) nextFeatures[`${key}_missing`] = text.trim() ? 0 : 1;
  });
  return nextFeatures;
}

function syncMeasurementMetadata(nextFeatures, key, isMissing) {
  const missingKey = `${key}_missing`;
  const countKey = `${key}_count`;
  const countMissingKey = `${countKey}_missing`;

  if (missingKey in nextFeatures) nextFeatures[missingKey] = isMissing ? 1 : 0;
  if (countKey in nextFeatures) nextFeatures[countKey] = isMissing ? 0 : 1;
  if (countMissingKey in nextFeatures) nextFeatures[countMissingKey] = isMissing ? 1 : 0;
}

function syncInteractionMissing(nextFeatures, interactionKey, componentKeys) {
  const missingKey = `${interactionKey}_missing`;
  if (!(missingKey in nextFeatures)) return;
  nextFeatures[missingKey] = componentKeys.some((key) => Number(nextFeatures[`${key}_missing`] ?? 0) === 1) ? 1 : 0;
}

function recomputeBmi(nextFeatures) {
  const weightMissing = Number(nextFeatures.omr_weight_lbs_mean_missing ?? 0) === 1;
  const heightMissing = Number(nextFeatures.omr_height_inches_mean_missing ?? 0) === 1;
  const weightLbs = Number(nextFeatures.omr_weight_lbs_mean);
  const heightInches = Number(nextFeatures.omr_height_inches_mean);

  if (weightMissing || heightMissing || !Number.isFinite(weightLbs) || !Number.isFinite(heightInches) || heightInches <= 0) {
    nextFeatures.omr_bmi_mean = optionalDefaults.omr_bmi_mean;
    syncMeasurementMetadata(nextFeatures, "omr_bmi_mean", true);
    return;
  }

  nextFeatures.omr_bmi_mean = (weightLbs / (heightInches * heightInches)) * 703;
  clearedFieldKeys.delete("omr_bmi_mean");
  syncMeasurementMetadata(nextFeatures, "omr_bmi_mean", false);
}

function recomputeDerivedFeatures(nextFeatures) {
  recomputeBmi(nextFeatures);
  if ("interaction_age_omr_sbp" in nextFeatures) {
    nextFeatures.interaction_age_omr_sbp = Number(nextFeatures.age) * Number(nextFeatures.omr_sbp_mean);
    syncInteractionMissing(nextFeatures, "interaction_age_omr_sbp", ["age", "omr_sbp_mean"]);
  }
  if ("interaction_bmi_omr_sbp" in nextFeatures) {
    nextFeatures.interaction_bmi_omr_sbp = Number(nextFeatures.omr_bmi_mean) * Number(nextFeatures.omr_sbp_mean);
    syncInteractionMissing(nextFeatures, "interaction_bmi_omr_sbp", ["omr_bmi_mean", "omr_sbp_mean"]);
  }
  if ("interaction_glucose_bmi" in nextFeatures) {
    nextFeatures.interaction_glucose_bmi = Number(nextFeatures.lab_glucose_mean) * Number(nextFeatures.omr_bmi_mean);
    syncInteractionMissing(nextFeatures, "interaction_glucose_bmi", ["lab_glucose_mean", "omr_bmi_mean"]);
  }
  if ("interaction_ntprobnp_age" in nextFeatures) {
    nextFeatures.interaction_ntprobnp_age = Number(nextFeatures.lab_ntprobnp_mean) * Number(nextFeatures.age);
    syncInteractionMissing(nextFeatures, "interaction_ntprobnp_age", ["lab_ntprobnp_mean", "age"]);
  }
  return nextFeatures;
}

function updateFeatureFromInput(key, rawValue) {
  const field = editableFields.find((item) => item.key === key);
  const nextFeatures = { ...features };
  const normalizedValue = String(rawValue).replace(",", ".").trim();

  clearedFieldKeys.delete(key);
  if (field?.optional && normalizedValue === "") {
    clearedFieldKeys.add(key);
    nextFeatures[key] = optionalDefaults[key];
    syncMeasurementMetadata(nextFeatures, key, true);
  } else {
    if (normalizedValue === "") {
      clearedFieldKeys.add(key);
      return;
    }
    let value = Number(normalizedValue);
    if (!Number.isFinite(value)) return;
    if (field?.displayUnit === "kg") value *= 2.20462;
    if (field?.displayUnit === "cm") value /= 2.54;
    if (field?.displayUnit === "celsius") value = value * (9 / 5) + 32;
    nextFeatures[key] = value;
    syncMeasurementMetadata(nextFeatures, key, false);
  }

  features = recomputeDerivedFeatures(nextFeatures);
}

function clearPatientData() {
  const baseFeatures = sample ? { ...sample.features } : { ...features };
  editableFields.forEach((field) => {
    clearedFieldKeys.add(field.key);
    if (field.type === "boolean") baseFeatures[field.key] = 0;
    if (field.optional) syncMeasurementMetadata(baseFeatures, field.key, true);
  });
  symptomText = "";
  ecgFinding = "not_available";
  ecgNote = "";
  baselineSbp = "";
  baselineDbp = "";
  features = recomputeDerivedFeatures(baseFeatures);
  result = null;
  statusText = "ყველა მონაცემი გასუფთავდა.";
}

function fieldDisabled(field) {
  return !features;
}

function renderInputField(field) {
  const status = fieldStatus(field);
  return `
    <label class="field ${status ? status.className : ""}">
      <span>
        ${field.label}
        ${status ? `<small class="field-status">${status.label}</small>` : field.unit ? `<small>${field.unit}</small>` : ""}
      </span>
      ${
        field.type === "computed"
          ? `<div class="computed-field">
              <div>
                <strong>${inputValue(field) || "—"}</strong>
                <em class="${bmiStatus().className}">${bmiStatus().label}</em>
              </div>
              <small>ნორმა ${labRangeText(bmiReference)}<br>ითვლება წონით და სიმაღლით</small>
            </div>`
          : 
        field.type === "select" || field.type === "boolean"
          ? `<select data-feature="${field.key}" ${fieldDisabled(field) ? "disabled" : ""}>
              <option value="" ${clearedFieldKeys.has(field.key) ? "selected" : ""}>აირჩიეთ</option>
              ${(field.options || [
                { value: 0, label: "არა" },
                { value: 1, label: "დიახ" },
              ])
                .map(
                  (option) => `
                    <option value="${option.value}" ${!clearedFieldKeys.has(field.key) && Number(features?.[field.key]) === option.value ? "selected" : ""}>
                      ${option.label}
                    </option>
                  `,
                )
                .join("")}
            </select>`
          : `<input
              data-feature="${field.key}"
              type="text"
              inputmode="decimal"
              placeholder="${field.optional ? "არასავალდებულო" : "შეიყვანეთ"}"
              value="${inputValue(field)}"
              ${fieldDisabled(field) ? "disabled" : ""}
            />`
      }
    </label>
  `;
}

function renderBaselineBpInput() {
  const assessment = baselineBpAssessment();
  return `
    <section class="form-section baseline-bp-section">
      <div class="section-heading">
        <div>
          <h3>პაციენტის ჩვეულებრივი არტერიული წნევა (თუ ცნობილია)</h3>
          <p>არასავალდებულოა. თუ მითითებულია, სისტემა მიმდინარე წნევას პაციენტის საკუთარ baseline მაჩვენებელს შეადარებს.</p>
        </div>
      </div>
      <div class="field-grid baseline-grid">
        <label class="field">
          <span>ჩვეულებრივი სისტოლური წნევა <small>mmHg</small></span>
          <input id="baseline-sbp" type="text" inputmode="decimal" placeholder="არასავალდებულო" value="${escapeHtml(baselineSbp)}" ${features ? "" : "disabled"} />
        </label>
        <label class="field">
          <span>ჩვეულებრივი დიასტოლური წნევა <small>mmHg</small></span>
          <input id="baseline-dbp" type="text" inputmode="decimal" placeholder="არასავალდებულო" value="${escapeHtml(baselineDbp)}" ${features ? "" : "disabled"} />
        </label>
      </div>
      <p class="baseline-note ${assessment.className}">${escapeHtml(assessment.text)}</p>
    </section>
  `;
}

function renderFormSections() {
  return formSections
    .map(
      (section) => `
        <section class="form-section">
          <div class="section-heading">
            <div>
              <h3>${section.title}</h3>
              <p>${section.description}</p>
            </div>
            ${
              section.reference === "labs"
                ? `<button class="section-action" id="lab-reference-button">ნორმები</button>`
                : ""
            }
          </div>
          <div class="field-grid">
            ${section.keys.map((key) => renderInputField(editableFieldByKey[key])).join("")}
          </div>
        </section>
      `,
    )
    .join("");
}

function renderLabReferenceWindow() {
  if (!isLabReferenceOpen) return "";
  return `
    <div class="reference-overlay" role="dialog" aria-modal="true">
      <div class="reference-window">
        <div class="reference-header">
          <div>
            <h2>ლაბორატორიული ნორმები</h2>
            <p>საორიენტაციო დიაპაზონები. ზუსტი ნორმები შეიძლება პაციენტის მდგომარეობისა და ლაბორატორიის მიხედვით განსხვავდებოდეს.</p>
          </div>
          <button class="icon-button" id="close-lab-reference" aria-label="დახურვა">×</button>
        </div>
        <div class="reference-table">
          ${labReferenceRanges
            .map((reference) => {
              const status = labStatus(reference);
              return `
                <div class="reference-row">
                  <strong>${reference.label}</strong>
                  <span>${labDisplayValue(reference)} ${labDisplayValue(reference) === "—" ? "" : reference.unit}</span>
                  <span>${labRangeText(reference)}</span>
                  <em class="${status.className}">${status.label}</em>
                </div>
              `;
            })
            .join("")}
        </div>
      </div>
    </div>
  `;
}

function updateSymptomText(rawText) {
  symptomText = rawText;
  features = recomputeDerivedFeatures(applySymptomText({ ...features }, symptomText));
}

function syncSymptomControls() {
  symptomTextRules.forEach((rule) => {
    const select = document.querySelector(`select[data-feature="${rule.key}"]`);
    if (select) select.value = String(features[rule.key] ?? 0);
  });
  const detected = document.getElementById("detected-symptoms");
  if (detected) detected.innerHTML = renderDetectedSymptoms();
}

function renderFactors() {
  if (!result) return "";

  return `
    <div class="factors">
      <h3>მთავარი SHAP ფაქტორები</h3>
      ${result.top_factors
        .map(
          (factor) => `
            <div class="factor-row">
              <div>
                <strong>${displayFeatureName(factor.feature)}</strong>
                <span>${factor.feature_group || "კლინიკური მახასიათებელი"} · მნიშვნელობა: ${Number(factor.value).toFixed(3)}</span>
              </div>
              <div class="${factor.direction === "increases_risk" ? "positive" : "negative"}">
                ${factor.direction === "increases_risk" ? "+" : ""}${Number(factor.shap_value).toFixed(4)}
              </div>
            </div>
          `,
        )
        .join("")}
    </div>
  `;
}

function riskReasonText(risk, limit = 3) {
  const reasons = clinicalReasonList(risk, limit);
  return reasons.length
    ? reasons.join(", ")
    : "მკვეთრი განმსაზღვრელი ფაქტორი არ გამოიკვეთა";
}

function clinicalReasonList(risk, limit = 4) {
  if (!risk?.reason_factors?.length) return [];
  const seen = new Set();
  return risk.reason_factors
    .map((item) => String(item || "").replace(/\s+/g, " ").replace(/^[-–•]\s*/, "").trim())
    .filter(Boolean)
    .filter((item) => {
      const key = item.toLowerCase();
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    })
    .slice(0, limit);
}

function renderReasonChips(risk, limit = 4) {
  const reasons = clinicalReasonList(risk, limit);
  if (!reasons.length) return `<span class="driver-chip muted">მკვეთრი განმსაზღვრელი ფაქტორი არ გამოიკვეთა</span>`;
  return reasons.map((item) => `<span class="driver-chip">${escapeHtml(item)}</span>`).join("");
}

function clinicalResemblanceText(risk) {
  const reasons = clinicalReasonList(risk, 5);
  if (!reasons.length) return "მკვეთრი განმსაზღვრელი კლინიკური კომბინაცია არ გამოიკვეთა";
  return reasons.join(" + ");
}

function ecgResultContext() {
  const selected = selectedEcgOption();
  if (selected.value === "not_available") return "";
  if (selected.value === "normal") {
    return "ECG კონტექსტი: ნორმალური ECG ამ ეტაპზე მწვავე ECG-სიგნალს არ ამატებს, თუმცა კლინიკურ შეფასებას სრულად არ ცვლის.";
  }
  return `ECG კონტექსტი: ${selected.label} აძლიერებს შესაბამისი კარდიოლოგიური მიმართულების გადამოწმების საჭიროებას.`;
}

function getPrimaryDiagnosticRisk() {
  if (!result?.subtype_risks?.length) return null;
  const diagnosticCandidates = result.subtype_risks.filter((risk) =>
    ["high", "diagnostic_signal"].includes(risk.diagnosis_confidence),
  );
  return diagnosticCandidates[0] || result.subtype_risks[0];
}

function diagnosisSeverityRank(risk) {
  const confidenceRank = {
    high: 4,
    diagnostic_signal: 3,
    borderline: 2,
    low: 1,
  }[risk.diagnosis_confidence] || 0;
  const riskRank = { high: 3, medium: 2, low: 1 }[risk.risk_level] || 0;
  const supportRank = { strong: 3, partial: 2, weak: 1 }[risk.clinical_support_level] || 0;
  return confidenceRank * 100 + supportRank * 10 + riskRank;
}

function sortByClinicalSeverity(risks) {
  return [...risks].sort((a, b) => {
    const severityDelta = diagnosisSeverityRank(b) - diagnosisSeverityRank(a);
    if (severityDelta) return severityDelta;
    return (b.diagnosis_probability ?? b.risk_probability) - (a.diagnosis_probability ?? a.risk_probability);
  });
}

function renderProbabilityMeter(risk) {
  const probability = clampPercent(risk.diagnosis_probability ?? risk.risk_probability);
  const threshold = clampPercent(risk.diagnosis_threshold ?? 0.5);
  return `
    <div class="probability-meter" aria-label="ალბათობა ${probability}% ზღვარი ${threshold}%">
      <div class="meter-track">
        <span class="meter-fill ${confidenceClass(risk.diagnosis_confidence)}" style="width: ${probability}%"></span>
        <span class="meter-threshold" style="left: ${threshold}%"></span>
      </div>
      <div class="meter-labels">
        <span>${probability}%</span>
        <span>ზღვარი ${threshold}%</span>
      </div>
    </div>
  `;
}

function renderClinicalSupport(risk) {
  const score = Number(risk.clinical_support_score ?? 0);
  const level = risk.clinical_support_level || "weak";
  const reasons = risk.clinical_support_reasons || [];
  return `
    <div class="clinical-support ${supportClass(level)}">
      <div class="support-heading">
        <div>
          <span>კლინიკური მხარდაჭერა</span>
          <strong>${escapeHtml(supportLabel(level))}</strong>
        </div>
        <b>${Math.round(score)}%</b>
      </div>
      <div class="support-meter" aria-label="კლინიკური მხარდაჭერა ${Math.round(score)}%">
        <span style="width: ${Math.max(0, Math.min(100, score))}%"></span>
      </div>
      <ul>
        ${reasons.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
      </ul>
      ${risk.verification_priority ? `<em>${escapeHtml(risk.verification_priority)}</em>` : ""}
      ${risk.reliability_note ? `<small>${escapeHtml(risk.reliability_note)}</small>` : ""}
    </div>
  `;
}

function renderClinicalTriagePanel(risk) {
  const urgency = urgencyAssessment(risk);
  const ecg = ecgAlignment(risk);
  return `
    <div class="triage-panel">
      <section class="triage-card ${urgency.className}">
        <span>სასწრაფოობის დონე</span>
        <strong>${escapeHtml(urgency.label)}</strong>
        <p>${escapeHtml(urgency.text)}</p>
        <ul>
          ${urgency.reasons.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </section>
      <section class="triage-card ecg-${ecg.className}">
        <span>ECG შესაბამისობა</span>
        <strong>${escapeHtml(ecg.label)}</strong>
        <p>${escapeHtml(ecg.text)}</p>
      </section>
    </div>
  `;
}

function renderMissingAssessmentPanel(risk) {
  const missing = missingForBetterAssessment(risk);
  if (!missing.length) return "";
  return `
    <div class="missing-assessment">
      <span>რა გააუმჯობესებს შეფასებას</span>
      <ul>
        ${missing.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
      </ul>
    </div>
  `;
}

function renderDecisionSummary() {
  if (!result?.subtype_risks?.length) return "";
  const topRisk = getPrimaryDiagnosticRisk();
  const secondRisk = result.subtype_risks.find((risk) => risk.target_name !== topRisk.target_name);
  const ecgContext = ecgResultContext();

  return `
    <div class="decision-summary">
      <div class="decision-topline">
        <span>მთავარი სავარაუდო მიმართულება</span>
        <em class="status-pill ${confidenceClass(topRisk.diagnosis_confidence)}">${diagnosisConfidenceLabel(topRisk.diagnosis_confidence)}</em>
      </div>
      <strong>${escapeHtml(topRisk.diagnosis_label || topRisk.display_name)}</strong>
      <div class="decision-score">
        <b>${formatPercent(topRisk.diagnosis_probability ?? topRisk.risk_probability)}</b>
        <em>დიაგნოსტიკური ზღვარი ${formatPercent(topRisk.diagnosis_threshold ?? 0.5)}</em>
      </div>
      ${renderProbabilityMeter(topRisk)}
      ${renderClinicalSupport(topRisk)}
      ${renderClinicalTriagePanel(topRisk)}
      ${renderMissingAssessmentPanel(topRisk)}
      <div class="clinical-driver-block">
        <span>3 მთავარი მიზეზი</span>
        <div class="driver-list">${renderReasonChips(topRisk)}</div>
      </div>
      <div class="clinical-driver-block resemblance-block">
        <span>რატომ ჰგავს ამ დიაგნოზს</span>
        <p>${escapeHtml(clinicalResemblanceText(topRisk))}</p>
      </div>
      ${ecgContext ? `<div class="ecg-context-note">${escapeHtml(ecgContext)}</div>` : ""}
      <p>${escapeHtml(topRisk.diagnosis_interpretation || "სისტემა ამ პაციენტის მონაცემებში ხედავს მსგავსებას შესაბამის ICD-კოდირებულ შემთხვევებთან.")}</p>
      ${
        secondRisk
          ? `<small>შემდეგი შესადარებელი მიმართულება: ${escapeHtml(secondRisk.display_name)} (${formatPercent(secondRisk.risk_probability)}). ეს არ ნიშნავს საბოლოო დიაგნოზს.</small>`
          : ""
      }
    </div>
  `;
}

function renderSubtypeRisks() {
  if (!result?.subtype_risks?.length) return "";
  const topRisk = getPrimaryDiagnosticRisk();
  const otherRisks = sortByClinicalSeverity(result.subtype_risks.filter((risk) => risk.target_name !== topRisk.target_name));
  const visibleRisks = isAllDiagnosesOpen ? otherRisks : otherRisks.slice(0, 4);
  const hiddenCount = Math.max(0, otherRisks.length - visibleRisks.length);

  return `
    <div class="subtype-section">
      <h3>რისკები დაავადების ჯგუფების მიხედვით</h3>
      <div class="top-disease ${topRisk.risk_level}">
        <div class="disease-heading">
          <span>მთავარი სავარაუდო მიმართულება</span>
          <em class="status-pill ${confidenceClass(topRisk.diagnosis_confidence)}">${topRisk.diagnosis_status || diseaseRiskLabel(topRisk.risk_level)}</em>
        </div>
        <strong>${escapeHtml(topRisk.display_name)}</strong>
        <b>${formatPercent(topRisk.diagnosis_probability ?? topRisk.risk_probability)}</b>
        ${renderProbabilityMeter(topRisk)}
        ${renderClinicalSupport(topRisk)}
        <div class="driver-list compact">${renderReasonChips(topRisk, 3)}</div>
      </div>
      <div class="subtype-list-header">
        <div>
          <strong>${isAllDiagnosesOpen ? "ყველა დიაგნოზის ჯგუფი" : "მნიშვნელოვანი შედარებითი მიმართულებები"}</strong>
          <span>${isAllDiagnosesOpen ? "ნაჩვენებია ყველა მოდელირებული ICD-ჯგუფი." : "ნაჩვენებია მხოლოდ top 4, რომ მთავარი დასკვნა არ გადაიტვირთოს."}</span>
        </div>
        ${
          otherRisks.length > 4
            ? `<button class="secondary-button compact-button" id="toggle-diagnoses-button">
                ${isAllDiagnosesOpen ? "მხოლოდ top 4" : `ყველა ჯგუფის ნახვა (${hiddenCount} მეტი)`}
              </button>`
            : ""
        }
      </div>
      <div class="subtype-grid">
        ${visibleRisks
          .map(
            (risk) => `
              <div class="subtype-card ${risk.risk_level}">
                <div class="subtype-main">
                  <strong>${escapeHtml(risk.display_name)}</strong>
                  <em>${risk.diagnosis_status || diseaseRiskLabel(risk.risk_level)}</em>
                  <small>${escapeHtml(risk.verification_priority || supportLabel(risk.clinical_support_level))}</small>
                  <span>${escapeHtml(riskReasonText(risk, 2))}</span>
                  ${renderProbabilityMeter(risk)}
                </div>
                <b class="${confidenceClass(risk.diagnosis_confidence)}">${diagnosisConfidenceLabel(risk.diagnosis_confidence)}</b>
              </div>
            `,
          )
          .join("")}
      </div>
      <p class="diagnosis-note">შეზღუდვა: სისტემა არ სვამს საბოლოო დიაგნოზს. ის აჩვენებს სავარაუდო ICD-კოდირებულ მიმართულებებს MIMIC-IV მონაცემებზე ნასწავლი მსგავსებების მიხედვით და საჭიროებს ექიმის დადასტურებას.</p>
      ${renderClinicalChecks(topRisk)}
    </div>
  `;
}

function renderDataQualityPanel() {
  const quality = dataQualitySummary();
  return `
    <div class="data-quality-card ${quality.className}">
      <div class="data-quality-header">
        <div>
          <span>მონაცემების ხარისხი</span>
          <strong>${quality.label}</strong>
        </div>
        <b>${quality.score}%</b>
      </div>
      <div class="quality-meter" aria-label="მონაცემების ხარისხი ${quality.score}%">
        <span style="width: ${quality.score}%"></span>
      </div>
      <p>${escapeHtml(quality.recommendation)}</p>
      <div class="quality-groups">
        ${
          quality.presentGroups.length
            ? `<span>შევსებულია: ${escapeHtml(quality.presentGroups.map((group) => group.title).slice(0, 3).join(", "))}</span>`
            : ""
        }
        ${
          quality.missingGroups.length
            ? `<span>დასამატებელია: ${escapeHtml(quality.missingGroups.map((group) => group.title).slice(0, 3).join(", "))}</span>`
            : ""
        }
      </div>
    </div>
  `;
}

function renderClinicalChecks(risk) {
  const actionGroups = clinicalActionGroups(risk);
  return `
    <div class="clinical-checks">
      <h4>ექიმმა დამატებით გადაამოწმოს</h4>
      <div class="clinical-check-groups">
        ${actionGroups
          .map(
            (group) => `
              <section class="check-group">
                <strong>${escapeHtml(group.title)}</strong>
                <ul>
                  ${group.items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
                </ul>
              </section>
            `,
          )
          .join("")}
      </div>
    </div>
  `;
}

function renderModelTrust() {
  if (!isModelTrustOpen) return "";
  return `
    <div class="reference-overlay" id="model-trust-overlay" role="dialog" aria-modal="true">
      <div class="reference-window">
        <div class="reference-header">
          <div>
            <h2>მოდელის ტექნიკური შეფასება</h2>
            <p>მოკლე, ადამიანურად წაკითხვადი შეფასება იმისა, რამდენად სანდოა მოდელის სიგნალები test მონაცემებზე.</p>
          </div>
          <button class="icon-button" id="close-model-trust" aria-label="დახურვა">×</button>
        </div>
        <div class="model-trust">
          <div class="trust-summary">
            ${modelTrustNotes
              .map(
                (note) => `
                  <section>
                    <strong>${note.title}</strong>
                    <p>${note.text}</p>
                  </section>
                `,
              )
              .join("")}
          </div>
          <div class="metric-guide" aria-label="მეტრიკების განმარტება">
            ${metricDescriptions
              .map(
                (description) => `
                  <div>
                    <b>${description.label}</b>
                    <span>${description.note}</span>
                    <small>${description.technical}</small>
                  </div>
                `,
              )
              .join("")}
          </div>
          <div class="metric-grid">
            ${modelMetrics
              .map(
                (metric) => `
                  <div class="metric-row">
                    <strong>${metric.label}</strong>
                    ${metricDescriptions
                      .map(
                        (description) => `
                          <span title="${description.note}">
                            <small>${description.label}</small>
                            <b>${metric[description.key]}</b>
                            <i>${description.technical}</i>
                          </span>
                        `,
                      )
                      .join("")}
                  </div>
                `,
              )
              .join("")}
          </div>
          <div class="trust-footnote">
            <strong>საბოლოო ინტერპრეტაცია</strong>
            <p>მაჩვენებლები დათვლილია test ნაწილზე. დიაგნოზის ჯგუფებისთვის ზღვარი შეირჩა validation ნაწილზე, რათა დადებითი და უარყოფითი პასუხები უკეთ დაბალანსდეს. დაბალი precision ზოგ subtype-ში ნიშნავს, რომ დადებითი სიგნალი ექიმმა დამატებით უნდა გადაამოწმოს.</p>
          </div>
        </div>
      </div>
    </div>
  `;
}

function renderModelTrustAction() {
  return `
    <div class="model-trust-action">
      <button class="secondary-button" id="model-trust-button">მოდელის ტექნიკური შეფასება</button>
    </div>
  `;
}

function patientProfileText() {
  if (!features) return "";
  const sex = Number(features.gender_male) === 1 ? "მამრობითი" : "მდედრობითი";
  const bmi = Number(features.omr_bmi_mean).toFixed(1);
  const sbp = Math.round(Number(features.omr_sbp_mean));
  const dbp = Math.round(Number(features.omr_dbp_mean));
  const glucose = Number(features.lab_glucose_mean).toFixed(2);
  const creatinine = Number(features.lab_creatinine_mean).toFixed(2);
  const symptomDetails = Object.values(parseSymptomTextDetailed(symptomText)).filter((item) => item.status !== "absent");
  const symptoms = symptomText.trim()
    ? symptomDetails.length
      ? symptomDetails.map((item) => `${item.label} - ${symptomStatusLabel(item.status)}`).join(", ")
      : "ტექსტში სპეციფიკური გულ-სისხლძარღვთა სიმპტომი არ დაფიქსირდა"
    : "სიმპტომების დამატებითი ტექსტი არ არის მითითებული";

  return [
    `პაციენტი: ასაკი ${Math.round(Number(features.age))} წელი, სქესი ${sex}.`,
    `ძირითადი მონაცემები: BMI ${bmi}, არტერიული წნევა ${sbp}/${dbp} mmHg, გლუკოზა ${glucose} mg/dL, კრეატინინი ${creatinine} mg/dL.`,
    `სიმპტომები: ${symptoms}.`,
    `ECG: ${ecgClinicalText()}.`,
  ].join("\n");
}

function patientReportText() {
  if (!result?.subtype_risks?.length) return "";
  const topRisk = getPrimaryDiagnosticRisk();
  const quality = dataQualitySummary();
  const actionGroups = clinicalActionGroups(topRisk);
  const topThree = result.subtype_risks
    .slice(0, 3)
    .map((risk, index) => `${index + 1}. ${risk.display_name}: ${formatPercent(risk.diagnosis_probability ?? risk.risk_probability)} (${risk.diagnosis_status})`)
    .join("\n");
  const reasons = clinicalReasonList(topRisk, 5).map((item) => `- ${item}`).join("\n") || "- მკვეთრი განმსაზღვრელი ფაქტორი არ გამოიკვეთა";
  const supportReasons =
    (topRisk.clinical_support_reasons || []).map((item) => `- ${item}`).join("\n") || "- სპეციფიკური კლინიკური დამადასტურებელი ნიშანი მკვეთრად არ ჩანს";
  const urgency = urgencyAssessment(topRisk);
  const ecgAlignmentSummary = ecgAlignment(topRisk);
  const bpAssessment = baselineBpAssessment();
  const missingAssessment = missingForBetterAssessment(topRisk);
  const ecgContext = ecgResultContext();
  const checks = actionGroups
    .map((group) => [`${group.title}:`, ...group.items.map((item) => `- ${item}`)].join("\n"))
    .join("\n\n");

  return [
    "პაციენტის სავარაუდო დიაგნოსტიკური ანგარიში",
    "",
    patientProfileText(),
    "",
    "სავარაუდო მთავარი მიმართულება:",
    `${topRisk.display_name} - ${formatPercent(topRisk.diagnosis_probability ?? topRisk.risk_probability)} (${topRisk.diagnosis_status}).`,
    "",
    "რა განსაზღვრავს ამ რისკს:",
    reasons,
    "",
    "რატომ ჰგავს ამ დიაგნოზს:",
    clinicalResemblanceText(topRisk),
    "",
    "კლინიკური მხარდაჭერა:",
    `${supportLabel(topRisk.clinical_support_level)} - ${Math.round(Number(topRisk.clinical_support_score ?? 0))}%.`,
    supportReasons,
    topRisk.reliability_note || "",
    topRisk.verification_priority ? `პრიორიტეტი: ${topRisk.verification_priority}` : "",
    "",
    "სასწრაფოობის დონე:",
    `${urgency.label}. ${urgency.text}`,
    ...urgency.reasons.map((item) => `- ${item}`),
    "",
    "წნევის baseline შედარება:",
    bpAssessment.text,
    ...(missingAssessment.length ? ["", "რა გააუმჯობესებს შეფასებას:", ...missingAssessment.map((item) => `- ${item}`)] : []),
    "",
    "ECG შესაბამისობა:",
    `${ecgAlignmentSummary.label}. ${ecgAlignmentSummary.text}`,
    ...(ecgContext ? ["", ecgContext] : []),
    "",
    "მონაცემების ხარისხი:",
    `${quality.label} - ${quality.score}%. ${quality.recommendation}`,
    "",
    "სხვა შესადარებელი მიმართულებები:",
    topThree,
    "",
    "ექიმმა დამატებით უნდა გადაამოწმოს:",
    checks,
    "",
    `საერთო გულ-სისხლძარღვთა სიგნალი: ${formatPercent(result.risk_probability)} (${riskLabel(result.risk_level)}).`,
    "შეზღუდვა: სისტემა არ სვამს საბოლოო დიაგნოზს; ის აჩვენებს სავარაუდო დიაგნოსტიკურ მიმართულებებს MIMIC-IV მონაცემებზე ნასწავლი მსგავსებების მიხედვით.",
  ].join("\n");
}

function renderPatientReport() {
  if (!result) return "";
  return `
    <div class="patient-report">
      <div class="report-header">
        <h3>პაციენტის ანგარიში</h3>
        <button class="secondary-button" id="copy-report-button">ანგარიშის კოპირება</button>
      </div>
      <textarea readonly>${escapeHtml(patientReportText())}</textarea>
    </div>
  `;
}

function renderClinicalImpacts() {
  if (!result?.clinical_impacts?.length) return "";

  return `
    <div class="patient-analysis">
      <h3>ახალი პაციენტის მოდელური ანალიზი</h3>
      <p>${result.patient_analysis_summary}</p>
      <div class="impact-grid">
        ${result.clinical_impacts
          .map(
            (impact) => `
              <div class="impact-row ${impact.risk_delta >= 0 ? "risk-up" : "risk-down"}">
                <div>
                  <strong>${impact.factor_group}</strong>
                  <span>${impact.explanation}</span>
                  <small>${impact.reference_profile}</small>
                </div>
                <b>${impact.risk_delta >= 0 ? "+" : ""}${formatPercent(impact.risk_delta)}</b>
              </div>
            `,
          )
          .join("")}
      </div>
    </div>
  `;
}

function renderDetectedSymptoms() {
  if (!symptomText.trim()) return "სიმპტომების ტექსტი ცარიელია.";
  const details = Object.values(parseSymptomTextDetailed(symptomText)).filter((item) => item.status !== "absent");
  if (!details.length) return "ტექსტიდან ცნობილი გულ-სისხლძარღვთა სიმპტომი ჯერ არ ამოიცნო.";
  return `
    <span class="symptom-parser-title">ტექსტის ანალიზი</span>
    ${details
      .map(
        (item) => `
          <span class="symptom-chip ${item.status}">
            ${item.label}: ${symptomStatusLabel(item.status)}${item.severity === "high" ? " · ძლიერი" : ""}
          </span>
        `,
      )
      .join("")}
  `;
}

function renderEcgInput() {
  return `
    <div class="ecg-box">
      <div class="section-heading">
        <div>
          <h3>ECG პასუხი / ელექტროკარდიოგრამა</h3>
          <p>არასავალდებულო კლინიკური კონტექსტი. ეს ველი არ ცვლის მოდელის probability-ს, მაგრამ ჩანს ინტერპრეტაციასა და პაციენტის ანგარიშში.</p>
        </div>
      </div>
      <div class="ecg-grid">
        <label class="field">
          <span>
            ECG შეფასება
            <small>optional</small>
          </span>
          <select id="ecg-finding" ${features ? "" : "disabled"}>
            ${ecgOptions
              .map(
                (option) => `
                  <option value="${option.value}" ${option.value === ecgFinding ? "selected" : ""}>
                    ${option.label}
                  </option>
                `,
              )
              .join("")}
          </select>
        </label>
        <label class="field ecg-note-field">
          <span>
            ECG აღწერა
            <small>ტექსტი</small>
          </span>
          <textarea
            id="ecg-note"
            placeholder="მაგ: სინუსური რიტმი; ST depression V4-V6; წინაგულთა ფიბრილაცია"
            ${features ? "" : "disabled"}
          >${escapeHtml(ecgNote)}</textarea>
        </label>
      </div>
      <p class="ecg-status ${selectedEcgOption().severity}">
        ${escapeHtml(ecgClinicalText())}
      </p>
    </div>
  `;
}

function symptomStatusLabel(status) {
  if (status === "present") return "დადებითი";
  if (status === "negated") return "უარყოფილია";
  if (status === "historical") return "წარსული/ისტორია";
  if (status === "uncertain") return "გაურკვეველი";
  return "არ ჩანს";
}

function render() {
  document.getElementById("root").innerHTML = `
    <main class="app-shell">
      <section class="topbar">
        <div class="topbar-title">
          <div class="clinical-mark" aria-hidden="true">
            <svg viewBox="0 0 64 64" role="img">
              <path class="heart-shadow" d="M32 53s-19.5-11.4-24-26.1C5.3 18.1 10.2 11 18.5 11c5 0 8.8 2.8 11.1 6.2C31.9 13.8 35.7 11 40.7 11c8.3 0 13.2 7.1 10.5 15.9C46.7 41.6 32 53 32 53Z" />
              <path class="heart-shape" d="M32 50.5s-18.2-10.7-22.4-24.4C7.1 18 11.7 11.5 19.4 11.5c4.7 0 8.2 2.6 10.3 5.8C31.8 14.1 35.3 11.5 40 11.5c7.7 0 12.3 6.5 9.8 14.6C45.6 39.8 32 50.5 32 50.5Z" />
              <path class="heart-highlight" d="M19.8 16.6c-4.3 0-6.8 3.7-5.4 8.1" />
              <path class="heart-pulse" d="M12.5 33h10.1l3.8-7.6 5.5 15.6 5.2-19 4.3 11h10.1" />
            </svg>
          </div>
          <div>
            <p class="eyebrow">კლინიკური გადაწყვეტილების დამხმარე პროტოტიპი</p>
            <h1>გულ-სისხლძარღვთა სავარაუდო დიაგნოზის პროგნოზირება</h1>
          </div>
        </div>
        <div class="server-status">${statusText}</div>
      </section>

      <section class="workspace">
        <div class="panel input-panel">
          <div class="panel-header">
            <div>
              <h2>პაციენტის მონაცემები</h2>
              <p>არასავალდებულო ველები ცარიელი დატოვეთ; დიახ/არა ველები გამოიყენება დიაგნოსტიკურ ახსნაში.</p>
            </div>
            <div class="panel-actions">
              <select class="sample-select" id="sample-select" aria-label="სატესტო პაციენტის არჩევა">
                ${samplePatientOptions
                  .map((option) => `<option value="${option.value}" ${selectedSampleId === option.value ? "selected" : ""}>${option.label}</option>`)
                  .join("")}
              </select>
              <button class="secondary-button compact-button" id="load-sample-button">ჩატვირთვა</button>
              <button class="secondary-button compact-button" id="clear-data-button" ${features ? "" : "disabled"}>გასუფთავება</button>
            </div>
          </div>

          ${renderFormSections()}
          ${renderBaselineBpInput()}
          ${renderEcgInput()}

          <div class="symptom-text-box">
            <label class="field">
              <span>
                დამატებითი სიმპტომები
                <small>ტექსტი</small>
              </span>
              <textarea
                id="symptom-text"
                placeholder="მაგ: პაციენტს აქვს გულმკერდის ტკივილი, ქოშინი და გულის ფრიალი"
                ${features ? "" : "disabled"}
              >${escapeHtml(symptomText)}</textarea>
            </label>
            <p id="detected-symptoms">${renderDetectedSymptoms()}</p>
          </div>

          <div class="action-row">
            <button class="primary-button" id="predict-button" ${!features || isPredicting || hasBlockingClearedFields() ? "disabled" : ""}>
              ${isPredicting ? "მიმდინარეობს პროგნოზირება..." : "პროგნოზის გაშვება"}
            </button>
          </div>
        </div>

        <div class="panel result-panel">
          <div class="panel-header">
            <div>
              <h2>სავარაუდო დიაგნოზის ჯგუფი</h2>
              <p>სისტემა აჩვენებს, რომელ ICD-კოდირებულ გულ-სისხლძარღვთა დიაგნოზის ჯგუფთან ხედავს ყველაზე ძლიერ სიგნალს.</p>
            </div>
          </div>

          ${
            result
              ? `${renderDecisionSummary()}${renderDataQualityPanel()}${renderSubtypeRisks()}${renderModelTrustAction()}${renderPatientReport()}`
              : `<div class="empty-state">სავარაუდო დიაგნოსტიკური მიმართულების სანახავად გაუშვით პროგნოზი.</div>`
          }
        </div>
      </section>
      ${renderLabReferenceWindow()}
      ${renderModelTrust()}
    </main>
  `;

  document.querySelectorAll("input[data-feature]").forEach((input) => {
    input.addEventListener("input", (event) => {
      updateFeatureFromInput(event.target.dataset.feature, event.target.value);
      result = null;
    });
  });

  document.querySelectorAll("select[data-feature]").forEach((input) => {
    input.addEventListener("change", (event) => {
      updateFeatureFromInput(event.target.dataset.feature, event.target.value);
      result = null;
      render();
    });
  });

  document.getElementById("symptom-text")?.addEventListener("input", (event) => {
    updateSymptomText(event.target.value);
    result = null;
    syncSymptomControls();
  });
  document.getElementById("ecg-finding")?.addEventListener("change", (event) => {
    ecgFinding = event.target.value;
    render();
  });
  document.getElementById("ecg-note")?.addEventListener("input", (event) => {
    ecgNote = event.target.value;
    const status = document.querySelector(".ecg-status");
    if (status) status.textContent = ecgClinicalText();
  });
  document.getElementById("baseline-sbp")?.addEventListener("input", (event) => {
    baselineSbp = event.target.value;
    result = null;
  });
  document.getElementById("baseline-dbp")?.addEventListener("input", (event) => {
    baselineDbp = event.target.value;
    result = null;
  });

  document.getElementById("clear-data-button")?.addEventListener("click", () => {
    clearPatientData();
    render();
  });
  document.getElementById("sample-select")?.addEventListener("change", (event) => {
    selectedSampleId = event.target.value;
  });
  document.getElementById("load-sample-button")?.addEventListener("click", loadSample);

  document.getElementById("predict-button")?.addEventListener("click", runPrediction);
  document.getElementById("copy-report-button")?.addEventListener("click", copyPatientReport);
  document.getElementById("lab-reference-button")?.addEventListener("click", () => {
    isLabReferenceOpen = true;
    render();
  });
  document.getElementById("model-trust-button")?.addEventListener("click", () => {
    isModelTrustOpen = true;
    render();
  });
  document.getElementById("toggle-diagnoses-button")?.addEventListener("click", () => {
    isAllDiagnosesOpen = !isAllDiagnosesOpen;
    render();
  });
  document.getElementById("close-lab-reference")?.addEventListener("click", () => {
    isLabReferenceOpen = false;
    render();
  });
  document.getElementById("close-model-trust")?.addEventListener("click", () => {
    isModelTrustOpen = false;
    render();
  });
  document.querySelectorAll(".reference-overlay").forEach((overlay) =>
    overlay.addEventListener("click", (event) => {
      if (event.target.classList.contains("reference-overlay")) {
        isLabReferenceOpen = false;
        isModelTrustOpen = false;
        render();
      }
    }),
  );
}

async function loadSample() {
  try {
    const response = await fetch(`${API_BASE}/sample-patient?sample_id=${encodeURIComponent(selectedSampleId)}`);
    if (!response.ok) throw new Error(`API-მ დააბრუნა ${response.status}`);
    sample = await response.json();
    selectedSampleId = sample.sample_id || selectedSampleId;
    symptomText = sample.symptom_text || "";
    ecgFinding = sample.ecg_finding || "not_available";
    ecgNote = sample.ecg_note || "";
    baselineSbp = sample.features?.omr_sbp_mean ? String(Math.round(Number(sample.features.omr_sbp_mean))) : "";
    baselineDbp = sample.features?.omr_dbp_mean ? String(Math.round(Number(sample.features.omr_dbp_mean))) : "";
    clearedFieldKeys = new Set();
    isAllDiagnosesOpen = false;
    features = recomputeDerivedFeatures({ ...sample.features });
    statusText = "სატესტო პაციენტი ჩაიტვირთა.";
  } catch (error) {
    statusText = `სატესტო პაციენტის ჩატვირთვა ვერ მოხერხდა: ${error.message}`;
  }
  render();
}

async function runPrediction() {
  isPredicting = true;
  statusText = "მიმდინარეობს პროგნოზირება...";
  render();

  try {
    const response = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ features, top_n: 8 }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data?.detail?.message || `API-მ დააბრუნა ${response.status}`);
    result = data;
    statusText = "პროგნოზი დასრულებულია.";
  } catch (error) {
    statusText = `პროგნოზი ვერ შესრულდა: ${error.message}`;
  } finally {
    isPredicting = false;
    render();
  }
}

async function copyPatientReport() {
  const text = patientReportText();
  try {
    await navigator.clipboard.writeText(text);
    statusText = "პაციენტის ანგარიში დაკოპირდა.";
  } catch {
    statusText = "ანგარიშის ავტომატური კოპირება ვერ მოხერხდა.";
  }
  render();
}

render();
loadSample();
