# Diagnosis Thresholds

Thresholds were selected on the validation split using a precision-oriented rule: maximize F1 among thresholds with validation precision >= 0.30. If a subtype cannot reach that precision with enough positive predictions, the fallback is maximum precision.

| Target | Label | Threshold | Rule | Validation F1 | Validation Recall | Validation Precision | Test F1 | Test Recall | Test Precision |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| `target_myocardial_infarction` | მიოკარდიუმის ინფარქტი | 0.92 | max_f1_with_precision_at_least_0.30 | 0.5967 | 0.5563 | 0.6434 | 0.5876 | 0.5487 | 0.6324 |
| `target_heart_failure` | გულის უკმარისობა | 0.655 | max_f1_with_precision_at_least_0.30 | 0.5494 | 0.6475 | 0.4771 | 0.5611 | 0.6549 | 0.4907 |
| `target_subarachnoid_hemorrhage` | სუბარაქნოიდული სისხლჩაქცევა | 0.97 | max_f1_with_precision_at_least_0.30 | 0.2091 | 0.1575 | 0.3108 | 0.1909 | 0.14 | 0.3 |
| `target_intracerebral_hemorrhage` | ინტრაცერებრული სისხლჩაქცევა | 0.935 | max_f1_with_precision_at_least_0.30 | 0.3335 | 0.356 | 0.3137 | 0.334 | 0.3725 | 0.3028 |
| `target_ischemic_stroke` | იშემიური ინსულტი / ცერებრული ინფარქტი | 0.895 | max_f1_with_precision_at_least_0.30 | 0.3604 | 0.3544 | 0.3667 | 0.3618 | 0.3555 | 0.3683 |
| `target_other_cerebrovascular_disease` | სხვა ცერებროვასკულური დაავადება | 0.85 | max_f1_with_precision_at_least_0.30 | 0.1878 | 0.1364 | 0.3012 | 0.1781 | 0.1307 | 0.2793 |
| `target_av_conduction_block` | AV ბლოკადა / გამტარობის დარღვევა | 0.875 | max_f1_with_precision_at_least_0.30 | 0.0683 | 0.0384 | 0.31 | 0.0518 | 0.0291 | 0.2338 |
| `target_cardiac_arrest` | გულის გაჩერება | 0.96 | max_f1_with_precision_at_least_0.30 | 0.2208 | 0.172 | 0.3082 | 0.3093 | 0.2425 | 0.4269 |
| `target_paroxysmal_tachycardia` | პაროქსიზმული ტაქიკარდია | 0.935 | max_f1_with_precision_at_least_0.30 | 0.027 | 0.0141 | 0.34 | 0.0279 | 0.0147 | 0.2742 |
| `target_atrial_fibrillation_flutter` | წინაგულთა ფიბრილაცია / flutter | 0.6446 | max_f1_with_precision_at_least_0.30 | 0.4847 | 0.6576 | 0.3838 | 0.4859 | 0.6543 | 0.3864 |
| `target_other_arrhythmia` | სხვა გულის არითმია | 0.87 | max_f1_with_precision_at_least_0.30 | 0.0603 | 0.0335 | 0.3003 | 0.063 | 0.0351 | 0.3069 |
| `target_primary_hypertension` | პირველადი ჰიპერტენზია | 0.4544 | max_f1_with_precision_at_least_0.30 | 0.6561 | 0.8522 | 0.5333 | 0.6525 | 0.8486 | 0.53 |
| `target_hypertensive_heart_disease` | ჰიპერტენზიული გულის დაავადება | 0.88 | max_f1_with_precision_at_least_0.30 | 0.1577 | 0.1062 | 0.3066 | 0.154 | 0.1038 | 0.2981 |
| `target_hypertensive_kidney_disease` | ჰიპერტენზიული თირკმლის დაავადება | 0.7753 | max_f1_with_precision_at_least_0.30 | 0.6011 | 0.7542 | 0.4997 | 0.6059 | 0.7703 | 0.4993 |
| `target_hypertensive_heart_kidney_disease` | ჰიპერტენზიული გულის და თირკმლის დაავადება | 0.875 | max_f1_with_precision_at_least_0.30 | 0.423 | 0.5281 | 0.3527 | 0.4158 | 0.5258 | 0.3438 |
| `target_hypertensive_crisis` | ჰიპერტენზიული კრიზი | 0.97 | max_f1_with_precision_at_least_0.30 | 0.1051 | 0.0631 | 0.3133 | 0.1342 | 0.0805 | 0.4038 |
| `target_angina_pectoris` | სტენოკარდია | 0.965 | max_f1_with_precision_at_least_0.30 | 0.0103 | 0.0052 | 0.4 | 0.0054 | 0.0027 | 0.3333 |
| `target_acute_ischemic_heart_disease` | მწვავე იშემიური გულის დაავადება | 0.965 | fallback_max_precision_below_0.30 | 0.0035 | 0.0018 | 0.25 | 0.0035 | 0.0018 | 0.2 |
| `target_chronic_ischemic_heart_disease` | ქრონიკული იშემიური გულის დაავადება | 0.6189 | max_f1_with_precision_at_least_0.30 | 0.5464 | 0.6564 | 0.468 | 0.5496 | 0.6617 | 0.47 |
