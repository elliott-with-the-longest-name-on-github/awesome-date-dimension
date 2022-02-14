from dataclasses import asdict, dataclass, field
from datetime import date, datetime, tzinfo
from pathlib import Path
from typing import Callable

from pytz import timezone


@dataclass(frozen=True)
class DateRange:
    start_date: date = field(
        default_factory=lambda: datetime.fromisoformat("2000-01-01").date()
    )
    num_years: int = 100

    def __post_init__(self):
        assert self.num_years > 0, "num_years must be greater than 0."


@dataclass(frozen=True)
class FiscalConfig:
    month_start_day: int = 1
    year_start_month: int = 1
    month_end_matches_calendar: bool = True
    quarter_end_matches_calendar: bool = True
    year_end_matches_calendar: bool = True

    def __post_init__(self):
        assert (
            1 <= self.month_start_day <= 28
        ), "fiscal_month_start_day must be between 1 and 28."
        assert (
            1 <= self.year_start_month <= 12
        ), "fiscal_year_start_month must be between 1 and 12."


@dataclass(frozen=True)
class HolidayType:
    name: str
    generated_column_prefix: str
    generated_flag_column_postfix: str = "HolidayFlag"
    generated_name_column_postfix: str = "HolidayName"
    generated_monthly_count_column_postfix: str = "HolidaysInMonth"
    included_in_business_day_calc: bool = False


@dataclass(frozen=True)
class Holiday:
    holiday_name: str
    holiday_date: date


@dataclass(frozen=True)
class HolidayCalendar:
    holiday_type: HolidayType
    holidays: list[Holiday]


def default_company_holidays() -> HolidayCalendar:
    return HolidayCalendar(
        HolidayType("Company Holiday", "Company", included_in_business_day_calc=True),
        [
            Holiday("New Year" "s Day", datetime.fromisoformat("2012-01-02")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2012-01-16")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2012-05-28")),
            Holiday("Independence Day", datetime.fromisoformat("2012-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2012-09-03")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2012-11-22")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2012-11-23")),
            Holiday("Christmas Eve", datetime.fromisoformat("2012-12-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2012-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2013-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2013-01-21")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2013-05-27")),
            Holiday("Independence Day", datetime.fromisoformat("2013-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2013-09-02")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2013-11-28")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2013-11-29")),
            Holiday("Christmas Eve", datetime.fromisoformat("2013-12-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2013-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2014-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2014-01-20")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2014-05-26")),
            Holiday("Independence Day", datetime.fromisoformat("2014-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2014-09-01")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2014-11-28")),
            Holiday("Christmas Eve", datetime.fromisoformat("2014-12-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2014-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2015-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2015-01-19")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2015-05-25")),
            Holiday("Independence Day", datetime.fromisoformat("2015-07-03")),
            Holiday("Labor Day", datetime.fromisoformat("2015-09-07")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2015-11-26")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2015-11-27")),
            Holiday("Christmas Eve", datetime.fromisoformat("2015-12-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2015-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2016-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2016-01-18")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2016-05-30")),
            Holiday("Independence Day", datetime.fromisoformat("2016-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2016-09-05")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2016-11-24")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2016-11-25")),
            Holiday("Christmas Eve", datetime.fromisoformat("2016-12-23")),
            Holiday("Christmas Day", datetime.fromisoformat("2016-12-26")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2017-01-02")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2017-01-16")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2017-05-29")),
            Holiday("Independence Day", datetime.fromisoformat("2017-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2017-09-04")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2017-11-23")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2017-11-24")),
            Holiday("Christmas Eve", datetime.fromisoformat("2017-12-25")),
            Holiday("Christmas Day", datetime.fromisoformat("2017-12-26")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2018-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2018-01-15")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2018-05-28")),
            Holiday("Independence Day", datetime.fromisoformat("2018-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2018-09-03")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2018-11-22")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2018-11-23")),
            Holiday("Christmas Eve", datetime.fromisoformat("2018-12-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2018-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2019-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2019-01-21")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2019-05-27")),
            Holiday("Independence Day", datetime.fromisoformat("2019-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2019-09-02")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2019-11-28")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2019-11-29")),
            Holiday("Christmas Eve", datetime.fromisoformat("2019-12-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2019-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2020-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2020-01-20")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2020-05-25")),
            Holiday("Independence Day", datetime.fromisoformat("2020-07-03")),
            Holiday("Labor Day", datetime.fromisoformat("2020-09-07")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2020-11-26")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2020-11-27")),
            Holiday("Christmas Eve", datetime.fromisoformat("2020-12-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2020-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2021-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2021-01-18")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2021-05-31")),
            Holiday("Independence Day", datetime.fromisoformat("2021-07-05")),
            Holiday("Labor Day", datetime.fromisoformat("2021-09-06")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2021-11-26")),
            Holiday("Christmas Eve", datetime.fromisoformat("2021-12-23")),
            Holiday("Christmas Day", datetime.fromisoformat("2021-12-24")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2021-12-31")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2022-01-17")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2022-05-30")),
            Holiday("Independence Day", datetime.fromisoformat("2022-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2022-09-05")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2022-11-24")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2022-11-25")),
            Holiday("Christmas Eve", datetime.fromisoformat("2022-12-23")),
            Holiday("Christmas Day", datetime.fromisoformat("2022-12-26")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2023-01-02")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2023-01-16")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2023-05-29")),
            Holiday("Independence Day", datetime.fromisoformat("2023-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2023-09-04")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2023-11-23")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2023-11-24")),
            Holiday("Christmas Eve", datetime.fromisoformat("2023-12-25")),
            Holiday("Christmas Day", datetime.fromisoformat("2023-12-26")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2024-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2024-01-15")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2024-05-27")),
            Holiday("Independence Day", datetime.fromisoformat("2024-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2024-09-02")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2024-11-28")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2024-11-29")),
            Holiday("Christmas Eve", datetime.fromisoformat("2024-12-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2024-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2025-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2025-01-20")
            ),
            Holiday("Memorial Day", datetime.fromisoformat("2025-05-26")),
            Holiday("Independence Day", datetime.fromisoformat("2025-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2025-09-01")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2025-11-27")),
            Holiday("Friday After Thanksgiving", datetime.fromisoformat("2025-11-28")),
            Holiday("Christmas Eve", datetime.fromisoformat("2025-12-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2025-12-25")),
        ],
    )


def default_us_public_holidays() -> HolidayCalendar:
    return HolidayCalendar(
        HolidayType("US Public Holiday", "USPublic"),
        [
            Holiday("New Year" "s Day", datetime.fromisoformat("2012-01-02")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2012-01-16")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2012-02-20")),
            Holiday("Memorial Day", datetime.fromisoformat("2012-05-28")),
            Holiday("Independence Day", datetime.fromisoformat("2012-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2012-09-03")),
            Holiday("Columbus Day", datetime.fromisoformat("2012-10-08")),
            Holiday("Veterans Day", datetime.fromisoformat("2012-11-12")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2012-11-22")),
            Holiday("Christmas Day", datetime.fromisoformat("2012-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2013-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2013-01-21")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2013-02-18")),
            Holiday("Memorial Day", datetime.fromisoformat("2013-05-27")),
            Holiday("Independence Day", datetime.fromisoformat("2013-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2013-09-02")),
            Holiday("Columbus Day", datetime.fromisoformat("2013-10-14")),
            Holiday("Veterans Day", datetime.fromisoformat("2013-11-11")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2013-11-28")),
            Holiday("Christmas Day", datetime.fromisoformat("2013-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2014-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2014-01-20")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2014-02-17")),
            Holiday("Memorial Day", datetime.fromisoformat("2014-05-26")),
            Holiday("Independence Day", datetime.fromisoformat("2014-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2014-09-01")),
            Holiday("Columbus Day", datetime.fromisoformat("2014-10-13")),
            Holiday("Veterans Day", datetime.fromisoformat("2014-11-11")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2014-11-27")),
            Holiday("Christmas Day", datetime.fromisoformat("2014-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2015-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2015-01-19")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2015-02-16")),
            Holiday("Memorial Day", datetime.fromisoformat("2015-05-25")),
            Holiday("Independence Day", datetime.fromisoformat("2015-07-03")),
            Holiday("Labor Day", datetime.fromisoformat("2015-09-07")),
            Holiday("Columbus Day", datetime.fromisoformat("2015-10-12")),
            Holiday("Veterans Day", datetime.fromisoformat("2015-11-11")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2015-11-26")),
            Holiday("Christmas Day", datetime.fromisoformat("2015-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2016-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2016-01-18")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2016-02-15")),
            Holiday("Memorial Day", datetime.fromisoformat("2016-05-30")),
            Holiday("Independence Day", datetime.fromisoformat("2016-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2016-09-05")),
            Holiday("Columbus Day", datetime.fromisoformat("2016-10-10")),
            Holiday("Veterans Day", datetime.fromisoformat("2016-11-11")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2016-11-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2016-12-26")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2017-01-02")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2017-01-16")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2017-02-20")),
            Holiday("Memorial Day", datetime.fromisoformat("2017-05-29")),
            Holiday("Independence Day", datetime.fromisoformat("2017-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2017-09-04")),
            Holiday("Columbus Day", datetime.fromisoformat("2017-10-09")),
            Holiday("Veterans Day", datetime.fromisoformat("2017-11-10")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2017-11-23")),
            Holiday("Christmas Day", datetime.fromisoformat("2017-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2018-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2018-01-15")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2018-02-19")),
            Holiday("Memorial Day", datetime.fromisoformat("2018-05-28")),
            Holiday("Independence Day", datetime.fromisoformat("2018-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2018-09-03")),
            Holiday("Columbus Day", datetime.fromisoformat("2018-10-08")),
            Holiday("Veterans Day", datetime.fromisoformat("2018-11-12")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2018-11-22")),
            Holiday("Christmas Day", datetime.fromisoformat("2018-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2019-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2019-01-21")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2019-02-18")),
            Holiday("Memorial Day", datetime.fromisoformat("2019-05-27")),
            Holiday("Independence Day", datetime.fromisoformat("2019-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2019-09-02")),
            Holiday("Columbus Day", datetime.fromisoformat("2019-10-14")),
            Holiday("Veterans Day", datetime.fromisoformat("2019-11-11")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2019-11-28")),
            Holiday("Christmas Day", datetime.fromisoformat("2019-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2020-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2020-01-20")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2020-02-17")),
            Holiday("Memorial Day", datetime.fromisoformat("2020-05-25")),
            Holiday("Independence Day", datetime.fromisoformat("2020-07-03")),
            Holiday("Labor Day", datetime.fromisoformat("2020-09-07")),
            Holiday("Columbus Day", datetime.fromisoformat("2020-10-12")),
            Holiday("Veterans Day", datetime.fromisoformat("2020-11-11")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2020-11-26")),
            Holiday("Christmas Day", datetime.fromisoformat("2020-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2021-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2021-01-18")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2021-02-15")),
            Holiday("Memorial Day", datetime.fromisoformat("2021-05-31")),
            Holiday("Independence Day", datetime.fromisoformat("2021-07-05")),
            Holiday("Labor Day", datetime.fromisoformat("2021-09-06")),
            Holiday("Columbus Day", datetime.fromisoformat("2021-10-11")),
            Holiday("Veterans Day", datetime.fromisoformat("2021-11-11")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2021-11-25")),
            Holiday("Christmas Day", datetime.fromisoformat("2021-12-24")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2021-12-31")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2022-01-17")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2022-02-21")),
            Holiday("Memorial Day", datetime.fromisoformat("2022-05-30")),
            Holiday("Independence Day", datetime.fromisoformat("2022-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2022-09-05")),
            Holiday("Columbus Day", datetime.fromisoformat("2022-10-10")),
            Holiday("Veterans Day", datetime.fromisoformat("2022-11-11")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2022-11-24")),
            Holiday("Christmas Day", datetime.fromisoformat("2022-12-26")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2023-01-02")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2023-01-16")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2023-02-20")),
            Holiday("Memorial Day", datetime.fromisoformat("2023-05-29")),
            Holiday("Independence Day", datetime.fromisoformat("2023-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2023-09-04")),
            Holiday("Columbus Day", datetime.fromisoformat("2023-10-09")),
            Holiday("Veterans Day", datetime.fromisoformat("2023-11-10")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2023-11-23")),
            Holiday("Christmas Day", datetime.fromisoformat("2023-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2024-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2024-01-15")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2024-02-19")),
            Holiday("Memorial Day", datetime.fromisoformat("2024-05-27")),
            Holiday("Independence Day", datetime.fromisoformat("2024-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2024-09-02")),
            Holiday("Columbus Day", datetime.fromisoformat("2024-10-14")),
            Holiday("Veterans Day", datetime.fromisoformat("2024-11-11")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2024-11-28")),
            Holiday("Christmas Day", datetime.fromisoformat("2024-12-25")),
            Holiday("New Year" "s Day", datetime.fromisoformat("2025-01-01")),
            Holiday(
                "Martin Luther King, Jr. Day", datetime.fromisoformat("2025-01-20")
            ),
            Holiday("Presidents" " Day", datetime.fromisoformat("2025-02-17")),
            Holiday("Memorial Day", datetime.fromisoformat("2025-05-26")),
            Holiday("Independence Day", datetime.fromisoformat("2025-07-04")),
            Holiday("Labor Day", datetime.fromisoformat("2025-09-01")),
            Holiday("Columbus Day", datetime.fromisoformat("2025-10-13")),
            Holiday("Veterans Day", datetime.fromisoformat("2025-11-11")),
            Holiday("Thanksgiving Day", datetime.fromisoformat("2025-11-27")),
            Holiday("Christmas Day", datetime.fromisoformat("2025-12-25")),
        ],
    )


@dataclass(frozen=True)
class Column:
    name: str
    include: bool
    sort_index: int


@dataclass(frozen=True)
class HolidayTypesColumns:
    holiday_type_key: Column = field(
        default_factory=lambda: Column("HolidayTypeKey", True, 0)
    )
    holiday_type_name: Column = field(
        default_factory=lambda: Column("HolidayTypeName", True, 1)
    )

    def __post_init__(self):
        assert (
            self.holiday_type_key.include and self.holiday_type_name.include
        ), "all HolidayTypes columns must be included."


@dataclass(frozen=True)
class HolidaysColumns:
    date_key: Column = field(default_factory=lambda: Column("DateKey", True, 0))
    holiday_name: Column = field(default_factory=lambda: Column("HolidayName", True, 1))
    holiday_type_key: Column = field(
        default_factory=lambda: Column("HolidayTypeKey", True, 2)
    )

    def __post_init__(self):
        assert (
            self.date_key.include
            and self.holiday_name.include
            and self.holiday_type_key.include
        ), "all Holidays columns must be included."


@dataclass(frozen=True)
class HolidayConfig:
    generate_holidays: bool = True
    holiday_types_schema_name: str = "integration"
    holiday_types_table_name: str = "manual_HolidayTypes"
    holiday_types_columns: HolidayTypesColumns = field(
        default_factory=lambda: HolidayTypesColumns()
    )
    holidays_schema_name: str = "integration"
    holidays_table_name: str = "manual_Holidays"
    holidays_columns: HolidaysColumns = field(default_factory=lambda: HolidaysColumns())
    holiday_calendars: list[HolidayCalendar] = field(
        default_factory=lambda: [
            default_company_holidays(),
            default_us_public_holidays(),
        ]
    )
    holiday_types: list[HolidayType] = field(init=False, default_factory=list)

    def __post_init__(self):
        if self.generate_holidays:
            holiday_types = [cal.holiday_type for cal in self.holiday_calendars]
            holiday_type_names = [t.name for t in holiday_types]
            holiday_type_prefixes = [t.generated_column_prefix for t in holiday_types]
            assert len(holiday_type_names) == len(
                set(holiday_type_names)
            ), "detected a duplicate HolidayType name in HolidayConfig. This would create multiple columns with the same name, which is not allowed."
            assert len(holiday_type_prefixes) == len(
                set(holiday_type_prefixes)
            ), "detected a duplicate HolidayTypePrefix in HolidayConfig. This would create multiple columns with the same name, which is not allowed."
            object.__setattr__(self, "holiday_types", holiday_types)


@dataclass(frozen=True)
class DimDateColumns:
    date_key: Column = field(default_factory=lambda: Column("DateKey", True, 1000))
    the_date: Column = field(default_factory=lambda: Column("TheDate", True, 2000))
    iso_date_name: Column = field(
        default_factory=lambda: Column("ISODateName", True, 3000)
    )
    iso_week_date_name: Column = field(
        default_factory=lambda: Column("ISOWeekDateName", True, 4000)
    )
    american_date_name: Column = field(
        default_factory=lambda: Column("AmericanDateName", True, 5000)
    )
    day_of_week_name: Column = field(
        default_factory=lambda: Column("DayOfWeekName", True, 6000)
    )
    day_of_week_abbrev: Column = field(
        default_factory=lambda: Column("DayOfWeekAbbrev", True, 7000)
    )
    month_name: Column = field(default_factory=lambda: Column("MonthName", True, 8000))
    month_abbrev: Column = field(
        default_factory=lambda: Column("MonthAbbrev", True, 9000)
    )
    year_week_name: Column = field(
        default_factory=lambda: Column("YearWeekName", True, 10000)
    )
    year_month_name: Column = field(
        default_factory=lambda: Column("YearMonthName", True, 11000)
    )
    month_year_name: Column = field(
        default_factory=lambda: Column("MonthYearName", True, 12000)
    )
    year_quarter_name: Column = field(
        default_factory=lambda: Column("YearQuarterName", True, 13000)
    )
    year: Column = field(default_factory=lambda: Column("Year", True, 14000))
    year_week: Column = field(default_factory=lambda: Column("YearWeek", True, 15000))
    iso_year_week_code: Column = field(
        default_factory=lambda: Column("ISOYearWeekCode", True, 16000)
    )
    year_month: Column = field(default_factory=lambda: Column("YearMonth", True, 17000))
    year_quarter: Column = field(
        default_factory=lambda: Column("YearQuarter", True, 18000)
    )
    day_of_week_starting_monday: Column = field(
        default_factory=lambda: Column("DayOfWeekStartingMonday", True, 19000)
    )
    day_of_week: Column = field(
        default_factory=lambda: Column("DayOfWeek", True, 20000)
    )
    day_of_month: Column = field(
        default_factory=lambda: Column("DayOfMonth", True, 21000)
    )
    day_of_quarter: Column = field(
        default_factory=lambda: Column("DayOfQuarter", True, 22000)
    )
    day_of_year: Column = field(
        default_factory=lambda: Column("DayOfYear", True, 23000)
    )
    week_of_quarter: Column = field(
        default_factory=lambda: Column("WeekOfQuarter", True, 24000)
    )
    week_of_year: Column = field(
        default_factory=lambda: Column("WeekOfYear", True, 25000)
    )
    iso_week_of_year: Column = field(
        default_factory=lambda: Column("ISOWeekOfYear", True, 26000)
    )
    month: Column = field(default_factory=lambda: Column("Month", True, 27000))
    month_of_quarter: Column = field(
        default_factory=lambda: Column("MonthOfQuarter", True, 28000)
    )
    quarter: Column = field(default_factory=lambda: Column("Quarter", True, 29000))
    days_in_month: Column = field(
        default_factory=lambda: Column("DaysInMonth", True, 30000)
    )
    days_in_quarter: Column = field(
        default_factory=lambda: Column("DaysInQuarter", True, 31000)
    )
    days_in_year: Column = field(
        default_factory=lambda: Column("DaysInYear", True, 32000)
    )
    day_offset_from_today: Column = field(
        default_factory=lambda: Column("DayOffsetFromToday", True, 33000)
    )
    month_offset_from_today: Column = field(
        default_factory=lambda: Column("MonthOffsetFromToday", True, 34000)
    )
    quarter_offset_from_today: Column = field(
        default_factory=lambda: Column("QuarterOffsetFromToday", True, 35000)
    )
    year_offset_from_today: Column = field(
        default_factory=lambda: Column("YearOffsetFromToday", True, 36000)
    )
    today_flag: Column = field(default_factory=lambda: Column("TodayFlag", True, 37000))
    current_week_starting_monday_flag: Column = field(
        default_factory=lambda: Column("CurrentWeekStartingMondayFlag", True, 38000)
    )
    current_week_flag: Column = field(
        default_factory=lambda: Column("CurrentWeekFlag", True, 39000)
    )
    prior_week_flag: Column = field(
        default_factory=lambda: Column("PriorWeekFlag", True, 40000)
    )
    next_week_flag: Column = field(
        default_factory=lambda: Column("NextWeekFlag", True, 41000)
    )
    current_month_flag: Column = field(
        default_factory=lambda: Column("CurrentMonthFlag", True, 42000)
    )
    prior_month_flag: Column = field(
        default_factory=lambda: Column("PriorMonthFlag", True, 43000)
    )
    next_month_flag: Column = field(
        default_factory=lambda: Column("NextMonthFlag", True, 44000)
    )
    current_quarter_flag: Column = field(
        default_factory=lambda: Column("CurrentQuarterFlag", True, 45000)
    )
    prior_quarter_flag: Column = field(
        default_factory=lambda: Column("PriorQuarterFlag", True, 46000)
    )
    next_quarter_flag: Column = field(
        default_factory=lambda: Column("NextQuarterFlag", True, 47000)
    )
    current_year_flag: Column = field(
        default_factory=lambda: Column("CurrentYearFlag", True, 48000)
    )
    prior_year_flag: Column = field(
        default_factory=lambda: Column("PriorYearFlag", True, 49000)
    )
    next_year_flag: Column = field(
        default_factory=lambda: Column("NextYearFlag", True, 50000)
    )
    weekday_flag: Column = field(
        default_factory=lambda: Column("WeekdayFlag", True, 51000)
    )
    business_day_flag: Column = field(
        default_factory=lambda: Column("BusinessDayFlag", True, 52000)
    )
    first_day_of_month_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfMonthFlag", True, 53000)
    )
    last_day_of_month_flag: Column = field(
        default_factory=lambda: Column("LastDayOfMonthFlag", True, 54000)
    )
    first_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfQuarterFlag", True, 55000)
    )
    last_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("LastDayOfQuarterFlag", True, 56000)
    )
    first_day_of_year_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfYearFlag", True, 57000)
    )
    last_day_of_year_flag: Column = field(
        default_factory=lambda: Column("LastDayOfYearFlag", True, 58000)
    )
    fraction_of_week: Column = field(
        default_factory=lambda: Column("FractionOfWeek", True, 59000)
    )
    fraction_of_month: Column = field(
        default_factory=lambda: Column("FractionOfMonth", True, 60000)
    )
    fraction_of_quarter: Column = field(
        default_factory=lambda: Column("FractionOfQuarter", True, 61000)
    )
    fraction_of_year: Column = field(
        default_factory=lambda: Column("FractionOfYear", True, 62000)
    )
    prior_day: Column = field(default_factory=lambda: Column("PriorDay", True, 63000))
    next_day: Column = field(default_factory=lambda: Column("NextDay", True, 64000))
    same_day_prior_week: Column = field(
        default_factory=lambda: Column("SameDayPriorWeek", True, 65000)
    )
    same_day_prior_month: Column = field(
        default_factory=lambda: Column("SameDayPriorMonth", True, 66000)
    )
    same_day_prior_quarter: Column = field(
        default_factory=lambda: Column("SameDayPriorQuarter", True, 67000)
    )
    same_day_prior_year: Column = field(
        default_factory=lambda: Column("SameDayPriorYear", True, 68000)
    )
    same_day_next_week: Column = field(
        default_factory=lambda: Column("SameDayNextWeek", True, 69000)
    )
    same_day_next_month: Column = field(
        default_factory=lambda: Column("SameDayNextMonth", True, 70000)
    )
    same_day_next_quarter: Column = field(
        default_factory=lambda: Column("SameDayNextQuarter", True, 71000)
    )
    same_day_next_year: Column = field(
        default_factory=lambda: Column("SameDayNextYear", True, 72000)
    )
    current_week_start: Column = field(
        default_factory=lambda: Column("CurrentWeekStart", True, 73000)
    )
    current_week_end: Column = field(
        default_factory=lambda: Column("CurrentWeekEnd", True, 74000)
    )
    current_month_start: Column = field(
        default_factory=lambda: Column("CurrentMonthStart", True, 75000)
    )
    current_month_end: Column = field(
        default_factory=lambda: Column("CurrentMonthEnd", True, 76000)
    )
    current_quarter_start: Column = field(
        default_factory=lambda: Column("CurrentQuarterStart", True, 77000)
    )
    current_quarter_end: Column = field(
        default_factory=lambda: Column("CurrentQuarterEnd", True, 78000)
    )
    current_year_start: Column = field(
        default_factory=lambda: Column("CurrentYearStart", True, 79000)
    )
    current_year_end: Column = field(
        default_factory=lambda: Column("CurrentYearEnd", True, 80000)
    )
    prior_week_start: Column = field(
        default_factory=lambda: Column("PriorWeekStart", True, 81000)
    )
    prior_week_end: Column = field(
        default_factory=lambda: Column("PriorWeekEnd", True, 82000)
    )
    prior_month_start: Column = field(
        default_factory=lambda: Column("PriorMonthStart", True, 83000)
    )
    prior_month_end: Column = field(
        default_factory=lambda: Column("PriorMonthEnd", True, 84000)
    )
    prior_quarter_start: Column = field(
        default_factory=lambda: Column("PriorQuarterStart", True, 85000)
    )
    prior_quarter_end: Column = field(
        default_factory=lambda: Column("PriorQuarterEnd", True, 86000)
    )
    prior_year_start: Column = field(
        default_factory=lambda: Column("PriorYearStart", True, 87000)
    )
    prior_year_end: Column = field(
        default_factory=lambda: Column("PriorYearEnd", True, 88000)
    )
    next_week_start: Column = field(
        default_factory=lambda: Column("NextWeekStart", True, 89000)
    )
    next_week_end: Column = field(
        default_factory=lambda: Column("NextWeekEnd", True, 90000)
    )
    next_month_start: Column = field(
        default_factory=lambda: Column("NextMonthStart", True, 91000)
    )
    next_month_end: Column = field(
        default_factory=lambda: Column("NextMonthEnd", True, 92000)
    )
    next_quarter_start: Column = field(
        default_factory=lambda: Column("NextQuarterStart", True, 93000)
    )
    next_quarter_end: Column = field(
        default_factory=lambda: Column("NextQuarterEnd", True, 94000)
    )
    next_year_start: Column = field(
        default_factory=lambda: Column("NextYearStart", True, 95000)
    )
    next_year_end: Column = field(
        default_factory=lambda: Column("NextYearEnd", True, 96000)
    )
    weekly_burnup_starting_monday: Column = field(
        default_factory=lambda: Column("WeeklyBurnupStartingMonday", True, 97000)
    )
    weekly_burnup: Column = field(
        default_factory=lambda: Column("WeeklyBurnup", True, 98000)
    )
    monthly_burnup: Column = field(
        default_factory=lambda: Column("MonthlyBurnup", True, 99000)
    )
    quarterly_burnup: Column = field(
        default_factory=lambda: Column("QuarterlyBurnup", True, 100000)
    )
    yearly_burnup: Column = field(
        default_factory=lambda: Column("YearlyBurnup", True, 101000)
    )
    fiscal_month_name: Column = field(
        default_factory=lambda: Column("FiscalMonthName", True, 102000)
    )
    fiscal_month_abbrev: Column = field(
        default_factory=lambda: Column("FiscalMonthAbbrev", True, 103000)
    )
    fiscal_year_week_name: Column = field(
        default_factory=lambda: Column("FiscalYearWeekName", True, 104000)
    )
    fiscal_year_month_name: Column = field(
        default_factory=lambda: Column("FiscalYearMonthName", True, 105000)
    )
    fiscal_month_year_name: Column = field(
        default_factory=lambda: Column("FiscalMonthYearName", True, 106000)
    )
    fiscal_year_quarter_name: Column = field(
        default_factory=lambda: Column("FiscalYearQuarterName", True, 107000)
    )
    fiscal_year: Column = field(
        default_factory=lambda: Column("FiscalYear", True, 108000)
    )
    fiscal_year_week: Column = field(
        default_factory=lambda: Column("FiscalYearWeek", True, 109000)
    )
    fiscal_year_month: Column = field(
        default_factory=lambda: Column("FiscalYearMonth", True, 110000)
    )
    fiscal_year_quarter: Column = field(
        default_factory=lambda: Column("FiscalYearQuarter", True, 111000)
    )
    fiscal_day_of_month: Column = field(
        default_factory=lambda: Column("FiscalDayOfMonth", True, 112000)
    )
    fiscal_day_of_quarter: Column = field(
        default_factory=lambda: Column("FiscalDayOfQuarter", True, 113000)
    )
    fiscal_day_of_year: Column = field(
        default_factory=lambda: Column("FiscalDayOfYear", True, 114000)
    )
    fiscal_week_of_quarter: Column = field(
        default_factory=lambda: Column("FiscalWeekOfQuarter", True, 115000)
    )
    fiscal_week_of_year: Column = field(
        default_factory=lambda: Column("FiscalWeekOfYear", True, 116000)
    )
    fiscal_month: Column = field(
        default_factory=lambda: Column("FiscalMonth", True, 117000)
    )
    fiscal_month_of_quarter: Column = field(
        default_factory=lambda: Column("FiscalMonthOfQuarter", True, 118000)
    )
    fiscal_quarter: Column = field(
        default_factory=lambda: Column("FiscalQuarter", True, 119000)
    )
    fiscal_days_in_month: Column = field(
        default_factory=lambda: Column("FiscalDaysInMonth", True, 120000)
    )
    fiscal_days_in_quarter: Column = field(
        default_factory=lambda: Column("FiscalDaysInQuarter", True, 121000)
    )
    fiscal_days_in_year: Column = field(
        default_factory=lambda: Column("FiscalDaysInYear", True, 122000)
    )
    fiscal_current_month_flag: Column = field(
        default_factory=lambda: Column("FiscalCurrentMonthFlag", True, 123000)
    )
    fiscal_prior_month_flag: Column = field(
        default_factory=lambda: Column("FiscalPriorMonthFlag", True, 124000)
    )
    fiscal_next_month_flag: Column = field(
        default_factory=lambda: Column("FiscalNextMonthFlag", True, 125000)
    )
    fiscal_current_quarter_flag: Column = field(
        default_factory=lambda: Column("FiscalCurrentQuarterFlag", True, 126000)
    )
    fiscal_prior_quarter_flag: Column = field(
        default_factory=lambda: Column("FiscalPriorQuarterFlag", True, 127000)
    )
    fiscal_next_quarter_flag: Column = field(
        default_factory=lambda: Column("FiscalNextQuarterFlag", True, 128000)
    )
    fiscal_current_year_flag: Column = field(
        default_factory=lambda: Column("FiscalCurrentYearFlag", True, 129000)
    )
    fiscal_prior_year_flag: Column = field(
        default_factory=lambda: Column("FiscalPriorYearFlag", True, 130000)
    )
    fiscal_next_year_flag: Column = field(
        default_factory=lambda: Column("FiscalNextYearFlag", True, 131000)
    )
    fiscal_first_day_of_month_flag: Column = field(
        default_factory=lambda: Column("FiscalFirstDayOfMonthFlag", True, 132000)
    )
    fiscal_last_day_of_month_flag: Column = field(
        default_factory=lambda: Column("FiscalLastDayOfMonthFlag", True, 133000)
    )
    fiscal_first_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("FiscalFirstDayOfQuarterFlag", True, 134000)
    )
    fiscal_last_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("FiscalLastDayOfQuarterFlag", True, 135000)
    )
    fiscal_first_day_of_year_flag: Column = field(
        default_factory=lambda: Column("FiscalFirstDayOfYearFlag", True, 136000)
    )
    fiscal_last_day_of_year_flag: Column = field(
        default_factory=lambda: Column("FiscalLastDayOfYearFlag", True, 137000)
    )
    fiscal_fraction_of_month: Column = field(
        default_factory=lambda: Column("FiscalFractionOfMonth", True, 138000)
    )
    fiscal_fraction_of_quarter: Column = field(
        default_factory=lambda: Column("FiscalFractionOfQuarter", True, 139000)
    )
    fiscal_fraction_of_year: Column = field(
        default_factory=lambda: Column("FiscalFractionOfYear", True, 140000)
    )
    fiscal_current_month_start: Column = field(
        default_factory=lambda: Column("FiscalCurrentMonthStart", True, 141000)
    )
    fiscal_current_month_end: Column = field(
        default_factory=lambda: Column("FiscalCurrentMonthEnd", True, 142000)
    )
    fiscal_current_quarter_start: Column = field(
        default_factory=lambda: Column("FiscalCurrentQuarterStart", True, 143000)
    )
    fiscal_current_quarter_end: Column = field(
        default_factory=lambda: Column("FiscalCurrentQuarterEnd", True, 144000)
    )
    fiscal_current_year_start: Column = field(
        default_factory=lambda: Column("FiscalCurrentYearStart", True, 145000)
    )
    fiscal_current_year_end: Column = field(
        default_factory=lambda: Column("FiscalCurrentYearEnd", True, 146000)
    )
    fiscal_prior_month_start: Column = field(
        default_factory=lambda: Column("FiscalPriorMonthStart", True, 147000)
    )
    fiscal_prior_month_end: Column = field(
        default_factory=lambda: Column("FiscalPriorMonthEnd", True, 148000)
    )
    fiscal_prior_quarter_start: Column = field(
        default_factory=lambda: Column("FiscalPriorQuarterStart", True, 149000)
    )
    fiscal_prior_quarter_end: Column = field(
        default_factory=lambda: Column("FiscalPriorQuarterEnd", True, 150000)
    )
    fiscal_prior_year_start: Column = field(
        default_factory=lambda: Column("FiscalPriorYearStart", True, 151000)
    )
    fiscal_prior_year_end: Column = field(
        default_factory=lambda: Column("FiscalPriorYearEnd", True, 152000)
    )
    fiscal_next_month_start: Column = field(
        default_factory=lambda: Column("FiscalNextMonthStart", True, 153000)
    )
    fiscal_next_month_end: Column = field(
        default_factory=lambda: Column("FiscalNextMonthEnd", True, 154000)
    )
    fiscal_next_quarter_start: Column = field(
        default_factory=lambda: Column("FiscalNextQuarterStart", True, 155000)
    )
    fiscal_next_quarter_end: Column = field(
        default_factory=lambda: Column("FiscalNextQuarterEnd", True, 156000)
    )
    fiscal_next_year_start: Column = field(
        default_factory=lambda: Column("FiscalNextYearStart", True, 157000)
    )
    fiscal_next_year_end: Column = field(
        default_factory=lambda: Column("FiscalNextYearEnd", True, 158000)
    )
    fiscal_monthly_burnup: Column = field(
        default_factory=lambda: Column("FiscalMonthlyBurnup", True, 159000)
    )
    fiscal_quarterly_burnup: Column = field(
        default_factory=lambda: Column("FiscalQuarterlyBurnup", True, 160000)
    )
    fiscal_yearly_burnup: Column = field(
        default_factory=lambda: Column("FiscalYearlyBurnup", True, 161000)
    )


@dataclass(frozen=True)
class DimDateConfig:
    table_schema: str = "dbo"
    table_name: str = "DimDate"
    columns: DimDateColumns = field(default_factory=lambda: DimDateColumns())
    column_factory: Callable[[str, Column], Column] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v["sort_index"] for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys
        ), "there was a duplicate sort key in the column definitions for DimDateColumn."

        if self.column_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_col = self.column_factory(k, v)
                assert isinstance(
                    new_col, Column
                ), f"column_factory returned a value that was not a column. This is not allowed. Value: {new_col}"
                new_cols[k] = self.column_factory(v)

            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass(frozen=True)
class DimFiscalMonthColumns:
    month_start_key: Column = field(
        default_factory=lambda: Column("MonthStartKey", True, 1000)
    )
    month_end_key: Column = field(
        default_factory=lambda: Column("MonthEndKey", True, 2000)
    )
    month_start_date: Column = field(
        default_factory=lambda: Column("MonthStartDate", True, 3000)
    )
    month_end_date: Column = field(
        default_factory=lambda: Column("MonthEndDate", True, 4000)
    )
    month_start_iso_date_name: Column = field(
        default_factory=lambda: Column("MonthStartISODateName", True, 5000)
    )
    month_end_iso_date_name: Column = field(
        default_factory=lambda: Column("MonthEndISODateName", True, 6000)
    )
    month_start_iso_week_date_name: Column = field(
        default_factory=lambda: Column("MonthStartISOWeekDateName", True, 7000)
    )
    month_end_iso_week_date_name: Column = field(
        default_factory=lambda: Column("MonthEndISOWeekDateName", True, 8000)
    )
    month_start_american_date_name: Column = field(
        default_factory=lambda: Column("MonthStartAmericanDateName", True, 9000)
    )
    month_end_american_date_name: Column = field(
        default_factory=lambda: Column("MonthEndAmericanDateName", True, 10000)
    )
    month_name: Column = field(default_factory=lambda: Column("MonthName", True, 11000))
    month_abbrev: Column = field(
        default_factory=lambda: Column("MonthAbbrev", True, 12000)
    )
    month_start_year_week_name: Column = field(
        default_factory=lambda: Column("MonthStartYearWeekName", True, 13000)
    )
    month_end_year_week_name: Column = field(
        default_factory=lambda: Column("MonthEndYearWeekName", True, 14000)
    )
    year_month_name: Column = field(
        default_factory=lambda: Column("YearMonthName", True, 15000)
    )
    month_year_name: Column = field(
        default_factory=lambda: Column("MonthYearName", True, 16000)
    )
    year_quarter_name: Column = field(
        default_factory=lambda: Column("YearQuarterName", True, 17000)
    )
    year: Column = field(default_factory=lambda: Column("Year", True, 18000))
    month_start_year_week: Column = field(
        default_factory=lambda: Column("MonthStartYearWeek", True, 19000)
    )
    month_end_year_week: Column = field(
        default_factory=lambda: Column("MonthEndYearWeek", True, 20000)
    )
    year_month: Column = field(default_factory=lambda: Column("YearMonth", True, 21000))
    year_quarter: Column = field(
        default_factory=lambda: Column("YearQuarter", True, 22000)
    )
    month_start_day_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartDayOfQuarter", True, 23000)
    )
    month_end_day_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndDayOfQuarter", True, 24000)
    )
    month_start_day_of_year: Column = field(
        default_factory=lambda: Column("MonthStartDayOfYear", True, 25000)
    )
    month_end_day_of_year: Column = field(
        default_factory=lambda: Column("MonthEndDayOfYear", True, 26000)
    )
    month_start_week_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartWeekOfQuarter", True, 27000)
    )
    month_end_week_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndWeekOfQuarter", True, 28000)
    )
    month_start_week_of_year: Column = field(
        default_factory=lambda: Column("MonthStartWeekOfYear", True, 29000)
    )
    month_end_week_of_year: Column = field(
        default_factory=lambda: Column("MonthEndWeekOfYear", True, 30000)
    )
    month_of_quarter: Column = field(
        default_factory=lambda: Column("MonthOfQuarter", True, 31000)
    )
    quarter: Column = field(default_factory=lambda: Column("Quarter", True, 32000))
    days_in_month: Column = field(
        default_factory=lambda: Column("DaysInMonth", True, 33000)
    )
    days_in_quarter: Column = field(
        default_factory=lambda: Column("DaysInQuarter", True, 34000)
    )
    days_in_year: Column = field(
        default_factory=lambda: Column("DaysInYear", True, 35000)
    )
    current_month_flag: Column = field(
        default_factory=lambda: Column("CurrentMonthFlag", True, 36000)
    )
    prior_month_flag: Column = field(
        default_factory=lambda: Column("PriorMonthFlag", True, 37000)
    )
    next_month_flag: Column = field(
        default_factory=lambda: Column("NextMonthFlag", True, 38000)
    )
    current_quarter_flag: Column = field(
        default_factory=lambda: Column("CurrentQuarterFlag", True, 39000)
    )
    prior_quarter_flag: Column = field(
        default_factory=lambda: Column("PriorQuarterFlag", True, 40000)
    )
    next_quarter_flag: Column = field(
        default_factory=lambda: Column("NextQuarterFlag", True, 41000)
    )
    current_year_flag: Column = field(
        default_factory=lambda: Column("CurrentYearFlag", True, 42000)
    )
    prior_year_flag: Column = field(
        default_factory=lambda: Column("PriorYearFlag", True, 43000)
    )
    next_year_flag: Column = field(
        default_factory=lambda: Column("NextYearFlag", True, 44000)
    )
    first_day_of_month_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfMonthFlag", True, 45000)
    )
    last_day_of_month_flag: Column = field(
        default_factory=lambda: Column("LastDayOfMonthFlag", True, 46000)
    )
    first_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfQuarterFlag", True, 47000)
    )
    last_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("LastDayOfQuarterFlag", True, 48000)
    )
    first_day_of_year_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfYearFlag", True, 49000)
    )
    last_day_of_year_flag: Column = field(
        default_factory=lambda: Column("LastDayOfYearFlag", True, 50000)
    )
    month_start_fraction_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartFractionOfQuarter", True, 51000)
    )
    month_end_fraction_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndFractionOfQuarter", True, 52000)
    )
    month_start_fraction_of_year: Column = field(
        default_factory=lambda: Column("MonthStartFractionOfYear", True, 53000)
    )
    month_end_fraction_of_year: Column = field(
        default_factory=lambda: Column("MonthEndFractionOfYear", True, 54000)
    )
    current_quarter_start: Column = field(
        default_factory=lambda: Column("CurrentQuarterStart", True, 55000)
    )
    current_quarter_end: Column = field(
        default_factory=lambda: Column("CurrentQuarterEnd", True, 56000)
    )
    current_year_start: Column = field(
        default_factory=lambda: Column("CurrentYearStart", True, 57000)
    )
    current_year_end: Column = field(
        default_factory=lambda: Column("CurrentYearEnd", True, 58000)
    )
    prior_month_start: Column = field(
        default_factory=lambda: Column("PriorMonthStart", True, 59000)
    )
    prior_month_end: Column = field(
        default_factory=lambda: Column("PriorMonthEnd", True, 60000)
    )
    prior_quarter_start: Column = field(
        default_factory=lambda: Column("PriorQuarterStart", True, 61000)
    )
    prior_quarter_end: Column = field(
        default_factory=lambda: Column("PriorQuarterEnd", True, 62000)
    )
    prior_year_start: Column = field(
        default_factory=lambda: Column("PriorYearStart", True, 63000)
    )
    prior_year_end: Column = field(
        default_factory=lambda: Column("PriorYearEnd", True, 64000)
    )
    next_month_start: Column = field(
        default_factory=lambda: Column("NextMonthStart", True, 65000)
    )
    next_month_end: Column = field(
        default_factory=lambda: Column("NextMonthEnd", True, 66000)
    )
    next_quarter_start: Column = field(
        default_factory=lambda: Column("NextQuarterStart", True, 67000)
    )
    next_quarter_end: Column = field(
        default_factory=lambda: Column("NextQuarterEnd", True, 68000)
    )
    next_year_start: Column = field(
        default_factory=lambda: Column("NextYearStart", True, 69000)
    )
    next_year_end: Column = field(
        default_factory=lambda: Column("NextYearEnd", True, 70000)
    )
    month_start_quarterly_burnup: Column = field(
        default_factory=lambda: Column("MonthStartQuarterlyBurnup", True, 71000)
    )
    month_end_quarterly_burnup: Column = field(
        default_factory=lambda: Column("MonthEndQuarterlyBurnup", True, 72000)
    )
    month_start_yearly_burnup: Column = field(
        default_factory=lambda: Column("MonthStartYearlyBurnup", True, 73000)
    )
    month_end_yearly_burnup: Column = field(
        default_factory=lambda: Column("MonthEndYearlyBurnup", True, 74000)
    )


@dataclass(frozen=True)
class DimFiscalMonthConfig:
    table_schema: str = "dbo"
    table_name: str = "DimFiscalMonth"
    columns: DimFiscalMonthColumns = field(
        default_factory=lambda: DimFiscalMonthColumns()
    )
    column_factory: Callable[[str, Column], Column] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v["sort_index"] for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys
        ), "there was a duplicate sort key in the column definitions for DimFiscalMonthColumn."

        if self.column_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_col = self.column_factory(k, v)
                assert isinstance(
                    new_col, Column
                ), f"column_factory returned a value that was not a column. This is not allowed. Value: {new_col}"
                new_cols[k] = self.column_factory(v)

            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass(frozen=True)
class DimCalendarMonthColumns:
    month_start_key: Column = field(
        default_factory=lambda: Column("MonthStartKey", True, 1000)
    )
    month_end_key: Column = field(
        default_factory=lambda: Column("MonthEndKey", True, 2000)
    )
    month_start_date: Column = field(
        default_factory=lambda: Column("MonthStartDate", True, 3000)
    )
    month_end_date: Column = field(
        default_factory=lambda: Column("MonthEndDate", True, 4000)
    )
    month_start_iso_date_name: Column = field(
        default_factory=lambda: Column("MonthStartISODateName", True, 5000)
    )
    month_end_iso_date_name: Column = field(
        default_factory=lambda: Column("MonthEndISODateName", True, 6000)
    )
    month_start_iso_week_date_name: Column = field(
        default_factory=lambda: Column("MonthStartISOWeekDateName", True, 7000)
    )
    month_end_iso_week_date_name: Column = field(
        default_factory=lambda: Column("MonthEndISOWeekDateName", True, 8000)
    )
    month_start_american_date_name: Column = field(
        default_factory=lambda: Column("MonthStartAmericanDateName", True, 9000)
    )
    month_end_american_date_name: Column = field(
        default_factory=lambda: Column("MonthEndAmericanDateName", True, 10000)
    )
    month_name: Column = field(default_factory=lambda: Column("MonthName", True, 11000))
    month_abbrev: Column = field(
        default_factory=lambda: Column("MonthAbbrev", True, 12000)
    )
    month_start_year_week_name: Column = field(
        default_factory=lambda: Column("MonthStartYearWeekName", True, 13000)
    )
    month_end_year_week_name: Column = field(
        default_factory=lambda: Column("MonthEndYearWeekName", True, 14000)
    )
    year_month_name: Column = field(
        default_factory=lambda: Column("YearMonthName", True, 15000)
    )
    month_year_name: Column = field(
        default_factory=lambda: Column("MonthYearName", True, 16000)
    )
    year_quarter_name: Column = field(
        default_factory=lambda: Column("YearQuarterName", True, 17000)
    )
    year: Column = field(default_factory=lambda: Column("Year", True, 18000))
    month_start_year_week: Column = field(
        default_factory=lambda: Column("MonthStartYearWeek", True, 19000)
    )
    month_end_year_week: Column = field(
        default_factory=lambda: Column("MonthEndYearWeek", True, 20000)
    )
    year_month: Column = field(default_factory=lambda: Column("YearMonth", True, 21000))
    year_quarter: Column = field(
        default_factory=lambda: Column("YearQuarter", True, 22000)
    )
    month_start_day_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartDayOfQuarter", True, 23000)
    )
    month_end_day_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndDayOfQuarter", True, 24000)
    )
    month_start_day_of_year: Column = field(
        default_factory=lambda: Column("MonthStartDayOfYear", True, 25000)
    )
    month_end_day_of_year: Column = field(
        default_factory=lambda: Column("MonthEndDayOfYear", True, 26000)
    )
    month_start_week_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartWeekOfQuarter", True, 27000)
    )
    month_end_week_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndWeekOfQuarter", True, 28000)
    )
    month_start_week_of_year: Column = field(
        default_factory=lambda: Column("MonthStartWeekOfYear", True, 29000)
    )
    month_end_week_of_year: Column = field(
        default_factory=lambda: Column("MonthEndWeekOfYear", True, 30000)
    )
    month_of_quarter: Column = field(
        default_factory=lambda: Column("MonthOfQuarter", True, 31000)
    )
    quarter: Column = field(default_factory=lambda: Column("Quarter", True, 32000))
    days_in_month: Column = field(
        default_factory=lambda: Column("DaysInMonth", True, 33000)
    )
    days_in_quarter: Column = field(
        default_factory=lambda: Column("DaysInQuarter", True, 34000)
    )
    days_in_year: Column = field(
        default_factory=lambda: Column("DaysInYear", True, 35000)
    )
    current_month_flag: Column = field(
        default_factory=lambda: Column("CurrentMonthFlag", True, 36000)
    )
    prior_month_flag: Column = field(
        default_factory=lambda: Column("PriorMonthFlag", True, 37000)
    )
    next_month_flag: Column = field(
        default_factory=lambda: Column("NextMonthFlag", True, 38000)
    )
    current_quarter_flag: Column = field(
        default_factory=lambda: Column("CurrentQuarterFlag", True, 39000)
    )
    prior_quarter_flag: Column = field(
        default_factory=lambda: Column("PriorQuarterFlag", True, 40000)
    )
    next_quarter_flag: Column = field(
        default_factory=lambda: Column("NextQuarterFlag", True, 41000)
    )
    current_year_flag: Column = field(
        default_factory=lambda: Column("CurrentYearFlag", True, 42000)
    )
    prior_year_flag: Column = field(
        default_factory=lambda: Column("PriorYearFlag", True, 43000)
    )
    next_year_flag: Column = field(
        default_factory=lambda: Column("NextYearFlag", True, 44000)
    )
    first_day_of_month_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfMonthFlag", True, 45000)
    )
    last_day_of_month_flag: Column = field(
        default_factory=lambda: Column("LastDayOfMonthFlag", True, 46000)
    )
    first_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfQuarterFlag", True, 47000)
    )
    last_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("LastDayOfQuarterFlag", True, 48000)
    )
    first_day_of_year_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfYearFlag", True, 49000)
    )
    last_day_of_year_flag: Column = field(
        default_factory=lambda: Column("LastDayOfYearFlag", True, 50000)
    )
    month_start_fraction_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartFractionOfQuarter", True, 51000)
    )
    month_end_fraction_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndFractionOfQuarter", True, 52000)
    )
    month_start_fraction_of_year: Column = field(
        default_factory=lambda: Column("MonthStartFractionOfYear", True, 53000)
    )
    month_end_fraction_of_year: Column = field(
        default_factory=lambda: Column("MonthEndFractionOfYear", True, 54000)
    )
    current_quarter_start: Column = field(
        default_factory=lambda: Column("CurrentQuarterStart", True, 55000)
    )
    current_quarter_end: Column = field(
        default_factory=lambda: Column("CurrentQuarterEnd", True, 56000)
    )
    current_year_start: Column = field(
        default_factory=lambda: Column("CurrentYearStart", True, 57000)
    )
    current_year_end: Column = field(
        default_factory=lambda: Column("CurrentYearEnd", True, 58000)
    )
    prior_month_start: Column = field(
        default_factory=lambda: Column("PriorMonthStart", True, 59000)
    )
    prior_month_end: Column = field(
        default_factory=lambda: Column("PriorMonthEnd", True, 60000)
    )
    prior_quarter_start: Column = field(
        default_factory=lambda: Column("PriorQuarterStart", True, 61000)
    )
    prior_quarter_end: Column = field(
        default_factory=lambda: Column("PriorQuarterEnd", True, 62000)
    )
    prior_year_start: Column = field(
        default_factory=lambda: Column("PriorYearStart", True, 63000)
    )
    prior_year_end: Column = field(
        default_factory=lambda: Column("PriorYearEnd", True, 64000)
    )
    next_month_start: Column = field(
        default_factory=lambda: Column("NextMonthStart", True, 65000)
    )
    next_month_end: Column = field(
        default_factory=lambda: Column("NextMonthEnd", True, 66000)
    )
    next_quarter_start: Column = field(
        default_factory=lambda: Column("NextQuarterStart", True, 67000)
    )
    next_quarter_end: Column = field(
        default_factory=lambda: Column("NextQuarterEnd", True, 68000)
    )
    next_year_start: Column = field(
        default_factory=lambda: Column("NextYearStart", True, 69000)
    )
    next_year_end: Column = field(
        default_factory=lambda: Column("NextYearEnd", True, 70000)
    )
    month_start_quarterly_burnup: Column = field(
        default_factory=lambda: Column("MonthStartQuarterlyBurnup", True, 71000)
    )
    month_end_quarterly_burnup: Column = field(
        default_factory=lambda: Column("MonthEndQuarterlyBurnup", True, 72000)
    )
    month_start_yearly_burnup: Column = field(
        default_factory=lambda: Column("MonthStartYearlyBurnup", True, 73000)
    )
    month_end_yearly_burnup: Column = field(
        default_factory=lambda: Column("MonthEndYearlyBurnup", True, 74000)
    )


@dataclass(frozen=True)
class DimCalendarMonthConfig:
    table_schema: str = "dbo"
    table_name: str = "DimCalendarMonth"
    columns: DimCalendarMonthColumns = field(
        default_factory=lambda: DimCalendarMonthColumns()
    )
    column_factory: Callable[[str, Column], Column] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v["sort_index"] for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys
        ), "there was a duplicate sort key in the column definitions for DimCalendarMonthColumn."

        if self.column_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_col = self.column_factory(k, v)
                assert isinstance(
                    new_col, Column
                ), f"column_factory returned a value that was not a column. This is not allowed. Value: {new_col}"
                new_cols[k] = self.column_factory(v)

            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass
class Config:
    output_dir: Path = field(default_factory=lambda: Path("./output"))
    clear_output_dir: bool = False
    date_range: DateRange = field(default_factory=DateRange)
    fiscal: FiscalConfig = field(default_factory=FiscalConfig)
    time_zone: tzinfo = field(default_factory=lambda: timezone("US/Mountain"))
    holidays: HolidayConfig = field(default_factory=HolidayConfig)
    dim_date: DimDateConfig = field(default_factory=DimDateConfig)
    dim_fiscal_month: DimFiscalMonthConfig = field(default_factory=DimFiscalMonthConfig)
    dim_calendar_month: DimCalendarMonthConfig = field(
        default_factory=DimCalendarMonthConfig
    )
