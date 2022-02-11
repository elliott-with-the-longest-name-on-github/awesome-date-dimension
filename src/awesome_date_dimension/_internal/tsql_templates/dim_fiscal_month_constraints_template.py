from ...config import Config


def dim_fiscal_month_constraints_template(config: Config) -> str:
    dfm_conf = config.dim_fiscal_month
    return f"""ALTER TABLE {dfm_conf.table_schema}.{dfm_conf.table_name}
ADD PRIMARY KEY CLUSTERED ({dfm_conf.columns.month_start_key.name}, {dfm_conf.columns.month_end_key.name} ASC);

CREATE NONCLUSTERED INDEX IDX_NC_{dfm_conf.table_schema}_{dfm_conf.table_name}_{dfm_conf.columns.month_start_date.name} ON {dfm_conf.table_schema}.{dfm_conf.table_name} ({dfm_conf.columns.month_start_date.name});
CREATE NONCLUSTERED INDEX IDX_NC_{dfm_conf.table_schema}_{dfm_conf.table_name}_{dfm_conf.columns.month_end_date.name} ON {dfm_conf.table_schema}.{dfm_conf.table_name} ({dfm_conf.columns.month_end_date.name});
"""
