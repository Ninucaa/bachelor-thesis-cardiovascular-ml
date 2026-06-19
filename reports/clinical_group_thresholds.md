# Clinical Group Thresholds

Two threshold tiers were selected on the validation split. The supportive tier targets precision >= 0.80. The high-precision tier targets precision >= 0.72. In the frontend this tier is used as a balanced main diagnostic direction: precision remains constrained, while recall is allowed to improve. Supportive thresholds are kept as secondary signals.

| Target | Label | Tier | Threshold | Rule | Validation F1 | Validation Recall | Validation Precision | Test F1 | Test Recall | Test Precision |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| `group_ischemic_heart_disease` | იშემიური გულის დაავადებები | supportive | 0.8484 | max_f1_with_precision_at_least_0.80 | 0.3312 | 0.2088 | 0.7998 | 0.3367 | 0.214 | 0.7901 |
| `group_ischemic_heart_disease` | იშემიური გულის დაავადებები | high_precision | 0.7996 | max_f1_with_precision_at_least_0.72 | 0.4189 | 0.2954 | 0.72 | 0.4297 | 0.306 | 0.7213 |
| `group_heart_failure` | გულის უკმარისობა | supportive | 0.9066 | max_f1_with_precision_at_least_0.80 | 0.3069 | 0.1899 | 0.7999 | 0.317 | 0.1966 | 0.8191 |
| `group_heart_failure` | გულის უკმარისობა | high_precision | 0.862 | max_f1_with_precision_at_least_0.72 | 0.4172 | 0.2937 | 0.7201 | 0.4292 | 0.3017 | 0.7434 |
| `group_arrhythmia_conduction` | არითმია და გამტარობის დარღვევები | supportive | 0.8969 | max_f1_with_precision_at_least_0.80 | 0.0874 | 0.0462 | 0.8002 | 0.0903 | 0.0477 | 0.838 |
| `group_arrhythmia_conduction` | არითმია და გამტარობის დარღვევები | high_precision | 0.8538 | max_f1_with_precision_at_least_0.72 | 0.1904 | 0.1097 | 0.72 | 0.1969 | 0.1135 | 0.7426 |
| `group_hypertensive_disease` | ჰიპერტენზიული დაავადებები | supportive | 0.6096 | max_f1_with_precision_at_least_0.80 | 0.7262 | 0.6652 | 0.7995 | 0.7288 | 0.6688 | 0.8007 |
| `group_hypertensive_disease` | ჰიპერტენზიული დაავადებები | high_precision | 0.3878 | max_f1_with_precision_at_least_0.72 | 0.791 | 0.8775 | 0.7199 | 0.79 | 0.8759 | 0.7195 |
| `group_cerebrovascular_disease` | ცერებროვასკულური დაავადებები | supportive | 0.9489 | max_f1_with_precision_at_least_0.80 | 0.1623 | 0.0903 | 0.7991 | 0.1705 | 0.0955 | 0.796 |
| `group_cerebrovascular_disease` | ცერებროვასკულური დაავადებები | high_precision | 0.9277 | max_f1_with_precision_at_least_0.72 | 0.2215 | 0.1309 | 0.7202 | 0.2215 | 0.1312 | 0.7109 |
| `group_valvular_heart_disease` | ვალვულარული გულის დაავადებები | supportive | 0.9801 | fallback_max_precision_below_0.80 | 0.0006 | 0.0003 | 1.0 | 0.0 | 0.0 | 0.0 |
| `group_valvular_heart_disease` | ვალვულარული გულის დაავადებები | high_precision | 0.9502 | max_f1_with_precision_at_least_0.72 | 0.0374 | 0.0192 | 0.7191 | 0.0382 | 0.0196 | 0.7831 |
