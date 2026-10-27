# Smart Expense Tracker

A Python-based command-line application that allows users to **record, categorize, manage, filter, analyze, and visualize** their personal expenses. Built as a college engineering project demonstrating core Python concepts, data analysis, and visualization.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Objectives](#objectives)
3. [Features](#features)
4. [Technologies Used](#technologies-used)
5. [Project Structure](#project-structure)
6. [Installation & Setup](#installation--setup)
7. [How to Run](#how-to-run)
8. [CSV Dataset Format](#csv-dataset-format)
9. [ExpenseTracker Class](#expensetracker-class)
10. [NumPy & Pandas Integration](#numpy--pandas-integration)
11. [Visualizations](#visualizations)
12. [Sample Workflow](#sample-workflow)
13. [Testing](#testing)
14. [Known Limitations](#known-limitations)

---

## Project Overview

The **Smart Expense Tracker** is a CLI-based personal finance tool that helps users:
- Add expenses with validation
- View and filter expense records
- Analyze spending by category and month
- Generate financial reports
- Visualize spending patterns with charts

All data is stored persistently in a CSV file, and a sample dataset (50–100 records) is generated automatically on first run.

---

## Objectives

- Demonstrate Python control structures (`if`, `elif`, `else`, `while`, `for`) and data structures (lists, dictionaries, arrays).
- Apply **Object-Oriented Programming** with a well-designed `ExpenseTracker` class.
- Use **NumPy** for numerical calculations (sum, mean, median, std, percentile).
- Use **Pandas** for data loading, cleaning, filtering, grouping, and aggregation.
- Create visualizations using **Matplotlib** and **Seaborn**.
- Handle CSV file I/O, data cleaning, and exceptions gracefully.

---

## Features

| Feature | Description |
|---|---|
| **Add Expense** | Input date, amount, category, and description with full validation |
| **View Expenses** | Display all records in a tabular format |
| **Expense Summary** | Total, average, median, std dev, max, min, percentiles |
| **Filter Expenses** | Filter by category, date range, amount range, or combinations |
| **Category Analysis** | Totals, averages, counts, percentages per category |
| **Monthly Analysis** | Monthly totals, averages, and transaction counts |
| **Financial Report** | Complete formatted report with all statistics |
| **Visualizations** | Bar chart, line graph, pie chart, and histogram |
| **Data Persistence** | CSV-based storage that persists across sessions |
| **Input Validation** | Rejects invalid dates, amounts, categories, and empty fields |
| **Cancel Support** | Type `cancel` at any prompt to abort an operation |

---

## Technologies Used

| Technology | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **NumPy** | Numerical calculations (sum, mean, median, std, percentile) |
| **Pandas** | CSV loading, data cleaning, filtering, grouping, aggregation |
| **Matplotlib** | Figure creation, axes, titles, layout for charts |
| **Seaborn** | Styling, color palettes, statistical plots (histogram with KDE) |
| **unittest** | Automated testing framework (Python standard library) |
| **csv / datetime / os** | Standard library modules for CSV I/O, date handling, file paths |

---

## Project Structure

```text
smart-expense-tracker/
│
├── expense_tracker.py        # Main application (all logic + CLI menu)
├── expenses.csv              # Persistent expense dataset (auto-generated)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── charts/                   # Generated chart images
│   ├── .gitkeep
│   ├── category_expenses.png
│   ├── monthly_trends.png
│   ├── category_distribution.png
│   └── expense_histogram.png
│
└── tests/
    └── test_expense_tracker.py  # Automated unit tests
```

---

## Installation & Setup

### Prerequisites

- **Python 3.10 or later** installed on your system.
- **pip** (Python package installer).

### Step 1: Navigate to the project directory

```bash
cd smart-expense-tracker
```

### Step 2: Create a virtual environment (recommended)

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run

```bash
python expense_tracker.py
```

The interactive menu will appear:

```text
=============================================
        SMART EXPENSE TRACKER
=============================================
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
=============================================
```

Select an option by entering its number (1–10).

---

## CSV Dataset Format

The `expenses.csv` file uses the following format:

```csv
Date,Amount,Category,Description
2026-01-10,500.00,Food,Grocery shopping
2026-01-15,1200.50,Transport,Monthly bus pass
```

| Column | Type | Format | Description |
|---|---|---|---|
| `Date` | String → datetime | `YYYY-MM-DD` | Date of the expense |
| `Amount` | Float | Positive number | Expense amount in ₹ |
| `Category` | String | Predefined list | One of 10 categories |
| `Description` | String | Free text | Brief description |

### Supported Categories

Food, Transport, Utilities, Entertainment, Healthcare, Education, Shopping, Housing, Travel, Other

---

## ExpenseTracker Class

The `ExpenseTracker` class is the core of the application. It manages all expense operations.

### Constructor: `__init__(self, filepath)`
- Loads the CSV file into a Pandas DataFrame.
- Generates sample data if the file doesn't exist.
- Cleans and validates all loaded records.

### Method A: `add_expense(self, date, amount, category, description)`
- Validates all four fields before saving.
- Appends the new record to the DataFrame and CSV file.
- Does **not** overwrite existing records.

### Method B: `get_summary(self)`
- Returns a dictionary with: total, average, median, std dev, count, max, min, percentiles, category totals, monthly spending, top category, and category percentages.
- Uses **NumPy** for numerical calculations and **Pandas** for grouping.

### Method C: `filter_expenses(self, condition)`
- Accepts a dictionary with optional keys: `category`, `start_date`, `end_date`, `min_amount`, `max_amount`.
- Returns a filtered **copy** of the DataFrame (original is not modified).

### Method D: `generate_report(self)`
- Produces a formatted financial report as a string.
- Includes all statistics, category breakdowns, monthly trends, and highlights.
- Optionally exports to `financial_report.txt`.

### Additional Methods
- `analyze_by_category()` — Category-wise totals, averages, counts, percentages.
- `analyze_monthly()` — Monthly totals, averages, and counts.
- `plot_category_bar_chart()` — Bar chart of category spending.
- `plot_monthly_trends()` — Line graph of monthly trends.
- `plot_category_pie_chart()` — Pie chart of spending distribution.
- `plot_expense_histogram()` — Histogram of expense amounts.
- `generate_all_charts()` — Generate and save all four charts.

---

## NumPy & Pandas Integration

### NumPy Usage

NumPy is used in `get_summary()` for numerical calculations on the amounts array:

```python
amounts_array = np.array(self.df["Amount"].values, dtype=np.float64)

np.sum(amounts_array)        # Total expenses
np.mean(amounts_array)       # Average expense
np.median(amounts_array)     # Median expense
np.std(amounts_array, ddof=1)  # Standard deviation
np.max(amounts_array)        # Maximum expense
np.min(amounts_array)        # Minimum expense
np.percentile(amounts_array, 25)  # 25th percentile
np.percentile(amounts_array, 75)  # 75th percentile
```

### Pandas Usage

Pandas handles all data operations:

- **Loading:** `pd.read_csv()` with encoding and error handling.
- **Cleaning:** `pd.to_datetime()`, `pd.to_numeric()`, handling NaN/invalid rows.
- **Filtering:** Boolean indexing with multiple conditions.
- **Grouping:** `groupby("Category")`, `groupby(Date.dt.to_period("M"))`.
- **Aggregation:** `.agg(["sum", "mean", "count", "min", "max"])`.
- **Sorting:** `.sort_values()` by spending totals.

A cross-check ensures NumPy and Pandas totals agree:

```python
assert abs(pandas_total - numpy_total) < 0.01
```

---

## Visualizations

All charts are saved to the `charts/` directory and can also be displayed interactively.

### Chart 1: Bar Chart (`category_expenses.png`)
- **Purpose:** Compare total expenses by category.
- Sorted by total spending, with value labels on each bar.
- Uses **Seaborn** `barplot` with the `viridis` palette.

### Chart 2: Line Graph (`monthly_trends.png`)
- **Purpose:** Show spending trends over time.
- Aggregated by month, sorted chronologically.
- Uses **Matplotlib** with markers and fill-between shading.

### Chart 3: Pie Chart (`category_distribution.png`)
- **Purpose:** Show proportional distribution of spending.
- Includes percentage labels for each category.
- Uses **Seaborn** `Set2` color palette.

### Chart 4: Histogram (`expense_histogram.png`)
- **Purpose:** Show frequency distribution of expense amounts.
- Uses **Seaborn** `histplot` with KDE (kernel density estimation).
- 20 bins with edge coloring for clarity.

---

## Sample Workflow

1. **Run the application:** `python expense_tracker.py`
2. **Add an expense (Option 1):**
   ```
   Date: 2026-10-27
   Amount: 450
   Category: Food
   Description: Weekly groceries
   ```
3. **View summary (Option 3):** See total, average, category breakdown.
4. **Filter expenses (Option 4):** Enter `Food` as category to see food expenses.
5. **Generate report (Option 7):** Get a complete financial summary.
6. **Visualize (Option 8):** Generate all four charts in `charts/`.
7. **Exit (Option 10):** Close the application.

---

## Testing

### Run all tests

```bash
python -m unittest discover -s tests -v
```

Or run the test file directly:

```bash
python -m pytest tests/test_expense_tracker.py -v
```

### What is tested

- ✅ Valid and invalid expense addition
- ✅ Date, amount, and category validation
- ✅ Expense summary calculations (total, average, max, min, median, std dev)
- ✅ Category filtering
- ✅ Date-range filtering
- ✅ Amount-range filtering
- ✅ Empty dataset behavior
- ✅ Missing CSV file handling
- ✅ Malformed CSV data cleaning
- ✅ CSV persistence after adding expenses
- ✅ NumPy calculation accuracy
- ✅ Chart generation

Tests use **temporary directories** so the actual `expenses.csv` is never modified.

---

## Known Limitations

1. **Single-user application** — no authentication or multi-user support.
2. **CLI-only** — no graphical user interface (by design, per project requirements).
3. **No database** — uses CSV for persistence (by design, per project requirements).
4. **Currency** — amounts displayed in ₹ (Indian Rupees); no multi-currency support.
5. **Interactive chart display** requires a GUI-capable environment (e.g., VS Code terminal with display access). Charts are always saved as PNG files regardless.
6. **No undo/delete** — individual expense deletion is not implemented in this version.

---

## License

This project is developed for academic/educational purposes.
