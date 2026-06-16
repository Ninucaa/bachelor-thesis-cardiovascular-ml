# Model Metrics

Best model by validation AUC-ROC: `xgboost`

| Model | Split | AUC-ROC | F1 | Recall/Sensitivity | Precision | Confusion Matrix [[TN, FP], [FN, TP]] |
|---|---:|---:|---:|---:|---:|---|
| logistic_regression | validation | 0.8918 | 0.8472 | 0.8134 | 0.8839 | `[[30713, 7575], [13231, 57669]]` |
| logistic_regression | test | 0.8885 | 0.8376 | 0.7963 | 0.8835 | `[[15843, 3719], [7213, 28192]]` |
| random_forest | validation | 0.8919 | 0.8548 | 0.8371 | 0.8733 | `[[29680, 8608], [11550, 59350]]` |
| random_forest | test | 0.8898 | 0.8489 | 0.8249 | 0.8743 | `[[15364, 4198], [6201, 29204]]` |
| xgboost | validation | 0.8966 | 0.871 | 0.8974 | 0.8461 | `[[26714, 11574], [7276, 63624]]` |
| xgboost | test | 0.8941 | 0.8647 | 0.8866 | 0.8439 | `[[13755, 5807], [4016, 31389]]` |
