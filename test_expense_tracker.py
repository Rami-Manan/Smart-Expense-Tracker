"""
Automated test suite for the Smart Expense Tracker application.

Uses Python's unittest framework with temporary directories so that
the actual expenses.csv dataset is never modified during testing.
"""

import os
import sys
import csv
import shutil
import tempfile
import unittest
from datetime import datetime

import numpy as np
import pandas as pd

# Ensure the parent directory is on sys.path so we can import the tracker
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from expense_tracker import (
    ExpenseTracker,
    validate_date,
    validate_amount,
    normalize_category,
    generate_sample_data,
    CATEGORIES,
    CSV_COLUMNS,
)


class TestValidationFunctions(unittest.TestCase):
    """Tests for standalone validation helper functions."""

    # ── Date validation ──────────────────────────────────────────────

    def test_valid_date(self):
        self.assertEqual(validate_date("2026-01-15"), "2026-01-15")

    def test_valid_date_with_whitespace(self):
        self.assertEqual(validate_date("  2026-06-01  "), "2026-06-01")

    def test_invalid_date_format(self):
        self.assertIsNone(validate_date("15-01-2026"))

    def test_invalid_date_impossible(self):
        """Feb 30 doesn't exist."""
        self.assertIsNone(validate_date("2026-02-30"))

    def test_invalid_date_month_out_of_range(self):
        self.assertIsNone(validate_date("2026-13-01"))

    def test_invalid_date_empty(self):
        self.assertIsNone(validate_date(""))

    def test_invalid_date_letters(self):
        self.assertIsNone(validate_date("not-a-date"))

    # ── Amount validation ────────────────────────────────────────────

    def test_valid_amount(self):
        self.assertEqual(validate_amount("150.50"), 150.50)

    def test_valid_amount_integer(self):
        self.assertEqual(validate_amount("200"), 200.0)

    def test_invalid_amount_zero(self):
        self.assertIsNone(validate_amount("0"))

    def test_invalid_amount_negative(self):
        self.assertIsNone(validate_amount("-50"))

    def test_invalid_amount_nan(self):
        self.assertIsNone(validate_amount("nan"))

    def test_invalid_amount_inf(self):
        self.assertIsNone(validate_amount("inf"))

    def test_invalid_amount_neg_inf(self):
        self.assertIsNone(validate_amount("-inf"))

    def test_invalid_amount_letters(self):
        self.assertIsNone(validate_amount("abc"))

    def test_invalid_amount_empty(self):
        self.assertIsNone(validate_amount(""))

    # ── Category validation ──────────────────────────────────────────

    def test_valid_category(self):
        self.assertEqual(normalize_category("Food"), "Food")

    def test_valid_category_case_insensitive(self):
        self.assertEqual(normalize_category("food"), "Food")
        self.assertEqual(normalize_category("TRANSPORT"), "Transport")
        self.assertEqual(normalize_category("hEaLtHcArE"), "Healthcare")

    def test_valid_category_with_whitespace(self):
        self.assertEqual(normalize_category("  entertainment  "), "Entertainment")

    def test_invalid_category(self):
        self.assertIsNone(normalize_category("Gambling"))

    def test_invalid_category_empty(self):
        self.assertIsNone(normalize_category(""))


class TestExpenseTracker(unittest.TestCase):
    """Tests for the ExpenseTracker class using a temporary CSV file."""

    def setUp(self):
        """Create a temp directory and a known CSV for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.test_dir, "test_expenses.csv")

        # Write a small known dataset
        self.sample_data = [
            ["2026-01-10", "500.00", "Food", "Grocery shopping"],
            ["2026-01-15", "1200.50", "Transport", "Monthly bus pass"],
            ["2026-02-01", "300.00", "Food", "Restaurant lunch"],
            ["2026-02-10", "2500.00", "Housing", "Monthly rent"],
            ["2026-03-05", "150.75", "Entertainment", "Movie tickets"],
        ]
        with open(self.test_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
            writer.writerows(self.sample_data)

        self.tracker = ExpenseTracker(filepath=self.test_csv)

    def tearDown(self):
        """Clean up temp directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # ── Add expense tests ────────────────────────────────────────────

    def test_add_valid_expense(self):
        """Adding a valid expense should succeed and increase record count."""
        initial_count = len(self.tracker.df)
        result = self.tracker.add_expense(
            "2026-04-01", 750.00, "Shopping", "New shoes"
        )
        self.assertTrue(result)
        self.assertEqual(len(self.tracker.df), initial_count + 1)

    def test_add_expense_persists_to_csv(self):
        """New expenses should be persisted to the CSV file."""
        self.tracker.add_expense("2026-04-15", 100.00, "Food", "Snacks")
        # Reload from CSV and verify
        new_tracker = ExpenseTracker(filepath=self.test_csv)
        self.assertEqual(len(new_tracker.df), len(self.sample_data) + 1)

    def test_add_expense_invalid_date(self):
        result = self.tracker.add_expense(
            "2026-02-30", 100.00, "Food", "Invalid date"
        )
        self.assertFalse(result)

    def test_add_expense_invalid_amount_zero(self):
        result = self.tracker.add_expense(
            "2026-04-01", 0, "Food", "Zero amount"
        )
        self.assertFalse(result)

    def test_add_expense_invalid_amount_negative(self):
        result = self.tracker.add_expense(
            "2026-04-01", -50, "Food", "Negative amount"
        )
        self.assertFalse(result)

    def test_add_expense_invalid_category(self):
        result = self.tracker.add_expense(
            "2026-04-01", 100.00, "Gambling", "Invalid category"
        )
        self.assertFalse(result)

    def test_add_expense_empty_description(self):
        result = self.tracker.add_expense(
            "2026-04-01", 100.00, "Food", ""
        )
        self.assertFalse(result)

    def test_add_expense_whitespace_description(self):
        result = self.tracker.add_expense(
            "2026-04-01", 100.00, "Food", "   "
        )
        self.assertFalse(result)

    # ── Summary tests ────────────────────────────────────────────────

    def test_summary_total(self):
        summary = self.tracker.get_summary()
        expected_total = sum(float(row[1]) for row in self.sample_data)
        self.assertAlmostEqual(summary["total"], expected_total, places=2)

    def test_summary_count(self):
        summary = self.tracker.get_summary()
        self.assertEqual(summary["count"], len(self.sample_data))

    def test_summary_average(self):
        summary = self.tracker.get_summary()
        expected_avg = sum(float(row[1]) for row in self.sample_data) / len(self.sample_data)
        self.assertAlmostEqual(summary["average"], expected_avg, places=2)

    def test_summary_max(self):
        summary = self.tracker.get_summary()
        expected_max = max(float(row[1]) for row in self.sample_data)
        self.assertAlmostEqual(summary["max"], expected_max, places=2)

    def test_summary_min(self):
        summary = self.tracker.get_summary()
        expected_min = min(float(row[1]) for row in self.sample_data)
        self.assertAlmostEqual(summary["min"], expected_min, places=2)

    def test_summary_category_totals(self):
        summary = self.tracker.get_summary()
        # Food total = 500.00 + 300.00 = 800.00
        self.assertAlmostEqual(summary["category_totals"]["Food"], 800.00, places=2)

    def test_summary_category_percentages_sum_to_100(self):
        summary = self.tracker.get_summary()
        total_pct = sum(summary["category_percentages"].values())
        self.assertAlmostEqual(total_pct, 100.0, places=1)

    def test_summary_top_category(self):
        summary = self.tracker.get_summary()
        # Housing has the highest single expense (2500)
        self.assertEqual(summary["top_category"], "Housing")

    # ── Filter tests ─────────────────────────────────────────────────

    def test_filter_by_category(self):
        result = self.tracker.filter_expenses({"category": "Food"})
        self.assertEqual(len(result), 2)
        self.assertTrue((result["Category"] == "Food").all())

    def test_filter_by_category_case_insensitive(self):
        result = self.tracker.filter_expenses({"category": "food"})
        self.assertEqual(len(result), 2)

    def test_filter_by_date_range(self):
        result = self.tracker.filter_expenses({
            "start_date": "2026-01-15",
            "end_date": "2026-02-15",
        })
        self.assertEqual(len(result), 3)

    def test_filter_by_min_amount(self):
        result = self.tracker.filter_expenses({"min_amount": 1000})
        self.assertEqual(len(result), 2)  # 1200.50 and 2500.00

    def test_filter_by_max_amount(self):
        result = self.tracker.filter_expenses({"max_amount": 500})
        self.assertEqual(len(result), 3)  # 500, 300, 150.75

    def test_filter_combined(self):
        result = self.tracker.filter_expenses({
            "category": "Food",
            "min_amount": 400,
        })
        self.assertEqual(len(result), 1)  # Only the 500.00 Food entry

    def test_filter_no_match(self):
        result = self.tracker.filter_expenses({"category": "Travel"})
        self.assertEqual(len(result), 0)

    def test_filter_does_not_modify_original(self):
        original_len = len(self.tracker.df)
        _ = self.tracker.filter_expenses({"category": "Food"})
        self.assertEqual(len(self.tracker.df), original_len)

    # ── Report tests ─────────────────────────────────────────────────

    def test_generate_report_returns_string(self):
        report = self.tracker.generate_report()
        self.assertIsInstance(report, str)
        self.assertIn("FINANCIAL REPORT", report)

    def test_generate_report_contains_statistics(self):
        report = self.tracker.generate_report()
        self.assertIn("Total Expenses", report)
        self.assertIn("Average Expense", report)
        self.assertIn("CATEGORY-WISE SPENDING", report)
        self.assertIn("MONTHLY SPENDING", report)

    # ── Category analysis tests ──────────────────────────────────────

    def test_analyze_by_category(self):
        analysis = self.tracker.analyze_by_category()
        self.assertIsNotNone(analysis)
        self.assertIn("Food", analysis.index)
        self.assertIn("Total", analysis.columns)
        self.assertIn("Percentage", analysis.columns)

    # ── Monthly analysis tests ───────────────────────────────────────

    def test_analyze_monthly(self):
        analysis = self.tracker.analyze_monthly()
        self.assertIsNotNone(analysis)
        self.assertIn("Total", analysis.columns)
        self.assertIn("Count", analysis.columns)


class TestEmptyDataset(unittest.TestCase):
    """Tests for edge cases with an empty dataset."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.test_dir, "empty_expenses.csv")

        # Write only headers
        with open(self.test_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)

        self.tracker = ExpenseTracker(filepath=self.test_csv)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_empty_dataset_is_empty(self):
        self.assertTrue(self.tracker.df.empty)

    def test_summary_on_empty_dataset(self):
        summary = self.tracker.get_summary()
        self.assertEqual(summary["total"], 0.0)
        self.assertEqual(summary["count"], 0)
        self.assertEqual(summary["average"], 0.0)

    def test_filter_on_empty_dataset(self):
        result = self.tracker.filter_expenses({"category": "Food"})
        self.assertTrue(result.empty)

    def test_report_on_empty_dataset(self):
        report = self.tracker.generate_report()
        self.assertIsInstance(report, str)

    def test_analyze_by_category_empty(self):
        result = self.tracker.analyze_by_category()
        self.assertIsNone(result)

    def test_analyze_monthly_empty(self):
        result = self.tracker.analyze_monthly()
        self.assertIsNone(result)

    def test_add_to_empty_then_verify(self):
        result = self.tracker.add_expense(
            "2026-05-01", 200.00, "Food", "Test expense"
        )
        self.assertTrue(result)
        self.assertEqual(len(self.tracker.df), 1)


class TestMissingCSV(unittest.TestCase):
    """Test behavior when the CSV file does not exist."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.test_dir, "nonexistent.csv")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_missing_csv_generates_sample(self):
        """When the CSV doesn't exist, sample data should be generated."""
        tracker = ExpenseTracker(filepath=self.test_csv)
        self.assertFalse(tracker.df.empty)
        self.assertTrue(os.path.exists(self.test_csv))


class TestMalformedCSV(unittest.TestCase):
    """Test handling of malformed CSV data."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.test_dir, "malformed_expenses.csv")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_invalid_dates_removed(self):
        """Rows with invalid dates should be cleaned out."""
        with open(self.test_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
            writer.writerow(["2026-01-10", "500", "Food", "Valid"])
            writer.writerow(["invalid-date", "300", "Food", "Bad date"])
            writer.writerow(["2026-02-30", "200", "Food", "Impossible date"])

        tracker = ExpenseTracker(filepath=self.test_csv)
        self.assertEqual(len(tracker.df), 1)

    def test_invalid_amounts_removed(self):
        """Rows with invalid amounts should be cleaned out."""
        with open(self.test_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
            writer.writerow(["2026-01-10", "500", "Food", "Valid"])
            writer.writerow(["2026-01-11", "-100", "Food", "Negative"])
            writer.writerow(["2026-01-12", "abc", "Food", "Non-numeric"])
            writer.writerow(["2026-01-13", "0", "Food", "Zero"])

        tracker = ExpenseTracker(filepath=self.test_csv)
        self.assertEqual(len(tracker.df), 1)

    def test_invalid_categories_removed(self):
        """Rows with invalid categories should be cleaned out."""
        with open(self.test_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
            writer.writerow(["2026-01-10", "500", "Food", "Valid"])
            writer.writerow(["2026-01-11", "300", "Gambling", "Bad cat"])

        tracker = ExpenseTracker(filepath=self.test_csv)
        self.assertEqual(len(tracker.df), 1)


class TestChartGeneration(unittest.TestCase):
    """Test that chart generation methods run without errors."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.test_dir, "chart_expenses.csv")

        # Create a small dataset
        with open(self.test_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
            writer.writerow(["2026-01-10", "500", "Food", "Grocery"])
            writer.writerow(["2026-01-15", "1200", "Transport", "Bus pass"])
            writer.writerow(["2026-02-01", "300", "Entertainment", "Movie"])
            writer.writerow(["2026-02-10", "2500", "Housing", "Rent"])
            writer.writerow(["2026-03-05", "150", "Shopping", "Clothes"])

        # Override CHARTS_DIR for this test
        import expense_tracker as et
        self._orig_charts_dir = et.CHARTS_DIR
        et.CHARTS_DIR = os.path.join(self.test_dir, "charts")
        os.makedirs(et.CHARTS_DIR, exist_ok=True)

        self.tracker = ExpenseTracker(filepath=self.test_csv)

    def tearDown(self):
        import expense_tracker as et
        et.CHARTS_DIR = self._orig_charts_dir
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_bar_chart_generation(self):
        path = self.tracker.plot_category_bar_chart()
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))

    def test_line_graph_generation(self):
        path = self.tracker.plot_monthly_trends()
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))

    def test_pie_chart_generation(self):
        path = self.tracker.plot_category_pie_chart()
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))

    def test_histogram_generation(self):
        path = self.tracker.plot_expense_histogram()
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))

    def test_generate_all_charts(self):
        paths = self.tracker.generate_all_charts()
        self.assertEqual(len(paths), 4)


class TestNumPyIntegration(unittest.TestCase):
    """Verify that NumPy calculations match expected values."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.test_csv = os.path.join(self.test_dir, "numpy_expenses.csv")

        self.amounts = [100.0, 200.0, 300.0, 400.0, 500.0]
        with open(self.test_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)
            for i, amt in enumerate(self.amounts):
                writer.writerow([f"2026-01-{10+i:02d}", str(amt), "Food",
                                 f"Expense {i+1}"])

        self.tracker = ExpenseTracker(filepath=self.test_csv)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_numpy_total(self):
        summary = self.tracker.get_summary()
        self.assertAlmostEqual(summary["total"], np.sum(self.amounts), places=2)

    def test_numpy_mean(self):
        summary = self.tracker.get_summary()
        self.assertAlmostEqual(summary["average"], np.mean(self.amounts), places=2)

    def test_numpy_median(self):
        summary = self.tracker.get_summary()
        self.assertAlmostEqual(summary["median"], np.median(self.amounts), places=2)

    def test_numpy_std(self):
        summary = self.tracker.get_summary()
        self.assertAlmostEqual(summary["std_dev"], np.std(self.amounts, ddof=1), places=2)

    def test_numpy_max(self):
        summary = self.tracker.get_summary()
        self.assertAlmostEqual(summary["max"], np.max(self.amounts), places=2)

    def test_numpy_min(self):
        summary = self.tracker.get_summary()
        self.assertAlmostEqual(summary["min"], np.min(self.amounts), places=2)


if __name__ == "__main__":
    unittest.main()
