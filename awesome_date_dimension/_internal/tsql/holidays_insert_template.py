from ...config import Config


def holidays_insert_template(config: Config):
    holiday_config = config.holidays
    join_str = ",\n    "
    holidays = []
    for cal in holiday_config.holiday_calendars:
        for holiday in cal.holidays:
            date_key = f"{str(holiday.holiday_date.year).zfill(4)}{str(holiday.holiday_date.month).zfill(2)}{str(holiday.holiday_date.day).zfill(2)}"
            holidays.append(
                f"({date_key}, '{holiday.holiday_name}', '{cal.holiday_type.name}')"
            )
    return f"""INSERT INTO {holiday_config.holidays_schema_name}.{holiday_config.holidays_table_name} ({holiday_config.holidays_columns.date_key.name}, {holiday_config.holidays_columns.holiday_name.name}, {holiday_config.holidays_columns.holiday_type_key.name})
  SELECT h.{holiday_config.holidays_columns.date_key.name}, h.{holiday_config.holidays_columns.holiday_name.name}, ht.{holiday_config.holiday_types_columns.holiday_type_key.name}
  FROM (
    VALUES
    {join_str.join(holidays)}
  ) AS h ({holiday_config.holidays_columns.date_key.name}, {holiday_config.holidays_columns.holiday_name.name}, {holiday_config.holiday_types_columns.holiday_type_name.name})
  -- Note the inner join -- if you haven't correctly specified your HolidayTypes, they'll be thrown out.
  INNER JOIN {holiday_config.holiday_types_schema_name}.{holiday_config.holiday_types_table_name} AS ht
    ON h.{holiday_config.holiday_types_columns.holiday_type_name.name} = ht.{holiday_config.holiday_types_columns.holiday_type_name.name}
"""
