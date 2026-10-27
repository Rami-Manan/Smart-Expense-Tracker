# 💰 Smart Expense Tracker

A beginner-friendly Python command-line application for recording, organizing, analyzing, and visualizing personal expenses using **Python, NumPy, Pandas, Matplotlib, and Seaborn**.

> **Project status:** This README is based on the project specification provided. Verify each feature against the implementation and update this document if the code differs.

## 📌 About the Project

The **Smart Expense Tracker** is designed to help users understand where their money goes. It stores transactions in a CSV file, supports filtering and category-based analysis, generates financial summaries, and creates charts that make spending patterns easier to understand.

The project demonstrates Python fundamentals, object-oriented programming, data cleaning, numerical analysis, file handling, exception handling, and data visualization.

## ✨ Features

The specification calls for these capabilities:

- ➕ Add expenses with a date, amount, category, and description.
- 📋 View transactions stored in the CSV dataset.
- 🧹 Validate dates, amounts, categories, and missing values.
- 💾 Preserve transactions in CSV storage across application restarts.
- 🔎 Filter by category, date range, minimum amount, maximum amount, or combined conditions.
- 📊 Calculate totals, averages, median, highest and lowest expenses, transaction count, and standard deviation.
- 🗂️ Analyze category totals, averages, counts, and percentages.
- 📅 Analyze monthly spending and spending trends.
- 🧾 Generate a financial report.
- 📈 Create a category bar chart, spending-trend line graph, category pie chart, and expense histogram.
- 🛡️ Handle invalid input, missing or empty CSV files, and filters with no matching records.

Only describe a feature as complete after confirming it works in the actual code.

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Application logic, validation, control flow, and file handling |
| NumPy | Numerical calculations on expense amounts |
| Pandas | CSV loading, data cleaning, filtering, grouping, and aggregation |
| Matplotlib | Chart creation and figure formatting |
| Seaborn | Visualization styling and statistical plotting |
| `unittest` | Automated testing using Python's standard library |
| CSV | Persistent storage for expense records |

## 📁 Project Structure

The planned project structure is:

```text
smart-expense-tracker/
├── expense_tracker.py
├── expenses.csv
├── requirements.txt
├── README.md
├── charts/
│   └── .gitkeep
└── tests/
    └── test_expense_tracker.py
```

- `expense_tracker.py` — main command-line application and `ExpenseTracker` class.
- `expenses.csv` — expense records stored as CSV.
- `requirements.txt` — third-party Python dependencies.
- `charts/` — directory for generated chart images.
- `tests/test_expense_tracker.py` — automated tests for core functionality.

Adjust this structure if the actual repository differs.

## 📋 Data Format

The CSV dataset is expected to use these columns:

```csv
Date,Amount,Category,Description
2026-10-01,250.00,Food,Lunch
2026-10-02,80.00,Transport,Bus fare
2026-10-03,499.00,Education,Course material
```

Dates use `YYYY-MM-DD`. Amounts should be positive finite numbers, and each record should have a valid category and non-empty description.

### Suggested expense categories

Food, Transport, Utilities, Entertainment, Healthcare, Education, Shopping, Housing, Travel, and Other.

## ⚙️ Requirements

- Python 3
- NumPy
- Pandas
- Matplotlib
- Seaborn

Check the source code and dependency file for the exact supported Python and package versions.

## 🚀 Installation

### 1. Clone the repository

Replace the placeholder URL with the actual URL of your repository:

```bash
git clone <YOUR_REPOSITORY_URL>
cd smart-expense-tracker
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `requirements.txt` is not available yet:

```bash
pip install numpy pandas matplotlib seaborn
```

## ▶️ Run the Application

From the project directory, run:

```bash
python expense_tracker.py
```

The planned interactive menu is:

```text
========================================
        SMART EXPENSE TRACKER
========================================

1. Add New Expense
2. View All Expenses
3. View Expense Summary
4. Filter Expenses
5. Analyze Expenses by Category
6. Analyze Monthly Spending
7. Generate Financial Report
8. Visualize Expenses
9. View Available Categories
10. Exit
```

Choose a menu option and follow the prompts. Ensure the menu documented here matches the final implementation.

## 📊 Financial Analysis

The application is intended to calculate:

| Metric | Meaning |
|---|---|
| Total expenses | Sum of all valid transaction amounts |
| Average expense | Mean transaction amount |
| Median expense | Middle amount after sorting transactions |
| Highest expense | Largest individual transaction |
| Lowest expense | Smallest individual transaction |
| Transaction count | Number of valid transactions |
| Category totals | Total amount spent in each category |
| Monthly spending | Total amount spent in each month |
| Category percentage | Category total as a percentage of all spending |
| Standard deviation | Measure of variation in transaction amounts |

Category percentage can be calculated as:

`Category Percentage = (Category Total / Total Expenses) × 100`

The implementation should handle empty datasets and avoid division by zero.

## 📈 Visualizations

The project specification calls for these charts, saved in the `charts/` directory:

| Chart | Purpose | Suggested output filename |
|---|---|---|
| Bar chart | Compare spending across categories | `category_expenses.png` |
| Line graph | Show spending trends over time | `monthly_trends.png` |
| Pie chart | Show each category's share of total spending | `category_distribution.png` |
| Histogram | Show the frequency distribution of expense amounts | `expense_histogram.png` |

Charts should have descriptive titles and readable labels. The application should handle empty or invalid data without creating misleading plots.

## 🧱 Object-Oriented Design

The planned `ExpenseTracker` class manages expense data and core operations. Its required methods are:

- `add_expense(date, amount, category, description)` — validates and saves an expense.
- `get_summary()` — returns overall and grouped expense statistics.
- `filter_expenses(condition)` — returns records matching the supplied filters without changing the original dataset.
- `generate_report()` — displays a readable financial report.

Document exact behavior and return values according to the final source code.

## 🧪 Run Tests

If the project includes the proposed test suite, run it from the project root:

```bash
python -m unittest discover -s tests -v
```

Tests should use temporary files or directories so they do not unintentionally change the real `expenses.csv` file. Do not claim that tests pass unless they have actually been run successfully.

## 🔒 Data Safety and Validation

The application should:

- Reject invalid dates and non-positive, `NaN`, or infinite amounts.
- Prevent incomplete or invalid transactions from being saved.
- Preserve existing records when starting the program.
- Avoid replacing valid data with sample data.
- Report malformed rows and data-cleaning problems clearly.
- Handle missing files and empty datasets gracefully.

Keep a backup of important financial data before making manual changes to the CSV file.

## 🛣️ Possible Future Improvements

- Monthly budgets and budget-limit warnings.
- Exportable PDF or spreadsheet reports.
- Recurring expense support.
- Search by description.
- Import and export tools.
- Multi-currency support.
- A graphical interface, if the project scope later permits one.

These are suggestions, not claims about existing functionality.

## 🤝 Contributing

1. Fork the repository.
2. Create a branch for your change.
3. Make your changes and add or update tests.
4. Run the tests locally.
5. Open a pull request describing the changes.

## 📄 License

Add the license used by this project before distributing it. If the repository does not contain a `LICENSE` file, no specific open-source license is implied by this README.

## 👨‍💻 Author

**GitHub:** [Rami-Manan](https://github.com/Rami-Manan)

---

⭐ If you find this project useful for learning Python data analysis, consider starring the repository.

**Note:** Keep this README synchronized with the actual source code. Remove or revise any feature description that is not implemented.
