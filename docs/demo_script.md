# დემოს სცენარი

ეს დოკუმენტი აღწერს, რა უნდა აჩვენო დაცვის დროს და რა უნდა თქვა თითოეულ ეტაპზე. მიზანია demo იყოს მოკლე, გასაგები და სტაბილური.

## მომზადება დემომდე

გახსენით ორი terminal ფანჯარა.

### 1. Backend

```bash
cd /Users/ninucaaa/Desktop/new_project/PythonProject
.venv/bin/uvicorn src.api.app:app --host 127.0.0.1 --port 8765
```

შესამოწმებელი მისამართი:

```text
http://127.0.0.1:8765/docs
```

### 2. Frontend

```bash
cd /Users/ninucaaa/Desktop/new_project/PythonProject/frontend
npm run dev
```

გასახსნელი მისამართი:

```text
http://127.0.0.1:5173/
```

## დემოს ძირითადი სცენარი

### ნაბიჯი 1 - პროექტის მოკლე ახსნა

სათქმელი:

> პროექტი არის გულ-სისხლძარღვთა დაავადების რისკის პროგნოზირების decision-support პროტოტიპი. ის იყენებს კლინიკურ მონაცემებს, XGBoost მოდელს და SHAP ახსნადობას, რათა პროგნოზთან ერთად აჩვენოს რომელი ფაქტორები მოქმედებს შედეგზე.

ხაზგასასმელი:

- სისტემა არ სვამს დამოუკიდებელ დიაგნოზს.
- სისტემა არის დამხმარე ანალიტიკური ინსტრუმენტი.
- მომხმარებლისთვის შედეგი ნაჩვენებია როგორც გულ-სისხლძარღვთა დაავადების დაბალი, საშუალო ან მაღალი რისკი.
- ტექნიკურად მოდელის სამიზნეა `target_cvd = 1`, ანუ CVD-positive class ამ dataset-ის მიხედვით.
- მთავარი აქცენტია prediction + explainability.

### ნაბიჯი 2 - Swagger API-ის ჩვენება

გახსენით:

```text
http://127.0.0.1:8765/docs
```

აჩვენეთ endpoint-ები:

- `GET /health`
- `GET /features`
- `GET /sample-patient`
- `POST /predict`

სათქმელი:

> Backend აწყობილია FastAPI-ზე. Swagger დოკუმენტაცია ავტომატურად გენერირდება და აჩვენებს ყველა endpoint-ს, request/response schema-ებს და შესაძლებელს ხდის API-ის ხელით შემოწმებას.

### ნაბიჯი 3 - Frontend-ის გახსნა

გახსენით:

```text
http://127.0.0.1:5173/
```

აჩვენეთ:

- sample patient metadata
- editable clinical fields
- Run Prediction ღილაკი

სათქმელი:

> მოდელი ელოდება 137 feature-ს, ამიტომ demo-სთვის ვიყენებ რეალურ test-split პაციენტს როგორც baseline-ს. მომხმარებელი ცვლის მხოლოდ რამდენიმე გასაგებ clinical field-ს, ხოლო დანარჩენი feature-ები რჩება sample patient-ის მნიშვნელობებით.

### ნაბიჯი 4 - პირველი პროგნოზი

დააჭირეთ:

```text
Run Prediction
```

აჩვენეთ:

- risk probability
- risk level
- predicted class
- SHAP top factors

სათქმელი:

> პროგნოზი ბრუნდება XGBoost მოდელიდან. Risk probability აჩვენებს სავარაუდო რისკს, ხოლო SHAP ფაქტორები აჩვენებს რომელი მახასიათებლები ზრდიდა ან ამცირებდა რისკს.

### ნაბიჯი 5 - ველების შეცვლა

შეცვალეთ რამდენიმე ველი:

- Age
- ED systolic BP
- Glucose
- Hemoglobin

შემდეგ ისევ დააჭირეთ:

```text
Run Prediction
```

სათქმელი:

> ცვლილებების შემდეგ frontend აგზავნის ახალ payload-ს backend-ში. backend ამოწმებს feature-ებს, მოდელი აბრუნებს ახალ probability-ს, ხოლო SHAP ხელახლა ითვლის მნიშვნელოვან ფაქტორებს კონკრეტული input-ისთვის.

### ნაბიჯი 6 - SHAP-ის ახსნა

აჩვენეთ top SHAP factors.

სათქმელი:

> SHAP-ის დადებითი მნიშვნელობა ნიშნავს, რომ feature ზრდიდა CVD risk-ის პროგნოზს. უარყოფითი მნიშვნელობა ნიშნავს, რომ feature ამცირებდა რისკის პროგნოზს. ეს მნიშვნელოვანია, რადგან სამედიცინო სისტემაში მოდელი არ უნდა იყოს მხოლოდ black box.

### ნაბიჯი 7 - შეცდომის დამუშავების ახსნა

Swagger-ში შეგიძლიათ ახსენოთ:

> თუ `/predict` endpoint-ზე არ გაიგზავნა ყველა საჭირო feature, backend აბრუნებს HTTP 422 შეცდომას და აჩვენებს რომელი feature-ები აკლია. ეს იცავს სისტემას არასწორი input-ისგან.

## 20-25 წუთიანი პრეზენტაციის სტრუქტურა

### Slide 1 - სათაური

- პროექტის დასახელება
- სტუდენტის სახელი
- ხელმძღვანელი

### Slide 2 - პრობლემა

- გულ-სისხლძარღვთა დაავადებები მაღალი სიკვდილიანობის მიზეზია.
- ექიმს უწევს მრავალი კლინიკური პარამეტრის ანალიზი.
- საჭიროა დამხმარე სისტემა, რომელიც სწრაფად აფასებს რისკს.

### Slide 3 - მიზანი

- ML-ზე დაფუძნებული risk prediction prototype.
- decision-support, არა დამოუკიდებელი დიაგნოზი.
- პროგნოზი + SHAP ახსნა.

### Slide 4 - მონაცემები

- `546,028` ჩანაწერი
- `target_cvd`
- train/validation/test split
- no patient leakage across splits

### Slide 5 - Preprocessing

- outlier handling
- missing indicators
- median imputation from train split
- identifiers removed

### Slide 6 - მოდელები

- Logistic Regression
- Random Forest
- XGBoost

### Slide 7 - შედეგები

XGBoost test metrics:

- AUC-ROC: `0.8754`
- F1-score: `0.8536`
- Recall/Sensitivity: `0.8818`
- Precision: `0.8271`

### Slide 8 - Explainable AI

- რატომ არის SHAP საჭირო
- top factors
- increases/decreases risk interpretation

### Slide 9 - არქიტექტურა

აჩვენეთ flow:

```text
Dataset -> Preprocessing -> Training -> Saved Model -> FastAPI -> React UI
```

### Slide 10 - Demo

- Swagger
- frontend
- prediction
- SHAP factors

### Slide 11 - შეზღუდვები

- retrospective hospital data
- high missingness
- ICU timing bias
- not clinically validated
- not final diagnostic system

### Slide 12 - მომავალი განვითარება

- early-screening model
- Docker
- external validation
- better UI
- patient history storage

## შესაძლო კითხვები და პასუხები

### კითხვა: რატომ XGBoost?

პასუხი:

> XGBoost კარგად მუშაობს tabular clinical data-ზე, უმკლავდება nonlinear ურთიერთობებს და validation/test შედეგებით აჯობა Logistic Regression-სა და Random Forest-ს.

### კითხვა: რატომ არ არის ეს დიაგნოსტიკური სისტემა?

პასუხი:

> რადგან მონაცემები არის რეტროსპექტული და სისტემა არ არის კლინიკურად ვალიდირებული რეალურ გარემოში. ამიტომ სწორია მისი აღწერა როგორც risk prediction decision-support prototype.

### კითხვა: როგორ დაამუშავეთ missing data?

პასუხი:

> არ წავშალე missing rows, რადგან ეს დიდ bias-ს გამოიწვევდა. დავამატე missing indicator სვეტები და რიცხვითი მნიშვნელობები შევავსე train split-ის მედიანებით, რათა validation/test leakage არ მომხდარიყო.

### კითხვა: რატომ sample patient frontend-ში?

პასუხი:

> მოდელს სჭირდება 137 feature. ყველა მათგანის ხელით შეყვანა demo-სთვის არაპრაქტიკულია. sample patient approach ინარჩუნებს სრულ model payload-ს და ამავე დროს აძლევს მომხმარებელს გასაგები კლინიკური ველების შეცვლის საშუალებას.

### კითხვა: რა არის SHAP?

პასუხი:

> SHAP არის explainable AI მეთოდი, რომელიც აჩვენებს თითოეული feature-ის გავლენას კონკრეტულ პროგნოზზე. ის ეხმარება მომხმარებელს გაიგოს, რატომ მიიღო მოდელმა კონკრეტული შედეგი.

### კითხვა: რა არის პროექტის მთავარი შეზღუდვა?

პასუხი:

> მთავარი შეზღუდვა არის ის, რომ მონაცემები მოდის ჰოსპიტალური ჩანაწერებიდან და არა რეალური outpatient screening გარემოდან. ამიტომ პროექტი არის პროტოტიპი და არა კლინიკურად დამტკიცებული სისტემა.

## Backup demo გეგმა

თუ frontend არ გაიხსნა:

1. გახსენით Swagger:

```text
http://127.0.0.1:8765/docs
```

2. აჩვენეთ `/health`.
3. აჩვენეთ `/features`.
4. აჩვენეთ `/sample-patient`.
5. ახსენით, რომ `/predict` იღებს სრულ feature payload-ს.

თუ backend არ გაეშვა:

1. აჩვენეთ `reports/model_metrics.md`.
2. გაუშვით:

```bash
.venv/bin/python src/predict.py --row-index 0 --top-n 6
```

3. აჩვენეთ CLI პროგნოზი და SHAP factors.
