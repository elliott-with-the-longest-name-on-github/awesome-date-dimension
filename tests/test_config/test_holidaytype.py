import unittest

from awesome_date_dimension.config import HolidayType


class TestHolidayType(unittest.TestCase):
    def test_defaults_are_immutable(self):
        holiday_name = "Everyday's a holiday if you're optimistic enough"
        holiday_prefix = "EverydayHoliday"
        default_holiday_type = HolidayType(holiday_name, holiday_prefix)
        self.assertEqual(default_holiday_type.name, holiday_name)
        self.assertEqual(default_holiday_type.generated_column_prefix, holiday_prefix)
        self.assertEqual(
            default_holiday_type.generated_flag_column_postfix, "HolidayFlag"
        )
        self.assertEqual(
            default_holiday_type.generated_name_column_postfix, "HolidayName"
        )
        self.assertEqual(
            default_holiday_type.generated_monthly_count_column_postfix,
            "HolidaysInMonth",
        )
        self.assertFalse(default_holiday_type.included_in_business_day_calc)


if __name__ == "main":
    unittest.main()
