# Time-Aware Model Metrics

Training data: `/Users/ninucaaa/Desktop/new_project/data/processed/cardio_time_aware_model_ready.csv`

| Target | Label | Split | AUC-ROC | Avg Precision | F1 | Recall | Precision | Positive Rate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `target_cvd` | Any cardiovascular diagnosis | validation | 0.8865 | 0.9162 | 0.8323 | 0.8135 | 0.852 | 0.6 |
| `target_cvd` | Any cardiovascular diagnosis | test | 0.8874 | 0.9168 | 0.8323 | 0.8139 | 0.8515 | 0.598 |
| `target_myocardial_infarction` | Myocardial infarction | validation | 0.9333 | 0.597 | 0.3315 | 0.8054 | 0.2087 | 0.031 |
| `target_myocardial_infarction` | Myocardial infarction | test | 0.9337 | 0.6079 | 0.3296 | 0.8054 | 0.2072 | 0.0309 |
| `target_heart_failure` | Heart failure | validation | 0.8729 | 0.5756 | 0.5099 | 0.795 | 0.3753 | 0.1444 |
| `target_heart_failure` | Heart failure | test | 0.8801 | 0.5971 | 0.5266 | 0.8087 | 0.3905 | 0.1488 |
| `target_stroke` | Stroke / cerebrovascular disease | validation | 0.8146 | 0.3362 | 0.2247 | 0.7141 | 0.1333 | 0.053 |
| `target_stroke` | Stroke / cerebrovascular disease | test | 0.8182 | 0.3415 | 0.2263 | 0.7149 | 0.1344 | 0.0534 |
| `target_arrhythmia` | Cardiac arrhythmia | validation | 0.8197 | 0.5234 | 0.5225 | 0.7842 | 0.3918 | 0.1951 |
| `target_arrhythmia` | Cardiac arrhythmia | test | 0.8188 | 0.5266 | 0.5228 | 0.7841 | 0.3921 | 0.1947 |
| `target_hypertension` | Hypertensive disease | validation | 0.846 | 0.8307 | 0.78 | 0.8132 | 0.7494 | 0.5101 |
| `target_hypertension` | Hypertensive disease | test | 0.8472 | 0.8319 | 0.7804 | 0.8148 | 0.7487 | 0.509 |
| `target_coronary_artery_disease` | Coronary artery / ischemic heart disease | validation | 0.8413 | 0.5667 | 0.5383 | 0.7983 | 0.4061 | 0.1957 |
| `target_coronary_artery_disease` | Coronary artery / ischemic heart disease | test | 0.8458 | 0.5714 | 0.5415 | 0.8082 | 0.4071 | 0.1937 |
