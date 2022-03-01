import pickle
import unittest
from datetime import datetime
from typing import Callable

from awesome_date_dimension.config import (
    Holiday,
    HolidayCalendar,
    HolidayType,
    default_company_holidays,
    default_us_public_holidays,
)


# Default holidays are pickled. The default holidays when using the default_holidays functions from
class TestHolidayCalendars(unittest.TestCase):
    def test_failure_on_duplicate_holidays_within_calendar(self):
        nyd = datetime.fromisoformat("2021-01-01").date()
        with self.assertRaises(AssertionError):
            HolidayCalendar(
                HolidayType(
                    "Anything can be a holiday if you want it to be!", "AnythingHoliday"
                ),
                [Holiday("New Year's Day", nyd), Holiday("New Year's Day", nyd)],
            )

    def test_failure_on_holidays_with_same_date_within_calendar(self):
        xmas = datetime.fromisoformat("2021-12-25").date()
        with self.assertRaises(AssertionError):
            HolidayCalendar(
                HolidayType("Ho HO HOHOHOHO", "HoHoliday"),
                [
                    Holiday("Christmas", xmas),
                    Holiday("DayBeforeChristmasWrongDay", xmas),
                ],
            )

    def test_default_company_holidays(self):
        self.generic_default_holidays_test(
            "./tests/files/default_company_holidays.pickle", default_company_holidays
        )

    def test_default_us_public_holidays(self):
        self.generic_default_holidays_test(
            "./tests/files/default_us_public_holidays.pickle",
            default_us_public_holidays,
        )

    def generic_default_holidays_test(
        self, pickle_path: str, default_holiday_func: Callable[[], HolidayCalendar]
    ):
        with open(pickle_path, "rb") as file:
            saved_default_holidays = pickle.load(file)

        default = default_holiday_func()

        self.assertEqual(saved_default_holidays.holiday_type, default.holiday_type)
        for i, h in enumerate(default.holidays):
            saved_h = saved_default_holidays.holidays[i]
            with self.subTest(f"{h.holiday_name} equals {saved_h.holiday_name}"):
                self.assertEqual(saved_h, h)


if __name__ == "main":
    unittest.main()
