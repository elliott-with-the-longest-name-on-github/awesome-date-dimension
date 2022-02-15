import pickle
import unittest

from awesome_date_dimension.config import HolidayConfig, default_company_holidays


class TestHolidayConfig(unittest.TestCase):
    def test_failure_when_hol_types_and_hols_tables_have_same_name(self):
        with self.assertRaises(AssertionError):
            HolidayConfig(holiday_types_table_name="dupe", holidays_table_name="dupe")

    def test_failure_with_duplicate_holtypes(self):
        with self.assertRaises(AssertionError):
            HolidayConfig(
                holiday_calendars=[
                    default_company_holidays(),
                    default_company_holidays(),
                ]
            )

    def test_defaults_are_immutable(self):
        with open("./tests/files/default_holiday_config.pickle", "rb") as file:
            saved_default_hconfig = pickle.load(file)

        self.assertEqual(HolidayConfig(), saved_default_hconfig)


if __name__ == "main":
    unittest.main()
