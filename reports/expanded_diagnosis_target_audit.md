# Expanded Diagnosis Target Audit

Source: `/Users/ninucaaa/Desktop/new_project/diagnoses_icd.csv.gz`
Admissions with diagnoses: `545,497`

Recommendation rule: keep targets with at least 1,000 positive admissions for the next model iteration.

| Target | Georgian label | English label | ICD-9 prefixes | ICD-10 prefixes | Positive admissions | Positive rate | Recommended |
|---|---|---|---|---|---:|---:|---|
| `target_primary_hypertension` | პირველადი ჰიპერტენზია | Primary hypertension | `401` | `I10` | 190,069 | 34.84% | yes |
| `target_chronic_ischemic_heart_disease` | ქრონიკული იშემიური გულის დაავადება | Chronic ischemic heart disease | `412, 414` | `I25` | 102,515 | 18.79% | yes |
| `target_atrial_fibrillation_flutter` | წინაგულთა ფიბრილაცია / flutter | Atrial fibrillation / flutter | `42731, 42732` | `I48` | 80,989 | 14.85% | yes |
| `target_heart_failure` | გულის უკმარისობა | Heart failure | `428` | `I50` | 80,611 | 14.78% | yes |
| `target_hypertensive_kidney_disease` | ჰიპერტენზიული თირკმლის დაავადება | Hypertensive kidney disease | `403` | `I12` | 55,408 | 10.16% | yes |
| `target_hypertensive_heart_kidney_disease` | ჰიპერტენზიული გულის და თირკმლის დაავადება | Hypertensive heart and kidney disease | `404` | `I13` | 16,887 | 3.10% | yes |
| `target_other_arrhythmia` | სხვა გულის არითმია | Other cardiac arrhythmia | `427` | `I49` | 16,586 | 3.04% | yes |
| `target_myocardial_infarction` | მიოკარდიუმის ინფარქტი | Myocardial infarction | `410` | `I21, I22` | 16,537 | 3.03% | yes |
| `target_hypertensive_heart_disease` | ჰიპერტენზიული გულის დაავადება | Hypertensive heart disease | `402` | `I11` | 16,238 | 2.98% | yes |
| `target_av_conduction_block` | AV ბლოკადა / გამტარობის დარღვევა | AV block / conduction disorder | `426` | `I44, I45` | 16,224 | 2.97% | yes |
| `target_other_cerebrovascular_disease` | სხვა ცერებროვასკულური დაავადება | Other cerebrovascular disease | `432` | `I62, I65, I66, I67, I68, I69` | 14,746 | 2.70% | yes |
| `target_ischemic_stroke` | იშემიური ინსულტი / ცერებრული ინფარქტი | Ischemic stroke / cerebral infarction | `433, 434, 436` | `I63, I64` | 12,017 | 2.20% | yes |
| `target_paroxysmal_tachycardia` | პაროქსიზმული ტაქიკარდია | Paroxysmal tachycardia | `4270, 4271, 4272` | `I47` | 11,538 | 2.12% | yes |
| `target_acute_ischemic_heart_disease` | მწვავე იშემიური გულის დაავადება | Acute ischemic heart disease | `411` | `I24` | 5,691 | 1.04% | yes |
| `target_intracerebral_hemorrhage` | ინტრაცერებრული სისხლჩაქცევა | Intracerebral hemorrhage | `431` | `I61` | 4,320 | 0.79% | yes |
| `target_angina_pectoris` | სტენოკარდია | Angina pectoris | `413` | `I20` | 3,583 | 0.66% | yes |
| `target_cardiac_arrest` | გულის გაჩერება | Cardiac arrest | `4275` | `I46` | 2,653 | 0.49% | yes |
| `target_hypertensive_crisis` | ჰიპერტენზიული კრიზი | Hypertensive crisis | `-` | `I16` | 2,276 | 0.42% | yes |
| `target_subarachnoid_hemorrhage` | სუბარაქნოიდული სისხლჩაქცევა | Subarachnoid hemorrhage | `430` | `I60` | 1,576 | 0.29% | yes |
| `target_secondary_hypertension` | მეორადი ჰიპერტენზია | Secondary hypertension | `405` | `I15` | 318 | 0.06% | no |
