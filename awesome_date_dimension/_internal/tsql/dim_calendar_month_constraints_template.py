from ...config import Config


def dim_calendar_month_constraints_template(config: Config) -> str:
    dcm_conf = config.dim_calendar_month
    return f"""ALTER TABLE {dcm_conf.table_schema}.{dcm_conf.table_name}
ADD PRIMARY KEY CLUSTERED ({dcm_conf.columns.month_start_key.name}, {dcm_conf.columns.month_end_key.name} ASC);

CREATE NONCLUSTERED INDEX IDX_NC_{dcm_conf.table_schema}_{dcm_conf.table_name}_{dcm_conf.columns.month_start_date.name} ON {dcm_conf.table_schema}.{dcm_conf.table_name} ({dcm_conf.columns.month_start_date.name});
CREATE NONCLUSTERED INDEX IDX_NC_{dcm_conf.table_schema}_{dcm_conf.table_name}_{dcm_conf.columns.month_end_date.name} ON {dcm_conf.table_schema}.{dcm_conf.table_name} ({dcm_conf.columns.month_end_date.name});
"""
