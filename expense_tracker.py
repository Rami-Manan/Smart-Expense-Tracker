"""
Smart Expense Tracker Application
===================================
A Python-based CLI application that allows users to record, categorize,
manage, filter, analyze, and visualize their personal expenses.

Demonstrates:
    - Python control structures and arrays
    - Functions and input validation
    - Object-Oriented Programming (OOP)
    - NumPy for numerical calculations
    - Pandas for dataset management and analysis
    - Matplotlib and Seaborn for data visualization
    - CSV file handling, data cleaning, and exception handling
"""

import os
import sys
import csv
import math
import random
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any

try:
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend; switched to TkAgg when displaying
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_DEPS = True
    _DEPS_ERROR = ""
except ImportError as _err:
    np = None  # type: ignore
    pd = None  # type: ignore
    plt = None  # type: ignore
    sns = None  # type: ignore
    HAS_DEPS = False
    _DEPS_ERROR = str(_err)

# ──────────────────────────── CONSTANTS ────────────────────────────

# File paths (relative to the script's directory)
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
CSV_FILE: str = os.path.join(BASE_DIR, "expenses.csv")
CHARTS_DIR: str = os.path.join(BASE_DIR, "charts")

# Supported expense categories
CATEGORIES: List[str] = [
    "Food",
    "Transport",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Education",
    "Shopping",
    "Housing",
    "Travel",
    "Other",
]

# CSV column names
CSV_COLUMNS: List[str] = ["Date", "Amount", "Category", "Description"]

# ──────────────────────────── HELPER / VALIDATION FUNCTIONS ────────

def normalize_category(category: str) -> Optional[str]:
    """Return the properly-cased category name if *category* matches one
    of the predefined categories (case-insensitive), else ``None``.

    Args:
        category: The raw category string entered by the user.

    Returns:
        The normalized category name, or None if invalid.
    """
    category_map: Dict[str, str] = {c.lower(): c for c in CATEGORIES}
    return category_map.get(category.strip().lower())


def validate_date(date_str: str) -> Optional[str]:
    """Validate that *date_str* is a real date in ``YYYY-MM-DD`` format.

    Args:
        date_str: The raw date string to validate.

    Returns:
        The validated date string, or None if invalid.
    """
    try:
        dt = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None


def validate_amount(amount_str: str) -> Optional[float]:
    """Validate that *amount_str* represents a positive, finite number.

    Rejects zero, negative, NaN, and infinite values.

    Args:
        amount_str: The raw amount string to validate.

    Returns:
        The validated amount as a float, or None if invalid.
    """
    try:
        value = float(amount_str.strip())
        if math.isnan(value) or math.isinf(value):
            return None
        if value <= 0:
            return None
        return round(value, 2)
    except (ValueError, TypeError):
        return None


# ──────────────────────────── SAMPLE DATA GENERATOR ────────────────

def generate_sample_data(filepath: str, num_records: int = 75) -> None:
    """Create a realistic sample CSV dataset with ~75 expense records.

    The function generates random but plausible transactions spanning
    the last six months across all supported categories.

    Args:
        filepath: Path where the CSV file will be written.
        num_records: Approximate number of records to generate.
    """
    descriptions: Dict[str, List[str]] = {
        "Food": [
            "Grocery shopping", "Restaurant dinner", "Coffee shop",
            "Lunch at cafeteria", "Online food delivery", "Snacks",
            "Bakery items", "Fruit and vegetables",
        ],
        "Transport": [
            "Bus fare", "Metro card recharge", "Cab to office",
            "Fuel refill", "Uber ride", "Auto rickshaw",
            "Parking charges", "Train ticket",
        ],
        "Utilities": [
            "Electricity bill", "Water bill", "Internet bill",
            "Mobile recharge", "Gas bill", "DTH recharge",
        ],
        "Entertainment": [
            "Movie tickets", "Netflix subscription", "Concert tickets",
            "Spotify subscription", "Bowling night", "Video game purchase",
        ],
        "Healthcare": [
            "Doctor consultation", "Pharmacy medicines", "Lab tests",
            "Dental checkup", "Health insurance premium", "Eye checkup",
        ],
        "Education": [
            "Textbooks", "Online course fee", "Stationery supplies",
            "Tuition fee", "Exam registration", "Workshop fee",
        ],
        "Shopping": [
            "Clothing purchase", "Electronics accessory", "Home decor",
            "Kitchen appliance", "Shoes", "Gift for friend",
        ],
        "Housing": [
            "Monthly rent", "Home maintenance", "Furniture repair",
            "Cleaning supplies", "Plumber visit", "Pest control",
        ],
        "Travel": [
            "Flight ticket", "Hotel booking", "Travel insurance",
            "Sightseeing tour", "Luggage purchase", "Visa fee",
        ],
        "Other": [
            "Charity donation", "Pet supplies", "Miscellaneous",
            "Subscription box", "Library fine", "Laundry service",
        ],
    }

    amount_ranges: Dict[str, tuple] = {
        "Food": (50, 2000),
        "Transport": (20, 1500),
        "Utilities": (200, 5000),
        "Entertainment": (100, 3000),
        "Healthcare": (100, 8000),
        "Education": (200, 15000),
        "Shopping": (200, 10000),
        "Housing": (1000, 25000),
        "Travel": (500, 30000),
        "Other": (50, 3000),
    }

    random.seed(42)  # Reproducible sample data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    rows: List[List[Any]] = []
    for _ in range(num_records):
        # Random date within the last 6 months
        random_days = random.randint(0, (end_date - start_date).days)
        date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

        # Random category and description
        category = random.choice(CATEGORIES)
        description = random.choice(descriptions[category])

        # Random amount within the category's typical range
        low, high = amount_ranges[category]
        amount = round(random.uniform(low, high), 2)

        rows.append([date, amount, category, description])

    # Sort by date for readability
    rows.sort(key=lambda r: r[0])

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)
        writer.writerows(rows)

    print(f"[INFO] Generated sample dataset with {num_records} records → {filepath}")


# ──────────────────────────── EXPENSE TRACKER CLASS ────────────────

class ExpenseTracker:
    """Core class that manages loading, validating, adding, filtering,
    analyzing, and reporting expenses.

    Attributes:
        filepath: Path to the CSV file used for persistent storage.
        df: Pandas DataFrame holding the current expense records.
    """

    def __init__(self, filepath: str = CSV_FILE) -> None:
        """Initialize the tracker and load existing data.

        If the CSV file does not exist, a sample dataset is generated
        automatically. Existing user data is never overwritten.

        Args:
            filepath: Path to the CSV file.
        """
        if not HAS_DEPS:
            raise ImportError(
                f"Required dependencies are missing ({_DEPS_ERROR}). "
                "Please run: pip install -r requirements.txt"
            )
        self.filepath: str = filepath
        self.df: pd.DataFrame = pd.DataFrame(columns=CSV_COLUMNS)
        self._ensure_csv_exists()
        self._load_data()

    # ── Private helpers ──────────────────────────────────────────────

    def _ensure_csv_exists(self) -> None:
        """Create a sample CSV if the file does not exist or is empty."""
        parent_dir = os.path.dirname(os.path.abspath(self.filepath))
        try:
            os.makedirs(parent_dir, exist_ok=True)
        except OSError as e:
            print(f"[ERROR] Could not create the CSV directory: {e}")
            return

        if not os.path.exists(self.filepath):
            print("[INFO] CSV file not found. Generating sample dataset...")
            generate_sample_data(self.filepath)
        else:
            # Check if file is empty (0 bytes or only whitespace)
            try:
                size = os.path.getsize(self.filepath)
                if size == 0:
                    print("[INFO] CSV file is empty. Generating sample dataset...")
                    generate_sample_data(self.filepath)
            except OSError as e:
                print(f"[WARNING] Could not check CSV file size: {e}")

    def _load_data(self) -> None:
        """Load and clean the CSV dataset into a Pandas DataFrame.

        Performs the following cleaning steps:
            1. Read CSV with proper encoding.
            2. Validate column names.
            3. Convert Date to datetime.
            4. Convert Amount to numeric.
            5. Validate categories.
            6. Report and drop invalid rows.
            7. Identify duplicates.
        """
        try:
            raw_df = pd.read_csv(self.filepath, encoding="utf-8")
        except FileNotFoundError:
            print("[WARNING] CSV file not found. Starting with empty dataset.")
            self.df = pd.DataFrame(columns=CSV_COLUMNS)
            return
        except pd.errors.EmptyDataError:
            print("[WARNING] CSV file is empty. Starting with empty dataset.")
            self.df = pd.DataFrame(columns=CSV_COLUMNS)
            return
        except (OSError, UnicodeError, pd.errors.ParserError) as e:
            print(f"[ERROR] Could not read CSV file: {e}")
            self.df = pd.DataFrame(columns=CSV_COLUMNS)
            return

        # Validate columns
        missing_cols = [c for c in CSV_COLUMNS if c not in raw_df.columns]
        if missing_cols:
            print(f"[WARNING] CSV is missing columns: {missing_cols}. "
                  f"Starting with empty dataset.")
            self.df = pd.DataFrame(columns=CSV_COLUMNS)
            return

        # Keep only required columns (extras are ignored)
        df = raw_df[CSV_COLUMNS].copy()
        invalid_indices: List[int] = []

        # --- Date validation ---
        df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d", errors="coerce")
        bad_dates = df["Date"].isna()
        if bad_dates.any():
            count = bad_dates.sum()
            print(f"[WARNING] Found {count} row(s) with invalid dates – these will be removed.")
            invalid_indices.extend(df[bad_dates].index.tolist())

        # --- Amount validation ---
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        bad_amounts = df["Amount"].isna() | (df["Amount"] <= 0) | np.isinf(df["Amount"])
        if bad_amounts.any():
            count = bad_amounts.sum()
            print(f"[WARNING] Found {count} row(s) with invalid amounts – these will be removed.")
            invalid_indices.extend(df[bad_amounts].index.tolist())

        # --- Category validation ---
        valid_lower = {c.lower() for c in CATEGORIES}
        bad_categories = ~df["Category"].astype(str).str.strip().str.lower().isin(valid_lower)
        if bad_categories.any():
            count = bad_categories.sum()
            print(f"[WARNING] Found {count} row(s) with invalid categories – these will be removed.")
            invalid_indices.extend(df[bad_categories].index.tolist())

        # --- Description validation ---
        bad_desc = df["Description"].isna() | (df["Description"].astype(str).str.strip() == "")
        if bad_desc.any():
            count = bad_desc.sum()
            print(f"[WARNING] Found {count} row(s) with empty descriptions – these will be removed.")
            invalid_indices.extend(df[bad_desc].index.tolist())

        # Drop all invalid rows (de-duplicate indices first)
        invalid_indices = list(set(invalid_indices))
        if invalid_indices:
            df = df.drop(index=invalid_indices).reset_index(drop=True)

        # Normalize category names
        df["Category"] = df["Category"].astype(str).str.strip().str.lower().map(
            {c.lower(): c for c in CATEGORIES}
        )

        # Round amounts to 2 decimal places
        df["Amount"] = df["Amount"].round(2)

        # Check for duplicate records
        duplicates = df.duplicated()
        if duplicates.any():
            count = duplicates.sum()
            print(f"[INFO] Found {count} duplicate row(s) in the dataset.")

        self.df = df
        print(f"[INFO] Loaded {len(self.df)} valid expense record(s) from CSV.")

    def _save_to_csv(self) -> None:
        """Save the current DataFrame to the CSV file."""
        try:
            save_df = self.df.copy()
            save_df["Date"] = save_df["Date"].dt.strftime("%Y-%m-%d")
            save_df.to_csv(self.filepath, index=False, encoding="utf-8")
        except PermissionError:
            print("[ERROR] Permission denied – could not save to CSV file.")
        except OSError as e:
            print(f"[ERROR] Could not save CSV file: {e}")

    # ── A. add_expense ───────────────────────────────────────────────

    def add_expense(self, date: str, amount: float, category: str,
                    description: str) -> bool:
        """Validate and add a new expense to the dataset and CSV file.

        Args:
            date: Expense date in YYYY-MM-DD format.
            amount: Positive expense amount.
            category: One of the predefined categories.
            description: Brief description of the expense.

        Returns:
            True if the expense was added successfully, False otherwise.
        """
        # Validate date
        validated_date = validate_date(date)
        if validated_date is None:
            print("[ERROR] Invalid date format. Use YYYY-MM-DD.")
            return False

        # Validate amount
        validated_amount = validate_amount(str(amount))
        if validated_amount is None:
            print("[ERROR] Amount must be a positive number.")
            return False

        # Validate category
        normalized_cat = normalize_category(category)
        if normalized_cat is None:
            print(f"[ERROR] Invalid category '{category}'. "
                  f"Valid categories: {', '.join(CATEGORIES)}")
            return False

        # Validate description
        if not description or not description.strip():
            print("[ERROR] Description cannot be empty.")
            return False

        description = description.strip()

        # Create new record
        new_row = pd.DataFrame([{
            "Date": pd.to_datetime(validated_date),
            "Amount": validated_amount,
            "Category": normalized_cat,
            "Description": description,
        }])

        # Append to CSV file (don't rewrite the whole file)
        try:
            file_exists = os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0
            with open(self.filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(CSV_COLUMNS)
                writer.writerow([validated_date, validated_amount,
                                 normalized_cat, description])
        except PermissionError:
            print("[ERROR] Permission denied – could not write to CSV file.")
            return False
        except OSError as e:
            print(f"[ERROR] Could not write to CSV file: {e}")
            return False

        # Update the in-memory dataset only after persistence succeeds.
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        print(f"[SUCCESS] Expense added: {validated_date} | "
              f"₹{validated_amount:,.2f} | {normalized_cat} | {description}")
        return True

    # ── B. get_summary ───────────────────────────────────────────────

    def get_summary(self) -> Dict[str, Any]:
        """Calculate and return a comprehensive expense summary.

        Uses both NumPy and Pandas for calculations. Returns a dictionary
        with all summary metrics.

        Returns:
            Dictionary containing total, average, count, max, min,
            category totals, monthly spending, top category, and
            spending percentages.
        """
        summary: Dict[str, Any] = {}

        if self.df.empty:
            summary["total"] = 0.0
            summary["average"] = 0.0
            summary["count"] = 0
            summary["max"] = 0.0
            summary["min"] = 0.0
            summary["median"] = 0.0
            summary["std_dev"] = 0.0
            summary["category_totals"] = {}
            summary["monthly_spending"] = {}
            summary["top_category"] = "N/A"
            summary["category_percentages"] = {}
            return summary

        # --- NumPy calculations ---
        amounts_array: np.ndarray = np.array(self.df["Amount"].values, dtype=np.float64)

        summary["total"] = float(np.sum(amounts_array))
        summary["average"] = float(np.mean(amounts_array))
        summary["count"] = int(len(amounts_array))
        summary["max"] = float(np.max(amounts_array))
        summary["min"] = float(np.min(amounts_array))
        summary["median"] = float(np.median(amounts_array))
        summary["std_dev"] = float(np.std(amounts_array, ddof=1)) if len(amounts_array) > 1 else 0.0

        # Percentile calculations using NumPy
        summary["25th_percentile"] = float(np.percentile(amounts_array, 25))
        summary["75th_percentile"] = float(np.percentile(amounts_array, 75))

        # --- Pandas calculations ---
        # Category-wise totals
        cat_totals: pd.Series = self.df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
        summary["category_totals"] = cat_totals.to_dict()

        # Monthly spending
        monthly: pd.Series = self.df.groupby(self.df["Date"].dt.to_period("M"))["Amount"].sum()
        summary["monthly_spending"] = {str(k): float(v) for k, v in monthly.items()}

        # Top spending category
        summary["top_category"] = cat_totals.index[0] if not cat_totals.empty else "N/A"

        # Category spending percentages
        total = summary["total"]
        if total > 0:
            summary["category_percentages"] = {
                cat: round((amt / total) * 100, 2)
                for cat, amt in cat_totals.items()
            }
        else:
            summary["category_percentages"] = {}

        # Verify NumPy and Pandas totals agree
        pandas_total = float(self.df["Amount"].sum())
        numpy_total = summary["total"]
        assert abs(pandas_total - numpy_total) < 0.01, (
            f"NumPy/Pandas total mismatch: {numpy_total} vs {pandas_total}"
        )

        return summary

    # ── C. filter_expenses ───────────────────────────────────────────

    def filter_expenses(self, condition: Dict[str, Any]) -> pd.DataFrame:
        """Filter expenses based on multiple optional conditions.

        Args:
            condition: Dictionary with optional keys:
                - 'category' (str): Filter by category name.
                - 'start_date' (str): Start date in YYYY-MM-DD format.
                - 'end_date' (str): End date in YYYY-MM-DD format.
                - 'min_amount' (float): Minimum expense amount.
                - 'max_amount' (float): Maximum expense amount.

        Returns:
            A filtered copy of the DataFrame (original is not modified).
        """
        filtered = self.df.copy()

        if filtered.empty:
            return filtered

        # Filter by category
        if "category" in condition and condition["category"]:
            cat = normalize_category(condition["category"])
            if cat:
                filtered = filtered[filtered["Category"] == cat]
            else:
                print(f"[WARNING] Invalid category '{condition['category']}' – "
                      f"filter not applied.")

        # Filter by start date
        if "start_date" in condition and condition["start_date"]:
            start = validate_date(condition["start_date"])
            if start:
                filtered = filtered[filtered["Date"] >= pd.to_datetime(start)]
            else:
                print("[WARNING] Invalid start date – filter not applied.")

        # Filter by end date
        if "end_date" in condition and condition["end_date"]:
            end = validate_date(condition["end_date"])
            if end:
                filtered = filtered[filtered["Date"] <= pd.to_datetime(end)]
            else:
                print("[WARNING] Invalid end date – filter not applied.")

        # Filter by minimum amount
        if "min_amount" in condition and condition["min_amount"] is not None:
            try:
                min_val = float(condition["min_amount"])
                filtered = filtered[filtered["Amount"] >= min_val]
            except (ValueError, TypeError):
                print("[WARNING] Invalid minimum amount – filter not applied.")

        # Filter by maximum amount
        if "max_amount" in condition and condition["max_amount"] is not None:
            try:
                max_val = float(condition["max_amount"])
                filtered = filtered[filtered["Amount"] <= max_val]
            except (ValueError, TypeError):
                print("[WARNING] Invalid maximum amount – filter not applied.")

        return filtered.reset_index(drop=True)

    # ── D. generate_report ───────────────────────────────────────────

    def generate_report(self) -> str:
        """Generate a comprehensive financial report as a formatted string.

        The report includes overall statistics, category-wise spending,
        monthly spending, and top spending categories.

        Returns:
            The formatted report as a string.
        """
        summary = self.get_summary()
        lines: List[str] = []
        sep = "=" * 55

        lines.append(sep)
        lines.append("         SMART EXPENSE TRACKER – FINANCIAL REPORT")
        lines.append(sep)
        lines.append(f"  Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(sep)

        # Overall statistics
        lines.append("\n── OVERALL EXPENSE STATISTICS ─────────────────────────")
        lines.append(f"  Total Expenses      : ₹{summary['total']:>12,.2f}")
        lines.append(f"  Average Expense     : ₹{summary['average']:>12,.2f}")
        lines.append(f"  Median Expense      : ₹{summary['median']:>12,.2f}")
        lines.append(f"  Std. Deviation      : ₹{summary['std_dev']:>12,.2f}")
        lines.append(f"  Number of Records   : {summary['count']:>13,}")
        lines.append(f"  Highest Expense     : ₹{summary['max']:>12,.2f}")
        lines.append(f"  Lowest Expense      : ₹{summary['min']:>12,.2f}")

        if summary["count"] > 0:
            lines.append(f"  25th Percentile     : ₹{summary.get('25th_percentile', 0):>12,.2f}")
            lines.append(f"  75th Percentile     : ₹{summary.get('75th_percentile', 0):>12,.2f}")

        # Category-wise spending
        lines.append("\n── CATEGORY-WISE SPENDING ─────────────────────────────")
        lines.append(f"  {'Category':<15} {'Total':>12} {'Percentage':>10}")
        lines.append(f"  {'-'*15} {'-'*12} {'-'*10}")
        for cat, total in summary["category_totals"].items():
            pct = summary["category_percentages"].get(cat, 0)
            lines.append(f"  {cat:<15} ₹{total:>10,.2f} {pct:>9.1f}%")

        if summary["category_totals"]:
            lines.append(f"\n  Top Spending Category: {summary['top_category']}")

        # Monthly spending
        lines.append("\n── MONTHLY SPENDING ───────────────────────────────────")
        lines.append(f"  {'Month':<12} {'Total':>12}")
        lines.append(f"  {'-'*12} {'-'*12}")
        for month, total in summary["monthly_spending"].items():
            lines.append(f"  {month:<12} ₹{total:>10,.2f}")

        if summary["monthly_spending"]:
            avg_monthly = summary["total"] / len(summary["monthly_spending"])
            lines.append(f"\n  Average Monthly Spending: ₹{avg_monthly:>10,.2f}")

        # Highest and lowest expense details
        if not self.df.empty:
            lines.append("\n── EXPENSE HIGHLIGHTS ─────────────────────────────────")
            idx_max = self.df["Amount"].idxmax()
            idx_min = self.df["Amount"].idxmin()
            row_max = self.df.loc[idx_max]
            row_min = self.df.loc[idx_min]
            lines.append(f"  Highest: ₹{row_max['Amount']:,.2f} – "
                         f"{row_max['Category']} – {row_max['Description']} "
                         f"({row_max['Date'].strftime('%Y-%m-%d')})")
            lines.append(f"  Lowest : ₹{row_min['Amount']:,.2f} – "
                         f"{row_min['Category']} – {row_min['Description']} "
                         f"({row_min['Date'].strftime('%Y-%m-%d')})")

        lines.append("\n" + sep)
        lines.append("                     END OF REPORT")
        lines.append(sep)

        report = "\n".join(lines)
        return report

    # ── Category analysis ────────────────────────────────────────────

    def analyze_by_category(self) -> Optional[pd.DataFrame]:
        """Analyze expenses grouped by category.

        Returns:
            DataFrame with category-wise total, mean, count, min, max,
            and spending percentage; or None if data is empty.
        """
        if self.df.empty:
            print("[INFO] No expenses to analyze.")
            return None

        cat_analysis = self.df.groupby("Category")["Amount"].agg(
            ["sum", "mean", "count", "min", "max"]
        ).rename(columns={
            "sum": "Total",
            "mean": "Average",
            "count": "Count",
            "min": "Min",
            "max": "Max",
        })

        total = self.df["Amount"].sum()
        cat_analysis["Percentage"] = (cat_analysis["Total"] / total * 100).round(2)
        cat_analysis = cat_analysis.sort_values("Total", ascending=False)

        return cat_analysis

    # ── Monthly analysis ─────────────────────────────────────────────

    def analyze_monthly(self) -> Optional[pd.DataFrame]:
        """Analyze expenses grouped by month.

        Returns:
            DataFrame with month-wise total, mean, count, min, and max;
            or None if data is empty.
        """
        if self.df.empty:
            print("[INFO] No expenses to analyze.")
            return None

        df_monthly = self.df.copy()
        df_monthly["Month"] = df_monthly["Date"].dt.to_period("M")
        monthly = df_monthly.groupby("Month")["Amount"].agg(
            ["sum", "mean", "count", "min", "max"]
        ).rename(columns={
            "sum": "Total",
            "mean": "Average",
            "count": "Count",
            "min": "Min",
            "max": "Max",
        })
        monthly = monthly.sort_index()

        return monthly

    # ── Visualization methods ────────────────────────────────────────

    def _ensure_charts_dir(self) -> None:
        """Create the charts directory if it does not exist."""
        os.makedirs(CHARTS_DIR, exist_ok=True)

    def plot_category_bar_chart(self) -> Optional[str]:
        """Chart 1: Bar chart comparing total expenses by category.

        Returns:
            Path to the saved chart image, or None if data is empty.
        """
        if self.df.empty:
            print("[INFO] No data available for bar chart.")
            return None

        self._ensure_charts_dir()
        cat_totals = self.df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=cat_totals.index, y=cat_totals.values, palette="viridis",
                    hue=cat_totals.index, legend=False, ax=ax)
        ax.set_title("Total Expenses by Category", fontsize=16, fontweight="bold")
        ax.set_xlabel("Category", fontsize=12)
        ax.set_ylabel("Total Amount (₹)", fontsize=12)
        ax.tick_params(axis="x", rotation=45)

        # Add value labels on bars
        for i, (cat, val) in enumerate(cat_totals.items()):
            ax.text(i, val + cat_totals.max() * 0.01, f"₹{val:,.0f}",
                    ha="center", va="bottom", fontsize=9)

        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, "category_expenses.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"[INFO] Bar chart saved → {path}")
        return path

    def plot_monthly_trends(self) -> Optional[str]:
        """Chart 2: Line graph showing spending trends over time.

        Returns:
            Path to the saved chart image, or None if data is empty.
        """
        if self.df.empty:
            print("[INFO] No data available for line graph.")
            return None

        self._ensure_charts_dir()
        monthly = self.df.groupby(self.df["Date"].dt.to_period("M"))["Amount"].sum()
        monthly.index = monthly.index.to_timestamp()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(monthly.index, monthly.values, marker="o", linewidth=2,
                color="royalblue", markersize=8)
        ax.fill_between(monthly.index, monthly.values, alpha=0.15, color="royalblue")
        ax.set_title("Monthly Spending Trends", fontsize=16, fontweight="bold")
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Total Amount (₹)", fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.7)

        # Format x-axis dates
        fig.autofmt_xdate()

        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, "monthly_trends.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"[INFO] Line graph saved → {path}")
        return path

    def plot_category_pie_chart(self) -> Optional[str]:
        """Chart 3: Pie chart showing spending distribution by category.

        Returns:
            Path to the saved chart image, or None if data is empty.
        """
        if self.df.empty:
            print("[INFO] No data available for pie chart.")
            return None

        total = self.df["Amount"].sum()
        if total == 0:
            print("[INFO] Total expenses are zero – cannot generate pie chart.")
            return None

        self._ensure_charts_dir()
        cat_totals = self.df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(8, 8))
        colors = sns.color_palette("Set2", n_colors=len(cat_totals))
        wedges, texts, autotexts = ax.pie(
            cat_totals.values,
            labels=cat_totals.index,
            autopct="%1.1f%%",
            colors=colors,
            startangle=140,
            pctdistance=0.85,
        )
        for autotext in autotexts:
            autotext.set_fontsize(9)
        ax.set_title("Spending Distribution by Category",
                      fontsize=16, fontweight="bold")
        plt.tight_layout()

        path = os.path.join(CHARTS_DIR, "category_distribution.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"[INFO] Pie chart saved → {path}")
        return path

    def plot_expense_histogram(self) -> Optional[str]:
        """Chart 4: Histogram showing frequency distribution of amounts.

        Returns:
            Path to the saved chart image, or None if data is empty.
        """
        if self.df.empty:
            print("[INFO] No data available for histogram.")
            return None

        self._ensure_charts_dir()
        amounts = self.df["Amount"].values

        fig, ax = plt.subplots(figsize=(10, 6))
        # Use Seaborn for the histogram with KDE
        sns.histplot(amounts, bins=20, kde=True, color="teal", ax=ax,
                     edgecolor="white", linewidth=0.5)
        ax.set_title("Expense Amount Distribution", fontsize=16, fontweight="bold")
        ax.set_xlabel("Amount (₹)", fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.grid(True, axis="y", linestyle="--", alpha=0.7)

        plt.tight_layout()
        path = os.path.join(CHARTS_DIR, "expense_histogram.png")
        fig.savefig(path, dpi=150)
        plt.close(fig)
        print(f"[INFO] Histogram saved → {path}")
        return path

    def generate_all_charts(self) -> List[str]:
        """Generate all four visualizations.

        Returns:
            List of paths to the saved chart images.
        """
        print("\n── Generating Visualizations ──────────────────────────")
        paths: List[str] = []
        for generator in [
            self.plot_category_bar_chart,
            self.plot_monthly_trends,
            self.plot_category_pie_chart,
            self.plot_expense_histogram,
        ]:
            path = generator()
            if path:
                paths.append(path)
        if paths:
            print(f"\n[INFO] {len(paths)} chart(s) saved to '{CHARTS_DIR}'.")
        else:
            print("[INFO] No charts were generated (dataset may be empty).")
        return paths


# ──────────────────────────── CLI MENU FUNCTIONS ───────────────────

def display_menu() -> None:
    """Display the main application menu."""
    print("\n" + "=" * 45)
    print("        SMART EXPENSE TRACKER")
    print("=" * 45)
    print("  1. Add New Expense")
    print("  2. View All Expenses")
    print("  3. View Expense Summary")
    print("  4. Filter Expenses")
    print("  5. Analyze Expenses by Category")
    print("  6. Analyze Monthly Spending")
    print("  7. Generate Financial Report")
    print("  8. Visualize Expenses")
    print("  9. View Available Categories")
    print(" 10. Exit")
    print("=" * 45)


def menu_add_expense(tracker: ExpenseTracker) -> None:
    """Handle the 'Add New Expense' menu option.

    Collects user input with validation and re-prompting for each field.
    The user can type 'cancel' at any point to abort.
    """
    print("\n── Add New Expense ────────────────────────────────────")
    print("  (Type 'cancel' at any prompt to abort.)\n")

    # Date
    while True:
        date_input = input("  Date (YYYY-MM-DD): ").strip()
        if date_input.lower() == "cancel":
            print("  [CANCELLED] Operation aborted.")
            return
        if validate_date(date_input):
            break
        print("  [INVALID] Please enter a valid date in YYYY-MM-DD format.\n")

    # Amount
    while True:
        amount_input = input("  Amount: ").strip()
        if amount_input.lower() == "cancel":
            print("  [CANCELLED] Operation aborted.")
            return
        validated = validate_amount(amount_input)
        if validated is not None:
            break
        print("  [INVALID] Please enter a positive numeric amount.\n")

    # Category
    while True:
        cat_input = input(f"  Category {CATEGORIES}: ").strip()
        if cat_input.lower() == "cancel":
            print("  [CANCELLED] Operation aborted.")
            return
        if normalize_category(cat_input):
            break
        print(f"  [INVALID] Choose from: {', '.join(CATEGORIES)}\n")

    # Description
    while True:
        desc_input = input("  Description: ").strip()
        if desc_input.lower() == "cancel":
            print("  [CANCELLED] Operation aborted.")
            return
        if desc_input:
            break
        print("  [INVALID] Description cannot be empty.\n")

    tracker.add_expense(date_input, float(amount_input), cat_input, desc_input)


def menu_view_all(tracker: ExpenseTracker) -> None:
    """Display all expenses in a readable tabular format."""
    print("\n── All Expenses ───────────────────────────────────────")
    if tracker.df.empty:
        print("  No expenses recorded yet.")
        return

    display_df = tracker.df.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    display_df.index = range(1, len(display_df) + 1)
    display_df.index.name = "#"
    print(display_df.to_string())
    print(f"\n  Total records: {len(display_df)}")


def menu_view_summary(tracker: ExpenseTracker) -> None:
    """Display the expense summary."""
    print("\n── Expense Summary ────────────────────────────────────")
    summary = tracker.get_summary()

    if summary["count"] == 0:
        print("  No expenses recorded yet.")
        return

    print(f"  Total Expenses     : ₹{summary['total']:>12,.2f}")
    print(f"  Average Expense    : ₹{summary['average']:>12,.2f}")
    print(f"  Median Expense     : ₹{summary['median']:>12,.2f}")
    print(f"  Std. Deviation     : ₹{summary['std_dev']:>12,.2f}")
    print(f"  Number of Records  : {summary['count']:>13,}")
    print(f"  Highest Expense    : ₹{summary['max']:>12,.2f}")
    print(f"  Lowest Expense     : ₹{summary['min']:>12,.2f}")
    print(f"  Top Category       : {summary['top_category']}")

    print("\n  Category Spending:")
    for cat, total in summary["category_totals"].items():
        pct = summary["category_percentages"].get(cat, 0)
        print(f"    {cat:<15} ₹{total:>10,.2f}  ({pct:.1f}%)")


def menu_filter_expenses(tracker: ExpenseTracker) -> None:
    """Handle the 'Filter Expenses' menu option."""
    print("\n── Filter Expenses ────────────────────────────────────")
    print("  (Leave blank to skip a filter.)\n")

    condition: Dict[str, Any] = {}

    cat = input("  Category: ").strip()
    if cat:
        condition["category"] = cat

    start = input("  Start date (YYYY-MM-DD): ").strip()
    if start:
        condition["start_date"] = start

    end = input("  End date (YYYY-MM-DD): ").strip()
    if end:
        condition["end_date"] = end

    min_amt = input("  Minimum amount: ").strip()
    if min_amt:
        condition["min_amount"] = min_amt

    max_amt = input("  Maximum amount: ").strip()
    if max_amt:
        condition["max_amount"] = max_amt

    if not condition:
        print("  [INFO] No filters applied – showing all records.")
        menu_view_all(tracker)
        return

    result = tracker.filter_expenses(condition)
    if result.empty:
        print("  [INFO] No expenses match the given filters.")
    else:
        display_df = result.copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
        display_df.index = range(1, len(display_df) + 1)
        display_df.index.name = "#"
        print(f"\n  Found {len(result)} matching record(s):\n")
        print(display_df.to_string())


def menu_category_analysis(tracker: ExpenseTracker) -> None:
    """Handle the 'Analyze by Category' menu option."""
    print("\n── Category-wise Expense Analysis ─────────────────────")
    analysis = tracker.analyze_by_category()
    if analysis is not None:
        # Format for display
        display = analysis.copy()
        display["Total"] = display["Total"].map("₹{:,.2f}".format)
        display["Average"] = display["Average"].map("₹{:,.2f}".format)
        display["Min"] = display["Min"].map("₹{:,.2f}".format)
        display["Max"] = display["Max"].map("₹{:,.2f}".format)
        display["Percentage"] = display["Percentage"].map("{:.1f}%".format)
        print(display.to_string())


def menu_monthly_analysis(tracker: ExpenseTracker) -> None:
    """Handle the 'Analyze Monthly Spending' menu option."""
    print("\n── Monthly Spending Analysis ──────────────────────────")
    analysis = tracker.analyze_monthly()
    if analysis is not None:
        display = analysis.copy()
        display["Total"] = display["Total"].map("₹{:,.2f}".format)
        display["Average"] = display["Average"].map("₹{:,.2f}".format)
        display["Min"] = display["Min"].map("₹{:,.2f}".format)
        display["Max"] = display["Max"].map("₹{:,.2f}".format)
        print(display.to_string())


def menu_generate_report(tracker: ExpenseTracker) -> None:
    """Handle the 'Generate Report' menu option."""
    report = tracker.generate_report()
    print("\n" + report)

    # Optionally export to file
    try:
        report_path = os.path.join(BASE_DIR, "financial_report.txt")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n[INFO] Report also saved to → {report_path}")
    except OSError as e:
        print(f"[WARNING] Could not save report file: {e}")


def menu_visualize(tracker: ExpenseTracker) -> None:
    """Handle the 'Visualize Expenses' menu option."""
    if tracker.df.empty:
        print("\n[INFO] No expenses to visualize.")
        return

    tracker.generate_all_charts()

    # Try to display charts interactively
    try:
        matplotlib.use("TkAgg")
        chart_files = [
            os.path.join(CHARTS_DIR, f)
            for f in ["category_expenses.png", "monthly_trends.png",
                       "category_distribution.png", "expense_histogram.png"]
            if os.path.exists(os.path.join(CHARTS_DIR, f))
        ]
        if chart_files:
            print("\n[INFO] Attempting to display charts...")
            for chart_path in chart_files:
                img = plt.imread(chart_path)
                fig, ax = plt.subplots(figsize=(10, 7))
                ax.imshow(img)
                ax.axis("off")
                fig.suptitle(os.path.basename(chart_path), fontsize=12)
                plt.show()
                plt.close(fig)
    except Exception:
        print("[INFO] Charts saved to the 'charts/' folder. "
              "Open them manually to view.")
    finally:
        matplotlib.use("Agg")  # Reset to non-interactive


def menu_view_categories() -> None:
    """Display the list of available expense categories."""
    print("\n── Available Expense Categories ────────────────────────")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i:>2}. {cat}")


# ──────────────────────────── MAIN ENTRY POINT ─────────────────────

def main() -> None:
    """Main application loop for the Smart Expense Tracker CLI."""
    print("\n" + "=" * 45)
    print("  Welcome to the Smart Expense Tracker!")
    print("=" * 45)

    tracker = ExpenseTracker()

    while True:
        display_menu()
        choice = input("\n  Enter your choice (1-10): ").strip()

        if choice == "1":
            menu_add_expense(tracker)
        elif choice == "2":
            menu_view_all(tracker)
        elif choice == "3":
            menu_view_summary(tracker)
        elif choice == "4":
            menu_filter_expenses(tracker)
        elif choice == "5":
            menu_category_analysis(tracker)
        elif choice == "6":
            menu_monthly_analysis(tracker)
        elif choice == "7":
            menu_generate_report(tracker)
        elif choice == "8":
            menu_visualize(tracker)
        elif choice == "9":
            menu_view_categories()
        elif choice == "10":
            print("\n  Thank you for using Smart Expense Tracker!")
            print("  Goodbye!\n")
            break
        else:
            print("\n  [INVALID] Please enter a number between 1 and 10.")


if __name__ == "__main__":
    main()
