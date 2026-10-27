# 💰 Smart Expense Tracker

A Python command-line application for recording, organizing, analyzing, and visualizing personal expenses using **Pandas, NumPy, Matplotlib, and Seaborn**. It stores transactions in CSV files and includes category-wise monthly budgets with overspending alerts.

[Repository](https://github.com/Rami-Manan/Smart-Expense-Tracker) · [Author](https://github.com/Rami-Manan)

## Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Data Format](#-data-format)
- [Installation](#-installation)
- [Run the Application](#-run-the-application)
- [Monthly Budgets](#-monthly-budgets)
- [Analysis and Charts](#-analysis-and-charts)
- [Testing](#-testing)
- [Data Safety and Limitations](#-data-safety-and-limitations)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)

## 📌 Overview

Smart Expense Tracker is a CLI-based personal finance and data-analysis project. It helps users keep expense records, filter transactions, examine spending patterns, generate a readable report, create charts, and compare monthly category spending against a budget.

The repository includes a demonstration `expenses.csv` dataset with 75 sample transactions. Use your own records only in a local copy and do not commit private financial information.

## ✨ Features

- **Expense records:** add and view expenses with date, amount, category, and description.
- **Input validation:** reject invalid dates, non-positive or non-finite amounts, unsupported categories, and empty descriptions.
- **CSV persistence:** load saved records and save new transactions; CSV writes use a temporary file and replace the target only after the write succeeds.
- **Data cleaning:** identify and exclude rows with invalid dates, amounts, categories, or descriptions when loading.
- **Filtering:** combine category, date range, minimum amount, and maximum amount conditions. Invalid filters return no matches instead of silently broadening the results.
- **Overall analysis:** calculate total, mean, median, standard deviation, maximum, minimum, percentiles, and transaction count.
- **Category analysis:** calculate totals, average, count, minimum, maximum, and percentage by category.
- **Monthly analysis:** summarize expense totals, averages, counts, minima, and maxima by month.
- **Financial report:** print a formatted report and save it as `financial_report.txt` from the CLI.
- **Visualizations:** save category bar, monthly trend line, category pie, and expense histogram charts under `charts/`.
- **Monthly budgets:** set a budget for a category and month, review spending against it, and receive an alert when a new expense pushes a category over budget.
- **Automated tests:** standard-library `unittest` tests use temporary directories for their expense and budget records.
- **Continuous integration:** the included GitHub Actions workflow is configured to run the test suite on pushes and pull requests.

## 🧰 Technology Stack

| Technology | Role |
|---|---|
| Python 3.10+ | Application logic, validation, CLI, and file operations |
| NumPy | Numerical calculations and summary statistics |
| Pandas | CSV loading, validation, filtering, grouping, and aggregation |
| Matplotlib | Chart generation and formatting |
| Seaborn | Chart styling and histogram plotting |
| `unittest` | Automated tests from Python's standard library |
| CSV | Persistent expense and budget storage |
| GitHub Actions | Automated test execution on pushes and pull requests |

## 📁 Project Structure

```text
Smart-Expense-Tracker/
├── .github/
│   └── workflows/
│       └── tests.yml
├── charts/
│   └── .gitkeep
├── tests/
│   └── test_expense_tracker.py
├── .gitignore
├── LICENSE
├── README.md
├── expense_tracker.py
├── expenses.csv
└── requirements.txt
```

Runtime files are created when needed: `budgets.csv` stores category/month budgets, `financial_report.txt` stores the report generated from menu option 7, and PNG charts are written to `charts/`. Those outputs are excluded by `.gitignore`.

## 📋 Data Format

The expense file uses these columns:

```csv
Date,Amount,Category,Description
2026-10-01,250.00,Food,Lunch
2026-10-02,80.00,Transport,Bus fare
2026-10-03,499.00,Education,Course material
```

Dates use `YYYY-MM-DD`. Expense amounts must be positive, finite numbers. Categories are case-insensitive on input and normalized to one of these supported values:

`Food`, `Transport`, `Utilities`, `Entertainment`, `Healthcare`, `Education`, `Shopping`, `Housing`, `Travel`, `Other`.

## 🚀 Installation

### Prerequisites

- Python 3.10 or newer.
- `pip`.
- Git, if cloning the repository.

### 1. Clone the repository

```bash
git clone https://github.com/Rami-Manan/Smart-Expense-Tracker.git
cd Smart-Expense-Tracker
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The dependency file lists NumPy, Pandas, Matplotlib, and Seaborn. `unittest` is included with Python and does not require a separate package.

## ▶️ Run the Application

From the project root, run:

```bash
python expense_tracker.py
```

The main menu contains these options:

```text
 1. Add New Expense
 2. View All Expenses
 3. View Expense Summary
 4. Filter Expenses
 5. Analyze Expenses by Category
 6. Analyze Monthly Spending
 7. Generate Financial Report
 8. Visualize Expenses
 9. View Available Categories
10. Manage Monthly Budgets
11. Exit
```

### Example workflow

1. Choose **1** and enter a date, amount, category, and description. Type `cancel` at an add-expense prompt to abort that operation.
2. Choose **3** to inspect summary statistics or **4** to filter records.
3. Choose **5** or **6** to review category or monthly summaries.
4. Choose **7** to print a financial report and save it as `financial_report.txt`.
5. Choose **8** to generate chart images in `charts/`.
6. Choose **10** to set a category budget or review a month's budget status.

On first run, if `expenses.csv` is missing, the application generates a 75-record sample dataset. If the CSV exists but is zero bytes, it initializes only the header and does **not** invent sample transactions.

## 💸 Monthly Budgets

Select **10. Manage Monthly Budgets**, enter a month as `YYYY-MM`, then choose whether to set/update a category budget or view the budget status.

Each budget is stored by month and category in `budgets.csv`. The status view includes the budget, amount spent, remaining amount, and one of these labels:

- `On track` — spending is below 80% of the budget.
- `Near limit` — spending has reached at least 80% but remains below the limit.
- `At limit` — spending equals the limit.
- `Over budget` — spending is above the limit.

When adding an expense takes a category over its monthly limit, the CLI prints a budget alert. Budget records are kept in a separate file from expense records.

## 📊 Analysis and Charts

### Summary statistics

The expense summary includes total, average, median, sample standard deviation, count, highest and lowest individual expenses, the 25th and 75th percentiles, category totals and percentages, monthly totals, and the top spending category. Empty datasets return zero-valued summary metrics without division by zero.

### Chart outputs

| Chart | Purpose | Output path |
|---|---|---|
| Category bar chart | Compare totals by category | `charts/category_expenses.png` |
| Monthly trend line | Compare total spending across months | `charts/monthly_trends.png` |
| Category pie chart | Show category shares of total spending | `charts/category_distribution.png` |
| Expense histogram | Show the distribution of transaction amounts | `charts/expense_histogram.png` |

The chart methods save files. Interactive chart display depends on whether the runtime has a working graphical environment.

## 🧪 Testing

Run the test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

Tests use temporary directories so that the committed sample `expenses.csv` is not modified. Coverage includes date/month/amount/category validation, add-and-reload persistence, malformed CSV rows, empty datasets, filtering, summary calculations, category/month analysis, chart generation, monthly-budget persistence, and budget alerts.

The included GitHub Actions workflow is configured to run the same test command on pushes and pull requests using Python 3.11. The workflow will run in GitHub after the files are pushed.

## 🛡️ Data Safety and Limitations

- This is a local, single-user CLI app. It has no authentication, cloud sync, or database.
- It uses CSV files and supports Indian Rupees (₹); multi-currency conversion is not implemented.
- Individual expense editing and deletion are not implemented.
- Loading malformed CSV data can exclude invalid rows from the in-memory dataset. Review warnings and keep a backup before working with important records.
- The application generates a sample dataset if `expenses.csv` is missing. Keep a backup of valuable data and make sure the file path is correct before first run.
- Do not commit real personal expense details, `budgets.csv`, generated reports, environment files, API keys, or passwords.

## 🛣️ Future Improvements

- Add edit/delete operations with confirmation and regression tests.
- Export reports as PDF or Excel.
- Add recurring transaction support and description search.
- Add optional currency selection without assuming an exchange rate.
- Capture screenshots from a live app run for the repository presentation.

These are potential extensions, not current features.

## 🤝 Contributing

1. Fork the repository.
2. Create a branch for your change.
3. Implement the change and add/update tests.
4. Run `python -m unittest discover -s tests -v`.
5. Open a pull request describing the change and verification performed.

## 📄 License

This project is released under the [MIT License](LICENSE).

## 👨‍💻 Author

**GitHub:** [Rami-Manan](https://github.com/Rami-Manan)  
**Project repository:** [Smart Expense Tracker](https://github.com/Rami-Manan/Smart-Expense-Tracker)

---

⭐ If this project helps you learn Python and data analysis, consider starring the repository.
