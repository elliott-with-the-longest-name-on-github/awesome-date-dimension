from ...config import Config


def dim_date_constraints_template(config: Config) -> str:
    dd_conf = config.dim_date
    return f"""ALTER TABLE {dd_conf.table_schema}.{dd_conf.table_name}
ADD PRIMARY KEY CLUSTERED ({dd_conf.columns.date_key.name} ASC);

CREATE NONCLUSTERED INDEX IDX_NC_{dd_conf.table_schema}_{dd_conf.table_name}_{dd_conf.columns.the_date.name} ON {dd_conf.table_schema}.{dd_conf.table_name} ({dd_conf.columns.the_date.name});
"""
