# Time-Aware Cardio Dataset Report

Output file: `/Users/ninucaaa/Desktop/new_project/data/processed/cardio_time_aware_model_ready.csv`
Shape: 546,028 rows x 164 columns
Observation window: first 24 hours after `admittime`.

## Target Distribution
- `0`: 219,877 (40.27%)
- `1`: 326,151 (59.73%)

## Split Distribution
- `train`: 382,953 (70.13%)
- `validation`: 107,952 (19.77%)
- `test`: 55,123 (10.10%)

## Patient Split Overlap
- `train_validation_overlap`: 0
- `train_test_overlap`: 0
- `validation_test_overlap`: 0

## Missing Handling
- Added 67 missing indicators.

## Out-of-Range Values Replaced
- `ed_triage_dbp_mean`: 299
- `ed_triage_heart_rate_mean`: 17
- `ed_triage_resp_rate_mean`: 22
- `ed_triage_sbp_mean`: 104
- `ed_triage_spo2_mean`: 72
- `ed_triage_temperature_c_mean`: 299
- `icu_dbp_mean`: 72
- `icu_heart_rate_mean`: 4
- `icu_resp_rate_mean`: 12
- `icu_sbp_mean`: 16
- `icu_spo2_mean`: 37
- `icu_temperature_c_mean`: 186
- `lab_chol_ratio_mean`: 38
- `lab_chol_total_mean`: 33
- `lab_creatinine_mean`: 19
- `lab_glucose_mean`: 13
- `lab_hdl_mean`: 3
- `lab_ldl_calc_mean`: 4
- `lab_platelets_mean`: 25
- `lab_triglycerides_mean`: 78
- `omr_bmi_mean`: 525
- `omr_dbp_mean`: 162
- `omr_height_inches_mean`: 436
- `omr_sbp_mean`: 1
- `omr_weight_lbs_mean`: 282
- `triage_pain_mean`: 7,683
