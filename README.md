# გულ-სისხლძარღვთა დაავადებების რისკის პროგნოზირების სისტემა

ეს პროექტი წარმოადგენს მანქანური სწავლების პროტოტიპს, რომელიც კლინიკური მონაცემების საფუძველზე აფასებს გულ-სისხლძარღვთა დაავადების რისკს. სისტემა იყენებს წინასწარ დამუშავებულ მონაცემებს, გაწვრთნილ ML მოდელს და SHAP ახსნადობის კომპონენტს, რათა პროგნოზთან ერთად აჩვენოს რომელი მახასიათებლები ახდენს ყველაზე დიდ გავლენას შედეგზე.

პროექტი არ წარმოადგენს დამოუკიდებელ კლინიკურ დიაგნოსტიკურ სისტემას. მისი მიზანია გადაწყვეტილების მიღების მხარდამჭერი პროტოტიპის შექმნა.

## მიმდინარე მდგომარეობა

- მონაცემები გასუფთავებულია და მომზადებულია მოდელისთვის.
- გაწვრთნილია სამი მოდელი: Logistic Regression, Random Forest და XGBoost.
- საუკეთესო შედეგი აჩვენა XGBoost მოდელმა.
- დამატებულია SHAP ახსნადობა ერთი პაციენტის პროგნოზისთვის.
- დამატებულია FastAPI backend პროგნოზის მისაღებად.
- დამატებულია React frontend დემოსთვის.

## მოდელის შედეგები

საუკეთესო მოდელი: `xgboost`

პროგნოზის სამიზნე ცვლადი არის `target_cvd`, მაგრამ მომხმარებლისთვის ის ნაჩვენებია როგორც გულ-სისხლძარღვთა დაავადების რისკი.

მოდელი აფასებს ალბათობას, რომ პაციენტის კლინიკური პროფილი მსგავსია იმ პაციენტების, რომლებიც dataset-ში გულ-სისხლძარღვთა დაავადების დადებით კლასში იყვნენ. ეს არ არის კონკრეტული დიაგნოზი, მაგალითად heart attack ან stroke.

ტესტურ მონაცემებზე:

- AUC-ROC: `0.8754`
- F1-score: `0.8536`
- Recall/Sensitivity: `0.8818`
- Precision: `0.8271`

## პროექტის სტრუქტურა

```text
PythonProject/
├── main.py
├── requirements.txt
├── src/
│   ├── train_model.py
│   ├── predict.py
│   └── api/
│       ├── app.py
│       ├── model_service.py
│       └── schemas.py
├── models/
│   ├── xgboost.pkl
│   ├── random_forest.pkl
│   ├── logistic_regression.pkl
│   └── feature_columns.json
├── reports/
│   ├── model_metrics.md
│   └── model_metrics.json
└── docs/
    ├── progress_log.md
    ├── four_day_completion_plan.md
    ├── architecture.md
    ├── demo_script.md
    └── target_definition.md
frontend/
├── package.json
├── index.html
└── src/
    ├── main.js
    └── styles.css
```

## ინსტალაცია

```bash
cd /Users/ninucaaa/Desktop/new_project/PythonProject
.venv/bin/python -m pip install -r requirements.txt
```

## მოდელის გაწვრთნა

```bash
cd /Users/ninucaaa/Desktop/new_project/PythonProject
.venv/bin/python src/train_model.py
```

## ერთი პაციენტის პროგნოზი

```bash
cd /Users/ninucaaa/Desktop/new_project/PythonProject
.venv/bin/python src/predict.py --row-index 0 --top-n 6
```

სკრიპტი აბრუნებს:

- რისკის ალბათობას
- პროგნოზირებულ კლასს
- რისკის დონეს
- რეალურ target-ს, თუ მონაცემში არსებობს
- SHAP-ის მიხედვით ყველაზე მნიშვნელოვან ფაქტორებს

## FastAPI backend

backend-ის გაშვება:

```bash
cd /Users/ninucaaa/Desktop/new_project/PythonProject
.venv/bin/uvicorn src.api.app:app --host 127.0.0.1 --port 8765
```

Swagger დოკუმენტაცია:

```text
http://127.0.0.1:8765/docs
```

endpoint-ები:

- `GET /health` - ამოწმებს მუშაობს თუ არა API და ჩატვირთულია თუ არა მოდელი.
- `GET /features` - აბრუნებს იმ feature-ების სიას, რომლებსაც მოდელი ელოდება.
- `GET /sample-patient` - აბრუნებს ერთ test-split პაციენტს frontend demo-სთვის.
- `POST /predict` - იღებს პაციენტის model-ready feature-ებს და აბრუნებს პროგნოზს SHAP ახსნით.

`POST /predict` მოთხოვნის ზოგადი ფორმა:

```json
{
  "features": {
    "age": 67,
    "gender_male": 1
  },
  "top_n": 6
}
```

შენიშვნა: რეალურ მოთხოვნაში `features` ობიექტში უნდა იყოს ყველა `137` feature, რომელსაც აბრუნებს `/features`.

## React frontend

frontend-ის გაშვება:

```bash
cd /Users/ninucaaa/Desktop/new_project/PythonProject/frontend
npm install
npm run dev
```

მისამართი:

```text
http://127.0.0.1:5173/
```

frontend იყენებს `GET /sample-patient` endpoint-ს, რათა ჩატვირთოს ერთი რეალური test-split პაციენტი. მომხმარებელი ცვლის მხოლოდ რამდენიმე გასაგებ კლინიკურ ველს, ხოლო დანარჩენი feature-ები რჩება sample patient-ის მნიშვნელობებით. ეს საშუალებას იძლევა demo იყოს მარტივი, მაგრამ backend-ში მაინც გაიგზავნოს სრული `137` feature payload.

## შეზღუდვები

- მონაცემები არის რეტროსპექტული ჰოსპიტალური ჩანაწერები.
- ზოგიერთი კლინიკური მახასიათებელი ხშირ შემთხვევაში გამოტოვებულია.
- ICU მახასიათებლები შეიძლება ასახავდეს პაციენტის უკვე მძიმე მდგომარეობას და არა მხოლოდ ადრეულ რისკს.
- სისტემა არ სვამს დიაგნოზს დამოუკიდებლად; იგი მხოლოდ დამხმარე ანალიტიკური ინსტრუმენტია.
