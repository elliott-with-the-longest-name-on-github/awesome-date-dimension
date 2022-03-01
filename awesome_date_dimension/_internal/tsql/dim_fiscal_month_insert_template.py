from ...config import Config
from .tsql_columns import TSQLDimFiscalMonthColumns


def dim_fiscal_month_insert_template(
    config: Config, columns: TSQLDimFiscalMonthColumns
) -> str:
    dfm_conf = config.dim_fiscal_month
    dfm_cols = dfm_conf.columns
    dd_conf = config.dim_date
    dd_cols = dd_conf.columns
    h_conf = config.holidays
    holiday_columndef: list[str] = []
    holiday_colselect: list[str] = []
    if h_conf.generate_holidays:
        for i, t in enumerate(h_conf.holiday_types):
            holiday_columndef.append(
                f"{t.generated_column_prefix}{t.generated_monthly_count_column_postfix} = SUM({t.generated_column_prefix}{t.generated_flag_column_postfix} * 1)"
            )
            holiday_colselect.append(
                f"{t.generated_column_prefix}{t.generated_monthly_count_column_postfix}"
            )

        holiday_columndef_str = ",\n  ".join(holiday_columndef)
    else:
        holiday_columndef_str = ""

    dfm_to_dd_colmap = {
        dfm_cols.month_start_date.name: f"startdate.{dd_cols.the_date.name}",
        dfm_cols.month_end_date.name: f"enddate.{dd_cols.the_date.name}",
        dfm_cols.month_start_iso_date_name.name: f"startdate.{dd_cols.iso_date_name.name}",
        dfm_cols.month_end_iso_date_name.name: f"enddate.{dd_cols.iso_date_name.name}",
        dfm_cols.month_start_iso_week_date_name.name: f"startdate.{dd_cols.iso_week_date_name.name}",
        dfm_cols.month_end_iso_week_date_name.name: f"enddate.{dd_cols.iso_week_date_name.name}",
        dfm_cols.month_start_american_date_name.name: f"startdate.{dd_cols.american_date_name.name}",
        dfm_cols.month_end_american_date_name.name: f"enddate.{dd_cols.american_date_name.name}",
        dfm_cols.month_name.name: f"startdate.{dd_cols.fiscal_month_name.name}",
        dfm_cols.month_abbrev.name: f"startdate.{dd_cols.fiscal_month_abbrev.name}",
        dfm_cols.month_start_year_week_name.name: f"startdate.{dd_cols.fiscal_year_week_name.name}",
        dfm_cols.month_end_year_week_name.name: f"enddate.{dd_cols.fiscal_year_week_name.name}",
        dfm_cols.year_month_name.name: f"startdate.{dd_cols.fiscal_year_month_name.name}",
        dfm_cols.month_year_name.name: f"startdate.{dd_cols.fiscal_month_year_name.name}",
        dfm_cols.year_quarter_name.name: f"startdate.{dd_cols.fiscal_year_quarter_name.name}",
        dfm_cols.year.name: f"startdate.{dd_cols.fiscal_year.name}",
        dfm_cols.month_start_year_week.name: f"startdate.{dd_cols.fiscal_year_week.name}",
        dfm_cols.month_end_year_week.name: f"enddate.{dd_cols.fiscal_year_week.name}",
        dfm_cols.year_month.name: f"startdate.{dd_cols.fiscal_year_month.name}",
        dfm_cols.year_quarter.name: f"startdate.{dd_cols.fiscal_year_quarter.name}",
        dfm_cols.month_start_day_of_quarter.name: f"startdate.{dd_cols.fiscal_day_of_quarter.name}",
        dfm_cols.month_end_day_of_quarter.name: f"enddate.{dd_cols.fiscal_day_of_quarter.name}",
        dfm_cols.month_start_day_of_year.name: f"startdate.{dd_cols.fiscal_day_of_year.name}",
        dfm_cols.month_end_day_of_year.name: f"enddate.{dd_cols.fiscal_day_of_year.name}",
        dfm_cols.month_start_week_of_quarter.name: f"startdate.{dd_cols.fiscal_week_of_quarter.name}",
        dfm_cols.month_end_week_of_quarter.name: f"enddate.{dd_cols.fiscal_week_of_quarter.name}",
        dfm_cols.month_start_week_of_year.name: f"startdate.{dd_cols.fiscal_week_of_year.name}",
        dfm_cols.month_end_week_of_year.name: f"enddate.{dd_cols.fiscal_week_of_year.name}",
        dfm_cols.month_of_quarter.name: f"startdate.{dd_cols.fiscal_month_of_quarter.name}",
        dfm_cols.quarter.name: f"startdate.{dd_cols.fiscal_quarter.name}",
        dfm_cols.days_in_month.name: f"startdate.{dd_cols.fiscal_days_in_month.name}",
        dfm_cols.days_in_quarter.name: f"startdate.{dd_cols.fiscal_days_in_quarter.name}",
        dfm_cols.days_in_year.name: f"startdate.{dd_cols.fiscal_days_in_year.name}",
        dfm_cols.current_month_flag.name: f"startdate.{dd_cols.fiscal_current_month_flag.name}",
        dfm_cols.prior_month_flag.name: f"startdate.{dd_cols.fiscal_prior_month_flag.name}",
        dfm_cols.next_month_flag.name: f"startdate.{dd_cols.fiscal_next_month_flag.name}",
        dfm_cols.current_quarter_flag.name: f"startdate.{dd_cols.fiscal_current_quarter_flag.name}",
        dfm_cols.prior_quarter_flag.name: f"startdate.{dd_cols.fiscal_prior_quarter_flag.name}",
        dfm_cols.next_quarter_flag.name: f"startdate.{dd_cols.fiscal_next_quarter_flag.name}",
        dfm_cols.current_year_flag.name: f"startdate.{dd_cols.fiscal_current_year_flag.name}",
        dfm_cols.prior_year_flag.name: f"startdate.{dd_cols.fiscal_prior_year_flag.name}",
        dfm_cols.next_year_flag.name: f"startdate.{dd_cols.fiscal_next_year_flag.name}",
        dfm_cols.first_day_of_month_flag.name: f"startdate.{dd_cols.fiscal_first_day_of_month_flag.name}",
        dfm_cols.last_day_of_month_flag.name: f"startdate.{dd_cols.fiscal_last_day_of_month_flag.name}",
        dfm_cols.first_day_of_quarter_flag.name: f"startdate.{dd_cols.fiscal_first_day_of_quarter_flag.name}",
        dfm_cols.last_day_of_quarter_flag.name: f"startdate.{dd_cols.fiscal_last_day_of_quarter_flag.name}",
        dfm_cols.first_day_of_year_flag.name: f"startdate.{dd_cols.fiscal_first_day_of_year_flag.name}",
        dfm_cols.last_day_of_year_flag.name: f"startdate.{dd_cols.fiscal_last_day_of_year_flag.name}",
        dfm_cols.month_start_fraction_of_quarter.name: f"startdate.{dd_cols.fiscal_fraction_of_quarter.name}",
        dfm_cols.month_end_fraction_of_quarter.name: f"enddate.{dd_cols.fiscal_fraction_of_quarter.name}",
        dfm_cols.month_start_fraction_of_year.name: f"startdate.{dd_cols.fiscal_fraction_of_year.name}",
        dfm_cols.month_end_fraction_of_year.name: f"enddate.{dd_cols.fiscal_fraction_of_year.name}",
        dfm_cols.current_quarter_start.name: f"startdate.{dd_cols.fiscal_current_quarter_start.name}",
        dfm_cols.current_quarter_end.name: f"startdate.{dd_cols.fiscal_current_quarter_end.name}",
        dfm_cols.current_year_start.name: f"startdate.{dd_cols.fiscal_current_year_start.name}",
        dfm_cols.current_year_end.name: f"startdate.{dd_cols.fiscal_current_year_end.name}",
        dfm_cols.prior_month_start.name: f"startdate.{dd_cols.fiscal_prior_month_start.name}",
        dfm_cols.prior_month_end.name: f"startdate.{dd_cols.fiscal_prior_month_end.name}",
        dfm_cols.prior_quarter_start.name: f"startdate.{dd_cols.fiscal_prior_quarter_start.name}",
        dfm_cols.prior_quarter_end.name: f"startdate.{dd_cols.fiscal_prior_quarter_end.name}",
        dfm_cols.prior_year_start.name: f"startdate.{dd_cols.fiscal_prior_year_start.name}",
        dfm_cols.prior_year_end.name: f"startdate.{dd_cols.fiscal_prior_year_end.name}",
        dfm_cols.next_month_start.name: f"startdate.{dd_cols.fiscal_next_month_start.name}",
        dfm_cols.next_month_end.name: f"startdate.{dd_cols.fiscal_next_month_end.name}",
        dfm_cols.next_quarter_start.name: f"startdate.{dd_cols.fiscal_next_quarter_start.name}",
        dfm_cols.next_quarter_end.name: f"startdate.{dd_cols.fiscal_next_quarter_end.name}",
        dfm_cols.next_year_start.name: f"startdate.{dd_cols.fiscal_next_year_start.name}",
        dfm_cols.next_year_end.name: f"startdate.{dd_cols.fiscal_next_year_end.name}",
        dfm_cols.month_start_quarterly_burnup.name: f"startdate.{dd_cols.fiscal_quarterly_burnup.name}",
        dfm_cols.month_end_quarterly_burnup.name: f"enddate.{dd_cols.fiscal_quarterly_burnup.name}",
        dfm_cols.month_start_yearly_burnup.name: f"startdate.{dd_cols.fiscal_yearly_burnup.name}",
        dfm_cols.month_end_yearly_burnup.name: f"enddate.{dd_cols.fiscal_yearly_burnup.name}",
    }

    insert_columns_clause = ",\n  ".join((c.name for c in columns))
    select_columns = []
    for col in columns:
        if (dd_name := dfm_to_dd_colmap.get(col.name)) is not None:
            select_columns.append(f"{col.name} = {dd_name}")
        else:
            select_columns.append(f"{col.name} = base.{col.name}")

    select_columns_clause = ",\n  ".join(select_columns)

    return f"""WITH DistinctMonths AS (
  SELECT
  {dfm_cols.month_start_key.name} = CONVERT(
    int,
    CONVERT(
    varchar(8),
    {dd_cols.fiscal_current_month_start.name},
    112
    )
  ),
  {dfm_cols.month_end_key.name} = CONVERT(
    int,
    CONVERT(
    varchar(8),
    {dd_cols.fiscal_current_month_end.name},
    112
    )
  ),
  {holiday_columndef_str}
  FROM
    {dd_conf.table_schema}.{dd_conf.table_name}
    GROUP BY {dd_cols.fiscal_current_month_start.name}, {dd_cols.fiscal_current_month_end.name}
)

INSERT INTO {dfm_conf.table_schema}.{dfm_conf.table_name} (
  {insert_columns_clause}
)
-- Yank the day-level stuff we need for both the start and end dates from {dd_conf.table_name}
SELECT  
  {select_columns_clause}
FROM
  DistinctMonths AS base
  INNER JOIN {dd_conf.table_schema}.{dd_conf.table_name} AS startdate
    ON base.{dfm_cols.month_start_key.name} = startdate.{dd_cols.date_key.name}
  INNER JOIN {dd_conf.table_schema}.{dd_conf.table_name} AS enddate
    ON base.{dfm_cols.month_end_key.name} = enddate.{dd_cols.date_key.name};"""
