from ...config import HolidayConfig


def holidays_insert_template(holiday_config: HolidayConfig):
    join_str = ',\n    '
    holidays = []
    for cal in holiday_config.holiday_calendars:
        for holiday in cal.holidays:
            date_key = f'{str(holiday.holiday_date.year).zfill(4)}{str(holiday.holiday_date.month).zfill(2)}{str(holiday.holiday_date.day).zfill(2)}'
            holidays.append(
                f"({date_key}, '{holiday.holiday_name}', '{cal.holiday_type.name}')")
    return f"""INSERT INTO {holiday_config.holidays_schema_name}.{holiday_config.holidays_table_name} (DateKey, HolidayName, HolidayTypeKey)
  SELECT h.DateKey, h.HolidayName, ht.HolidayTypeKey
  FROM (
    VALUES
    {join_str.join(holidays)}
  ) AS h (DateKey, HolidayName, HolidayTypeName)
  -- Note the inner join -- if you haven't correctly specified your HolidayTypes, they'll be thrown out.
  INNER JOIN {holiday_config.holiday_types_schema_name}.{holiday_config.holiday_types_table_name} AS ht
    ON h.HolidayTypeName = ht.HolidayTypeName
"""
