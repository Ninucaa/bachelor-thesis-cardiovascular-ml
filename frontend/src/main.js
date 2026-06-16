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
  { key: "ed_triage_temperature_f_mean", label: "ტემპერატურა", min: 80, max: 110, step: 0.1, unit: "F", optional: true },
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

const editableFieldByKey = Object.fromEntries(editableFields.map((field) => [field.key, field]));

const labReferenceRanges = [
  { key: "lab_creatinine_mean", label: "კრეატინინი", low: 0.6, high: 1.3, unit: "mg/dL" },
  { key: "lab_hemoglobin_mean", label: "ჰემოგლობინი", low: 12, high: 17.5, unit: "g/dL" },
  { key: "lab_glucose_mean", label: "გლუკოზა", low: 70, high: 140, unit: "mg/dL" },
  { key: "lab_ntprobnp_mean", label: "NT-proBNP (გულის დატვირთვის მარკერი)", low: 0, high: 450, unit: "pg/mL", highLabel: "მომატებული" },
  { key: "lab_troponin_t_mean", label: "Troponin T", low: 0, high: 0.01, unit: "ng/mL", highLabel: "მომატებული" },
  { key: "lab_chol_total_mean", label: "საერთო ქოლესტერინი", low: 0, high: 200, unit: "mg/dL", highLabel: "მომატებული" },
  { key: "lab_hdl_mean", label: "HDL ქოლესტერინი", low: 40, high: 1000, unit: "mg/dL", lowLabel: "დაბალი" },
  { key: "lab_ldl_calc_mean", label: "LDL ქოლესტერინი", low: 0, high: 100, unit: "mg/dL", highLabel: "მომატებული" },
  { key: "lab_triglycerides_mean", label: "ტრიგლიცერიდები", low: 0, high: 150, unit: "mg/dL", highLabel: "მომატებული" },
  { key: "lab_platelets_mean", label: "თრომბოციტები", low: 150, high: 450, unit: "K/uL" },
];

const bmiReference = { key: "omr_bmi_mean", label: "BMI", low: 18.5, high: 24.9, unit: "kg/m2" };

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
  { label: "საერთო გულ-სისხლძარღვთა დიაგნოსტიკური სიგნალი", auc: "0.8874", recall: "0.8139", precision: "0.8515" },
  { label: "მიოკარდიუმის ინფარქტი", auc: "0.9337", recall: "0.8054", precision: "0.2072" },
  { label: "გულის უკმარისობა", auc: "0.8801", recall: "0.8087", precision: "0.3905" },
  { label: "ინსულტი / ცერებროვასკულური დაავადება", auc: "0.8182", recall: "0.7149", precision: "0.1344" },
  { label: "გულის არითმია", auc: "0.8188", recall: "0.7841", precision: "0.3921" },
  { label: "ჰიპერტენზიული დაავადება", auc: "0.8472", recall: "0.8148", precision: "0.7487" },
  { label: "კორონარული არტერიის დაავადება", auc: "0.8458", recall: "0.8082", precision: "0.4071" },
];

const metricDescriptions = [
  { key: "auc", label: "გარჩევის უნარი", technical: "AUC", note: "რამდენად კარგად არჩევს შესაბამის და არაშესაბამის შემთხვევებს" },
  { key: "recall", label: "აღმოჩენის უნარი", technical: "Recall", note: "დაავადებული შემთხვევებიდან რამდენს პოულობს" },
  { key: "precision", label: "დადებითი პასუხის სიზუსტე", technical: "Precision", note: "დადებითი პასუხებიდან რამდენია უფრო სარწმუნო" },
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
let isLabReferenceOpen = false;
let isModelTrustOpen = false;

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
  if (confidence === "borderline") return "საზღვრული სიგნალი";
  return "დაბალი მხარდაჭერა";
}

function confidenceClass(confidence) {
  if (confidence === "high") return "confidence-high";
  if (confidence === "diagnostic_signal") return "confidence-signal";
  if (confidence === "borderline") return "confidence-borderline";
  return "confidence-low";
}

function formatPercent(value) {
  return `${Math.round(value * 1000) / 10}%`;
}

function clampPercent(value) {
  return Math.max(0, Math.min(100, Math.round(value * 1000) / 10));
}

function changedFieldCount() {
  if (!sample || !features) return 0;
  return editableFields.filter((field) => {
    const missingKey = `${field.key}_missing`;
    return (
      Number(features[field.key]) !== Number(sample.features[field.key]) ||
      Number(features[missingKey] ?? 0) !== Number(sample.features[missingKey] ?? 0)
    );
  }).length;
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

function inputValue(field) {
  if (!features) return "";
  if (isOptionalMissing(field)) return "";
  let value = Number(features[field.key]);
  if (Number.isNaN(value)) return "";
  if (field.displayUnit === "kg") value /= 2.20462;
  if (field.displayUnit === "cm") value *= 2.54;
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
  if (value > reference.high) return { label: reference.highLabel || "მაღალი", className: "high" };
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

  if (field?.optional && normalizedValue === "") {
    nextFeatures[key] = optionalDefaults[key];
    syncMeasurementMetadata(nextFeatures, key, true);
  } else {
    if (normalizedValue === "") return;
    let value = Number(normalizedValue);
    if (!Number.isFinite(value)) return;
    if (field?.displayUnit === "kg") value *= 2.20462;
    if (field?.displayUnit === "cm") value /= 2.54;
    nextFeatures[key] = value;
    syncMeasurementMetadata(nextFeatures, key, false);
  }

  features = recomputeDerivedFeatures(nextFeatures);
}

function updateChangedCountDisplay() {
  const changedCount = document.getElementById("changed-count");
  if (changedCount) changedCount.textContent = `შეცვლილია ${changedFieldCount()} ველი`;
}

function fieldDisabled(field) {
  return !features;
}

function renderInputField(field) {
  return `
    <label class="field">
      <span>
        ${field.label}
        ${field.unit ? `<small>${field.unit}</small>` : ""}
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
              ${(field.options || [
                { value: 0, label: "არა" },
                { value: 1, label: "დიახ" },
              ])
                .map(
                  (option) => `
                    <option value="${option.value}" ${Number(features?.[field.key]) === option.value ? "selected" : ""}>
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
              placeholder="${field.optional ? "არასავალდებულო" : ""}"
              value="${inputValue(field)}"
              ${fieldDisabled(field) ? "disabled" : ""}
            />`
      }
    </label>
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
            <h2>ლაბორატორიული და BMI ნორმები</h2>
            <p>საორიენტაციო დიაპაზონები. ზუსტი ნორმები შეიძლება პაციენტის მდგომარეობისა და ლაბორატორიის მიხედვით განსხვავდებოდეს.</p>
          </div>
          <button class="icon-button" id="close-lab-reference" aria-label="დახურვა">×</button>
        </div>
        <div class="reference-table">
          ${[...labReferenceRanges, bmiReference]
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

function getPrimaryDiagnosticRisk() {
  if (!result?.subtype_risks?.length) return null;
  const diagnosticCandidates = result.subtype_risks.filter((risk) =>
    ["high", "diagnostic_signal"].includes(risk.diagnosis_confidence),
  );
  return diagnosticCandidates[0] || result.subtype_risks[0];
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

function renderDecisionSummary() {
  if (!result?.subtype_risks?.length) return "";
  const topRisk = getPrimaryDiagnosticRisk();
  const secondRisk = result.subtype_risks.find((risk) => risk.target_name !== topRisk.target_name);

  return `
    <div class="decision-summary">
      <div class="decision-topline">
        <span>ყველაზე ძლიერი კლინიკური სიგნალი</span>
        <em class="status-pill ${confidenceClass(topRisk.diagnosis_confidence)}">${diagnosisConfidenceLabel(topRisk.diagnosis_confidence)}</em>
      </div>
      <strong>${escapeHtml(topRisk.diagnosis_label || topRisk.display_name)}</strong>
      <div class="decision-score">
        <b>${formatPercent(topRisk.diagnosis_probability ?? topRisk.risk_probability)}</b>
        <em>დიაგნოსტიკური ზღვარი ${formatPercent(topRisk.diagnosis_threshold ?? 0.5)}</em>
      </div>
      ${renderProbabilityMeter(topRisk)}
      <div class="clinical-driver-block">
        <span>რა განსაზღვრავს ამ სიგნალს</span>
        <div class="driver-list">${renderReasonChips(topRisk)}</div>
      </div>
      <p>${escapeHtml(topRisk.diagnosis_interpretation || "სისტემა ამ პაციენტის მონაცემებში ხედავს მსგავსებას შესაბამის ICD-კოდირებულ შემთხვევებთან.")}</p>
      ${
        secondRisk
          ? `<small>შემდეგი შესადარებელი მიმართულება: ${escapeHtml(secondRisk.display_name)} (${formatPercent(secondRisk.risk_probability)}).</small>`
          : ""
      }
    </div>
  `;
}

function renderSubtypeRisks() {
  if (!result?.subtype_risks?.length) return "";
  const topRisk = getPrimaryDiagnosticRisk();
  const otherRisks = result.subtype_risks.filter((risk) => risk.target_name !== topRisk.target_name);

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
        <div class="driver-list compact">${renderReasonChips(topRisk, 3)}</div>
      </div>
      <div class="subtype-grid">
        ${otherRisks
          .map(
            (risk) => `
              <div class="subtype-card ${risk.risk_level}">
                <div class="subtype-main">
                  <strong>${escapeHtml(risk.display_name)}</strong>
                  <em>${risk.diagnosis_status || diseaseRiskLabel(risk.risk_level)}</em>
                  <span>${escapeHtml(riskReasonText(risk, 2))}</span>
                  ${renderProbabilityMeter(risk)}
                </div>
                <b class="${confidenceClass(risk.diagnosis_confidence)}">${diagnosisConfidenceLabel(risk.diagnosis_confidence)}</b>
              </div>
            `,
          )
          .join("")}
      </div>
      <p class="diagnosis-note">ეს არის ICD-კოდირებული სავარაუდო დიაგნოზის ჯგუფის პროგნოზი, არა ექიმის საბოლოო დიაგნოზის ჩანაცვლება.</p>
      ${renderClinicalChecks(topRisk)}
    </div>
  `;
}

function renderClinicalChecks(risk) {
  if (!risk?.suggested_clinical_checks?.length) return "";
  return `
    <div class="clinical-checks">
      <h4>ექიმმა დამატებით გადაამოწმოს</h4>
      <ul>
        ${risk.suggested_clinical_checks.slice(0, 4).map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
      </ul>
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
            <p>ეს ნაწილი აჩვენებს, როგორ იმუშავა მოდელმა უკვე ცნობილ სატესტო პაციენტებზე. მაღალი რიცხვი უკეთეს შედეგს ნიშნავს, მაგრამ საბოლოო დიაგნოზს ექიმი ადასტურებს.</p>
          </div>
          <button class="icon-button" id="close-model-trust" aria-label="დახურვა">×</button>
        </div>
        <div class="model-trust">
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
          <p>მაჩვენებლები დათვლილია სატესტო ნაწილზე. დიაგნოზის ჯგუფებისთვის ზღვარი შერჩეულია validation ნაწილზე, რათა დადებითი და უარყოფითი პასუხები უკეთ დაბალანსდეს.</p>
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
  ].join("\n");
}

function patientReportText() {
  if (!result?.subtype_risks?.length) return "";
  const topRisk = getPrimaryDiagnosticRisk();
  const topThree = result.subtype_risks
    .slice(0, 3)
    .map((risk, index) => `${index + 1}. ${risk.display_name}: ${formatPercent(risk.diagnosis_probability ?? risk.risk_probability)} (${risk.diagnosis_status})`)
    .join("\n");
  const reasons = clinicalReasonList(topRisk, 5).map((item) => `- ${item}`).join("\n") || "- მკვეთრი განმსაზღვრელი ფაქტორი არ გამოიკვეთა";
  const checks =
    (topRisk.suggested_clinical_checks || [])
      .slice(0, 4)
      .map((item) => `- ${item}`)
      .join("\n") || "- ექიმის კლინიკური შეფასება და საჭიროების მიხედვით დამატებითი კვლევები";

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
    "სხვა შესადარებელი მიმართულებები:",
    topThree,
    "",
    "ექიმმა დამატებით უნდა გადაამოწმოს:",
    checks,
    "",
    `საერთო გულ-სისხლძარღვთა სიგნალი: ${formatPercent(result.risk_probability)} (${riskLabel(result.risk_level)}).`,
    "შენიშვნა: ეს არის კლინიკური გადაწყვეტილების დამხმარე პროგნოზი. იგი არ ცვლის ექიმის საბოლოო დიაგნოზს და საჭიროებს პაციენტის სრულ კლინიკურ შეფასებას.",
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
        <div>
          <p class="eyebrow">კლინიკური გადაწყვეტილების დამხმარე პროტოტიპი</p>
          <h1>გულ-სისხლძარღვთა სავარაუდო დიაგნოზის პროგნოზირება</h1>
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
            <button class="secondary-button" id="reset-button" ${sample ? "" : "disabled"}>საწყისზე დაბრუნება</button>
          </div>

          ${renderFormSections()}

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
            <button class="primary-button" id="predict-button" ${!features || isPredicting ? "disabled" : ""}>
              ${isPredicting ? "მიმდინარეობს პროგნოზირება..." : "პროგნოზის გაშვება"}
            </button>
            <span id="changed-count">შეცვლილია ${changedFieldCount()} ველი</span>
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
              ? `${renderDecisionSummary()}${renderSubtypeRisks()}${renderModelTrustAction()}${renderPatientReport()}`
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
      updateChangedCountDisplay();
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

  document.getElementById("reset-button")?.addEventListener("click", () => {
    if (!sample) return;
    symptomText = "";
    features = recomputeDerivedFeatures({ ...sample.features });
    result = null;
    statusText = "სატესტო პაციენტის საწყისი მონაცემები აღდგა.";
    render();
  });

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
    const response = await fetch(`${API_BASE}/sample-patient`);
    if (!response.ok) throw new Error(`API-მ დააბრუნა ${response.status}`);
    sample = await response.json();
    symptomText = "";
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
