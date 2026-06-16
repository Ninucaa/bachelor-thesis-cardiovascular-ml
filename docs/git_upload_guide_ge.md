# Git-ზე ატვირთვის გეგმა

ეს repository უნდა შეიცავდეს პროექტის კოდს, დოკუმენტაციას, მოდელის შეფასების ანგარიშებს და საჭირო configuration ფაილებს. MIMIC-IV-ის raw CSV ფაილები Git-ზე არ უნდა აიტვირთოს, რადგან არის დიდი ზომის და მონაცემთა გამოყენების პირობებით შეზღუდული.

## რა უნდა აიტვირთოს

- `README.md` - პროექტის აღწერა და გაშვების ინსტრუქცია.
- `requirements.txt` - Python dependency-ები.
- `src/` - preprocessing, training, prediction და API კოდი.
- `frontend/package.json` და `frontend/package-lock.json` - frontend dependency აღწერა.
- `frontend/index.html`
- `frontend/src/` - frontend-ის source code.
- `models/time_aware/*.pkl` და `models/time_aware/*.json` - demo-სთვის საჭირო გაწვრთნილი მოდელები და feature schema.
- `reports/` - მოდელის შედეგები და preprocessing/modeling ანგარიშები.
- `docs/` - პროექტის აღწერა, არქიტექტურა, progress log და დაცვისთვის საჭირო ტექსტები.
- `.gitignore` - დიდი და პირადი ფაილების Git-იდან გამორიცხვის წესები.

## რა არ უნდა აიტვირთოს

- `.venv/` - Python virtual environment.
- `frontend/node_modules/` - frontend dependency-ები.
- `frontend/dist/` - build output.
- `__pycache__/`
- `.idea/`
- raw MIMIC-IV ფაილები:
  - `admissions.csv.gz`
  - `patients.csv.gz`
  - `diagnoses_icd.csv.gz`
  - `labevents.csv.gz`
  - `chartevents.csv.gz`
  - `omr.csv.gz`
  - `triage.csv.gz`
  - სხვა `.csv` / `.csv.gz` ფაილები
- generated processed data:
  - `cardio_training_features.csv`
  - `data/processed/*.csv`

## მონაცემების pipeline-ის ახსნა

პროექტში raw მონაცემები Git-ზე არ ინახება. მათი არსებობა საჭიროა მხოლოდ ადგილობრივად, რადგან ისინი მოდელის ასაწყობად გამოიყენება.

ძველი assembled ფაილისთვის გამოყენებული preprocessing კოდი შენახულია:

```bash
src/preprocess_cardio_data.py
```

მისი გაშვების მაგალითი:

```bash
cd /Users/ninucaaa/Desktop/new_project/PythonProject
.venv/bin/python src/preprocess_cardio_data.py
```

ეს სკრიპტი კითხულობს:

- `../cardio_training_features.csv`
- `../omr.csv.gz`
- `../diagnoses_icd.csv.gz`
- `../triage.csv.gz`

და ქმნის:

```text
data/processed/cardio_model_ready.csv
reports/preprocessing_report.md
```

უფრო ახალი time-aware dataset-ის ასაწყობად გამოიყენება:

```bash
cd /Users/ninucaaa/Desktop/new_project/PythonProject
.venv/bin/python src/build_time_aware_dataset.py
```

შემდეგ მოდელის გაწვრთნა:

```bash
.venv/bin/python src/train_time_aware_model.py
.venv/bin/python src/build_diagnosis_thresholds.py
```

## რეკომენდებული commit-ები

1. `Initial project structure`
   - README, requirements, src, docs, reports.

2. `Add data preprocessing pipeline`
   - `src/preprocess_cardio_data.py`
   - `src/build_time_aware_dataset.py`
   - preprocessing/modeling reports.

3. `Add cardiovascular diagnosis models`
   - `models/time_aware/`
   - feature schema and thresholds.

4. `Add FastAPI prediction service`
   - `src/api/`
   - prediction schema and model service.

5. `Add Georgian frontend interface`
   - `frontend/src/`
   - Georgian UI, patient form, prediction output.

6. `Improve explainability and clinical interpretation`
   - subtype diagnosis cards
   - patient report
   - laboratory/BMI norms
   - technical model evaluation modal.

## Git ბრძანებები

თუ repository ჯერ არ არის შექმნილი:

```bash
cd /Users/ninucaaa/Desktop/new_project/PythonProject
git init
git status
git add .
git status
git commit -m "Initial cardiovascular diagnosis prediction project"
```

GitHub-ზე repository-ის შექმნის შემდეგ:

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

ატვირთვამდე ყოველთვის გადაამოწმე:

```bash
git status
git diff --cached --stat
```

თუ `*.csv`, `*.csv.gz`, `.venv`, ან `node_modules` გამოჩნდა staged ფაილებში, არ გააგრძელო commit.
