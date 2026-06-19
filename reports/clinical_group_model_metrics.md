# Clinical Group Model Metrics

Training data: `/Users/ninucaaa/Desktop/new_project/data/processed/cardio_time_aware_model_ready.csv`

| Target | Label | Split | AUC-ROC | Avg Precision | F1 | Recall | Precision | Positive Rate |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `group_ischemic_heart_disease` | იშემიური გულის დაავადებები | validation | 0.8484 | 0.6074 | 0.5597 | 0.7695 | 0.4398 | 0.2027 |
| `group_ischemic_heart_disease` | იშემიური გულის დაავადებები | test | 0.8535 | 0.6141 | 0.5634 | 0.7802 | 0.4408 | 0.2008 |
| `group_heart_failure` | გულის უკმარისობა | validation | 0.8739 | 0.5815 | 0.5211 | 0.7749 | 0.3925 | 0.1444 |
| `group_heart_failure` | გულის უკმარისობა | test | 0.8813 | 0.6038 | 0.5347 | 0.7849 | 0.4055 | 0.1488 |
| `group_arrhythmia_conduction` | არითმია და გამტარობის დარღვევები | validation | 0.8201 | 0.5224 | 0.5265 | 0.7586 | 0.4031 | 0.1933 |
| `group_arrhythmia_conduction` | არითმია და გამტარობის დარღვევები | test | 0.8188 | 0.5252 | 0.5254 | 0.7562 | 0.4025 | 0.1928 |
| `group_hypertensive_disease` | ჰიპერტენზიული დაავადებები | validation | 0.8465 | 0.8311 | 0.7743 | 0.7926 | 0.7568 | 0.5097 |
| `group_hypertensive_disease` | ჰიპერტენზიული დაავადებები | test | 0.8477 | 0.8322 | 0.776 | 0.7954 | 0.7575 | 0.5086 |
| `group_cerebrovascular_disease` | ცერებროვასკულური დაავადებები | validation | 0.8162 | 0.3425 | 0.2475 | 0.6474 | 0.153 | 0.053 |
| `group_cerebrovascular_disease` | ცერებროვასკულური დაავადებები | test | 0.8193 | 0.3464 | 0.2507 | 0.6497 | 0.1553 | 0.0534 |
| `group_critical_cardiac_event` | კრიტიკული კარდიული მოვლენა | validation | 0.8955 | 0.1591 | 0.0644 | 0.716 | 0.0337 | 0.0046 |
| `group_critical_cardiac_event` | კრიტიკული კარდიული მოვლენა | test | 0.8972 | 0.2448 | 0.0777 | 0.7342 | 0.041 | 0.0055 |
| `group_venous_thromboembolism` | ვენური თრომბოემბოლია / ფილტვის ემბოლია | validation | 0.7353 | 0.0979 | 0.1339 | 0.6061 | 0.0753 | 0.0357 |
| `group_venous_thromboembolism` | ვენური თრომბოემბოლია / ფილტვის ემბოლია | test | 0.742 | 0.1014 | 0.1367 | 0.6128 | 0.0769 | 0.0356 |
| `group_peripheral_vascular_disease` | პერიფერიული სისხლძარღვოვანი დაავადება | validation | 0.7776 | 0.1906 | 0.211 | 0.8149 | 0.1212 | 0.0644 |
| `group_peripheral_vascular_disease` | პერიფერიული სისხლძარღვოვანი დაავადება | test | 0.7829 | 0.1894 | 0.2114 | 0.8298 | 0.1211 | 0.0632 |
| `group_valvular_heart_disease` | ვალვულარული გულის დაავადებები | validation | 0.8203 | 0.2794 | 0.2635 | 0.7401 | 0.1603 | 0.0617 |
| `group_valvular_heart_disease` | ვალვულარული გულის დაავადებები | test | 0.8216 | 0.2835 | 0.2576 | 0.7337 | 0.1562 | 0.0603 |
| `group_cardiomyopathy` | კარდიომიოპათია | validation | 0.7867 | 0.1511 | 0.127 | 0.684 | 0.07 | 0.0292 |
| `group_cardiomyopathy` | კარდიომიოპათია | test | 0.7878 | 0.1436 | 0.1188 | 0.688 | 0.065 | 0.0269 |
| `group_inflammatory_heart_disease` | ანთებითი გულის დაავადებები | validation | 0.7848 | 0.0763 | 0.0672 | 0.6162 | 0.0356 | 0.0118 |
| `group_inflammatory_heart_disease` | ანთებითი გულის დაავადებები | test | 0.7835 | 0.0723 | 0.066 | 0.6151 | 0.0349 | 0.0115 |
