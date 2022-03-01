import pickle
import unittest

from awesome_date_dimension.config import Column, HolidayTypesColumns


class TestHolidayTypesColumns(unittest.TestCase):
    def test_failure_when_one_or_more_columns_are_excluded(self):
        with self.assertRaises(AssertionError):
            HolidayTypesColumns(holiday_type_key=Column("HolidayTypeKey", False, 1000))
        with self.assertRaises(AssertionError):
            HolidayTypesColumns(
                holiday_type_name=Column("HolidayTypeName", False, 2000)
            )

    def test_failure_when_duplicate_colnames(self):
        with self.assertRaises(AssertionError):
            HolidayTypesColumns(Column("Dupe", True, 1000), Column("Dupe", True, 2000))

    def test_failure_when_duplicate_sortkeys(self):
        with self.assertRaises(AssertionError):
            HolidayTypesColumns(
                Column("HolidayTypeKey", True, 1000),
                Column("HolidayTypeName", True, 1000),
            )

    def test_defaults_are_immutable(self):
        with open("./tests/files/default_holiday_types_columns.pickle", "rb") as file:
            saved_defaults = pickle.load(file)

        self.assertEqual(HolidayTypesColumns(), saved_defaults)


if __name__ == "main":
    unittest.main()
