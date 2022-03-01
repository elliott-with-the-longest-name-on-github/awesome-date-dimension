import unittest

from awesome_date_dimension.config import FiscalConfig


class TestFiscalConfig(unittest.TestCase):
    def test_fiscal_date_range_fails_over_28(self):
        with self.assertRaises(AssertionError):
            FiscalConfig(month_start_day=29)

    def test_fiscal_date_range_succeeds_1_thru_28(self):
        for i in range(1, 29):
            FiscalConfig(month_start_day=i)

    def test_fiscal_date_range_fails_under_1(self):
        with self.assertRaises(AssertionError):
            FiscalConfig(month_start_day=0)

    def test_fiscal_month_range_fails_over_12(self):
        with self.assertRaises(AssertionError):
            FiscalConfig(year_start_month=13)

    def test_fiscal_month_range_succeeds_1_thru_12(self):
        for i in range(1, 13):
            FiscalConfig(year_start_month=i)

    def test_fiscal_month_range_fails_under_1(self):
        with self.assertRaises(AssertionError):
            FiscalConfig(year_start_month=0)

    def test_defaults_are_immutable(self):
        default_config = FiscalConfig()
        self.assertEqual(default_config.month_start_day, 1)
        self.assertEqual(default_config.year_start_month, 1)
        self.assertTrue(default_config.month_end_matches_calendar)
        self.assertTrue(default_config.quarter_end_matches_calendar)
        self.assertTrue(default_config.year_end_matches_calendar)


if __name__ == "main":
    unittest.main()
