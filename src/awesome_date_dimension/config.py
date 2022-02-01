from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Callable
from pathlib import Path


@dataclass(frozen=True)
class DateRange:
    start_date: datetime.date = datetime.fromisoformat('2000-01-01').date()
    num_years: int = 100

    def __post_init__(self):
        assert self.num_years > 0, 'num_years must be greater than 0.'


@dataclass(frozen=True)
class FiscalConfig:
    fiscal_month_start_day: int = 1
    fiscal_year_start_month: int = 1
    fiscal_month_end_matches_calendar: bool = True
    fiscal_quarter_end_matches_calendar: bool = True
    fiscal_year_end_matches_calendar: bool = True

    def __post_init__(self):
        assert 1 <= self.fiscal_month_start_day <= 28, 'fiscal_month_start_day must be between 1 and 28.'
        assert 1 <= self.fiscal_year_start_month <= 12, 'fiscal_year_start_month must be between 1 and 12.'


@dataclass(frozen=True)
class HolidayType:
    name: str
    generated_column_prefix: str
    included_in_business_day_calc: bool


@dataclass(frozen=True)
class Holiday:
    holiday_name: str
    holiday_date: datetime.date


@dataclass(frozen=True)
class HolidayCalendar:
    holiday_type: HolidayType
    holidays: list[Holiday]


default_company_holidays: HolidayCalendar = HolidayCalendar(
    HolidayType('Company Holiday', 'Company', True),
    [
        Holiday('New Year''s Day', datetime.fromisoformat('2012-01-02')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2012-01-16')),
        Holiday('Memorial Day', datetime.fromisoformat('2012-05-28')),
        Holiday('Independence Day', datetime.fromisoformat('2012-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2012-09-03')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2012-11-22')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2012-11-23')),
        Holiday('Christmas Eve', datetime.fromisoformat('2012-12-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2012-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2013-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2013-01-21')),
        Holiday('Memorial Day', datetime.fromisoformat('2013-05-27')),
        Holiday('Independence Day', datetime.fromisoformat('2013-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2013-09-02')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2013-11-28')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2013-11-29')),
        Holiday('Christmas Eve', datetime.fromisoformat('2013-12-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2013-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2014-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2014-01-20')),
        Holiday('Memorial Day', datetime.fromisoformat('2014-05-26')),
        Holiday('Independence Day', datetime.fromisoformat('2014-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2014-09-01')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2014-11-28')),
        Holiday('Christmas Eve', datetime.fromisoformat('2014-12-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2014-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2015-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2015-01-19')),
        Holiday('Memorial Day', datetime.fromisoformat('2015-05-25')),
        Holiday('Independence Day', datetime.fromisoformat('2015-07-03')),
        Holiday('Labor Day', datetime.fromisoformat('2015-09-07')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2015-11-26')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2015-11-27')),
        Holiday('Christmas Eve', datetime.fromisoformat('2015-12-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2015-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2016-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2016-01-18')),
        Holiday('Memorial Day', datetime.fromisoformat('2016-05-30')),
        Holiday('Independence Day', datetime.fromisoformat('2016-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2016-09-05')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2016-11-24')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2016-11-25')),
        Holiday('Christmas Eve', datetime.fromisoformat('2016-12-23')),
        Holiday('Christmas Day', datetime.fromisoformat('2016-12-26')),

        Holiday('New Year''s Day', datetime.fromisoformat('2017-01-02')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2017-01-16')),
        Holiday('Memorial Day', datetime.fromisoformat('2017-05-29')),
        Holiday('Independence Day', datetime.fromisoformat('2017-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2017-09-04')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2017-11-23')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2017-11-24')),
        Holiday('Christmas Eve', datetime.fromisoformat('2017-12-25')),
        Holiday('Christmas Day', datetime.fromisoformat('2017-12-26')),

        Holiday('New Year''s Day', datetime.fromisoformat('2018-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2018-01-15')),
        Holiday('Memorial Day', datetime.fromisoformat('2018-05-28')),
        Holiday('Independence Day', datetime.fromisoformat('2018-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2018-09-03')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2018-11-22')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2018-11-23')),
        Holiday('Christmas Eve', datetime.fromisoformat('2018-12-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2018-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2019-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2019-01-21')),
        Holiday('Memorial Day', datetime.fromisoformat('2019-05-27')),
        Holiday('Independence Day', datetime.fromisoformat('2019-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2019-09-02')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2019-11-28')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2019-11-29')),
        Holiday('Christmas Eve', datetime.fromisoformat('2019-12-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2019-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2020-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2020-01-20')),
        Holiday('Memorial Day', datetime.fromisoformat('2020-05-25')),
        Holiday('Independence Day', datetime.fromisoformat('2020-07-03')),
        Holiday('Labor Day', datetime.fromisoformat('2020-09-07')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2020-11-26')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2020-11-27')),
        Holiday('Christmas Eve', datetime.fromisoformat('2020-12-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2020-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2021-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2021-01-18')),
        Holiday('Memorial Day', datetime.fromisoformat('2021-05-31')),
        Holiday('Independence Day', datetime.fromisoformat('2021-07-05')),
        Holiday('Labor Day', datetime.fromisoformat('2021-09-06')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2021-11-26')),
        Holiday('Christmas Eve', datetime.fromisoformat('2021-12-23')),
        Holiday('Christmas Day', datetime.fromisoformat('2021-12-24')),

        Holiday('New Year''s Day', datetime.fromisoformat('2021-12-31')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2022-01-17')),
        Holiday('Memorial Day', datetime.fromisoformat('2022-05-30')),
        Holiday('Independence Day', datetime.fromisoformat('2022-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2022-09-05')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2022-11-24')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2022-11-25')),
        Holiday('Christmas Eve', datetime.fromisoformat('2022-12-23')),
        Holiday('Christmas Day', datetime.fromisoformat('2022-12-26')),

        Holiday('New Year''s Day', datetime.fromisoformat('2023-01-02')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2023-01-16')),
        Holiday('Memorial Day', datetime.fromisoformat('2023-05-29')),
        Holiday('Independence Day', datetime.fromisoformat('2023-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2023-09-04')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2023-11-23')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2023-11-24')),
        Holiday('Christmas Eve', datetime.fromisoformat('2023-12-25')),
        Holiday('Christmas Day', datetime.fromisoformat('2023-12-26')),

        Holiday('New Year''s Day', datetime.fromisoformat('2024-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2024-01-15')),
        Holiday('Memorial Day', datetime.fromisoformat('2024-05-27')),
        Holiday('Independence Day', datetime.fromisoformat('2024-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2024-09-02')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2024-11-28')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2024-11-29')),
        Holiday('Christmas Eve', datetime.fromisoformat('2024-12-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2024-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2025-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2025-01-20')),
        Holiday('Memorial Day', datetime.fromisoformat('2025-05-26')),
        Holiday('Independence Day', datetime.fromisoformat('2025-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2025-09-01')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2025-11-27')),
        Holiday('Friday After Thanksgiving',
                datetime.fromisoformat('2025-11-28')),
        Holiday('Christmas Eve', datetime.fromisoformat('2025-12-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2025-12-25')),
    ]
)

default_us_public_holidays: HolidayCalendar = HolidayCalendar(
    HolidayType('US Public Holiday', 'USPublic', False),
    [
        Holiday('New Year''s Day', datetime.fromisoformat('2012-01-02')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2012-01-16')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2012-02-20')),
        Holiday('Memorial Day', datetime.fromisoformat('2012-05-28')),
        Holiday('Independence Day', datetime.fromisoformat('2012-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2012-09-03')),
        Holiday('Columbus Day', datetime.fromisoformat('2012-10-08')),
        Holiday('Veterans Day', datetime.fromisoformat('2012-11-12')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2012-11-22')),
        Holiday('Christmas Day', datetime.fromisoformat('2012-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2013-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2013-01-21')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2013-02-18')),
        Holiday('Memorial Day', datetime.fromisoformat('2013-05-27')),
        Holiday('Independence Day', datetime.fromisoformat('2013-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2013-09-02')),
        Holiday('Columbus Day', datetime.fromisoformat('2013-10-14')),
        Holiday('Veterans Day', datetime.fromisoformat('2013-11-11')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2013-11-28')),
        Holiday('Christmas Day', datetime.fromisoformat('2013-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2014-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2014-01-20')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2014-02-17')),
        Holiday('Memorial Day', datetime.fromisoformat('2014-05-26')),
        Holiday('Independence Day', datetime.fromisoformat('2014-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2014-09-01')),
        Holiday('Columbus Day', datetime.fromisoformat('2014-10-13')),
        Holiday('Veterans Day', datetime.fromisoformat('2014-11-11')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2014-11-27')),
        Holiday('Christmas Day', datetime.fromisoformat('2014-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2015-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2015-01-19')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2015-02-16')),
        Holiday('Memorial Day', datetime.fromisoformat('2015-05-25')),
        Holiday('Independence Day', datetime.fromisoformat('2015-07-03')),
        Holiday('Labor Day', datetime.fromisoformat('2015-09-07')),
        Holiday('Columbus Day', datetime.fromisoformat('2015-10-12')),
        Holiday('Veterans Day', datetime.fromisoformat('2015-11-11')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2015-11-26')),
        Holiday('Christmas Day', datetime.fromisoformat('2015-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2016-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2016-01-18')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2016-02-15')),
        Holiday('Memorial Day', datetime.fromisoformat('2016-05-30')),
        Holiday('Independence Day', datetime.fromisoformat('2016-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2016-09-05')),
        Holiday('Columbus Day', datetime.fromisoformat('2016-10-10')),
        Holiday('Veterans Day', datetime.fromisoformat('2016-11-11')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2016-11-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2016-12-26')),

        Holiday('New Year''s Day', datetime.fromisoformat('2017-01-02')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2017-01-16')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2017-02-20')),
        Holiday('Memorial Day', datetime.fromisoformat('2017-05-29')),
        Holiday('Independence Day', datetime.fromisoformat('2017-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2017-09-04')),
        Holiday('Columbus Day', datetime.fromisoformat('2017-10-09')),
        Holiday('Veterans Day', datetime.fromisoformat('2017-11-10')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2017-11-23')),
        Holiday('Christmas Day', datetime.fromisoformat('2017-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2018-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2018-01-15')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2018-02-19')),
        Holiday('Memorial Day', datetime.fromisoformat('2018-05-28')),
        Holiday('Independence Day', datetime.fromisoformat('2018-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2018-09-03')),
        Holiday('Columbus Day', datetime.fromisoformat('2018-10-08')),
        Holiday('Veterans Day', datetime.fromisoformat('2018-11-12')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2018-11-22')),
        Holiday('Christmas Day', datetime.fromisoformat('2018-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2019-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2019-01-21')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2019-02-18')),
        Holiday('Memorial Day', datetime.fromisoformat('2019-05-27')),
        Holiday('Independence Day', datetime.fromisoformat('2019-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2019-09-02')),
        Holiday('Columbus Day', datetime.fromisoformat('2019-10-14')),
        Holiday('Veterans Day', datetime.fromisoformat('2019-11-11')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2019-11-28')),
        Holiday('Christmas Day', datetime.fromisoformat('2019-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2020-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2020-01-20')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2020-02-17')),
        Holiday('Memorial Day', datetime.fromisoformat('2020-05-25')),
        Holiday('Independence Day', datetime.fromisoformat('2020-07-03')),
        Holiday('Labor Day', datetime.fromisoformat('2020-09-07')),
        Holiday('Columbus Day', datetime.fromisoformat('2020-10-12')),
        Holiday('Veterans Day', datetime.fromisoformat('2020-11-11')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2020-11-26')),
        Holiday('Christmas Day', datetime.fromisoformat('2020-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2021-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2021-01-18')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2021-02-15')),
        Holiday('Memorial Day', datetime.fromisoformat('2021-05-31')),
        Holiday('Independence Day', datetime.fromisoformat('2021-07-05')),
        Holiday('Labor Day', datetime.fromisoformat('2021-09-06')),
        Holiday('Columbus Day', datetime.fromisoformat('2021-10-11')),
        Holiday('Veterans Day', datetime.fromisoformat('2021-11-11')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2021-11-25')),
        Holiday('Christmas Day', datetime.fromisoformat('2021-12-24')),

        Holiday('New Year''s Day', datetime.fromisoformat('2021-12-31')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2022-01-17')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2022-02-21')),
        Holiday('Memorial Day', datetime.fromisoformat('2022-05-30')),
        Holiday('Independence Day', datetime.fromisoformat('2022-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2022-09-05')),
        Holiday('Columbus Day', datetime.fromisoformat('2022-10-10')),
        Holiday('Veterans Day', datetime.fromisoformat('2022-11-11')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2022-11-24')),
        Holiday('Christmas Day', datetime.fromisoformat('2022-12-26')),

        Holiday('New Year''s Day', datetime.fromisoformat('2023-01-02')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2023-01-16')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2023-02-20')),
        Holiday('Memorial Day', datetime.fromisoformat('2023-05-29')),
        Holiday('Independence Day', datetime.fromisoformat('2023-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2023-09-04')),
        Holiday('Columbus Day', datetime.fromisoformat('2023-10-09')),
        Holiday('Veterans Day', datetime.fromisoformat('2023-11-10')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2023-11-23')),
        Holiday('Christmas Day', datetime.fromisoformat('2023-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2024-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2024-01-15')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2024-02-19')),
        Holiday('Memorial Day', datetime.fromisoformat('2024-05-27')),
        Holiday('Independence Day', datetime.fromisoformat('2024-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2024-09-02')),
        Holiday('Columbus Day', datetime.fromisoformat('2024-10-14')),
        Holiday('Veterans Day', datetime.fromisoformat('2024-11-11')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2024-11-28')),
        Holiday('Christmas Day', datetime.fromisoformat('2024-12-25')),

        Holiday('New Year''s Day', datetime.fromisoformat('2025-01-01')),
        Holiday('Martin Luther King, Jr. Day',
                datetime.fromisoformat('2025-01-20')),
        Holiday('Presidents'' Day', datetime.fromisoformat('2025-02-17')),
        Holiday('Memorial Day', datetime.fromisoformat('2025-05-26')),
        Holiday('Independence Day', datetime.fromisoformat('2025-07-04')),
        Holiday('Labor Day', datetime.fromisoformat('2025-09-01')),
        Holiday('Columbus Day', datetime.fromisoformat('2025-10-13')),
        Holiday('Veterans Day', datetime.fromisoformat('2025-11-11')),
        Holiday('Thanksgiving Day', datetime.fromisoformat('2025-11-27')),
        Holiday('Christmas Day', datetime.fromisoformat('2025-12-25')),
    ]
)


@dataclass(frozen=True)
class HolidayConfig:
    generate_holidays: bool = True
    holiday_types_schema_name: str = 'integration'
    holiday_types_table_name: str = 'manual_HolidayTypes'
    holidays_schema_name: str = 'integration'
    holidays_table_name: str = 'manual_Holidays'
    holiday_calendars: list[HolidayCalendar] = [
        default_company_holidays, default_us_public_holidays]
    holiday_types: list[HolidayType] = field(init=False)

    def __post_init__(self):
        if self.generate_holidays:
            holiday_types = [
                cal.holiday_type for cal in self.holiday_calendars]
            holiday_type_names = [t.name for t in holiday_types]
            holiday_type_prefixes = [
                t.generated_column_prefix for t in holiday_types]
            assert len(holiday_type_names) == len(set(holiday_type_names)
                                                  ), 'detected a duplicate HolidayType name in Holiday.'
            assert len(holiday_type_prefixes) == len(set(holiday_type_prefixes)
                                                     ), 'detected a duplicate HolidayTypePrefix in Holiday.'
            self.holiday_types = holiday_types


@dataclass(frozen=True)
class Column:
    name: str
    include: bool
    sort_index: int


@dataclass(frozen=True)
class DimDateColumns:
    date_key = Column('DateKey', True, 0)
    the_date = Column('TheDate', True, 1)
    iso_date_name = Column('ISODateName', True, 2)
    american_date_name = Column('AmericanDateName', True, 3)
    day_of_week_name = Column('DayOfWeekName', True, 4)
    day_of_week_abbrev = Column('DayOfWeekAbbrev', True, 5)
    month_name = Column('MonthName', True, 6)
    month_abbrev = Column('MonthAbbrev', True, 7)
    year_week_name = Column('YearWeekName', True, 8)
    year_month_name = Column('YearMonthName', True, 9)
    month_year_name = Column('MonthYearName', True, 10)
    year_quarter_name = Column('YearQuarterName', True, 11)
    year = Column('Year', True, 12)
    year_week = Column('YearWeek', True, 13)
    iso_year_week_code = Column('ISOYearWeekCode', True, 14)
    year_month = Column('YearMonth', True, 15)
    year_quarter = Column('YearQuarter', True, 16)
    day_of_week_starting_monday = Column('DayOfWeekStartingMonday', True, 17)
    day_of_week = Column('DayOfWeek', True, 18)
    day_of_month = Column('DayOfMonth', True, 19)
    day_of_quarter = Column('DayOfQuarter', True, 20)
    day_of_year = Column('DayOfYear', True, 21)
    week_of_quarter = Column('WeekOfQuarter', True, 22)
    week_of_year = Column('WeekOfYear', True, 23)
    iso_week_of_year = Column('ISOWeekOfYear', True, 24)
    month = Column('Month', True, 25)
    month_of_quarter = Column('MonthOfQuarter', True, 26)
    quarter = Column('Quarter', True, 27)
    days_in_month = Column('DaysInMonth', True, 28)
    days_in_quarter = Column('DaysInQuarter', True, 29)
    days_in_year = Column('DaysInYear', True, 30)
    day_offset_from_today = Column('DayOffsetFromToday', True, 31)
    month_offset_from_today = Column('MonthOffsetFromToday', True, 32)
    quarter_offset_from_today = Column('QuarterOffsetFromToday', True, 33)
    year_offset_from_today = Column('YearOffsetFromToday', True, 34)
    today_flag = Column('TodayFlag', True, 35)
    current_week_starting_monday_flag = Column, 36(
        'CurrentWeekStartingMondayFlag', True, 36)
    current_week_flag = Column('CurrentWeekFlag', True, 37)
    prior_week_flag = Column('PriorWeekFlag', True, 38)
    next_week_flag = Column('NextWeekFlag', True, 39)
    current_month_flag = Column('CurrentMonthFlag', True, 40)
    prior_month_flag = Column('PriorMonthFlag', True, 41)
    next_month_flag = Column('NextMonthFlag', True, 42)
    current_quarter_flag = Column('CurrentQuarterFlag', True, 43)
    prior_quarter_flag = Column('PriorQuarterFlag', True, 44)
    next_quarter_flag = Column('NextQuarterFlag', True, 45)
    current_year_flag = Column('CurrentYearFlag', True, 46)
    prior_year_flag = Column('PriorYearFlag', True, 47)
    next_year_flag = Column('NextYearFlag', True, 48)
    weekday_flag = Column('WeekdayFlag', True, 49)
    business_day_flag = Column('BusinessDayFlag', True, 50)
    first_day_of_month_flag = Column('FirstDayOfMonthFlag', True, 51)
    last_day_of_month_flag = Column('LastDayOfMonthFlag', True, 52)
    first_day_of_quarter_flag = Column('FirstDayOfQuarterFlag', True, 53)
    last_day_of_quarter_flag = Column('LastDayOfQuarterFlag', True, 54)
    first_day_of_year_flag = Column('FirstDayOfYearFlag', True, 55)
    last_day_of_year_flag = Column('LastDayOfYearFlag', True, 56)
    fraction_of_week = Column('FractionOfWeek', True, 57)
    fraction_of_month = Column('FractionOfMonth', True, 58)
    fraction_of_quarter = Column('FractionOfQuarter', True, 59)
    fraction_of_year = Column('FractionOfYear', True, 60)
    prior_day = Column('PriorDay', True, 61)
    next_day = Column('NextDay', True, 62)
    same_day_prior_week = Column('SameDayPriorWeek', True, 63)
    same_day_prior_month = Column('SameDayPriorMonth', True, 64)
    same_day_prior_quarter = Column('SameDayPriorQuarter', True, 65)
    same_day_prior_year = Column('SameDayPriorYear', True, 66)
    same_day_next_week = Column('SameDayNextWeek', True, 67)
    same_day_next_month = Column('SameDayNextMonth', True, 68)
    same_day_next_quarter = Column('SameDayNextQuarter', True, 69)
    same_day_next_year = Column('SameDayNextYear', True, 70)
    current_week_start = Column('CurrentWeekStart', True, 71)
    current_week_end = Column('CurrentWeekEnd', True, 72)
    current_month_start = Column('CurrentMonthStart', True, 73)
    current_month_end = Column('CurrentMonthEnd', True, 74)
    current_quarter_start = Column('CurrentQuarterStart', True, 75)
    current_quarter_end = Column('CurrentQuarterEnd', True, 76)
    current_year_start = Column('CurrentYearStart', True, 77)
    current_year_end = Column('CurrentYearEnd', True, 78)
    prior_week_start = Column('PriorWeekStart', True, 79)
    prior_week_end = Column('PriorWeekEnd', True, 80)
    prior_month_start = Column('PriorMonthStart', True, 81)
    prior_month_end = Column('PriorMonthEnd', True, 82)
    prior_quarter_start = Column('PriorQuarterStart', True, 83)
    prior_quarter_end = Column('PriorQuarterEnd', True, 84)
    prior_year_start = Column('PriorYearStart', True, 85)
    prior_year_end = Column('PriorYearEnd', True, 86)
    next_week_start = Column('NextWeekStart', True, 87)
    next_week_end = Column('NextWeekEnd', True, 88)
    next_month_start = Column('NextMonthStart', True, 89)
    next_month_end = Column('NextMonthEnd', True, 90)
    next_quarter_start = Column('NextQuarterStart', True, 91)
    next_quarter_end = Column('NextQuarterEnd', True, 92)
    next_year_start = Column('NextYearStart', True, 93)
    next_year_end = Column('NextYearEnd', True, 94)
    weekly_burnup_starting_monday = Column(
        'WeeklyBurnupStartingMonday', True, 95)
    weekly_burnup = Column('WeeklyBurnup', True, 96)
    monthly_burnup = Column('MonthlyBurnup', True, 97)
    quarterly_burnup = Column('QuarterlyBurnup', True, 98)
    yearly_burnup = Column('YearlyBurnup', True, 99)
    fiscal_month_name = Column('FiscalMonthName', True, 100)
    fiscal_month_abbrev = Column('FiscalMonthAbbrev', True, 101)
    fiscal_year_name = Column('FiscalYearWeekName', True, 102)
    fiscal_year_month_name = Column('FiscalYearMonthName', True, 103)
    fiscal_month_year_name = Column('FiscalMonthYearName', True, 104)
    fiscal_year_quarter_name = Column('FiscalYearQuarterName', True, 105)
    fiscal_year = Column('FiscalYear', True, 106)
    fiscal_year_week = Column('FiscalYearWeek', True, 107)
    fiscal_year_month = Column('FiscalYearMonth', True, 108)
    fiscal_year_quarter = Column('FiscalYearQuarter', True, 109)
    fiscal_day_of_month = Column('FiscalDayOfMonth', True, 110)
    fiscal_day_of_quarter = Column('FiscalDayOfQuarter', True, 111)
    fiscal_day_of_year = Column('FiscalDayOfYear', True, 112)
    fiscal_week_of_quarter = Column('FiscalWeekOfQuarter', True, 113)
    fiscal_week_of_year = Column('FiscalWeekOfYear', True, 114)
    fiscal_month = Column('FiscalMonth', True, 115)
    fiscal_month_of_quarter = Column('FiscalMonthOfQuarter', True, 116)
    fiscal_quarter = Column('FiscalQuarter', True, 117)
    fiscal_days_in_month = Column('FiscalDaysInMonth', True, 118)
    fiscal_days_in_quarter = Column('FiscalDaysInQuarter', True, 119)
    fiscal_days_in_year = Column('FiscalDaysInYear', True, 120)
    fiscal_current_month_flag = Column('FiscalCurrentMonthFlag', True, 121)
    fiscal_prior_month_flag = Column('FiscalPriorMonthFlag', True, 122)
    fiscal_next_month_flag = Column('FiscalNextMonthFlag', True, 123)
    fiscal_current_quarter_flag = Column('FiscalCurrentQuarterFlag', True, 124)
    fiscal_prior_quarter_flag = Column('FiscalPriorQuarterFlag', True, 125)
    fiscal_next_quarter_flag = Column('FiscalNextQuarterFlag', True, 126)
    fiscal_current_year_flag = Column('FiscalCurrentYearFlag', True, 127)
    fiscal_prior_year_flag = Column('FiscalPriorYearFlag', True, 128)
    fiscal_next_year_flag = Column('FiscalNextYearFlag', True, 129)
    fiscal_first_day_of_month_flag = Column(
        'FiscalFirstDayOfMonthFlag', True, 130)
    fiscal_last_day_of_month_flag = Column(
        'FiscalLastDayOfMonthFlag', True, 131)
    fiscal_first_day_of_quarter_flag = Column, 132(
        'FiscalFirstDayOfQuarterFlag', True, 132)
    fiscal_last_day_of_quarter_flag = Column, 133(
        'FiscalLastDayOfQuarterFlag', True, 133)
    fiscal_first_day_of_year_flag = Column(
        'FiscalFirstDayOfYearFlag', True, 134)
    fiscal_last_day_of_year_flag = Column('FiscalLastDayOfYearFlag', True, 135)
    fiscal_fraction_of_month = Column('FiscalFractionOfMonth', True, 136)
    fiscal_fraction_of_quarter = Column('FiscalFractionOfQuarter', True, 137)
    fiscal_fraction_of_year = Column('FiscalFractionOfYear', True, 138)
    fiscal_current_month_start = Column('FiscalCurrentMonthStart', True, 139)
    fiscal_current_month_end = Column('FiscalCurrentMonthEnd', True, 140)
    fiscal_current_quarter_start = Column(
        'FiscalCurrentQuarterStart', True, 141)
    fiscal_current_quarter_end = Column('FiscalCurrentQuarterEnd', True, 142)
    fiscal_current_year_start = Column('FiscalCurrentYearStart', True, 143)
    fiscal_current_year_end = Column('FiscalCurrentYearEnd', True, 144)
    fiscal_prior_month_start = Column('FiscalPriorMonthStart', True, 145)
    fiscal_prior_month_end = Column('FiscalPriorMonthEnd', True, 146)
    fiscal_prior_quarter_start = Column('FiscalPriorQuarterStart', True, 147)
    fiscal_prior_quarter_end = Column('FiscalPriorQuarterEnd', True, 148)
    fiscal_prior_year_start = Column('FiscalPriorYearStart', True, 149)
    fiscal_prior_year_end = Column('FiscalPriorYearEnd', True, 150)
    fiscal_next_month_start = Column('FiscalNextMonthStart', True, 151)
    fiscal_next_month_end = Column('FiscalNextMonthEnd', True, 152)
    fiscal_next_quarter_start = Column('FiscalNextQuarterStart', True, 153)
    fiscal_next_quarter_end = Column('FiscalNextQuarterEnd', True, 154)
    fiscal_next_year_start = Column('FiscalNextYearStart', True, 155)
    fiscal_next_year_end = Column('FiscalNextYearEnd', True, 156)
    fiscal_monthly_burnup = Column('FiscalMonthlyBurnup', True, 157)
    fiscal_quarterly_burnup = Column('FiscalQuarterlyBurnup', True, 158)
    fiscal_yearly_burnup = Column('FiscalYearlyBurnup', True, 159)


@dataclass(frozen=True)
class DimDateConfig:
    table_schema: str = 'dbo'
    table_name: str = 'DimDate'
    columns: DimDateColumns = DimDateColumns()
    column_name_factory: Callable[[str], str] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v['sort_index']
                     for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys), 'there was a duplicate sort key in the column definitions for DimDateColumn.'

        if self.column_name_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_cols[k] = Column(self.column_name_factory(
                    v['name']), v['include'], v['sort_index'])
            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass(frozen=True)
class DimFiscalMonthColumns:
    month_start_key = Column('MonthStartKey', True, 0)
    month_end_key = Column('MonthEndKey', True, 1)
    month_start_date = Column('MonthStartDate', True, 2)
    month_end_date = Column('MonthEndDate', True, 3)
    month_start_iso_date_name = Column('MonthStartISODateName', True, 4)
    month_end_iso_date_name = Column('MonthEndISODateName', True, 5)
    month_start_american_date_name = Column(
        'MonthStartAmericanDateName', True, 6)
    month_end_american_date_name = Column('MonthEndAmericanDateName', True, 7)
    month_name = Column('MonthName', True, 8)
    month_abbrev = Column('MonthAbbrev', True, 9)
    month_start_year_week_name = Column('MonthStartYearWeekName', True, 10)
    month_end_year_week_name = Column('MonthEndYearWeekName', True, 11)
    year_month_name = Column('YearMonthName', True, 12)
    month_year_name = Column('MonthYearName', True, 13)
    year_quarter_name = Column('YearQuarterName', True, 14)
    year = Column('Year', True, 15)
    month_start_year_week = Column('MonthStartYearWeek', True, 16)
    month_end_year_week = Column('MonthEndYearWeek', True, 17)
    year_month = Column('YearMonth', True, 18)
    year_quarter = Column('YearQuarter', True, 19)
    month_start_day_of_quarter = Column('MonthStartDayOfQuarter', True, 20)
    month_end_day_of_quarter = Column('MonthEndDayOfQuarter', True, 21)
    month_start_day_of_year = Column('MonthStartDayOfYear', True, 22)
    month_end_day_of_year = Column('MonthEndDayOfYear', True, 23)
    month_start_week_of_quarter = Column('MonthStartWeekOfQuarter', True, 24)
    month_end_week_of_quarter = Column('MonthEndWeekOfQuarter', True, 25)
    month_start_week_of_year = Column('MonthStartWeekOfYear', True, 26)
    month_end_week_of_year = Column('MonthEndWeekOfYear', True, 27)
    month_of_quarter = Column('MonthOfQuarter', True, 28)
    quarter = Column('Quarter', True, 29)
    days_in_month = Column('DaysInMonth', True, 30)
    days_in_quarter = Column('DaysInQuarter', True, 31)
    days_in_year = Column('DaysInYear', True, 32)
    current_month_flag = Column('CurrentMonthFlag', True, 33)
    prior_month_flag = Column('PriorMonthFlag', True, 34)
    next_month_flag = Column('NextMonthFlag', True, 35)
    current_quarter_flag = Column('CurrentQuarterFlag', True, 36)
    prior_quarter_flag = Column('PriorQuarterFlag', True, 37)
    next_quarter_flag = Column('NextQuarterFlag', True, 38)
    current_year_flag = Column('CurrentYearFlag', True, 39)
    prior_year_flag = Column('PriorYearFlag', True, 40)
    next_year_flag = Column('NextYearFlag', True, 41)
    first_day_of_month_flag = Column('FirstDayOfMonthFlag', True, 42)
    last_day_of_month_flag = Column('LastDayOfMonthFlag', True, 43)
    first_day_of_quarter_flag = Column('FirstDayOfQuarterFlag', True, 44)
    last_day_of_quarter_flag = Column('LastDayOfQuarterFlag', True, 45)
    first_day_of_year_flag = Column('FirstDayOfYearFlag', True, 46)
    last_day_of_year_flag = Column('LastDayOfYearFlag', True, 47)
    month_start_fraction_of_quarter = Column(
        'MonthStartFractionOfQuarter', True, 48)
    month_end_fraction_of_quarter = Column(
        'MonthEndFractionOfQuarter', True, 49)
    month_start_fraction_of_year = Column('MonthStartFractionOfYear', True, 50)
    month_end_fraction_of_year = Column('MonthEndFractionOfYear', True, 51)
    month_start_current_quarter_start = Column(
        'MonthStartCurrentQuarterStart', True, 52)
    month_start_current_quarter_end = Column(
        'MonthStartCurrentQuarterEnd', True, 53)
    month_start_current_year_start = Column(
        'MonthStartCurrentYearStart', True, 54)
    month_start_current_year_end = Column('MonthStartCurrentYearEnd', True, 55)
    month_start_prior_month_start = Column(
        'MonthStartPriorMonthStart', True, 56)
    month_start_prior_month_end = Column('MonthStartPriorMonthEnd', True, 57)
    month_start_prior_quarter_start = Column(
        'MonthStartPriorQuarterStart', True, 58)
    month_start_prior_quarter_end = Column(
        'MonthStartPriorQuarterEnd', True, 59)
    month_start_prior_year_start = Column('MonthStartPriorYearStart', True, 60)
    month_start_prior_year_end = Column('MonthStartPriorYearEnd', True, 61)
    month_start_next_month_start = Column('MonthStartNextMonthStart', True, 62)
    month_start_next_month_end = Column('MonthStartNextMonthEnd', True, 63)
    month_start_next_quarter_start = Column(
        'MonthStartNextQuarterStart', True, 64)
    month_start_next_quarter_end = Column('MonthStartNextQuarterEnd', True, 65)
    month_start_next_year_start = Column('MonthStartNextYearStart', True, 66)
    month_start_next_year_end = Column('MonthStartNextYearEnd', True, 67)
    month_start_quarterly_burnup = Column(
        'MonthStartQuarterlyBurnup', True, 68)
    month_end_quarterly_burnup = Column('MonthEndQuarterlyBurnup', True, 69)
    month_start_yearly_burnup = Column('MonthStartYearlyBurnup', True, 70)
    month_end_yearly_burnup = Column('MonthEndYearlyBurnup', True, 71)


@dataclass(frozen=True)
class DimFiscalMonthConfig:
    table_schema: str = 'dbo'
    table_name: str = 'DimFiscalMonth'
    columns: DimFiscalMonthColumns = DimFiscalMonthColumns()
    column_name_factory: Callable[[str], str] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v['sort_index']
                     for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys), 'there was a duplicate sort key in the column definitions for DimFiscalMonthColumn.'

        if self.column_name_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_cols[k] = Column(self.column_name_factory(
                    v['name']), v['include'], v['sort_index'])
            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass(frozen=True)
class DimCalendarMonthColumns:
    month_start_key = Column('MonthStartKey', True, 0)
    month_end_key = Column('MonthEndKey', True, 1)
    month_start_date = Column('MonthStartDate', True, 2)
    month_end_date = Column('MonthEndDate', True, 3)
    month_start_iso_date_name = Column('MonthStartISODateName', True, 4)
    month_end_iso_date_name = Column('MonthEndISODateName', True, 5)
    month_start_american_date_name = Column(
        'MonthStartAmericanDateName', True, 6)
    month_end_american_date_name = Column('MonthEndAmericanDateName', True, 7)
    month_name = Column('MonthName', True, 8)
    month_abbrev = Column('MonthAbbrev', True, 9)
    month_start_year_week_name = Column('MonthStartYearWeekName', True, 10)
    month_end_year_week_name = Column('MonthEndYearWeekName', True, 11)
    year_month_name = Column('YearMonthName', True, 12)
    month_year_name = Column('MonthYearName', True, 13)
    year_quarter_name = Column('YearQuarterName', True, 14)
    year = Column('Year', True, 15)
    month_start_year_week = Column('MonthStartYearWeek', True, 16)
    month_end_year_week = Column('MonthEndYearWeek', True, 17)
    year_month = Column('YearMonth', True, 18)
    year_quarter = Column('YearQuarter', True, 19)
    month_start_day_of_quarter = Column('MonthStartDayOfQuarter', True, 20)
    month_end_day_of_quarter = Column('MonthEndDayOfQuarter', True, 21)
    month_start_day_of_year = Column('MonthStartDayOfYear', True, 22)
    month_end_day_of_year = Column('MonthEndDayOfYear', True, 23)
    month_start_week_of_quarter = Column('MonthStartWeekOfQuarter', True, 24)
    month_end_week_of_quarter = Column('MonthEndWeekOfQuarter', True, 25)
    month_start_week_of_year = Column('MonthStartWeekOfYear', True, 26)
    month_end_week_of_year = Column('MonthEndWeekOfYear', True, 27)
    month_of_quarter = Column('MonthOfQuarter', True, 28)
    quarter = Column('Quarter', True, 29)
    days_in_month = Column('DaysInMonth', True, 30)
    days_in_quarter = Column('DaysInQuarter', True, 31)
    days_in_year = Column('DaysInYear', True, 32)
    current_month_flag = Column('CurrentMonthFlag', True, 33)
    prior_month_flag = Column('PriorMonthFlag', True, 34)
    next_month_flag = Column('NextMonthFlag', True, 35)
    current_quarter_flag = Column('CurrentQuarterFlag', True, 36)
    prior_quarter_flag = Column('PriorQuarterFlag', True, 37)
    next_quarter_flag = Column('NextQuarterFlag', True, 38)
    current_year_flag = Column('CurrentYearFlag', True, 39)
    prior_year_flag = Column('PriorYearFlag', True, 40)
    next_year_flag = Column('NextYearFlag', True, 41)
    first_day_of_month_flag = Column('FirstDayOfMonthFlag', True, 42)
    last_day_of_month_flag = Column('LastDayOfMonthFlag', True, 43)
    first_day_of_quarter_flag = Column('FirstDayOfQuarterFlag', True, 44)
    last_day_of_quarter_flag = Column('LastDayOfQuarterFlag', True, 45)
    first_day_of_year_flag = Column('FirstDayOfYearFlag', True, 46)
    last_day_of_year_flag = Column('LastDayOfYearFlag', True, 47)
    month_start_fraction_of_quarter = Column(
        'MonthStartFractionOfQuarter', True, 48)
    month_end_fraction_of_quarter = Column(
        'MonthEndFractionOfQuarter', True, 49)
    month_start_fraction_of_year = Column('MonthStartFractionOfYear', True, 50)
    month_end_fraction_of_year = Column('MonthEndFractionOfYear', True, 51)
    month_start_current_quarter_start = Column(
        'MonthStartCurrentQuarterStart', True, 52)
    month_start_current_quarter_end = Column(
        'MonthStartCurrentQuarterEnd', True, 53)
    month_start_current_year_start = Column(
        'MonthStartCurrentYearStart', True, 54)
    month_start_current_year_end = Column('MonthStartCurrentYearEnd', True, 55)
    month_start_prior_month_start = Column(
        'MonthStartPriorMonthStart', True, 56)
    month_start_prior_month_end = Column('MonthStartPriorMonthEnd', True, 57)
    month_start_prior_quarter_start = Column(
        'MonthStartPriorQuarterStart', True, 58)
    month_start_prior_quarter_end = Column(
        'MonthStartPriorQuarterEnd', True, 59)
    month_start_prior_year_start = Column('MonthStartPriorYearStart', True, 60)
    month_start_prior_year_end = Column('MonthStartPriorYearEnd', True, 61)
    month_start_next_month_start = Column('MonthStartNextMonthStart', True, 62)
    month_start_next_month_end = Column('MonthStartNextMonthEnd', True, 63)
    month_start_next_quarter_start = Column(
        'MonthStartNextQuarterStart', True, 64)
    month_start_next_quarter_end = Column('MonthStartNextQuarterEnd', True, 65)
    month_start_next_year_start = Column('MonthStartNextYearStart', True, 66)
    month_start_next_year_end = Column('MonthStartNextYearEnd', True, 67)
    month_start_quarterly_burnup = Column(
        'MonthStartQuarterlyBurnup', True, 68)
    month_end_quarterly_burnup = Column('MonthEndQuarterlyBurnup', True, 69)
    month_start_yearly_burnup = Column('MonthStartYearlyBurnup', True, 70)
    month_end_yearly_burnup = Column('MonthEndYearlyBurnup', True, 71)


@dataclass(frozen=True)
class DimCalendarMonthConfig:
    table_schema: str = 'dbo'
    table_name: str = 'DimCalendarMonth'
    columns: DimCalendarMonthColumns = DimCalendarMonthColumns()
    column_name_factory: Callable[[str], str] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v['sort_index']
                     for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys), 'there was a duplicate sort key in the column definitions for DimCalendarMonthColumn.'

        if self.column_name_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_cols[k] = Column(self.column_name_factory(
                    v['name']), v['include'], v['sort_index'])
            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass
class Config:
    outdir_base: Path = Path('../output')
    date_range: DateRange = DateRange()
    fiscal: FiscalConfig = FiscalConfig()
    time_zone: str = "Mountain Standard Time"
    holidays: HolidayConfig = HolidayConfig()
    dim_date: DimDateConfig = DimDateConfig()
    dim_fiscal_month: DimFiscalMonthConfig = DimFiscalMonthConfig()
    dim_calendar_month: DimCalendarMonthConfig = DimCalendarMonthConfig()
