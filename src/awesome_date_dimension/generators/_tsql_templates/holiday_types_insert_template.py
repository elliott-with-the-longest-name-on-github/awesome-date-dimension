from ...config import HolidayType


def holiday_types_insert_template(table_schema: str, table_name: str, ht_column_name, holiday_types: list[HolidayType]) -> str:
    formatted_types = map(lambda t: f"('{t.name}')", holiday_types)
    join_str = ',\n  '
    return f"""INSERT INTO {table_schema}.{table_name} ({ht_column_name}) VALUES 
  {join_str.join(formatted_types)};"""
