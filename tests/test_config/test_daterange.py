import unittest
from datetime import datetime

from awesome_date_dimension.config import DateRange


class TestDateRange(unittest.TestCase):
    def test_failure_when_less_than_0_years(self):
        with self.assertRaises(AssertionError):
            DateRange(datetime.fromisoformat("2000-01-01").date(), -1)

    def test_failure_when_0_years(self):
        with self.assertRaises(AssertionError):
            DateRange(datetime.fromisoformat("2000-01-01").date(), 0)

    def test_defaults(self):
        default_range = DateRange()
        self.assertEqual(
            default_range.start_date, datetime.fromisoformat("2000-01-01").date()
        )
        self.assertEqual(default_range.num_years, 100)


if __name__ == "main":
    unittest.main()
