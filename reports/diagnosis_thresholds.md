# Diagnosis Thresholds

Thresholds were selected on the validation split by maximizing F1. Test metrics are reported using the selected validation threshold.

| Target | Label | Threshold | Validation F1 | Validation Recall | Validation Precision | Test F1 | Test Recall | Test Precision |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `target_myocardial_infarction` | მიოკარდიუმის ინფარქტი | 0.92 | 0.5945 | 0.5542 | 0.6412 | 0.5899 | 0.551 | 0.6347 |
| `target_heart_failure` | გულის უკმარისობა | 0.675 | 0.5504 | 0.626 | 0.4911 | 0.561 | 0.6315 | 0.5046 |
| `target_subarachnoid_hemorrhage` | სუბარაქნოიდული სისხლჩაქცევა | 0.945 | 0.2404 | 0.3219 | 0.1918 | 0.25 | 0.34 | 0.1977 |
| `target_intracerebral_hemorrhage` | ინტრაცერებრული სისხლჩაქცევა | 0.94 | 0.3263 | 0.3333 | 0.3196 | 0.3348 | 0.3499 | 0.3209 |
| `target_ischemic_stroke` | იშემიური ინსულტი / ცერებრული ინფარქტი | 0.89 | 0.362 | 0.3619 | 0.3622 | 0.3631 | 0.3646 | 0.3616 |
| `target_other_cerebrovascular_disease` | სხვა ცერებროვასკულური დაავადება | 0.785 | 0.2118 | 0.2085 | 0.2151 | 0.2091 | 0.206 | 0.2124 |
| `target_av_conduction_block` | AV ბლოკადა / გამტარობის დარღვევა | 0.7473 | 0.1752 | 0.2487 | 0.1352 | 0.1648 | 0.2354 | 0.1268 |
| `target_cardiac_arrest` | გულის გაჩერება | 0.945 | 0.2563 | 0.244 | 0.2699 | 0.3321 | 0.3056 | 0.3636 |
| `target_paroxysmal_tachycardia` | პაროქსიზმული ტაქიკარდია | 0.78 | 0.156 | 0.2008 | 0.1276 | 0.1553 | 0.2085 | 0.1237 |
| `target_atrial_fibrillation_flutter` | წინაგულთა ფიბრილაცია / flutter | 0.635 | 0.4849 | 0.6741 | 0.3786 | 0.4839 | 0.6677 | 0.3795 |
| `target_other_arrhythmia` | სხვა გულის არითმია | 0.675 | 0.1434 | 0.2831 | 0.0961 | 0.1509 | 0.2856 | 0.1025 |
| `target_primary_hypertension` | პირველადი ჰიპერტენზია | 0.45 | 0.6563 | 0.857 | 0.5318 | 0.6525 | 0.8524 | 0.5285 |
| `target_hypertensive_heart_disease` | ჰიპერტენზიული გულის დაავადება | 0.8 | 0.2437 | 0.2953 | 0.2074 | 0.2412 | 0.2912 | 0.2058 |
| `target_hypertensive_kidney_disease` | ჰიპერტენზიული თირკმლის დაავადება | 0.775 | 0.6004 | 0.7525 | 0.4994 | 0.6053 | 0.769 | 0.4991 |
| `target_hypertensive_heart_kidney_disease` | ჰიპერტენზიული გულის და თირკმლის დაავადება | 0.8832 | 0.4221 | 0.4987 | 0.3658 | 0.4243 | 0.5123 | 0.3621 |
| `target_hypertensive_crisis` | ჰიპერტენზიული კრიზი | 0.92 | 0.155 | 0.1772 | 0.1377 | 0.1877 | 0.2107 | 0.1692 |
| `target_angina_pectoris` | სტენოკარდია | 0.865 | 0.1227 | 0.1201 | 0.1253 | 0.1085 | 0.1071 | 0.1099 |
| `target_acute_ischemic_heart_disease` | მწვავე იშემიური გულის დაავადება | 0.87 | 0.156 | 0.2306 | 0.1179 | 0.1447 | 0.2218 | 0.1074 |
| `target_chronic_ischemic_heart_disease` | ქრონიკული იშემიური გულის დაავადება | 0.64 | 0.5466 | 0.6251 | 0.4856 | 0.5447 | 0.626 | 0.482 |
