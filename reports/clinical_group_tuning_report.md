# Clinical Group Tuning Report

Model selection score = average precision + 0.30 * supportive F1 + 0.15 * high-precision F1 + 0.05 * AUC.

| Target | Selected config | Validation AUC | Validation AP | Supportive F1 | High Precision F1 | Score |
|---|---|---:|---:|---:|---:|---:|
| `group_ischemic_heart_disease` | deeper_regularized | 0.8484 | 0.6074 | 0.3312 | 0.1788 | 0.7760 |
| `group_heart_failure` | deeper_regularized | 0.8739 | 0.5815 | 0.3069 | 0.1483 | 0.7395 |
| `group_arrhythmia_conduction` | deeper_regularized | 0.8201 | 0.5224 | 0.0874 | 0.0241 | 0.5932 |
| `group_hypertensive_disease` | deeper_regularized | 0.8465 | 0.8311 | 0.7262 | 0.377 | 1.1478 |
| `group_cerebrovascular_disease` | deeper_regularized | 0.8162 | 0.3425 | 0.1623 | 0.0669 | 0.4420 |
| `group_critical_cardiac_event` | regularized_precision | 0.8955 | 0.1591 | 0.0275 | 0.008 | 0.2133 |
| `group_venous_thromboembolism` | deeper_regularized | 0.7353 | 0.0979 | 0.0005 | 0.0005 | 0.1349 |
| `group_peripheral_vascular_disease` | recall_balanced | 0.7776 | 0.1906 | 0.0125 | 0.0125 | 0.2351 |
| `group_valvular_heart_disease` | deeper_regularized | 0.8203 | 0.2794 | 0.0006 | 0.0006 | 0.3207 |
| `group_cardiomyopathy` | baseline_balanced | 0.7867 | 0.1511 | 0.0044 | 0.0025 | 0.1921 |
| `group_inflammatory_heart_disease` | deeper_regularized | 0.7848 | 0.0763 | 0.0047 | 0.0047 | 0.1177 |
