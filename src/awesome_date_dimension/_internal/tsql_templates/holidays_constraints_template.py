from ...config import Config


def holidays_constraints_template(config: Config) -> str:
    h_conf = config.holidays
    return f"""ALTER TABLE {h_conf.holidays_schema_name}.{h_conf.holidays_table_name} 
ADD PRIMARY KEY CLUSTERED ({h_conf.holidays_columns.date_key.name} ASC, {h_conf.holidays_columns.holiday_type_key.name} ASC);

ALTER TABLE {h_conf.holidays_schema_name}.{h_conf.holidays_table_name}
ADD CONSTRAINT FK_{h_conf.holidays_table_name}_{h_conf.holidays_columns.holiday_type_key.name} FOREIGN KEY ({h_conf.holidays_columns.holiday_type_key.name})
  REFERENCES {h_conf.holiday_types_schema_name}.{h_conf.holiday_types_table_name} ({h_conf.holiday_types_columns.holiday_type_key.name})
  ON DELETE CASCADE
  ON UPDATE CASCADE;
"""
