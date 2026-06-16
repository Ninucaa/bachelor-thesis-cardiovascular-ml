# საბოლოო ჩაბარების checklist

ბოლო ვადა: 19 ივნისი, 23:59.

GitHub repository:

```text
https://github.com/Ninucaa/bachelor-thesis-cardiovascular-ml
```

## 1. სამუშაო პროდუქტი / პროტოტიპი

სტატუსი: მზად არის demo-სთვის.

არსებული კომპონენტები:

- FastAPI backend: `src/api/app.py`
- პროგნოზის სერვისი და მოდელის ლოგიკა: `src/api/model_service.py`
- Georgian frontend: `frontend/src/main.js`, `frontend/src/styles.css`
- გაწვრთნილი მოდელები: `models/time_aware/`
- ტექნიკური მოდელის შეფასების reports: `reports/`

Live demo-სთვის გასაშვები მისამართები:

```text
Backend API: http://127.0.0.1:8765
Swagger docs: http://127.0.0.1:8765/docs
Frontend: http://127.0.0.1:5173
```

## 2. Source Code / GitHub

სტატუსი: ატვირთულია GitHub-ზე.

Repository:

```text
https://github.com/Ninucaa/bachelor-thesis-cardiovascular-ml
```

Git history ამჟამად შეიცავს:

- initial project commit
- project folder reference update
- GitHub README merge
- final submission documentation branch

შენიშვნა: არ უნდა შეიქმნას ყალბი ძველი commit history. დარჩენილი გაუმჯობესებები უნდა გაკეთდეს რეალური branch/commit-ებით.

რეკომენდებული honest workflow დარჩენილი დღეებისთვის:

```bash
git checkout main
git pull
git checkout -b docs/final-report
# ცვლილებები
git add .
git commit -m "Improve final technical documentation"
git push -u origin docs/final-report
```

## 3. ტექნიკური დოკუმენტაცია / Report

სტატუსი: ნაწილობრივ მზად, უნდა დასრულდეს ერთიან ფაილად.

აუცილებელი მოთხოვნები და არსებული ფაილები:

| მოთხოვნა | არსებული ფაილი | სტატუსი |
|---|---|---|
| სისტემის არქიტექტურა და დიზაინი | `docs/architecture.md`, `docs/technical_report_ge.md` | დასასრულებელია |
| API დოკუმენტაცია | `docs/technical_report_ge.md`, Swagger `/docs` | დასასრულებელია |
| ინსტალაცია და კონფიგურაცია | `README.md`, `docs/technical_report_ge.md` | დასასრულებელია |
| მომხმარებლის სახელმძღვანელო | `docs/technical_report_ge.md` | დასასრულებელია |
| README | `README.md` | განახლება საჭიროა |
| GitHub link ერთ სივრცეში | `docs/technical_report_ge.md` | დაემატა |

სქრინშოტები ჯერ დასამატებელია საბოლოო report-ში:

- მთავარი frontend ეკრანი
- შევსებული პაციენტის ფორმა
- პროგნოზის შედეგი
- subtype risk cards
- ლაბორატორიული/BMI ნორმების ფანჯარა
- მოდელის ტექნიკური შეფასების ფანჯარა
- Swagger `/docs`

## 4. ფინალური პრეზენტაცია

სტატუსი: ჯერ შესაქმნელია.

პრეზენტაციის რეკომენდებული სტრუქტურა 10-15 წუთისთვის:

1. პრობლემა და მოტივაცია
2. პროექტის მიზანი
3. გამოყენებული მონაცემები
4. preprocessing და feature engineering
5. მოდელის არქიტექტურა
6. subtype დიაგნოზის ჯგუფები
7. შედეგები და მეტრიკები
8. ვებაპლიკაციის demo flow
9. შეზღუდვები და ეთიკური მხარე
10. მომავალი გაუმჯობესებები

## 5. PDF/სილაბუსთან შესაბამისობის რისკები

PDF-ში ნახსენებია რამდენიმე კომპონენტი, რომელიც საბოლოო პროექტში ან შეცვლილია, ან გადავიდა future work-ში:

- React/Tailwind: რეალურად გამოყენებულია Vite + vanilla JavaScript + CSS.
- Docker: ამჟამად არ არის დამატებული.
- PostgreSQL: ამ ეტაპზე არ გამოიყენება.
- SMOTE: საბოლოო pipeline-ში არ გამოიყენება.
- UCI external validation: არ არის შესრულებული.
- ECG digital features: საბოლოო time-aware მოდელში ძირითადი input არ არის; ECG გამოიყენება კლინიკური შემოწმების რეკომენდაციებში/მომავალი განვითარების ნაწილში.

ეს პუნქტები უნდა აიხსნას ტექნიკურ დოკუმენტაციაში როგორც პროექტის გეგმისგან განსხვავებული საბოლოო არქიტექტურული გადაწყვეტილებები ან მომავალი განვითარების ნაწილი.
