# 💰 Smart Expense Tracker

A Python command-line project for recording, organizing, analyzing, and visualizing personal expenses with **Pandas, NumPy, Matplotlib, and Seaborn**.

> **Accuracy note:** This README is based on the project description supplied for this repository. Confirm each command and feature against the current source code before publishing claims about implementation or test results.

## Table of Contents

- [About the Project](#-about-the-project)
- [Project Goals](#-project-goals)
- [Planned Feature Set](#-planned-feature-set)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Data Format](#-data-format)
- [Getting Started](#-getting-started)
- [Running the Application](#-running-the-application)
- [Analysis and Visualizations](#-analysis-and-visualizations)
- [Testing](#-testing)
- [Data Validation and Safety](#-data-validation-and-safety)
- [Limitations and Future Improvements](#-limitations-and-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

## 📌 About the Project

**Smart Expense Tracker** is intended to help users understand where their money goes. The project uses a CSV file for expense records and applies Python data-analysis and visualization libraries to summarize spending patterns.

It is also a practical learning project for Python fundamentals, file handling, input validation, object-oriented programming, data cleaning, numerical analysis, and visualization.

## 🎯 Project Goals

- Organize expense records in a consistent format.
- Summarize spending and compare expense categories.
- Explore spending patterns over time.
- Present numerical results with readable charts.
- Demonstrate practical use of Python's data-analysis ecosystem.

## ✨ Planned Feature Set

The project specification describes the following capabilities. **Verify each item against the current code before treating it as implemented.**

- Add and view expenses.
- Validate dates, amounts, categories, and required fields.
- Store expense records in CSV format between application runs.
- Filter transactions by category, date range, and amount.
- Calculate totals, averages, median, highest and lowest expenses, transaction count, and standard deviation.
- Summarize spending by category and month.
- Generate a financial summary report.
- Create category and time-trend charts, a category-distribution chart, and an expense histogram.
- Handle invalid input, missing or empty CSV files, and filters with no matching records.

## 🧰 Technology Stack

| Technology | Intended role |
|---|---|
| Python 3 | Application logic, input handling, validation, and file operations |
| Pandas | CSV handling, data cleaning, filtering, grouping, and aggregation |
| NumPy | Numerical calculations |
| Matplotlib | Chart creation and formatting |
| Seaborn | Statistical visualization and chart styling |
| CSV | Persistent storage for expense records |
| `unittest` | Standard-library testing, if included in the project |

Keep this list synchronized with the imports and dependency file in the repository.

## 📁 Project Structure

The following is a **proposed structure**, not a verified inventory of the current repository:

```text
Smart-Expense-Tracker/
├── expense_tracker.py
├── expenses.csv
├── requirements.txt
├── README.md
├── .gitignore
├── charts/
│   └── .gitkeep
└── tests/
    └── test_expense_tracker.py
```

Update this tree to match the files that actually exist. Do not commit private expense records or generated files unnecessarily.

## 📋 Data Format

If the application uses the described CSV schema, a record may look like this:

```csv
Date,Amount,Category,Description
2026-10-01,250.00,Food,Lunch
2026-10-02,80.00,Transport,Bus fare
2026-10-03,499.00,Education,Course material
```

The proposed format uses:

- `Date` — date of the transaction, ideally in `YYYY-MM-DD` format.
- `Amount` — expense amount, expected to be a positive finite number.
- `Category` — expense category.
- `Description` — short explanation of the transaction.

Confirm the column names and validation rules in the source code before relying on this example.

## ⚙️ Getting Started

### Prerequisites

- Python 3 installed and available from your terminal.
- Git, if cloning the repository.
- The Python packages listed in `requirements.txt`.

### 1. Clone the repository

```bash
git clone https://github.com/Rami-Manan/Smart-Expense-Tracker.git
cd Smart-Expense-Tracker
```

### 2. Create and activate a virtual environment

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

If the repository includes `requirements.txt`:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If there is no dependency file, install only the packages actually required by the source code. The project description lists:

```bash
python -m pip install numpy pandas matplotlib seaborn
```

## ▶️ Running the Application

If the main script is named `expense_tracker.py`, run:

```bash
python expense_tracker.py
```

Confirm the actual script name and available menu options in the repository before using this command in documentation.

### Example workflow

A typical expense-tracking workflow would be:

1. Start the application.
2. Add an expense with its date, amount, category, and description.
3. Review saved transactions.
4. Run the available summary or filtering operations.
5. Generate visualizations, if supported by the current implementation.
6. Exit and restart the application to check whether records persist.

The exact menu and workflow depend on the implemented code.

## 📊 Analysis and Visualizations

The project description identifies these potential analysis metrics:

| Metric | Meaning |
|---|---|
| Total expenses | Sum of valid transaction amounts |
| Average expense | Mean transaction amount |
| Median expense | Middle value after ordering transaction amounts |
| Highest / lowest expense | Largest and smallest transaction amounts |
| Transaction count | Number of included records |
| Category totals | Total spending grouped by category |
| Monthly spending | Total spending grouped by month |
| Category percentage | Category total as a share of total spending |
| Standard deviation | Measure of variation in transaction amounts |

Category share can be calculated as:

```text
Category Percentage = (Category Total / Total Expenses) × 100
```

The implementation should handle empty data and avoid division by zero.

The described visualization ideas are:

| Chart | Purpose | Suggested filename |
|---|---|---|
| Category bar chart | Compare spending between categories | `category_expenses.png` |
| Monthly trend line | Show spending over time | `monthly_trends.png` |
| Category pie chart | Show each category's share | `category_distribution.png` |
| Expense histogram | Show the distribution of transaction amounts | `expense_histogram.png` |

These filenames are suggestions until verified against the actual code.

## 🧪 Testing

If the repository includes tests under `tests/`, run them from the project root with:

```bash
python -m unittest discover -s tests -v
```

Do not report that tests pass unless the command has been executed successfully. Tests should use temporary files or isolated sample data so they do not modify real expense records.

## 🛡️ Data Validation and Safety

For a reliable expense tracker, validation should address:

- Invalid dates and malformed CSV rows.
- Missing required fields.
- Zero, negative, `NaN`, or infinite amounts, where these are not allowed.
- Missing files and empty datasets.
- Filters that return no matching transactions.
- Safe persistence without accidentally replacing existing records.

Back up important CSV data before editing it manually. Avoid committing real personal financial data, credentials, API keys, or tokens.

## 🛣️ Limitations and Future Improvements

Possible future enhancements include:

- Monthly budgets and overspending alerts.
- Exportable PDF or spreadsheet reports.
- Recurring expense support.
- Search by description.
- Data import and export tools.
- Multi-currency support.
- A graphical interface, if it fits the project's goals.

These are ideas for future work, not claims about current functionality.

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a branch for your change.
3. Make your changes and add or update tests.
4. Run the relevant tests.
5. Open a pull request explaining the change.

## 📄 License

This repository should retain and follow the license present in its `LICENSE` file. If no license file exists, add the intended license before claiming that the project is distributed under it.

## 👨‍💻 Author

**GitHub:** [Rami-Manan](https://github.com/Rami-Manan)

**Repository:** [Smart Expense Tracker](https://github.com/Rami-Manan/Smart-Expense-Tracker)

---

⭐ If you find this project useful for learning Python data analysis, consider starring the repository.
