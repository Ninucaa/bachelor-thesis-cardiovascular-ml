# გულ-სისხლძარღვთა დაავადებების რისკის პროგნოზირების სისტემა

ეს პროექტი წარმოადგენს მანქანური სწავლების პროტოტიპს, რომელიც კლინიკური მონაცემების საფუძველზე აფასებს გულ-სისხლძარღვთა დაავადებების სავარაუდო დიაგნოსტიკურ მიმართულებას. სისტემა იყენებს წინასწარ დამუშავებულ MIMIC-IV მონაცემებს, time-aware XGBoost მოდელებს და ახსნადობის კომპონენტს, რათა პროგნოზთან ერთად აჩვენოს რომელი მახასიათებლები ახდენს ყველაზე დიდ გავლენას შედეგზე.

პროექტი არ წარმოადგენს დამოუკიდებელ კლინიკურ დიაგნოსტიკურ სისტემას. მისი მიზანია გადაწყვეტილების მიღების მხარდამჭერი პროტოტიპის შექმნა.

## მიმდინარე მდგომარეობა

- მონაცემები დამუშავებულია time-aware პრინციპით და მომზადებულია მოდელისთვის.
- გაწვრთნილია XGBoost მოდელები საერთო გულ-სისხლძარღვთა სიგნალისთვის და 6 აქტიური კლინიკური დიაგნოსტიკური ჯგუფისთვის.
- დამატებულია პაციენტის პროგნოზის ახსნადობა და მოკლე კლინიკური ინტერპრეტაცია.
- დამატებულია FastAPI backend პროგნოზის მისაღებად.
- დამატებულია ქართულენოვანი Vite + JavaScript frontend დემოსთვის.
- frontend-ში დამატებულია optional ECG პასუხის ველი, რომელიც გამოიყენება პაციენტის ანგარიშისა და კლინიკური გადამოწმების კონტექსტში.
- დამატებულია input warning-ები საეჭვო მნიშვნელობებისთვის, Celsius/Fahrenheit დაცვა ტემპერატურის ველზე და ქართულენოვანი კლინიკური დასკვნის copy/TXT/PDF export.

## მოდელის შედეგები

ძირითადი მოდელი: `XGBoost`

პროგნოზის ძირითადი სამიზნე ცვლადია `target_cvd`, მაგრამ მომხმარებლისთვის შედეგი ნაჩვენებია როგორც სავარაუდო გულ-სისხლძარღვთა დიაგნოსტიკური მიმართულება. დამატებით სისტემა ამოწმებს 6 აქტიურ კლინიკურ ჯგუფს, რომლებიც 24 ICD subtype target-ის გაერთიანებით ან ცალკე target-ებად არის მიღებული. მთავარ UI-ში დიაგნოსტიკური მიმართულება აირჩევა balanced threshold-ით, რომელიც validation-ზე დაახლოებით 0.72 precision-ს უმიზნებს, რათა test-ზე precision 0.70-ზე ზემოთ დარჩეს და recall ზედმეტად დაბალი არ იყოს. დაახლოებით 0.80 precision-ის tier გამოიყენება უფრო მკაცრ მეორად სიგნალებად. ვენური თრომბოემბოლია/ფილტვის ემბოლია, პერიფერიული სისხლძარღვოვანი დაავადება, ანთებითი გულის დაავადებები, კარდიომიოპათია და კრიტიკული კარდიული მოვლენა active UI-დან ამოღებულია დაბალი practical recall/precision-ის გამო.

მოდელი აფასებს ალბათობას, რომ პაციენტის კლინიკური პროფილი მსგავსია იმ პაციენტების, რომლებსაც dataset-ში შესაბამისი ICD-კოდირებული გულ-სისხლძარღვთა დიაგნოზი ჰქონდათ. შედეგი არ ცვლის ექიმის საბოლოო დიაგნოზს.

სისტემა არის multi-label decision-support პროტოტიპი: თითოეული კლინიკური ჯგუფი დამოუკიდებლად ფასდება, რადგან MIMIC-IV/ICD მონაცემებში ერთ admission-ს ხშირად რამდენიმე თანმხლები დიაგნოზი აქვს. Frontend-ში ერთი ჯგუფი გამოიყოფა როგორც მთავარი სავარაუდო მიმართულება, ხოლო მის ქვემოთ ნაჩვენებია მაქსიმუმ top 2 დამატებით გადასამოწმებელი კლინიკური სიგნალი. დანარჩენი სიგნალები ხელმისაწვდომია “ყველა სიგნალის ნახვა” რეჟიმში და არ განიმარტება როგორც რამდენიმე საბოლოო დიაგნოზი.

ტესტურ მონაცემებზე:

- AUC-ROC: `0.8863`
- F1-score: `0.8357`
- Recall/Sensitivity: `0.8085`
- Precision: `0.8648`

## პროექტის სტრუქტურა

```text
bachelor-cardio-ai-project/
├── requirements.txt
├── src/
│   ├── build_time_aware_dataset.py
│   ├── train_time_aware_model.py
│   ├── build_diagnosis_thresholds.py
│   ├── train_clinical_group_models.py
│   ├── build_clinical_group_thresholds.py
│   ├── predict.py
│   └── api/
│       ├── app.py
│       ├── model_service.py
│       └── schemas.py
├── models/
│   └── time_aware/
│       ├── target_cvd.pkl
│       ├── target_myocardial_infarction.pkl
│       ├── target_heart_failure.pkl
│       └── feature_columns.json
├── reports/
│   ├── time_aware_model_metrics.md
│   └── diagnosis_thresholds.md
└── docs/
    ├── progress_log.md
    ├── four_day_completion_plan.md
    ├── architecture.md
    ├── demo_script.md
    ├── target_definition.md
    ├── technical_report_ge.md
    ├── user_manual_ge.md
    └── final_submission_checklist_ge.md
├── frontend/
│   ├── package.json
│   ├── index.html
│   └── src/
│       ├── main.js
│       └── styles.css
```

## ინსტალაცია

```bash
cd /Users/ninucaaa/Desktop/new_project/bachelor-cardio-ai-project
.venv/bin/python -m pip install -r requirements.txt
```

## მოდელის გაწვრთნა

```bash
cd /Users/ninucaaa/Desktop/new_project/bachelor-cardio-ai-project
.venv/bin/python src/train_time_aware_model.py
```

## ერთი პაციენტის პროგნოზი

```bash
cd /Users/ninucaaa/Desktop/new_project/bachelor-cardio-ai-project
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
cd /Users/ninucaaa/Desktop/new_project/bachelor-cardio-ai-project
scripts/run_backend.sh
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

შენიშვნა: რეალურ მოთხოვნაში `features` ობიექტში უნდა იყოს ყველა `260` feature, რომელსაც აბრუნებს `/features`.

## Frontend

frontend-ის გაშვება:

```bash
cd /Users/ninucaaa/Desktop/new_project/bachelor-cardio-ai-project/frontend
npm install
../scripts/run_frontend.sh
```

მისამართი:

```text
http://127.0.0.1:5173/
```

თუ `5173` დაკავებულია, Vite ავტომატურად გახსნის შემდეგ თავისუფალ პორტს, მაგალითად `5174`.

frontend აგებულია Vite + vanilla JavaScript + CSS-ით და იყენებს `GET /sample-patient` endpoint-ს, რათა ჩატვირთოს ერთი რეალური test-split პაციენტი. მომხმარებელი ცვლის გასაგებ კლინიკურ ველებს, ხოლო backend-ში იგზავნება სრული `260` feature payload.

## დოკუმენტაცია

საბოლოო ჩაბარებისთვის საჭირო ძირითადი დოკუმენტები:

- `docs/technical_report_ge.md` - ტექნიკური დოკუმენტაცია, არქიტექტურა, API, მოდელი და შეზღუდვები.
- `docs/user_manual_ge.md` - მომხმარებლის სახელმძღვანელო და use case-ები.
- `docs/demo_script.md` - დაცვის დროს demo-ს თანმიმდევრობა.
- `docs/final_submission_checklist_ge.md` - საბოლოო ჩაბარების checklist.

## ტესტირება

Backend API smoke tests:

```bash
cd /Users/ninucaaa/Desktop/new_project/bachelor-cardio-ai-project
scripts/test_backend.sh
```

სერვისების სწრაფი შემოწმება გაშვების შემდეგ:

```bash
scripts/check_services.sh
```

## Docker

Backend-ის containerized გაშვებისთვის დამატებულია `Dockerfile` და `docker-compose.yml`.

```bash
cd /Users/ninucaaa/Desktop/new_project/bachelor-cardio-ai-project
docker compose up --build
```

შენიშვნა: Docker Desktop/daemon უნდა იყოს გაშვებული. Docker image იყენებს saved models-ს და raw MIMIC CSV ფაილებს არ აკოპირებს.

## შეზღუდვები

- მონაცემები არის რეტროსპექტული ჰოსპიტალური ჩანაწერები.
- ზოგიერთი კლინიკური მახასიათებელი ხშირ შემთხვევაში გამოტოვებულია.
- ICU მახასიათებლები შეიძლება ასახავდეს პაციენტის უკვე მძიმე მდგომარეობას და არა მხოლოდ ადრეულ რისკს.
- სისტემა არ სვამს დიაგნოზს დამოუკიდებლად; იგი მხოლოდ დამხმარე ანალიტიკური ინსტრუმენტია.
