def table_setup_template(
    table_schema: str, table_name: str, column_def: list[str]
) -> str:
    join_str = ",\n  "
    return f"""CREATE TABLE {table_schema}.{table_name} (
  {join_str.join(column_def)}
);
"""
