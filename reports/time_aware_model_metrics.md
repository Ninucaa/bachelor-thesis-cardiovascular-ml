# Time-Aware Model Metrics

Training data: `/Users/ninucaaa/Desktop/new_project/data/processed/cardio_time_aware_model_ready.csv`

| Target | Label | Split | AUC-ROC | Avg Precision | F1 | Recall | Precision | Positive Rate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `target_cvd` | Any cardiovascular diagnosis | validation | 0.8863 | 0.916 | 0.8321 | 0.8134 | 0.8518 | 0.5998 |
| `target_cvd` | Any cardiovascular diagnosis | test | 0.8871 | 0.9165 | 0.8318 | 0.8134 | 0.8511 | 0.5977 |
| `target_myocardial_infarction` | Myocardial infarction | validation | 0.9333 | 0.597 | 0.3315 | 0.8054 | 0.2087 | 0.031 |
| `target_myocardial_infarction` | Myocardial infarction | test | 0.9337 | 0.6079 | 0.3296 | 0.8054 | 0.2072 | 0.0309 |
| `target_heart_failure` | Heart failure | validation | 0.8729 | 0.5756 | 0.5099 | 0.795 | 0.3753 | 0.1444 |
| `target_heart_failure` | Heart failure | test | 0.8801 | 0.5971 | 0.5266 | 0.8087 | 0.3905 | 0.1488 |
| `target_subarachnoid_hemorrhage` | Subarachnoid hemorrhage | validation | 0.9014 | 0.1467 | 0.0441 | 0.7089 | 0.0227 | 0.0027 |
| `target_subarachnoid_hemorrhage` | Subarachnoid hemorrhage | test | 0.9275 | 0.1406 | 0.0495 | 0.7867 | 0.0256 | 0.0027 |
| `target_intracerebral_hemorrhage` | Intracerebral hemorrhage | validation | 0.9098 | 0.2258 | 0.1049 | 0.7798 | 0.0563 | 0.0078 |
| `target_intracerebral_hemorrhage` | Intracerebral hemorrhage | test | 0.9107 | 0.2349 | 0.1069 | 0.7675 | 0.0574 | 0.008 |
| `target_ischemic_stroke` | Ischemic stroke / cerebral infarction | validation | 0.864 | 0.2717 | 0.1469 | 0.7466 | 0.0815 | 0.0223 |
| `target_ischemic_stroke` | Ischemic stroke / cerebral infarction | test | 0.86 | 0.2682 | 0.1407 | 0.7159 | 0.078 | 0.0218 |
| `target_other_cerebrovascular_disease` | Other cerebrovascular disease | validation | 0.7832 | 0.1476 | 0.114 | 0.6984 | 0.0621 | 0.0274 |
| `target_other_cerebrovascular_disease` | Other cerebrovascular disease | test | 0.7988 | 0.1439 | 0.1234 | 0.729 | 0.0674 | 0.0284 |
| `target_av_conduction_block` | AV block / conduction disorder | validation | 0.7789 | 0.1148 | 0.1219 | 0.734 | 0.0665 | 0.0299 |
| `target_av_conduction_block` | AV block / conduction disorder | test | 0.7709 | 0.1057 | 0.1173 | 0.7162 | 0.0639 | 0.0293 |
| `target_cardiac_arrest` | Cardiac arrest | validation | 0.8931 | 0.1601 | 0.0562 | 0.742 | 0.0292 | 0.0046 |
| `target_cardiac_arrest` | Cardiac arrest | test | 0.895 | 0.2452 | 0.0667 | 0.7508 | 0.0349 | 0.0055 |
| `target_paroxysmal_tachycardia` | Paroxysmal tachycardia | validation | 0.7712 | 0.0891 | 0.0971 | 0.6816 | 0.0523 | 0.0224 |
| `target_paroxysmal_tachycardia` | Paroxysmal tachycardia | test | 0.7866 | 0.0914 | 0.0966 | 0.7232 | 0.0518 | 0.021 |
| `target_atrial_fibrillation_flutter` | Atrial fibrillation / flutter | validation | 0.8382 | 0.4536 | 0.4582 | 0.8315 | 0.3162 | 0.1458 |
| `target_atrial_fibrillation_flutter` | Atrial fibrillation / flutter | test | 0.841 | 0.4654 | 0.4597 | 0.8334 | 0.3173 | 0.1452 |
| `target_other_arrhythmia` | Other cardiac arrhythmia | validation | 0.7355 | 0.093 | 0.1144 | 0.6634 | 0.0626 | 0.031 |
| `target_other_arrhythmia` | Other cardiac arrhythmia | test | 0.7247 | 0.1012 | 0.1143 | 0.6436 | 0.0627 | 0.032 |
| `target_primary_hypertension` | Primary hypertension | validation | 0.7939 | 0.6325 | 0.6552 | 0.8054 | 0.5523 | 0.3542 |
| `target_primary_hypertension` | Primary hypertension | test | 0.7929 | 0.6259 | 0.6522 | 0.802 | 0.5496 | 0.35 |
| `target_hypertensive_heart_disease` | Hypertensive heart disease | validation | 0.8448 | 0.1644 | 0.1473 | 0.7952 | 0.0812 | 0.0297 |
| `target_hypertensive_heart_disease` | Hypertensive heart disease | test | 0.8507 | 0.1631 | 0.1526 | 0.8127 | 0.0842 | 0.0295 |
| `target_hypertensive_kidney_disease` | Hypertensive kidney disease | validation | 0.9341 | 0.6062 | 0.5511 | 0.8928 | 0.3986 | 0.0977 |
| `target_hypertensive_kidney_disease` | Hypertensive kidney disease | test | 0.9363 | 0.6151 | 0.5577 | 0.9001 | 0.4041 | 0.0997 |
| `target_hypertensive_heart_kidney_disease` | Hypertensive heart and kidney disease | validation | 0.9429 | 0.3672 | 0.2646 | 0.8974 | 0.1552 | 0.0293 |
| `target_hypertensive_heart_kidney_disease` | Hypertensive heart and kidney disease | test | 0.943 | 0.3895 | 0.278 | 0.9062 | 0.1642 | 0.0309 |
| `target_hypertensive_crisis` | Hypertensive crisis | validation | 0.8734 | 0.0778 | 0.0383 | 0.7015 | 0.0197 | 0.0038 |
| `target_hypertensive_crisis` | Hypertensive crisis | test | 0.8946 | 0.1244 | 0.0497 | 0.7663 | 0.0257 | 0.0047 |
| `target_angina_pectoris` | Angina pectoris | validation | 0.8075 | 0.0541 | 0.0372 | 0.7206 | 0.0191 | 0.0071 |
| `target_angina_pectoris` | Angina pectoris | test | 0.8042 | 0.0582 | 0.0339 | 0.6868 | 0.0174 | 0.0066 |
| `target_acute_ischemic_heart_disease` | Acute ischemic heart disease | validation | 0.8613 | 0.0791 | 0.0791 | 0.7386 | 0.0418 | 0.0105 |
| `target_acute_ischemic_heart_disease` | Acute ischemic heart disease | test | 0.8769 | 0.0801 | 0.0813 | 0.7764 | 0.0429 | 0.0103 |
| `target_chronic_ischemic_heart_disease` | Chronic ischemic heart disease | validation | 0.8411 | 0.558 | 0.5307 | 0.8013 | 0.3968 | 0.1908 |
| `target_chronic_ischemic_heart_disease` | Chronic ischemic heart disease | test | 0.8457 | 0.5629 | 0.5333 | 0.8092 | 0.3977 | 0.1889 |
