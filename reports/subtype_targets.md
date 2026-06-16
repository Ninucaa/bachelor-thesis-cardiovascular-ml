# Disease-Specific Target Report

Rows: 546,028

| Target | Label | Positive rows | Positive rate |
|---|---|---:|---:|
| `target_myocardial_infarction` | Myocardial infarction | 16,537 | 3.03% |
| `target_heart_failure` | Heart failure | 80,611 | 14.76% |
| `target_stroke` | Stroke / cerebrovascular disease | 17,752 | 3.25% |
| `target_arrhythmia` | Cardiac arrhythmia | 106,818 | 19.56% |
| `target_hypertension` | Hypertensive disease | 278,087 | 50.93% |
| `target_coronary_artery_disease` | Coronary artery / ischemic heart disease | 105,089 | 19.25% |

## ICD Mapping

| Target | ICD-9 prefixes | ICD-10 prefixes |
|---|---|---|
| `target_myocardial_infarction` | `410` | `I21, I22` |
| `target_heart_failure` | `428` | `I50` |
| `target_stroke` | `430, 431, 432, 433, 434, 436` | `I60, I61, I62, I63, I64` |
| `target_arrhythmia` | `426, 427` | `I44, I45, I47, I48, I49` |
| `target_hypertension` | `401, 402, 403, 404, 405` | `I10, I11, I12, I13, I15, I16` |
| `target_coronary_artery_disease` | `411, 412, 413, 414` | `I20, I23, I24, I25` |

## Interpretation

These targets are diagnosis-code based labels. They are more specific than the original `target_cvd`, but they still represent retrospective coded hospital diagnoses, not real-time confirmed clinical diagnoses.
