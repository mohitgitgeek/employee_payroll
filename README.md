# employee_payroll

This started as my Grade 12 Python console project (salaries stored in a pickled flat file). It is now a
full-stack web application:

- **Frontend:** server-rendered Jinja templates (`templates/`) with a clean UI.
- **Backend:** Flask (`employee_payroll.py`) with add / list / modify / delete routes.
- **Database:** SQLite via SQLAlchemy (`payroll.db`, created automatically) — replaces the old pickle file.
- **Machine Learning:** an `IsolationForest` model (scikit-learn) on the **ML Insights** page flags
  anomalous salary records (potential data-entry errors / outliers) across BA, DA, TA, HRA, PF, ESI and net salary.

![Main Page](https://github.com/user-attachments/assets/9379fdc4-c476-434a-95f6-766597394dde)

## How to run it

```sh
pip install -r requirements.txt
python employee_payroll.py
# open http://localhost:5000
```

The original console program is preserved (commented out) at the bottom of `employee_payroll.py`.

## Deploy to GitHub Pages

This repository now includes a GitHub Actions workflow at
`.github/workflows/deploy-pages.yml` to deploy the static UI to GitHub Pages.

### Setup

1) In GitHub, go to **Settings → Pages**.
2) Under **Build and deployment**, set **Source** to **GitHub Actions**.
3) Push changes to the `main` branch (or run the workflow manually from the **Actions** tab).

The deployed site serves `index.html`.
