import pickle
import unittest

from awesome_date_dimension.config import Column, DimFiscalMonthColumns


class TestDimFiscalMonthColumns(unittest.TestCase):
    def test_failure_when_start_key_column_is_excluded(self):
        with self.assertRaises(AssertionError):
            DimFiscalMonthColumns(month_start_key=Column("MonthStartKey", False, 1000))

    def test_failure_when_end_key_column_is_excluded(self):
        with self.assertRaises(AssertionError):
            DimFiscalMonthColumns(month_end_key=Column("MonthEndKey", False, 1000))

    def test_failure_when_duplicate_colnames(self):
        with self.assertRaises(AssertionError):
            DimFiscalMonthColumns(
                Column("Dupe", True, 1000), Column("Dupe", True, 2000)
            )

    def test_failure_when_duplicate_sortkeys(self):
        with self.assertRaises(AssertionError):
            DimFiscalMonthColumns(
                Column("DateKey", True, 1000),
                Column("SomethingElse", True, 1000),
            )

    def test_defaults_are_immutable(self):
        with open(
            "./tests/files/default_dim_fiscal_month_columns.pickle", "rb"
        ) as file:
            saved_defaults = pickle.load(file)

        self.assertEqual(DimFiscalMonthColumns(), saved_defaults)


if __name__ == "main":
    unittest.main()
