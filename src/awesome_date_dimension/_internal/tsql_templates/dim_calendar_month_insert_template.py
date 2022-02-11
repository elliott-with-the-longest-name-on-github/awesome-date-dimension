from ...config import Config


def dim_calendar_month_insert_template(config: Config) -> str:
    dcm_conf = config.dim_calendar_month
    dcm_cols = dcm_conf.columns
    dd_conf = config.dim_date
    dd_cols = dd_conf.columns
    h_conf = config.holidays
    holiday_columndef: list[str] = []
    holiday_colselect: list[str] = []
    for i, t in enumerate(h_conf.holiday_types):
        holiday_columndef.append(
            f"{t.generated_column_prefix}{t.generated_monthly_count_column_postfix} = SUM({t.generated_column_prefix}{t.generated_flag_column_postfix} * 1)"
        )
        holiday_colselect.append(
            f"{t.generated_column_prefix}{t.generated_monthly_count_column_postfix}"
        )

    holiday_columndef_str = ",\n  ".join(holiday_columndef)

    holiday_colselect_str = ",\n  ".join(holiday_colselect)

    return f"""WITH DistinctMonths AS (
  SELECT
  {dcm_cols.month_start_key.name} = CONVERT(
    int,
    CONVERT(
    varchar(8),
    {dd_cols.current_month_start.name},
    112
    )
  ),
  {dcm_cols.month_end_key.name} = CONVERT(
    int,
    CONVERT(
    varchar(8),
    {dd_cols.current_month_end.name},
    112
    )
  ),
  {holiday_columndef_str}
  FROM
    {dd_conf.table_schema}.{dd_conf.table_name}
    GROUP BY {dd_cols.current_month_start.name}, {dd_cols.current_month_end.name}
)

INSERT INTO {dcm_conf.table_schema}.{dcm_conf.table_name} (
  {dcm_cols.month_start_key.name},
  {dcm_cols.month_end_key.name},
  {dcm_cols.month_start_date.name},
  {dcm_cols.month_end_date.name},
  {dcm_cols.month_start_iso_date_name.name},
  {dcm_cols.month_end_iso_date_name.name},
  {dcm_cols.month_start_american_date_name.name},
  {dcm_cols.month_end_american_date_name.name},
  {dcm_cols.month_name.name},
  {dcm_cols.month_abbrev.name},
  {dcm_cols.month_start_year_week_name.name},
  {dcm_cols.month_end_year_week_name.name},
  {dcm_cols.year_month_name.name},
  {dcm_cols.month_year_name.name},
  {dcm_cols.year_quarter_name.name},
  {dcm_cols.year.name},
  {dcm_cols.month_start_year_week.name},
  {dcm_cols.month_end_year_week.name},
  {dcm_cols.year_month.name},
  {dcm_cols.year_quarter.name},
  {dcm_cols.month_start_day_of_quarter.name},
  {dcm_cols.month_end_day_of_quarter.name},
  {dcm_cols.month_start_day_of_year.name},
  {dcm_cols.month_end_day_of_year.name},
  {dcm_cols.month_start_week_of_quarter.name},
  {dcm_cols.month_end_week_of_quarter.name},
  {dcm_cols.month_start_week_of_year.name},
  {dcm_cols.month_end_week_of_year.name},
  {dcm_cols.month_of_quarter.name},
  {dcm_cols.quarter.name},
  {dcm_cols.days_in_month.name},
  {dcm_cols.days_in_quarter.name},
  {dcm_cols.days_in_year.name},
  {dcm_cols.current_month_flag.name},
  {dcm_cols.prior_month_flag.name},
  {dcm_cols.next_month_flag.name},
  {dcm_cols.current_quarter_flag.name},
  {dcm_cols.prior_quarter_flag.name},
  {dcm_cols.next_quarter_flag.name},
  {dcm_cols.current_year_flag.name},
  {dcm_cols.prior_year_flag.name},
  {dcm_cols.next_year_flag.name},
  {dcm_cols.first_day_of_month_flag.name},
  {dcm_cols.last_day_of_month_flag.name},
  {dcm_cols.first_day_of_quarter_flag.name},
  {dcm_cols.last_day_of_quarter_flag.name},
  {dcm_cols.first_day_of_year_flag.name},
  {dcm_cols.last_day_of_year_flag.name},
  {dcm_cols.month_start_fraction_of_quarter.name},
  {dcm_cols.month_end_fraction_of_quarter.name},
  {dcm_cols.month_start_fraction_of_year.name},
  {dcm_cols.month_end_fraction_of_year.name},
  {dcm_cols.current_quarter_start.name},
  {dcm_cols.current_quarter_end.name},
  {dcm_cols.current_year_start.name},
  {dcm_cols.current_year_end.name},
  {dcm_cols.prior_month_start.name},
  {dcm_cols.prior_month_end.name},
  {dcm_cols.prior_quarter_start.name},
  {dcm_cols.prior_quarter_end.name},
  {dcm_cols.prior_year_start.name},
  {dcm_cols.prior_year_end.name},
  {dcm_cols.next_month_start.name},
  {dcm_cols.next_month_end.name},
  {dcm_cols.next_quarter_start.name},
  {dcm_cols.next_quarter_end.name},
  {dcm_cols.next_year_start.name},
  {dcm_cols.next_year_end.name},
  {dcm_cols.month_start_quarterly_burnup.name},
  {dcm_cols.month_end_quarterly_burnup.name},
  {dcm_cols.month_start_yearly_burnup.name},
  {dcm_cols.month_end_yearly_burnup.name},
  {holiday_colselect_str}
)
-- Yank the day-level stuff we need for both the start and end dates from {dd_conf.table_name}
SELECT  
  base.{dcm_cols.month_start_key.name},
  base.{dcm_cols.month_end_key.name},
  {dcm_cols.month_start_date.name} = startdate.{dd_cols.date_key.name},
  {dcm_cols.month_end_date.name} = enddate.{dd_cols.date_key.name},
  {dcm_cols.month_start_iso_date_name.name} = startdate.{dd_cols.iso_date_name.name},
  {dcm_cols.month_end_iso_date_name.name} = enddate.{dd_cols.iso_date_name.name},
  {dcm_cols.month_start_american_date_name.name} = startdate.{dd_cols.american_date_name.name},
  {dcm_cols.month_end_american_date_name.name} = enddate.{dd_cols.american_date_name.name},
  {dcm_cols.month_name.name} = startdate.{dd_cols.month_name.name},
  {dcm_cols.month_abbrev.name} = startdate.{dd_cols.month_abbrev.name},
  {dcm_cols.month_start_year_week_name.name} = startdate.{dd_cols.year_week_name.name},
  {dcm_cols.month_end_year_week_name.name} = enddate.{dd_cols.year_week_name.name},
  {dcm_cols.year_month_name.name} = startdate.{dd_cols.year_month_name.name},
  {dcm_cols.month_year_name.name} = startdate.{dd_cols.month_year_name.name},
  {dcm_cols.year_quarter_name.name} = startdate.{dd_cols.year_quarter_name.name},
  {dcm_cols.year.name} = startdate.{dd_cols.year.name},
  {dcm_cols.month_start_year_week.name} = startdate.{dd_cols.year_week.name},
  {dcm_cols.month_end_year_week.name} = enddate.{dd_cols.year_week.name},
  {dcm_cols.year_month.name} = startdate.{dd_cols.year_month.name},
  {dcm_cols.year_quarter.name} = startdate.{dd_cols.year_quarter.name},
  {dcm_cols.month_start_day_of_quarter.name} = startdate.{dd_cols.day_of_quarter.name},
  {dcm_cols.month_end_day_of_quarter.name} = enddate.{dd_cols.day_of_quarter.name},
  {dcm_cols.month_start_day_of_year.name} = startdate.{dd_cols.day_of_year.name},
  {dcm_cols.month_end_day_of_year.name} = enddate.{dd_cols.day_of_year.name},
  {dcm_cols.month_start_week_of_quarter.name} = startdate.{dd_cols.week_of_quarter.name},
  {dcm_cols.month_end_week_of_quarter.name} = enddate.{dd_cols.week_of_quarter.name},
  {dcm_cols.month_start_week_of_year.name} = startdate.{dd_cols.week_of_year.name},
  {dcm_cols.month_end_week_of_year.name} = enddate.{dd_cols.week_of_year.name},
  {dcm_cols.month_of_quarter.name} = startdate.{dd_cols.month_of_quarter.name},
  {dcm_cols.quarter.name} = startdate.{dd_cols.quarter.name},
  {dcm_cols.days_in_month.name} = startdate.{dd_cols.days_in_month.name},
  {dcm_cols.days_in_quarter.name} = startdate.{dd_cols.days_in_quarter.name},
  {dcm_cols.days_in_year.name} = startdate.{dd_cols.days_in_year.name},
  {dcm_cols.current_month_flag.name} = startdate.{dd_cols.current_month_flag.name},
  {dcm_cols.prior_month_flag.name} = startdate.{dd_cols.prior_month_flag.name},
  {dcm_cols.next_month_flag.name} = startdate.{dd_cols.next_month_flag.name},
  {dcm_cols.current_quarter_flag.name} = startdate.{dd_cols.current_quarter_flag.name},
  {dcm_cols.prior_quarter_flag.name} = startdate.{dd_cols.prior_quarter_flag.name},
  {dcm_cols.next_quarter_flag.name} = startdate.{dd_cols.next_quarter_flag.name},
  {dcm_cols.current_year_flag.name} = startdate.{dd_cols.current_year_flag.name},
  {dcm_cols.prior_year_flag.name} = startdate.{dd_cols.prior_year_flag.name},
  {dcm_cols.next_year_flag.name} = startdate.{dd_cols.next_year_flag.name},
  {dcm_cols.first_day_of_month_flag.name} = startdate.{dd_cols.first_day_of_month_flag.name},
  {dcm_cols.last_day_of_month_flag.name} = startdate.{dd_cols.last_day_of_month_flag.name},
  {dcm_cols.first_day_of_quarter_flag.name} = startdate.{dd_cols.first_day_of_quarter_flag.name},
  {dcm_cols.last_day_of_quarter_flag.name} = startdate.{dd_cols.last_day_of_quarter_flag.name},
  {dcm_cols.first_day_of_year_flag.name} = startdate.{dd_cols.first_day_of_year_flag.name},
  {dcm_cols.last_day_of_year_flag.name} = startdate.{dd_cols.last_day_of_year_flag.name},
  {dcm_cols.month_start_fraction_of_quarter.name} = startdate.{dd_cols.fraction_of_quarter.name},
  {dcm_cols.month_end_fraction_of_quarter.name} = enddate.{dd_cols.fraction_of_quarter.name},
  {dcm_cols.month_start_fraction_of_year.name} = startdate.{dd_cols.fraction_of_year.name},
  {dcm_cols.month_end_fraction_of_year.name} = enddate.{dd_cols.fraction_of_year.name},
  {dcm_cols.current_quarter_start.name} = startdate.{dd_cols.current_quarter_start.name},
  {dcm_cols.current_quarter_end.name} = startdate.{dd_cols.current_quarter_end.name},
  {dcm_cols.current_year_start.name} = startdate.{dd_cols.current_year_start.name},
  {dcm_cols.current_year_end.name} = startdate.{dd_cols.current_year_end.name},
  {dcm_cols.prior_month_start.name} = startdate.{dd_cols.prior_month_start.name},
  {dcm_cols.prior_month_end.name} = startdate.{dd_cols.prior_month_end.name},
  {dcm_cols.prior_quarter_start.name} = startdate.{dd_cols.prior_quarter_start.name},
  {dcm_cols.prior_quarter_end.name} = startdate.{dd_cols.prior_quarter_end.name},
  {dcm_cols.prior_year_start.name} = startdate.{dd_cols.prior_year_start.name},
  {dcm_cols.prior_year_end.name} = startdate.{dd_cols.prior_year_end.name},
  {dcm_cols.next_month_start.name} = startdate.{dd_cols.next_month_start.name},
  {dcm_cols.next_month_end.name} = startdate.{dd_cols.next_month_end.name},
  {dcm_cols.next_quarter_start.name} = startdate.{dd_cols.next_quarter_start.name},
  {dcm_cols.next_quarter_end.name} = startdate.{dd_cols.next_quarter_end.name},
  {dcm_cols.next_year_start.name} = startdate.{dd_cols.next_year_start.name},
  {dcm_cols.next_year_end.name} = startdate.{dd_cols.next_year_end.name},
  {dcm_cols.month_start_quarterly_burnup.name} = startdate.{dd_cols.quarterly_burnup.name},
  {dcm_cols.month_end_quarterly_burnup.name} = enddate.{dd_cols.quarterly_burnup.name},
  {dcm_cols.month_start_yearly_burnup.name} = startdate.{dd_cols.yearly_burnup.name},
  {dcm_cols.month_end_yearly_burnup.name} = enddate.{dd_cols.yearly_burnup.name},
  {holiday_colselect_str}
FROM
  DistinctMonths AS base
  INNER JOIN {dd_conf.table_schema}.{dd_conf.table_name} AS startdate
    ON base.{dcm_cols.month_start_key.name} = startdate.{dd_cols.date_key.name}
  INNER JOIN {dd_conf.table_schema}.{dd_conf.table_name} AS enddate
    ON base.{dcm_cols.month_end_key.name} = enddate.{dd_cols.date_key.name};"""
