# Time-Aware Model Metrics

Training data: `/Users/ninucaaa/Desktop/new_project/data/processed/cardio_time_aware_model_ready.csv`

| Target | Label | Split | AUC-ROC | Avg Precision | F1 | Recall | Precision | Positive Rate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `target_cvd` | Any cardiovascular diagnosis | validation | 0.8865 | 0.9245 | 0.8362 | 0.8081 | 0.8664 | 0.624 |
| `target_cvd` | Any cardiovascular diagnosis | test | 0.8863 | 0.9234 | 0.8357 | 0.8085 | 0.8648 | 0.6211 |
| `target_myocardial_infarction` | Myocardial infarction | validation | 0.9338 | 0.5997 | 0.333 | 0.8039 | 0.21 | 0.031 |
| `target_myocardial_infarction` | Myocardial infarction | test | 0.9338 | 0.6059 | 0.3325 | 0.8019 | 0.2098 | 0.0309 |
| `target_heart_failure` | Heart failure | validation | 0.8733 | 0.5788 | 0.5123 | 0.7963 | 0.3776 | 0.1444 |
| `target_heart_failure` | Heart failure | test | 0.8809 | 0.6007 | 0.5278 | 0.8089 | 0.3917 | 0.1488 |
| `target_subarachnoid_hemorrhage` | Subarachnoid hemorrhage | validation | 0.8999 | 0.1469 | 0.0451 | 0.6952 | 0.0233 | 0.0027 |
| `target_subarachnoid_hemorrhage` | Subarachnoid hemorrhage | test | 0.9244 | 0.1473 | 0.0499 | 0.7733 | 0.0258 | 0.0027 |
| `target_intracerebral_hemorrhage` | Intracerebral hemorrhage | validation | 0.9092 | 0.2288 | 0.1037 | 0.769 | 0.0556 | 0.0078 |
| `target_intracerebral_hemorrhage` | Intracerebral hemorrhage | test | 0.9123 | 0.2348 | 0.1077 | 0.763 | 0.0579 | 0.008 |
| `target_ischemic_stroke` | Ischemic stroke / cerebral infarction | validation | 0.8641 | 0.2716 | 0.146 | 0.7391 | 0.081 | 0.0223 |
| `target_ischemic_stroke` | Ischemic stroke / cerebral infarction | test | 0.8603 | 0.2696 | 0.1408 | 0.7159 | 0.0781 | 0.0218 |
| `target_other_cerebrovascular_disease` | Other cerebrovascular disease | validation | 0.7833 | 0.1482 | 0.1149 | 0.7007 | 0.0626 | 0.0274 |
| `target_other_cerebrovascular_disease` | Other cerebrovascular disease | test | 0.7975 | 0.1421 | 0.1231 | 0.7232 | 0.0673 | 0.0284 |
| `target_av_conduction_block` | AV block / conduction disorder | validation | 0.7788 | 0.1144 | 0.1215 | 0.7346 | 0.0662 | 0.0299 |
| `target_av_conduction_block` | AV block / conduction disorder | test | 0.7697 | 0.1071 | 0.1167 | 0.7125 | 0.0635 | 0.0293 |
| `target_cardiac_arrest` | Cardiac arrest | validation | 0.8919 | 0.1531 | 0.0565 | 0.726 | 0.0294 | 0.0046 |
| `target_cardiac_arrest` | Cardiac arrest | test | 0.8911 | 0.2314 | 0.0682 | 0.7442 | 0.0357 | 0.0055 |
| `target_paroxysmal_tachycardia` | Paroxysmal tachycardia | validation | 0.7705 | 0.0902 | 0.0963 | 0.6737 | 0.0519 | 0.0224 |
| `target_paroxysmal_tachycardia` | Paroxysmal tachycardia | test | 0.7867 | 0.0927 | 0.0953 | 0.7102 | 0.0511 | 0.021 |
| `target_atrial_fibrillation_flutter` | Atrial fibrillation / flutter | validation | 0.8382 | 0.4543 | 0.4591 | 0.8309 | 0.3172 | 0.1458 |
| `target_atrial_fibrillation_flutter` | Atrial fibrillation / flutter | test | 0.8414 | 0.4655 | 0.461 | 0.8327 | 0.3187 | 0.1452 |
| `target_other_arrhythmia` | Other cardiac arrhythmia | validation | 0.7347 | 0.0933 | 0.1147 | 0.661 | 0.0628 | 0.031 |
| `target_other_arrhythmia` | Other cardiac arrhythmia | test | 0.7238 | 0.0987 | 0.1146 | 0.6402 | 0.0629 | 0.032 |
| `target_primary_hypertension` | Primary hypertension | validation | 0.7944 | 0.6336 | 0.6554 | 0.8062 | 0.5521 | 0.3542 |
| `target_primary_hypertension` | Primary hypertension | test | 0.7933 | 0.6271 | 0.6521 | 0.8024 | 0.5491 | 0.35 |
| `target_hypertensive_heart_disease` | Hypertensive heart disease | validation | 0.845 | 0.1664 | 0.1475 | 0.7943 | 0.0813 | 0.0297 |
| `target_hypertensive_heart_disease` | Hypertensive heart disease | test | 0.8516 | 0.1639 | 0.1526 | 0.8096 | 0.0843 | 0.0295 |
| `target_hypertensive_kidney_disease` | Hypertensive kidney disease | validation | 0.9342 | 0.6064 | 0.5524 | 0.8906 | 0.4004 | 0.0977 |
| `target_hypertensive_kidney_disease` | Hypertensive kidney disease | test | 0.9365 | 0.6176 | 0.5589 | 0.8986 | 0.4055 | 0.0997 |
| `target_hypertensive_heart_kidney_disease` | Hypertensive heart and kidney disease | validation | 0.9432 | 0.3701 | 0.2671 | 0.8987 | 0.1569 | 0.0293 |
| `target_hypertensive_heart_kidney_disease` | Hypertensive heart and kidney disease | test | 0.943 | 0.3894 | 0.2788 | 0.9045 | 0.1648 | 0.0309 |
| `target_hypertensive_crisis` | Hypertensive crisis | validation | 0.8735 | 0.0742 | 0.0392 | 0.7063 | 0.0202 | 0.0038 |
| `target_hypertensive_crisis` | Hypertensive crisis | test | 0.8966 | 0.1095 | 0.0515 | 0.7778 | 0.0266 | 0.0047 |
| `target_angina_pectoris` | Angina pectoris | validation | 0.8095 | 0.0552 | 0.0374 | 0.7089 | 0.0192 | 0.0071 |
| `target_angina_pectoris` | Angina pectoris | test | 0.8023 | 0.0541 | 0.0347 | 0.6896 | 0.0178 | 0.0066 |
| `target_acute_ischemic_heart_disease` | Acute ischemic heart disease | validation | 0.8609 | 0.0785 | 0.0793 | 0.7306 | 0.0419 | 0.0105 |
| `target_acute_ischemic_heart_disease` | Acute ischemic heart disease | test | 0.8752 | 0.0797 | 0.0811 | 0.7641 | 0.0428 | 0.0103 |
| `target_chronic_ischemic_heart_disease` | Chronic ischemic heart disease | validation | 0.8409 | 0.5578 | 0.5311 | 0.7996 | 0.3976 | 0.1908 |
| `target_chronic_ischemic_heart_disease` | Chronic ischemic heart disease | test | 0.8454 | 0.5623 | 0.5351 | 0.8108 | 0.3993 | 0.1889 |
| `target_venous_thromboembolism` | Venous thromboembolism / pulmonary embolism | validation | 0.7341 | 0.0967 | 0.1253 | 0.6701 | 0.0691 | 0.0357 |
| `target_venous_thromboembolism` | Venous thromboembolism / pulmonary embolism | test | 0.7421 | 0.1009 | 0.1276 | 0.6816 | 0.0704 | 0.0356 |
| `target_peripheral_vascular_disease` | Peripheral vascular disease | validation | 0.7775 | 0.1921 | 0.2223 | 0.7615 | 0.1302 | 0.0644 |
| `target_peripheral_vascular_disease` | Peripheral vascular disease | test | 0.7828 | 0.1912 | 0.2223 | 0.7759 | 0.1297 | 0.0632 |
| `target_valvular_heart_disease` | Valvular heart disease | validation | 0.8193 | 0.2747 | 0.2532 | 0.7679 | 0.1516 | 0.0617 |
| `target_valvular_heart_disease` | Valvular heart disease | test | 0.821 | 0.2802 | 0.2467 | 0.7635 | 0.1471 | 0.0603 |
| `target_cardiomyopathy` | Cardiomyopathy | validation | 0.7867 | 0.1511 | 0.127 | 0.684 | 0.07 | 0.0292 |
| `target_cardiomyopathy` | Cardiomyopathy | test | 0.7878 | 0.1436 | 0.1188 | 0.688 | 0.065 | 0.0269 |
| `target_inflammatory_heart_disease` | Inflammatory heart disease | validation | 0.7845 | 0.0707 | 0.0593 | 0.6805 | 0.031 | 0.0118 |
| `target_inflammatory_heart_disease` | Inflammatory heart disease | test | 0.7844 | 0.0687 | 0.0579 | 0.6845 | 0.0302 | 0.0115 |
