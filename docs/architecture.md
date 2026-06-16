# სისტემის არქიტექტურა

## პროექტის მიზანი

პროექტის მიზანია გულ-სისხლძარღვთა დაავადების რისკის პროგნოზირების დამხმარე სისტემის შექმნა. სისტემა იღებს პაციენტის კლინიკურ მახასიათებლებს, იყენებს გაწვრთნილ მანქანური სწავლების მოდელს და აბრუნებს რისკის ალბათობას SHAP ახსნადობით.

სისტემა არ სვამს საბოლოო კლინიკურ დიაგნოზს. იგი წარმოადგენს decision-support პროტოტიპს, რომელიც შეიძლება გამოყენებულ იქნას როგორც დამატებითი ანალიტიკური ინსტრუმენტი.

## მაღალი დონის არქიტექტურა

```text
CSV Dataset
    |
    v
Preprocessing Script
    |
    v
Model-ready Dataset
    |
    v
Training Script
    |
    v
Saved ML Models + Feature List
    |
    v
FastAPI Backend
    |
    v
React Frontend
```

## ძირითადი კომპონენტები

### 1. მონაცემთა წყარო

საწყისი მონაცემი არის `cardio_training_features.csv`.

მონაცემი შეიცავს:

- დემოგრაფიულ მახასიათებლებს
- ლაბორატორიულ მაჩვენებლებს
- ED vital signs
- ICU vital signs
- ECG მახასიათებლებს
- სამიზნე ცვლადს `target_cvd`
- train/validation/test დაყოფას `split_hint`

სამიზნე ცვლადის განმარტება:

- `target_cvd = 1` ნიშნავს CVD-positive class-ს ამ dataset-ის განსაზღვრებით.
- `target_cvd = 0` ნიშნავს non-CVD class-ს ამ dataset-ის განსაზღვრებით.
- მოდელი არ პროგნოზირებს კონკრეტულ ერთ დიაგნოზს, მაგალითად heart attack-ს ან stroke-ს.

მნიშვნელოვანი თვისება:

- train, validation და test ნაწილებს შორის პაციენტის გადაკვეთა არ დაფიქსირდა, რაც ამცირებს data leakage-ის რისკს.

### 2. მონაცემთა წინასწარი დამუშავება

Preprocessing ეტაპზე შესრულდა:

- იდენტიფიკატორების ამოღება:
  - `subject_id`
  - `hadm_id`
- უსარგებლო/ცარიელი სვეტების ამოღება:
  - `lab_troponin_i_mean`
  - `lab_troponin_i_count`
- არარეალისტური კლინიკური outlier-ების დამუშავება
- ECG sentinel/artifact მნიშვნელობების დამუშავება
- missing indicator სვეტების დამატება
- გამოტოვებული მნიშვნელობების შევსება train split-ის მედიანებით

შედეგი:

- `data/processed/cardio_model_ready.csv`
- `546,028` ჩანაწერი
- `137` model feature
- `0` გამოტოვებული მნიშვნელობა საბოლოო model-ready ფაილში

### 3. მოდელის გაწვრთნა

გაწვრთნილი მოდელები:

- Logistic Regression
- Random Forest
- XGBoost

გამოყენებული შეფასების მეტრიკები:

- AUC-ROC
- F1-score
- Recall/Sensitivity
- Precision
- Confusion Matrix

საუკეთესო მოდელი:

- XGBoost

ტესტური შედეგები:

```text
AUC-ROC: 0.8754
F1-score: 0.8536
Recall/Sensitivity: 0.8818
Precision: 0.8271
```

მოდელის ფაილები:

```text
models/xgboost.pkl
models/random_forest.pkl
models/logistic_regression.pkl
models/feature_columns.json
```

### 4. SHAP ახსნადობა

სამედიცინო სისტემაში მხოლოდ პროგნოზის დაბრუნება საკმარისი არ არის. ამიტომ პროექტში დამატებულია SHAP ახსნადობა.

SHAP აბრუნებს:

- რომელი feature იყო ყველაზე მნიშვნელოვანი კონკრეტული პაციენტის პროგნოზისთვის
- feature ზრდიდა თუ ამცირებდა რისკს
- feature-ის მნიშვნელობას
- SHAP contribution-ს

ეს კომპონენტი ზრდის სისტემის გამჭვირვალობას და ეხმარება მომხმარებელს უკეთ გაიგოს მოდელის გადაწყვეტილება.

### 5. FastAPI Backend

Backend მდებარეობს:

```text
src/api/
├── app.py
├── model_service.py
└── schemas.py
```

როლები:

- `app.py` - API endpoint-ები და FastAPI აპლიკაცია
- `model_service.py` - მოდელის ჩატვირთვა, feature validation, prediction, SHAP explanation
- `schemas.py` - request/response schema-ები

Endpoint-ები:

```text
GET  /health
GET  /features
GET  /sample-patient
POST /predict
```

`/health`

- ამოწმებს API-ის სტატუსს
- აბრუნებს ჩატვირთულია თუ არა მოდელი
- აბრუნებს feature-ების რაოდენობას

`/features`

- აბრუნებს ყველა feature-ს, რომელსაც მოდელი ელოდება

`/sample-patient`

- აბრუნებს ერთ რეალურ test split პაციენტს
- frontend იყენებს მას demo-სთვის

`/predict`

- იღებს სრულ feature payload-ს
- აბრუნებს:
  - risk probability
  - predicted class
  - risk level
  - SHAP top factors

### 6. React Frontend

Frontend მდებარეობს:

```text
frontend/
├── package.json
├── index.html
└── src/
    ├── main.js
    └── styles.css
```

Frontend-ის ლოგიკა:

1. იტვირთება sample patient backend-იდან.
2. მომხმარებელი ცვლის რამდენიმე გასაგებ clinical field-ს.
3. დანარჩენი 137 feature რჩება sample patient-ის მნიშვნელობებით.
4. frontend აგზავნის სრულ payload-ს `/predict` endpoint-ზე.
5. ეკრანზე ჩანს პროგნოზი და SHAP ფაქტორები.

რატომ sample patient approach?

მოდელი ელოდება `137` feature-ს. ყველა feature-ის ხელით შეყვანა demo-სთვის არაპრაქტიკულია. ამიტომ UI მომხმარებელს აძლევს მხოლოდ რამდენიმე მნიშვნელოვან ველს, ხოლო სრული payload ინარჩუნებს ტექნიკურ სისწორეს.

## Prediction Flow

```text
User opens frontend
    |
    v
Frontend calls GET /sample-patient
    |
    v
User edits key fields
    |
    v
Frontend sends POST /predict
    |
    v
Backend validates all 137 features
    |
    v
XGBoost model predicts probability
    |
    v
SHAP calculates top factors
    |
    v
Frontend displays risk and explanation
```

## Error Handling

თუ `/predict` endpoint-ზე გაგზავნილი payload არ შეიცავს ყველა საჭირო feature-ს, backend აბრუნებს:

```text
HTTP 422
```

პასუხში ჩანს:

- რამდენი feature აკლია
- არის თუ არა ზედმეტი feature
- missing feature-ების პირველი ნაწილი

ეს ამარტივებს debugging-ს და იცავს backend-ს არასწორი input-ისგან.

## ტექნოლოგიური Stack

Backend:

- Python
- FastAPI
- Pydantic
- Pandas
- Joblib

Machine Learning:

- scikit-learn
- XGBoost
- SHAP

Frontend:

- React
- Vite
- CSS

Development:

- `.venv`
- npm
- Git/GitHub-ისთვის მზად სტრუქტურა

## შეზღუდვები

- მონაცემები არის რეტროსპექტული ჰოსპიტალური მონაცემები.
- სისტემა არ არის კლინიკურად ვალიდირებული რეალურ სამედიცინო გარემოში.
- ბევრი feature თავდაპირველად იყო missing, ამიტომ გამოყენებულია missing indicator-ები და median imputation.
- ICU მონაცემები შეიძლება ასახავდეს უკვე განვითარებულ მძიმე მდგომარეობას და არა მხოლოდ ადრეულ რისკს.
- frontend demo იყენებს sample patient-ს, რადგან სრული 137 feature-ის ხელით შეყვანა პრაქტიკული არ არის.

## მომავალი გაუმჯობესება

- Early-screening model-ის დამატება მხოლოდ ადრეულად ხელმისაწვდომი feature-ებით.
- Docker კონტეინერიზაცია.
- უფრო სრული frontend ფორმა კლინიკური ველების ჯგუფებით.
- მოდელის calibration-ის შემოწმება.
- დამატებითი external validation დამოუკიდებელ dataset-ზე.
- user authentication და პაციენტის ისტორიის შენახვა.
