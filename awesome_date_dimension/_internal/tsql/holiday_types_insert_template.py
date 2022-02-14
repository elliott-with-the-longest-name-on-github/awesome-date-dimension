from ...config import Config


def holiday_types_insert_template(config: Config) -> str:
    table_schema = config.holidays.holiday_types_schema_name
    table_name = config.holidays.holiday_types_table_name
    ht_column_name = config.holidays.holiday_types_columns.holiday_type_name.name
    holiday_types = config.holidays.holiday_types
    formatted_types = map(lambda t: f"('{t.name}')", holiday_types)
    join_str = ",\n  "
    return f"""INSERT INTO {table_schema}.{table_name} ({ht_column_name}) VALUES 
  {join_str.join(formatted_types)};"""
