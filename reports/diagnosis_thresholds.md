# Diagnosis Thresholds

Thresholds were selected on the validation split by maximizing F1. Test metrics are reported using the selected validation threshold.

| Target | Label | Threshold | Validation F1 | Validation Recall | Validation Precision | Test F1 | Test Recall | Test Precision |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `target_myocardial_infarction` | მიოკარდიუმის ინფარქტი | 0.92 | 0.5945 | 0.5542 | 0.6412 | 0.5899 | 0.551 | 0.6347 |
| `target_heart_failure` | გულის უკმარისობა | 0.675 | 0.5504 | 0.626 | 0.4911 | 0.561 | 0.6315 | 0.5046 |
| `target_stroke` | ინსულტი / ცერებროვასკულური დაავადება | 0.7892 | 0.3699 | 0.342 | 0.4028 | 0.3683 | 0.3381 | 0.4045 |
| `target_arrhythmia` | გულის არითმია | 0.58 | 0.5341 | 0.6975 | 0.4328 | 0.5342 | 0.6959 | 0.4335 |
| `target_hypertension` | ჰიპერტენზიული დაავადება | 0.385 | 0.7914 | 0.8927 | 0.7108 | 0.7909 | 0.8914 | 0.7108 |
| `target_coronary_artery_disease` | კორონარული არტერიის დაავადება | 0.6249 | 0.5525 | 0.6433 | 0.4841 | 0.5535 | 0.6474 | 0.4834 |
