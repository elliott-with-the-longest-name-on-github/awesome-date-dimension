from ...config import Config


def holiday_types_constraints_template(config: Config) -> str:
    h_conf = config.holidays
    return f"""ALTER TABLE {h_conf.holiday_types_schema_name}.{h_conf.holiday_types_table_name}
ADD PRIMARY KEY CLUSTERED ({h_conf.holiday_types_columns.holiday_type_key.name} ASC);
"""
