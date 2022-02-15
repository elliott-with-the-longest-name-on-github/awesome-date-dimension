import pickle
import unittest

from awesome_date_dimension.config import Column, HolidaysColumns


class TestHolidaysColumns(unittest.TestCase):
    def test_failure_when_one_or_more_columns_are_excluded(self):
        with self.assertRaises(AssertionError):
            HolidaysColumns(date_key=Column("DateKey", False, 1000))
        with self.assertRaises(AssertionError):
            HolidaysColumns(holiday_name=Column("HolidayName", False, 2000))
        with self.assertRaises(AssertionError):
            HolidaysColumns(
                Column("DateKey", False, 1000), Column("HolidayName", False, 2000)
            )

    def test_failure_when_duplicate_colnames(self):
        with self.assertRaises(AssertionError):
            HolidaysColumns(Column("Dupe", True, 1000), Column("Dupe", True, 2000))

    def test_failure_when_duplicate_sortkeys(self):
        with self.assertRaises(AssertionError):
            HolidaysColumns(
                Column("DateKey", True, 1000),
                Column("HolidayName", True, 1000),
            )

    def test_defaults_are_immutable(self):
        with open("./tests/files/default_holidays_columns.pickle", "rb") as file:
            saved_defaults = pickle.load(file)

        self.assertEqual(HolidaysColumns(), saved_defaults)


if __name__ == "main":
    unittest.main()
