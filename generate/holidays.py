from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Holiday:
    holiday_type: str
    holiday_date: datetime.date
    holiday_name: str


default_holidays: list[Holiday] = [
    Holiday("New Year's Day", datetime.fromisoformat(
        '2012-01-02'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2012-01-02'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2012-01-16'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2012-01-16'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2012-02-20'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2012-05-28'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2012-05-28'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2012-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2012-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2012-09-03'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2012-09-03'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2012-10-08'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2012-11-12'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2012-11-22'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2012-11-22'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2012-11-23'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2012-12-24'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2012-12-25'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2012-12-25'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2013-01-01'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2013-01-01'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2013-01-21'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2013-01-21'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2013-02-18'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2013-05-27'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2013-05-27'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2013-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2013-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2013-09-02'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2013-09-02'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2013-10-14'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2013-11-11'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2013-11-28'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2013-11-28'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2013-11-29'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2013-12-24'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2013-12-25'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2013-12-25'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2014-01-01'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2014-01-01'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2014-01-20'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2014-01-20'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2014-02-17'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2014-05-26'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2014-05-26'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2014-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2014-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2014-09-01'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2014-09-01'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2014-10-13'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2014-11-11'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2014-11-27'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2014-11-28'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2014-12-24'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2014-12-25'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2014-12-25'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2015-01-01'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2015-01-01'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2015-01-19'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2015-01-19'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2015-02-16'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2015-05-25'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2015-05-25'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2015-07-03'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2015-07-03'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2015-09-07'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2015-09-07'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2015-10-12'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2015-11-11'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2015-11-26'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2015-11-26'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2015-11-27'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2015-12-24'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2015-12-25'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2015-12-25'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2016-01-01'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2016-01-01'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2016-01-18'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2016-01-18'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2016-02-15'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2016-05-30'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2016-05-30'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2016-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2016-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2016-09-05'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2016-09-05'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2016-10-10'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2016-11-11'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2016-11-24'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2016-11-24'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2016-11-25'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2016-12-23'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2016-12-26'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2016-12-26'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2017-01-02'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2017-01-02'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2017-01-16'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2017-01-16'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2017-02-20'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2017-05-29'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2017-05-29'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2017-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2017-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2017-09-04'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2017-09-04'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2017-10-09'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2017-11-10'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2017-11-23'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2017-11-23'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2017-11-24'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2017-12-25'), 'Company Holiday'),
    # This Christmas is weird. For my company,
    # Christmas Eve pushes Christmas to the 26th, but
    # for the government, Christmas still falls on the
    # 25th.
    Holiday('Christmas Day', datetime.fromisoformat(
        '2017-12-25'), 'US Public Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2017-12-26'), 'Company Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2018-01-01'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2018-01-01'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2018-01-15'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2018-01-15'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2018-02-19'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2018-05-28'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2018-05-28'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2018-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2018-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2018-09-03'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2018-09-03'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2018-10-08'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2018-11-12'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2018-11-22'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2018-11-22'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2018-11-23'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2018-12-24'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2018-12-25'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2018-12-25'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2019-01-01'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2019-01-01'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2019-01-21'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2019-01-21'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2019-02-18'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2019-05-27'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2019-05-27'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2019-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2019-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2019-09-02'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2019-09-02'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2019-10-14'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2019-11-11'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2019-11-28'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2019-11-28'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2019-11-29'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2019-12-24'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2019-12-25'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2019-12-25'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2020-01-01'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2020-01-01'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2020-01-20'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2020-01-20'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2020-02-17'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2020-05-25'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2020-05-25'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2020-07-03'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2020-07-03'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2020-09-07'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2020-09-07'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2020-10-12'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2020-11-11'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2020-11-26'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2020-11-26'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2020-11-27'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2020-12-24'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2020-12-25'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2020-12-25'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2021-01-01'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2021-01-01'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2021-01-18'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2021-01-18'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2021-02-15'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2021-05-31'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2021-05-31'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2021-07-05'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2021-07-05'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2021-09-06'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2021-09-06'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2021-10-11'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2021-11-11'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2021-11-25'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2021-11-26'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2021-12-23'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2021-12-24'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2021-12-24'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2021-12-31'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2021-12-31'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2022-01-17'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2022-01-17'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2022-02-21'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2022-05-30'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2022-05-30'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2022-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2022-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2022-09-05'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2022-09-05'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2022-10-10'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2022-11-11'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2022-11-24'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2022-11-24'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2022-11-25'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2022-12-23'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2022-12-26'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2022-12-26'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2023-01-02'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2023-01-02'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2023-01-16'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2023-01-16'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2023-02-20'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2023-05-29'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2023-05-29'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2023-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2023-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2023-09-04'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2023-09-04'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2023-10-09'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2023-11-10'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2023-11-23'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2023-11-23'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2023-11-24'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2023-12-25'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2023-12-25'), 'US Public Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2023-12-26'), 'Company Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2024-01-01'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2024-01-01'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2024-01-15'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2024-01-15'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2024-02-19'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2024-05-27'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2024-05-27'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2024-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2024-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2024-09-02'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2024-09-02'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2024-10-14'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2024-11-11'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2024-11-28'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2024-11-28'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2024-11-29'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2024-12-24'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2024-12-25'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2024-12-25'), 'US Public Holiday'),

    Holiday("New Year's Day", datetime.fromisoformat(
        '2025-01-01'), 'Company Holiday'),
    Holiday("New Year's Day", datetime.fromisoformat(
        '2025-01-01'), 'US Public Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2025-01-20'), 'Company Holiday'),
    Holiday('Martin Luther King, Jr. Day', datetime.fromisoformat(
        '2025-01-20'), 'US Public Holiday'),
    Holiday("Presidents' Day", datetime.fromisoformat(
        '2025-02-17'), 'US Public Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2025-05-26'), 'Company Holiday'),
    Holiday('Memorial Day', datetime.fromisoformat(
        '2025-05-26'), 'US Public Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2025-07-04'), 'Company Holiday'),
    Holiday('Independence Day', datetime.fromisoformat(
        '2025-07-04'), 'US Public Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2025-09-01'), 'Company Holiday'),
    Holiday('Labor Day', datetime.fromisoformat(
        '2025-09-01'), 'US Public Holiday'),
    Holiday('Columbus Day', datetime.fromisoformat(
        '2025-10-13'), 'US Public Holiday'),
    Holiday('Veterans Day', datetime.fromisoformat(
        '2025-11-11'), 'US Public Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2025-11-27'), 'Company Holiday'),
    Holiday('Thanksgiving Day', datetime.fromisoformat(
        '2025-11-27'), 'US Public Holiday'),
    Holiday('Friday After Thanksgiving', datetime.fromisoformat(
        '2025-11-28'), 'Company Holiday'),
    Holiday('Christmas Eve', datetime.fromisoformat(
        '2025-12-24'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2025-12-25'), 'Company Holiday'),
    Holiday('Christmas Day', datetime.fromisoformat(
        '2025-12-25'), 'US Public Holiday'),
]
