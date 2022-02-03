from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Callable


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
    date_key: Column = field(default_factory=lambda: Column("DateKey", True, 0))
    the_date: Column = field(default_factory=lambda: Column("TheDate", True, 1))
    iso_date_name: Column = field(
        default_factory=lambda: Column("ISODateName", True, 2)
    )
    american_date_name: Column = field(
        default_factory=lambda: Column("AmericanDateName", True, 3)
    )
    day_of_week_name: Column = field(
        default_factory=lambda: Column("DayOfWeekName", True, 4)
    )
    day_of_week_abbrev: Column = field(
        default_factory=lambda: Column("DayOfWeekAbbrev", True, 5)
    )
    month_name: Column = field(default_factory=lambda: Column("MonthName", True, 6))
    month_abbrev: Column = field(default_factory=lambda: Column("MonthAbbrev", True, 7))
    year_week_name: Column = field(
        default_factory=lambda: Column("YearWeekName", True, 8)
    )
    year_month_name: Column = field(
        default_factory=lambda: Column("YearMonthName", True, 9)
    )
    month_year_name: Column = field(
        default_factory=lambda: Column("MonthYearName", True, 10)
    )
    year_quarter_name: Column = field(
        default_factory=lambda: Column("YearQuarterName", True, 11)
    )
    year: Column = field(default_factory=lambda: Column("Year", True, 12))
    year_week: Column = field(default_factory=lambda: Column("YearWeek", True, 13))
    iso_year_week_code: Column = field(
        default_factory=lambda: Column("ISOYearWeekCode", True, 14)
    )
    year_month: Column = field(default_factory=lambda: Column("YearMonth", True, 15))
    year_quarter: Column = field(
        default_factory=lambda: Column("YearQuarter", True, 16)
    )
    day_of_week_starting_monday: Column = field(
        default_factory=lambda: Column("DayOfWeekStartingMonday", True, 17)
    )
    day_of_week: Column = field(default_factory=lambda: Column("DayOfWeek", True, 18))
    day_of_month: Column = field(default_factory=lambda: Column("DayOfMonth", True, 19))
    day_of_quarter: Column = field(
        default_factory=lambda: Column("DayOfQuarter", True, 20)
    )
    day_of_year: Column = field(default_factory=lambda: Column("DayOfYear", True, 21))
    week_of_quarter: Column = field(
        default_factory=lambda: Column("WeekOfQuarter", True, 22)
    )
    week_of_year: Column = field(default_factory=lambda: Column("WeekOfYear", True, 23))
    iso_week_of_year: Column = field(
        default_factory=lambda: Column("ISOWeekOfYear", True, 24)
    )
    month: Column = field(default_factory=lambda: Column("Month", True, 25))
    month_of_quarter: Column = field(
        default_factory=lambda: Column("MonthOfQuarter", True, 26)
    )
    quarter: Column = field(default_factory=lambda: Column("Quarter", True, 27))
    days_in_month: Column = field(
        default_factory=lambda: Column("DaysInMonth", True, 28)
    )
    days_in_quarter: Column = field(
        default_factory=lambda: Column("DaysInQuarter", True, 29)
    )
    days_in_year: Column = field(default_factory=lambda: Column("DaysInYear", True, 30))
    day_offset_from_today: Column = field(
        default_factory=lambda: Column("DayOffsetFromToday", True, 31)
    )
    month_offset_from_today: Column = field(
        default_factory=lambda: Column("MonthOffsetFromToday", True, 32)
    )
    quarter_offset_from_today: Column = field(
        default_factory=lambda: Column("QuarterOffsetFromToday", True, 33)
    )
    year_offset_from_today: Column = field(
        default_factory=lambda: Column("YearOffsetFromToday", True, 34)
    )
    today_flag: Column = field(default_factory=lambda: Column("TodayFlag", True, 35))
    current_week_starting_monday_flag: Column = field(
        default_factory=lambda: Column("CurrentWeekStartingMondayFlag", True, 36)
    )
    current_week_flag: Column = field(
        default_factory=lambda: Column("CurrentWeekFlag", True, 37)
    )
    prior_week_flag: Column = field(
        default_factory=lambda: Column("PriorWeekFlag", True, 38)
    )
    next_week_flag: Column = field(
        default_factory=lambda: Column("NextWeekFlag", True, 39)
    )
    current_month_flag: Column = field(
        default_factory=lambda: Column("CurrentMonthFlag", True, 40)
    )
    prior_month_flag: Column = field(
        default_factory=lambda: Column("PriorMonthFlag", True, 41)
    )
    next_month_flag: Column = field(
        default_factory=lambda: Column("NextMonthFlag", True, 42)
    )
    current_quarter_flag: Column = field(
        default_factory=lambda: Column("CurrentQuarterFlag", True, 43)
    )
    prior_quarter_flag: Column = field(
        default_factory=lambda: Column("PriorQuarterFlag", True, 44)
    )
    next_quarter_flag: Column = field(
        default_factory=lambda: Column("NextQuarterFlag", True, 45)
    )
    current_year_flag: Column = field(
        default_factory=lambda: Column("CurrentYearFlag", True, 46)
    )
    prior_year_flag: Column = field(
        default_factory=lambda: Column("PriorYearFlag", True, 47)
    )
    next_year_flag: Column = field(
        default_factory=lambda: Column("NextYearFlag", True, 48)
    )
    weekday_flag: Column = field(
        default_factory=lambda: Column("WeekdayFlag", True, 49)
    )
    business_day_flag: Column = field(
        default_factory=lambda: Column("BusinessDayFlag", True, 50)
    )
    first_day_of_month_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfMonthFlag", True, 51)
    )
    last_day_of_month_flag: Column = field(
        default_factory=lambda: Column("LastDayOfMonthFlag", True, 52)
    )
    first_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfQuarterFlag", True, 53)
    )
    last_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("LastDayOfQuarterFlag", True, 54)
    )
    first_day_of_year_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfYearFlag", True, 55)
    )
    last_day_of_year_flag: Column = field(
        default_factory=lambda: Column("LastDayOfYearFlag", True, 56)
    )
    fraction_of_week: Column = field(
        default_factory=lambda: Column("FractionOfWeek", True, 57)
    )
    fraction_of_month: Column = field(
        default_factory=lambda: Column("FractionOfMonth", True, 58)
    )
    fraction_of_quarter: Column = field(
        default_factory=lambda: Column("FractionOfQuarter", True, 59)
    )
    fraction_of_year: Column = field(
        default_factory=lambda: Column("FractionOfYear", True, 60)
    )
    prior_day: Column = field(default_factory=lambda: Column("PriorDay", True, 61))
    next_day: Column = field(default_factory=lambda: Column("NextDay", True, 62))
    same_day_prior_week: Column = field(
        default_factory=lambda: Column("SameDayPriorWeek", True, 63)
    )
    same_day_prior_month: Column = field(
        default_factory=lambda: Column("SameDayPriorMonth", True, 64)
    )
    same_day_prior_quarter: Column = field(
        default_factory=lambda: Column("SameDayPriorQuarter", True, 65)
    )
    same_day_prior_year: Column = field(
        default_factory=lambda: Column("SameDayPriorYear", True, 66)
    )
    same_day_next_week: Column = field(
        default_factory=lambda: Column("SameDayNextWeek", True, 67)
    )
    same_day_next_month: Column = field(
        default_factory=lambda: Column("SameDayNextMonth", True, 68)
    )
    same_day_next_quarter: Column = field(
        default_factory=lambda: Column("SameDayNextQuarter", True, 69)
    )
    same_day_next_year: Column = field(
        default_factory=lambda: Column("SameDayNextYear", True, 70)
    )
    current_week_start: Column = field(
        default_factory=lambda: Column("CurrentWeekStart", True, 71)
    )
    current_week_end: Column = field(
        default_factory=lambda: Column("CurrentWeekEnd", True, 72)
    )
    current_month_start: Column = field(
        default_factory=lambda: Column("CurrentMonthStart", True, 73)
    )
    current_month_end: Column = field(
        default_factory=lambda: Column("CurrentMonthEnd", True, 74)
    )
    current_quarter_start: Column = field(
        default_factory=lambda: Column("CurrentQuarterStart", True, 75)
    )
    current_quarter_end: Column = field(
        default_factory=lambda: Column("CurrentQuarterEnd", True, 76)
    )
    current_year_start: Column = field(
        default_factory=lambda: Column("CurrentYearStart", True, 77)
    )
    current_year_end: Column = field(
        default_factory=lambda: Column("CurrentYearEnd", True, 78)
    )
    prior_week_start: Column = field(
        default_factory=lambda: Column("PriorWeekStart", True, 79)
    )
    prior_week_end: Column = field(
        default_factory=lambda: Column("PriorWeekEnd", True, 80)
    )
    prior_month_start: Column = field(
        default_factory=lambda: Column("PriorMonthStart", True, 81)
    )
    prior_month_end: Column = field(
        default_factory=lambda: Column("PriorMonthEnd", True, 82)
    )
    prior_quarter_start: Column = field(
        default_factory=lambda: Column("PriorQuarterStart", True, 83)
    )
    prior_quarter_end: Column = field(
        default_factory=lambda: Column("PriorQuarterEnd", True, 84)
    )
    prior_year_start: Column = field(
        default_factory=lambda: Column("PriorYearStart", True, 85)
    )
    prior_year_end: Column = field(
        default_factory=lambda: Column("PriorYearEnd", True, 86)
    )
    next_week_start: Column = field(
        default_factory=lambda: Column("NextWeekStart", True, 87)
    )
    next_week_end: Column = field(
        default_factory=lambda: Column("NextWeekEnd", True, 88)
    )
    next_month_start: Column = field(
        default_factory=lambda: Column("NextMonthStart", True, 89)
    )
    next_month_end: Column = field(
        default_factory=lambda: Column("NextMonthEnd", True, 90)
    )
    next_quarter_start: Column = field(
        default_factory=lambda: Column("NextQuarterStart", True, 91)
    )
    next_quarter_end: Column = field(
        default_factory=lambda: Column("NextQuarterEnd", True, 92)
    )
    next_year_start: Column = field(
        default_factory=lambda: Column("NextYearStart", True, 93)
    )
    next_year_end: Column = field(
        default_factory=lambda: Column("NextYearEnd", True, 94)
    )
    weekly_burnup_starting_monday: Column = field(
        default_factory=lambda: Column("WeeklyBurnupStartingMonday", True, 95)
    )
    weekly_burnup: Column = field(
        default_factory=lambda: Column("WeeklyBurnup", True, 96)
    )
    monthly_burnup: Column = field(
        default_factory=lambda: Column("MonthlyBurnup", True, 97)
    )
    quarterly_burnup: Column = field(
        default_factory=lambda: Column("QuarterlyBurnup", True, 98)
    )
    yearly_burnup: Column = field(
        default_factory=lambda: Column("YearlyBurnup", True, 99)
    )
    fiscal_month_name: Column = field(
        default_factory=lambda: Column("FiscalMonthName", True, 100)
    )
    fiscal_month_abbrev: Column = field(
        default_factory=lambda: Column("FiscalMonthAbbrev", True, 101)
    )
    fiscal_year_week_name: Column = field(
        default_factory=lambda: Column("FiscalYearWeekName", True, 102)
    )
    fiscal_year_month_name: Column = field(
        default_factory=lambda: Column("FiscalYearMonthName", True, 103)
    )
    fiscal_month_year_name: Column = field(
        default_factory=lambda: Column("FiscalMonthYearName", True, 104)
    )
    fiscal_year_quarter_name: Column = field(
        default_factory=lambda: Column("FiscalYearQuarterName", True, 105)
    )
    fiscal_year: Column = field(default_factory=lambda: Column("FiscalYear", True, 106))
    fiscal_year_week: Column = field(
        default_factory=lambda: Column("FiscalYearWeek", True, 107)
    )
    fiscal_year_month: Column = field(
        default_factory=lambda: Column("FiscalYearMonth", True, 108)
    )
    fiscal_year_quarter: Column = field(
        default_factory=lambda: Column("FiscalYearQuarter", True, 109)
    )
    fiscal_day_of_month: Column = field(
        default_factory=lambda: Column("FiscalDayOfMonth", True, 110)
    )
    fiscal_day_of_quarter: Column = field(
        default_factory=lambda: Column("FiscalDayOfQuarter", True, 111)
    )
    fiscal_day_of_year: Column = field(
        default_factory=lambda: Column("FiscalDayOfYear", True, 112)
    )
    fiscal_week_of_quarter: Column = field(
        default_factory=lambda: Column("FiscalWeekOfQuarter", True, 113)
    )
    fiscal_week_of_year: Column = field(
        default_factory=lambda: Column("FiscalWeekOfYear", True, 114)
    )
    fiscal_month: Column = field(
        default_factory=lambda: Column("FiscalMonth", True, 115)
    )
    fiscal_month_of_quarter: Column = field(
        default_factory=lambda: Column("FiscalMonthOfQuarter", True, 116)
    )
    fiscal_quarter: Column = field(
        default_factory=lambda: Column("FiscalQuarter", True, 117)
    )
    fiscal_days_in_month: Column = field(
        default_factory=lambda: Column("FiscalDaysInMonth", True, 118)
    )
    fiscal_days_in_quarter: Column = field(
        default_factory=lambda: Column("FiscalDaysInQuarter", True, 119)
    )
    fiscal_days_in_year: Column = field(
        default_factory=lambda: Column("FiscalDaysInYear", True, 120)
    )
    fiscal_current_month_flag: Column = field(
        default_factory=lambda: Column("FiscalCurrentMonthFlag", True, 121)
    )
    fiscal_prior_month_flag: Column = field(
        default_factory=lambda: Column("FiscalPriorMonthFlag", True, 122)
    )
    fiscal_next_month_flag: Column = field(
        default_factory=lambda: Column("FiscalNextMonthFlag", True, 123)
    )
    fiscal_current_quarter_flag: Column = field(
        default_factory=lambda: Column("FiscalCurrentQuarterFlag", True, 124)
    )
    fiscal_prior_quarter_flag: Column = field(
        default_factory=lambda: Column("FiscalPriorQuarterFlag", True, 125)
    )
    fiscal_next_quarter_flag: Column = field(
        default_factory=lambda: Column("FiscalNextQuarterFlag", True, 126)
    )
    fiscal_current_year_flag: Column = field(
        default_factory=lambda: Column("FiscalCurrentYearFlag", True, 127)
    )
    fiscal_prior_year_flag: Column = field(
        default_factory=lambda: Column("FiscalPriorYearFlag", True, 128)
    )
    fiscal_next_year_flag: Column = field(
        default_factory=lambda: Column("FiscalNextYearFlag", True, 129)
    )
    fiscal_first_day_of_month_flag: Column = field(
        default_factory=lambda: Column("FiscalFirstDayOfMonthFlag", True, 130)
    )
    fiscal_last_day_of_month_flag: Column = field(
        default_factory=lambda: Column("FiscalLastDayOfMonthFlag", True, 131)
    )
    fiscal_first_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("FiscalFirstDayOfQuarterFlag", True, 132)
    )
    fiscal_last_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("FiscalLastDayOfQuarterFlag", True, 133)
    )
    fiscal_first_day_of_year_flag: Column = field(
        default_factory=lambda: Column("FiscalFirstDayOfYearFlag", True, 134)
    )
    fiscal_last_day_of_year_flag: Column = field(
        default_factory=lambda: Column("FiscalLastDayOfYearFlag", True, 135)
    )
    fiscal_fraction_of_month: Column = field(
        default_factory=lambda: Column("FiscalFractionOfMonth", True, 136)
    )
    fiscal_fraction_of_quarter: Column = field(
        default_factory=lambda: Column("FiscalFractionOfQuarter", True, 137)
    )
    fiscal_fraction_of_year: Column = field(
        default_factory=lambda: Column("FiscalFractionOfYear", True, 138)
    )
    fiscal_current_month_start: Column = field(
        default_factory=lambda: Column("FiscalCurrentMonthStart", True, 139)
    )
    fiscal_current_month_end: Column = field(
        default_factory=lambda: Column("FiscalCurrentMonthEnd", True, 140)
    )
    fiscal_current_quarter_start: Column = field(
        default_factory=lambda: Column("FiscalCurrentQuarterStart", True, 141)
    )
    fiscal_current_quarter_end: Column = field(
        default_factory=lambda: Column("FiscalCurrentQuarterEnd", True, 142)
    )
    fiscal_current_year_start: Column = field(
        default_factory=lambda: Column("FiscalCurrentYearStart", True, 143)
    )
    fiscal_current_year_end: Column = field(
        default_factory=lambda: Column("FiscalCurrentYearEnd", True, 144)
    )
    fiscal_prior_month_start: Column = field(
        default_factory=lambda: Column("FiscalPriorMonthStart", True, 145)
    )
    fiscal_prior_month_end: Column = field(
        default_factory=lambda: Column("FiscalPriorMonthEnd", True, 146)
    )
    fiscal_prior_quarter_start: Column = field(
        default_factory=lambda: Column("FiscalPriorQuarterStart", True, 147)
    )
    fiscal_prior_quarter_end: Column = field(
        default_factory=lambda: Column("FiscalPriorQuarterEnd", True, 148)
    )
    fiscal_prior_year_start: Column = field(
        default_factory=lambda: Column("FiscalPriorYearStart", True, 149)
    )
    fiscal_prior_year_end: Column = field(
        default_factory=lambda: Column("FiscalPriorYearEnd", True, 150)
    )
    fiscal_next_month_start: Column = field(
        default_factory=lambda: Column("FiscalNextMonthStart", True, 151)
    )
    fiscal_next_month_end: Column = field(
        default_factory=lambda: Column("FiscalNextMonthEnd", True, 152)
    )
    fiscal_next_quarter_start: Column = field(
        default_factory=lambda: Column("FiscalNextQuarterStart", True, 153)
    )
    fiscal_next_quarter_end: Column = field(
        default_factory=lambda: Column("FiscalNextQuarterEnd", True, 154)
    )
    fiscal_next_year_start: Column = field(
        default_factory=lambda: Column("FiscalNextYearStart", True, 155)
    )
    fiscal_next_year_end: Column = field(
        default_factory=lambda: Column("FiscalNextYearEnd", True, 156)
    )
    fiscal_monthly_burnup: Column = field(
        default_factory=lambda: Column("FiscalMonthlyBurnup", True, 157)
    )
    fiscal_quarterly_burnup: Column = field(
        default_factory=lambda: Column("FiscalQuarterlyBurnup", True, 158)
    )
    fiscal_yearly_burnup: Column = field(
        default_factory=lambda: Column("FiscalYearlyBurnup", True, 159)
    )


@dataclass(frozen=True)
class DimDateConfig:
    table_schema: str = "dbo"
    table_name: str = "DimDate"
    columns: DimDateColumns = field(default_factory=lambda: DimDateColumns())
    column_name_factory: Callable[[str], str] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v["sort_index"] for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys
        ), "there was a duplicate sort key in the column definitions for DimDateColumn."

        if self.column_name_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_cols[k] = Column(
                    self.column_name_factory(v["name"]), v["include"], v["sort_index"]
                )
            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass(frozen=True)
class DimFiscalMonthColumns:
    month_start_key: Column = field(
        default_factory=lambda: Column("MonthStartKey", True, 0)
    )
    month_end_key: Column = field(
        default_factory=lambda: Column("MonthEndKey", True, 1)
    )
    month_start_date: Column = field(
        default_factory=lambda: Column("MonthStartDate", True, 2)
    )
    month_end_date: Column = field(
        default_factory=lambda: Column("MonthEndDate", True, 3)
    )
    month_start_iso_date_name: Column = field(
        default_factory=lambda: Column("MonthStartISODateName", True, 4)
    )
    month_end_iso_date_name: Column = field(
        default_factory=lambda: Column("MonthEndISODateName", True, 5)
    )
    month_start_american_date_name: Column = field(
        default_factory=lambda: Column("MonthStartAmericanDateName", True, 6)
    )
    month_end_american_date_name: Column = field(
        default_factory=lambda: Column("MonthEndAmericanDateName", True, 7)
    )
    month_name: Column = field(default_factory=lambda: Column("MonthName", True, 8))
    month_abbrev: Column = field(default_factory=lambda: Column("MonthAbbrev", True, 9))
    month_start_year_week_name: Column = field(
        default_factory=lambda: Column("MonthStartYearWeekName", True, 10)
    )
    month_end_year_week_name: Column = field(
        default_factory=lambda: Column("MonthEndYearWeekName", True, 11)
    )
    year_month_name: Column = field(
        default_factory=lambda: Column("YearMonthName", True, 12)
    )
    month_year_name: Column = field(
        default_factory=lambda: Column("MonthYearName", True, 13)
    )
    year_quarter_name: Column = field(
        default_factory=lambda: Column("YearQuarterName", True, 14)
    )
    year: Column = field(default_factory=lambda: Column("Year", True, 15))
    month_start_year_week: Column = field(
        default_factory=lambda: Column("MonthStartYearWeek", True, 16)
    )
    month_end_year_week: Column = field(
        default_factory=lambda: Column("MonthEndYearWeek", True, 17)
    )
    year_month: Column = field(default_factory=lambda: Column("YearMonth", True, 18))
    year_quarter: Column = field(
        default_factory=lambda: Column("YearQuarter", True, 19)
    )
    month_start_day_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartDayOfQuarter", True, 20)
    )
    month_end_day_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndDayOfQuarter", True, 21)
    )
    month_start_day_of_year: Column = field(
        default_factory=lambda: Column("MonthStartDayOfYear", True, 22)
    )
    month_end_day_of_year: Column = field(
        default_factory=lambda: Column("MonthEndDayOfYear", True, 23)
    )
    month_start_week_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartWeekOfQuarter", True, 24)
    )
    month_end_week_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndWeekOfQuarter", True, 25)
    )
    month_start_week_of_year: Column = field(
        default_factory=lambda: Column("MonthStartWeekOfYear", True, 26)
    )
    month_end_week_of_year: Column = field(
        default_factory=lambda: Column("MonthEndWeekOfYear", True, 27)
    )
    month_of_quarter: Column = field(
        default_factory=lambda: Column("MonthOfQuarter", True, 28)
    )
    quarter: Column = field(default_factory=lambda: Column("Quarter", True, 29))
    days_in_month: Column = field(
        default_factory=lambda: Column("DaysInMonth", True, 30)
    )
    days_in_quarter: Column = field(
        default_factory=lambda: Column("DaysInQuarter", True, 31)
    )
    days_in_year: Column = field(default_factory=lambda: Column("DaysInYear", True, 32))
    current_month_flag: Column = field(
        default_factory=lambda: Column("CurrentMonthFlag", True, 33)
    )
    prior_month_flag: Column = field(
        default_factory=lambda: Column("PriorMonthFlag", True, 34)
    )
    next_month_flag: Column = field(
        default_factory=lambda: Column("NextMonthFlag", True, 35)
    )
    current_quarter_flag: Column = field(
        default_factory=lambda: Column("CurrentQuarterFlag", True, 36)
    )
    prior_quarter_flag: Column = field(
        default_factory=lambda: Column("PriorQuarterFlag", True, 37)
    )
    next_quarter_flag: Column = field(
        default_factory=lambda: Column("NextQuarterFlag", True, 38)
    )
    current_year_flag: Column = field(
        default_factory=lambda: Column("CurrentYearFlag", True, 39)
    )
    prior_year_flag: Column = field(
        default_factory=lambda: Column("PriorYearFlag", True, 40)
    )
    next_year_flag: Column = field(
        default_factory=lambda: Column("NextYearFlag", True, 41)
    )
    first_day_of_month_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfMonthFlag", True, 42)
    )
    last_day_of_month_flag: Column = field(
        default_factory=lambda: Column("LastDayOfMonthFlag", True, 43)
    )
    first_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfQuarterFlag", True, 44)
    )
    last_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("LastDayOfQuarterFlag", True, 45)
    )
    first_day_of_year_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfYearFlag", True, 46)
    )
    last_day_of_year_flag: Column = field(
        default_factory=lambda: Column("LastDayOfYearFlag", True, 47)
    )
    month_start_fraction_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartFractionOfQuarter", True, 48)
    )
    month_end_fraction_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndFractionOfQuarter", True, 49)
    )
    month_start_fraction_of_year: Column = field(
        default_factory=lambda: Column("MonthStartFractionOfYear", True, 50)
    )
    month_end_fraction_of_year: Column = field(
        default_factory=lambda: Column("MonthEndFractionOfYear", True, 51)
    )
    month_start_current_quarter_start: Column = field(
        default_factory=lambda: Column("MonthStartCurrentQuarterStart", True, 52)
    )
    month_start_current_quarter_end: Column = field(
        default_factory=lambda: Column("MonthStartCurrentQuarterEnd", True, 53)
    )
    month_start_current_year_start: Column = field(
        default_factory=lambda: Column("MonthStartCurrentYearStart", True, 54)
    )
    month_start_current_year_end: Column = field(
        default_factory=lambda: Column("MonthStartCurrentYearEnd", True, 55)
    )
    month_start_prior_month_start: Column = field(
        default_factory=lambda: Column("MonthStartPriorMonthStart", True, 56)
    )
    month_start_prior_month_end: Column = field(
        default_factory=lambda: Column("MonthStartPriorMonthEnd", True, 57)
    )
    month_start_prior_quarter_start: Column = field(
        default_factory=lambda: Column("MonthStartPriorQuarterStart", True, 58)
    )
    month_start_prior_quarter_end: Column = field(
        default_factory=lambda: Column("MonthStartPriorQuarterEnd", True, 59)
    )
    month_start_prior_year_start: Column = field(
        default_factory=lambda: Column("MonthStartPriorYearStart", True, 60)
    )
    month_start_prior_year_end: Column = field(
        default_factory=lambda: Column("MonthStartPriorYearEnd", True, 61)
    )
    month_start_next_month_start: Column = field(
        default_factory=lambda: Column("MonthStartNextMonthStart", True, 62)
    )
    month_start_next_month_end: Column = field(
        default_factory=lambda: Column("MonthStartNextMonthEnd", True, 63)
    )
    month_start_next_quarter_start: Column = field(
        default_factory=lambda: Column("MonthStartNextQuarterStart", True, 64)
    )
    month_start_next_quarter_end: Column = field(
        default_factory=lambda: Column("MonthStartNextQuarterEnd", True, 65)
    )
    month_start_next_year_start: Column = field(
        default_factory=lambda: Column("MonthStartNextYearStart", True, 66)
    )
    month_start_next_year_end: Column = field(
        default_factory=lambda: Column("MonthStartNextYearEnd", True, 67)
    )
    month_start_quarterly_burnup: Column = field(
        default_factory=lambda: Column("MonthStartQuarterlyBurnup", True, 68)
    )
    month_end_quarterly_burnup: Column = field(
        default_factory=lambda: Column("MonthEndQuarterlyBurnup", True, 69)
    )
    month_start_yearly_burnup: Column = field(
        default_factory=lambda: Column("MonthStartYearlyBurnup", True, 70)
    )
    month_end_yearly_burnup: Column = field(
        default_factory=lambda: Column("MonthEndYearlyBurnup", True, 71)
    )


@dataclass(frozen=True)
class DimFiscalMonthConfig:
    table_schema: str = "dbo"
    table_name: str = "DimFiscalMonth"
    columns: DimFiscalMonthColumns = field(
        default_factory=lambda: DimFiscalMonthColumns()
    )
    column_name_factory: Callable[[str], str] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v["sort_index"] for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys
        ), "there was a duplicate sort key in the column definitions for DimFiscalMonthColumn."

        if self.column_name_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_cols[k] = Column(
                    self.column_name_factory(v["name"]), v["include"], v["sort_index"]
                )
            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass(frozen=True)
class DimCalendarMonthColumns:
    month_start_key: Column = field(
        default_factory=lambda: Column("MonthStartKey", True, 0)
    )
    month_end_key: Column = field(
        default_factory=lambda: Column("MonthEndKey", True, 1)
    )
    month_start_date: Column = field(
        default_factory=lambda: Column("MonthStartDate", True, 2)
    )
    month_end_date: Column = field(
        default_factory=lambda: Column("MonthEndDate", True, 3)
    )
    month_start_iso_date_name: Column = field(
        default_factory=lambda: Column("MonthStartISODateName", True, 4)
    )
    month_end_iso_date_name: Column = field(
        default_factory=lambda: Column("MonthEndISODateName", True, 5)
    )
    month_start_american_date_name: Column = field(
        default_factory=lambda: Column("MonthStartAmericanDateName", True, 6)
    )
    month_end_american_date_name: Column = field(
        default_factory=lambda: Column("MonthEndAmericanDateName", True, 7)
    )
    month_name: Column = field(default_factory=lambda: Column("MonthName", True, 8))
    month_abbrev: Column = field(default_factory=lambda: Column("MonthAbbrev", True, 9))
    month_start_year_week_name: Column = field(
        default_factory=lambda: Column("MonthStartYearWeekName", True, 10)
    )
    month_end_year_week_name: Column = field(
        default_factory=lambda: Column("MonthEndYearWeekName", True, 11)
    )
    year_month_name: Column = field(
        default_factory=lambda: Column("YearMonthName", True, 12)
    )
    month_year_name: Column = field(
        default_factory=lambda: Column("MonthYearName", True, 13)
    )
    year_quarter_name: Column = field(
        default_factory=lambda: Column("YearQuarterName", True, 14)
    )
    year: Column = field(default_factory=lambda: Column("Year", True, 15))
    month_start_year_week: Column = field(
        default_factory=lambda: Column("MonthStartYearWeek", True, 16)
    )
    month_end_year_week: Column = field(
        default_factory=lambda: Column("MonthEndYearWeek", True, 17)
    )
    year_month: Column = field(default_factory=lambda: Column("YearMonth", True, 18))
    year_quarter: Column = field(
        default_factory=lambda: Column("YearQuarter", True, 19)
    )
    month_start_day_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartDayOfQuarter", True, 20)
    )
    month_end_day_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndDayOfQuarter", True, 21)
    )
    month_start_day_of_year: Column = field(
        default_factory=lambda: Column("MonthStartDayOfYear", True, 22)
    )
    month_end_day_of_year: Column = field(
        default_factory=lambda: Column("MonthEndDayOfYear", True, 23)
    )
    month_start_week_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartWeekOfQuarter", True, 24)
    )
    month_end_week_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndWeekOfQuarter", True, 25)
    )
    month_start_week_of_year: Column = field(
        default_factory=lambda: Column("MonthStartWeekOfYear", True, 26)
    )
    month_end_week_of_year: Column = field(
        default_factory=lambda: Column("MonthEndWeekOfYear", True, 27)
    )
    month_of_quarter: Column = field(
        default_factory=lambda: Column("MonthOfQuarter", True, 28)
    )
    quarter: Column = field(default_factory=lambda: Column("Quarter", True, 29))
    days_in_month: Column = field(
        default_factory=lambda: Column("DaysInMonth", True, 30)
    )
    days_in_quarter: Column = field(
        default_factory=lambda: Column("DaysInQuarter", True, 31)
    )
    days_in_year: Column = field(default_factory=lambda: Column("DaysInYear", True, 32))
    current_month_flag: Column = field(
        default_factory=lambda: Column("CurrentMonthFlag", True, 33)
    )
    prior_month_flag: Column = field(
        default_factory=lambda: Column("PriorMonthFlag", True, 34)
    )
    next_month_flag: Column = field(
        default_factory=lambda: Column("NextMonthFlag", True, 35)
    )
    current_quarter_flag: Column = field(
        default_factory=lambda: Column("CurrentQuarterFlag", True, 36)
    )
    prior_quarter_flag: Column = field(
        default_factory=lambda: Column("PriorQuarterFlag", True, 37)
    )
    next_quarter_flag: Column = field(
        default_factory=lambda: Column("NextQuarterFlag", True, 38)
    )
    current_year_flag: Column = field(
        default_factory=lambda: Column("CurrentYearFlag", True, 39)
    )
    prior_year_flag: Column = field(
        default_factory=lambda: Column("PriorYearFlag", True, 40)
    )
    next_year_flag: Column = field(
        default_factory=lambda: Column("NextYearFlag", True, 41)
    )
    first_day_of_month_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfMonthFlag", True, 42)
    )
    last_day_of_month_flag: Column = field(
        default_factory=lambda: Column("LastDayOfMonthFlag", True, 43)
    )
    first_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfQuarterFlag", True, 44)
    )
    last_day_of_quarter_flag: Column = field(
        default_factory=lambda: Column("LastDayOfQuarterFlag", True, 45)
    )
    first_day_of_year_flag: Column = field(
        default_factory=lambda: Column("FirstDayOfYearFlag", True, 46)
    )
    last_day_of_year_flag: Column = field(
        default_factory=lambda: Column("LastDayOfYearFlag", True, 47)
    )
    month_start_fraction_of_quarter: Column = field(
        default_factory=lambda: Column("MonthStartFractionOfQuarter", True, 48)
    )
    month_end_fraction_of_quarter: Column = field(
        default_factory=lambda: Column("MonthEndFractionOfQuarter", True, 49)
    )
    month_start_fraction_of_year: Column = field(
        default_factory=lambda: Column("MonthStartFractionOfYear", True, 50)
    )
    month_end_fraction_of_year: Column = field(
        default_factory=lambda: Column("MonthEndFractionOfYear", True, 51)
    )
    month_start_current_quarter_start: Column = field(
        default_factory=lambda: Column("MonthStartCurrentQuarterStart", True, 52)
    )
    month_start_current_quarter_end: Column = field(
        default_factory=lambda: Column("MonthStartCurrentQuarterEnd", True, 53)
    )
    month_start_current_year_start: Column = field(
        default_factory=lambda: Column("MonthStartCurrentYearStart", True, 54)
    )
    month_start_current_year_end: Column = field(
        default_factory=lambda: Column("MonthStartCurrentYearEnd", True, 55)
    )
    month_start_prior_month_start: Column = field(
        default_factory=lambda: Column("MonthStartPriorMonthStart", True, 56)
    )
    month_start_prior_month_end: Column = field(
        default_factory=lambda: Column("MonthStartPriorMonthEnd", True, 57)
    )
    month_start_prior_quarter_start: Column = field(
        default_factory=lambda: Column("MonthStartPriorQuarterStart", True, 58)
    )
    month_start_prior_quarter_end: Column = field(
        default_factory=lambda: Column("MonthStartPriorQuarterEnd", True, 59)
    )
    month_start_prior_year_start: Column = field(
        default_factory=lambda: Column("MonthStartPriorYearStart", True, 60)
    )
    month_start_prior_year_end: Column = field(
        default_factory=lambda: Column("MonthStartPriorYearEnd", True, 61)
    )
    month_start_next_month_start: Column = field(
        default_factory=lambda: Column("MonthStartNextMonthStart", True, 62)
    )
    month_start_next_month_end: Column = field(
        default_factory=lambda: Column("MonthStartNextMonthEnd", True, 63)
    )
    month_start_next_quarter_start: Column = field(
        default_factory=lambda: Column("MonthStartNextQuarterStart", True, 64)
    )
    month_start_next_quarter_end: Column = field(
        default_factory=lambda: Column("MonthStartNextQuarterEnd", True, 65)
    )
    month_start_next_year_start: Column = field(
        default_factory=lambda: Column("MonthStartNextYearStart", True, 66)
    )
    month_start_next_year_end: Column = field(
        default_factory=lambda: Column("MonthStartNextYearEnd", True, 67)
    )
    month_start_quarterly_burnup: Column = field(
        default_factory=lambda: Column("MonthStartQuarterlyBurnup", True, 68)
    )
    month_end_quarterly_burnup: Column = field(
        default_factory=lambda: Column("MonthEndQuarterlyBurnup", True, 69)
    )
    month_start_yearly_burnup: Column = field(
        default_factory=lambda: Column("MonthStartYearlyBurnup", True, 70)
    )
    month_end_yearly_burnup: Column = field(
        default_factory=lambda: Column("MonthEndYearlyBurnup", True, 71)
    )


@dataclass(frozen=True)
class DimCalendarMonthConfig:
    table_schema: str = "dbo"
    table_name: str = "DimCalendarMonth"
    columns: DimCalendarMonthColumns = field(
        default_factory=lambda: DimCalendarMonthColumns()
    )
    column_name_factory: Callable[[str], str] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v["sort_index"] for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys
        ), "there was a duplicate sort key in the column definitions for DimCalendarMonthColumn."

        if self.column_name_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_cols[k] = Column(
                    self.column_name_factory(v["name"]), v["include"], v["sort_index"]
                )
            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass
class Config:
    output_dir: Path = field(default_factory=lambda: Path("./output"))
    clear_output_dir: bool = False
    date_range: DateRange = field(default_factory=DateRange)
    fiscal: FiscalConfig = field(default_factory=FiscalConfig)
    time_zone: str = "Mountain Standard Time"
    holidays: HolidayConfig = field(default_factory=HolidayConfig)
    dim_date: DimDateConfig = field(default_factory=DimDateConfig)
    dim_fiscal_month: DimFiscalMonthConfig = field(default_factory=DimFiscalMonthConfig)
    dim_calendar_month: DimCalendarMonthConfig = field(
        default_factory=DimCalendarMonthConfig
    )
