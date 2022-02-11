from ...config import Config


def dim_date_refresh_template(config: Config) -> str:
    dd_conf = config.dim_date
    dd_cols = dd_conf.columns

    holiday_columndef: list[str] = []
    holiday_column_list: list[str] = []
    business_day_list: list[str] = []
    holiday_join: list[str] = []
    for i, t in enumerate(config.holidays.holiday_types):
        holiday_join.append(
            f"      LEFT OUTER JOIN {config.holidays.holidays_schema_name}.{config.holidays.holidays_table_name} AS h{i} -- {t.name}"
        )
        holiday_join.append(
            f"        ON d.{dd_cols.date_key.name} = h{i}.{config.holidays.holidays_columns.date_key.name} AND h{i}.{config.holidays.holidays_columns.holiday_type_key.name} = (SELECT {config.holidays.holiday_types_columns.holiday_type_key.name} FROM {config.holidays.holiday_types_schema_name}.{config.holidays.holiday_types_table_name} WHERE {config.holidays.holiday_types_columns.holiday_type_name.name} = '{t.name}')"
        )
        if t.included_in_business_day_calc:
            business_day_list.append(
                f"h{i}.{config.holidays.holidays_columns.date_key.name} IS NOT NULL"
            )
        holiday_columndef.append(
            f"      {t.generated_column_prefix}{t.generated_flag_column_postfix} = IIF("
        )
        holiday_columndef.append(
            f"        h{i}.{config.holidays.holidays_columns.date_key.name} IS NOT NULL,"
        )
        holiday_columndef.append(f"        1,")
        holiday_columndef.append(f"        0")
        holiday_columndef.append(f"      ),")
        holiday_columndef.append(
            f"      {t.generated_column_prefix}{t.generated_name_column_postfix} = h{i}.{config.holidays.holidays_columns.holiday_name.name},"
        )
        holiday_column_list.append(
            f"    d.{t.generated_column_prefix}{t.generated_flag_column_postfix} = dc.{t.generated_column_prefix}{t.generated_flag_column_postfix},"
        )
        holiday_column_list.append(
            f"    d.{t.generated_column_prefix}{t.generated_name_column_postfix} = dc.{t.generated_column_prefix}{t.generated_name_column_postfix},"
        )

    holiday_join = "\n".join(holiday_join)
    business_day_clause = "\n".join(business_day_list) + "\n        OR "
    holiday_column_clause = "\n".join(holiday_columndef)[:-2]
    holiday_columns = "\n".join(holiday_column_list)[:-1]
    return f"""CREATE PROCEDURE {dd_conf.table_schema}.sp_build_{dd_conf.table_name} AS BEGIN
  DECLARE @TodayInLocal date;
  DECLARE @FiscalMonthStartDay int;
  DECLARE @FiscalYearStartMonth int;

  SET @FiscalMonthStartDay={config.fiscal.month_start_day}; -- Cannot be >28 or you'll blow up
  SET @FiscalYearStartMonth={config.fiscal.year_start_month};

  SET @TodayInLocal = CONVERT(
    date, 
    -- You need to figure out what your local TZ is called in your server host's registry.
    -- See https://docs.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql?view=sql-server-ver15
    -- for more info.
    -- For example, on my machine, for MST, the following line would be:
    -- GETUTCDATE() AT TIME ZONE 'UTC' AT TIME ZONE 'Mountain Standard Time'
    GETUTCDATE() AT TIME ZONE 'UTC' AT TIME ZONE IntentionallyCrashScriptIfItTriesToRun
  );

  WITH RelativeToToday AS (
    SELECT
      FiscalYearStartToday = IIF(
        DATEDIFF(
          day, 
          DATEFROMPARTS(
            DATEPART(year, @TodayInLocal), 
            @FiscalYearStartMonth,
            @FiscalMonthStartDay
          ),
          @TodayInLocal
        ) >= 0,
        DATEFROMPARTS(
          DATEPART(year, @TodayInLocal), 
          @FiscalYearStartMonth,
          @FiscalMonthStartDay
        ),
        DATEFROMPARTS(
            DATEPART(year, @TodayInLocal) - 1, 
            @FiscalYearStartMonth,
            @FiscalMonthStartDay
          )
      ),

      FiscalMonthStartToday = IIF(
        DATEPART(
          day,
          @TodayInLocal
        ) >= @FiscalMonthStartDay,
        DATEFROMPARTS(
          YEAR(@TodayInLocal),
          MONTH(@TodayInLocal),
          @FiscalMonthStartDay
        ),
        DATEFROMPARTS(
          YEAR(
            DATEADD(
              month,
              -1,
              @TodayInLocal
            )
          ),
          MONTH(
            DATEADD(
              month,
              -1,
              @TodayInLocal
            )
          ),
          @FiscalMonthStartDay
        )
      )
  ),

  RelativeToTodayQuarter AS (
    SELECT
      *,
      FiscalQuarterStartToday = IIF(
        DATEPART(
          quarter,
          @TodayInLocal
        ) = DATEPART(
          quarter,
          DATEADD(
            day,
            -1,
            DATEADD(
              month,
              1,
              FiscalMonthStartToday
            )
          )
        ),
        DATEFROMPARTS(
          YEAR(
            DATEADD(
              month,
              -1,
              DATEADD(
                  quarter,
                  DATEDIFF(quarter, 0, @TodayInLocal),
                  0
              )
            )
          ),
          MONTH(
            DATEADD(
              month,
              -1,
              DATEADD(
                  quarter,
                  DATEDIFF(quarter, 0, @TodayInLocal),
                  0
              )
            )
          ),
          @FiscalMonthStartDay
        ),
        DATEFROMPARTS(
          YEAR(
            DATEADD(
              month,
              -1,
              DATEADD(
                  quarter,
                  DATEDIFF(quarter, 0, @TodayInLocal) + 1,
                  0
              )
            )
          ),
          MONTH(
            DATEADD(
              month,
              -1,
              DATEADD(
                  quarter,
                  DATEDIFF(quarter, 0, @TodayInLocal) + 1,
                  0
              )
            )
          ),
          @FiscalMonthStartDay
        )
      )
    FROM
      RelativeToToday
  ),

  BurnupsAsOfToday AS (
    SELECT
      DayOfWeekToday = DATEPART(
        weekday,
        @TodayInLocal
      ),
      DayOfMonthToday = DATEPART(
        day,
        @TodayInLocal
      ),
      DayOfQuarterToday = DATEDIFF(
        day,
        DATEADD(
          quarter,
          DATEDIFF(quarter, 0, @TodayInLocal),
          0
        ),
        @TodayInLocal
      ) + 1,
      DayOfYearToday = DATEPART(
        dayofyear,
        @TodayInLocal
      ),
      FiscalDayOfMonthToday = DATEDIFF(
        day,
        FiscalMonthStartToday,
        @TodayInLocal
      ) + 1,
      FiscalDayOfQuarterToday = DATEDIFF(
        day,
        FiscalQuarterStartToday,
        @TodayInLocal
      ) + 1,
      FiscalDayOfYearToday = DATEDIFF(
        day,
        FiscalYearStartToday,
        @TodayInLocal
      ) + 1
    FROM
      RelativeToTodayQuarter
  ),
  
  DateCalculations AS (
    SELECT
      d.{dd_cols.date_key.name},
      {dd_cols.day_offset_from_today.name} = DATEDIFF(
        day,
        @TodayInLocal,
        d.{dd_cols.the_date.name}
      ),
      {dd_cols.month_offset_from_today.name} = DATEDIFF(
        month,
        @TodayInLocal,
        d.{dd_cols.the_date.name}
      ),
      {dd_cols.quarter_offset_from_today.name} = DATEDIFF(
        quarter,
        @TodayInLocal,
        d.{dd_cols.the_date.name}
      ),
      {dd_cols.year_offset_from_today.name} = DATEDIFF(
        year,
        @TodayInLocal,
        d.{dd_cols.the_date.name}
      ),
      {dd_cols.today_flag.name} = IIF(
        d.{dd_cols.the_date.name} = @TodayInLocal,
        1,
        0
      ),
      {dd_cols.current_week_starting_monday_flag.name} = IIF(
        DATEDIFF(
          week,
          CONVERT(date, GETDATE()),
          DATEADD(day, -1, d.{dd_cols.the_date.name})
        ) = 0,
        1,
        0
      ),
      {dd_cols.current_week_flag.name} = IIF(
        DATEDIFF(week, @TodayInLocal, d.{dd_cols.the_date.name}) = 0,
        1,
        0
      ),
      {dd_cols.prior_week_flag.name} = IIF(
        DATEDIFF(week, @TodayInLocal, d.{dd_cols.the_date.name}) = -1,
        1,
        0
      ),
      {dd_cols.next_week_flag.name} = IIF(
        DATEDIFF(week, @TodayInLocal, d.{dd_cols.the_date.name}) = 1,
        1,
        0
      ),
      {dd_cols.current_month_flag.name} = IIF(
        DATEDIFF(month, @TodayInLocal, d.{dd_cols.the_date.name}) = 0,
        1,
        0
      ),
      {dd_cols.prior_month_flag.name} = IIF(
        DATEDIFF(month, @TodayInLocal, d.{dd_cols.the_date.name}) = -1,
        1,
        0
      ),
      {dd_cols.next_month_flag.name} = IIF(
        DATEDIFF(month, @TodayInLocal, d.{dd_cols.the_date.name}) = 1,
        1,
        0
      ),
      {dd_cols.current_quarter_flag.name} = IIF(
        DATEDIFF(quarter, @TodayInLocal, d.{dd_cols.the_date.name}) = 0,
        1,
        0
      ),
      {dd_cols.prior_quarter_flag.name} = IIF(
        DATEDIFF(quarter, @TodayInLocal, d.{dd_cols.the_date.name}) = -1,
        1,
        0
      ),
      {dd_cols.next_quarter_flag.name} = IIF(
        DATEDIFF(quarter, @TodayInLocal, d.{dd_cols.the_date.name}) = 1,
        1,
        0
      ),
      {dd_cols.current_year_flag.name} = IIF(
        DATEDIFF(year, @TodayInLocal, d.{dd_cols.the_date.name}) = 0,
        1,
        0
      ),
      {dd_cols.prior_year_flag.name} = IIF(
        DATEDIFF(year, @TodayInLocal, d.{dd_cols.the_date.name}) = -1,
        1,
        0
      ),
      {dd_cols.next_year_flag.name} = IIF(
        DATEDIFF(year, @TodayInLocal, d.{dd_cols.the_date.name}) = 1,
        1,
        0
      ),
      {dd_cols.weekly_burnup_starting_monday.name} = IIF(
        DayOfWeekStartingMonday <= (
          DATEPART(
            weekday,
            @TodayInLocal
          ) + @@DATEFIRST + 6 - 1
        ) % 7 + 1,
        1,
        0
      ),
      {dd_cols.weekly_burnup.name} = IIF(
        d.{dd_cols.day_of_week.name} <= r.DayOfWeekToday,
        1,
        0
      ),
      {dd_cols.monthly_burnup.name} = IIF(
        d.{dd_cols.day_of_month.name} <= r.DayOfMonthToday,
        1,
        0
      ),
      {dd_cols.quarterly_burnup.name} = IIF(
        d.{dd_cols.day_of_quarter.name} <= r.DayOfQuarterToday,
        1,
        0
      ),
      {dd_cols.yearly_burnup.name} = IIF(
        d.{dd_cols.day_of_year.name} <= r.DayOfYearToday,
        1,
        0
      ),
      {dd_cols.fiscal_current_month_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          d.{dd_cols.fiscal_current_month_start.name} AND d.{dd_cols.fiscal_current_month_end.name},
        1,
        0
      ),
      {dd_cols.fiscal_prior_month_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          d.{dd_cols.fiscal_prior_month_start.name} AND d.{dd_cols.fiscal_prior_month_end.name},
        1,
        0
      ),
      {dd_cols.fiscal_next_month_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          d.{dd_cols.fiscal_next_month_start.name} AND d.{dd_cols.fiscal_next_month_end.name},
        1,
        0
      ),
      {dd_cols.fiscal_current_quarter_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          d.{dd_cols.fiscal_current_quarter_start.name} AND d.{dd_cols.fiscal_current_quarter_end.name},
        1,
        0
      ),
      {dd_cols.fiscal_prior_quarter_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          d.{dd_cols.fiscal_prior_quarter_start.name} AND d.{dd_cols.fiscal_prior_quarter_end.name},
        1,
        0
      ),
      {dd_cols.fiscal_next_quarter_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          d.{dd_cols.fiscal_next_quarter_start.name} AND d.{dd_cols.fiscal_next_quarter_end.name},
        1,
        0
      ),
      {dd_cols.fiscal_current_year_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          d.{dd_cols.fiscal_current_year_start.name} AND d.{dd_cols.fiscal_current_year_end.name},
        1,
        0
      ),
      {dd_cols.fiscal_prior_year_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          d.{dd_cols.fiscal_prior_year_start.name} AND d.{dd_cols.fiscal_prior_year_end.name},
        1,
        0
      ),
      {dd_cols.fiscal_next_year_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          d.{dd_cols.fiscal_next_year_start.name} AND d.{dd_cols.fiscal_next_year_end.name},
        1,
        0
      ),
      {dd_cols.fiscal_monthly_burnup.name} = IIF(
        d.{dd_cols.fiscal_day_of_month.name} <= r.FiscalDayOfMonthToday,
        1,
        0
      ),
      {dd_cols.fiscal_quarterly_burnup.name} = IIF(
        d.{dd_cols.fiscal_day_of_quarter.name} <= r.FiscalDayOfQuarterToday,
        1,
        0
      ),
      {dd_cols.fiscal_yearly_burnup.name} = IIF(
        d.{dd_cols.fiscal_day_of_year.name} <= r.FiscalDayOfyearToday,
        1,
        0
      ),
      BusinessDayFlag = IIF(
        {business_day_clause if len(business_day_list) > 0 else ''}DATEPART(
          weekday,
          d.{dd_cols.the_date.name}
        ) IN (1, 7),
        0,
        1
      ),
{holiday_column_clause}
    FROM
      {dd_conf.table_schema}.{dd_conf.table_name} AS d
      CROSS JOIN BurnupsAsOfToday AS r
{holiday_join}
  )

  UPDATE d
  SET
    d.{dd_cols.date_key.name} = dc.{dd_cols.date_key.name},
    d.{dd_cols.the_date.name} = dc.{dd_cols.the_date.name},
    d.{dd_cols.iso_date_name.name} = dc.{dd_cols.iso_date_name.name},
    d.{dd_cols.american_date_name.name} = dc.{dd_cols.american_date_name.name},
    d.{dd_cols.day_of_week_name.name} = dc.{dd_cols.day_of_week_name.name},
    d.{dd_cols.day_of_week_abbrev.name} = dc.{dd_cols.day_of_week_abbrev.name},
    d.{dd_cols.month_name.name} = dc.{dd_cols.month_name.name},
    d.{dd_cols.month_abbrev.name} = dc.{dd_cols.month_abbrev.name},
    d.{dd_cols.year_week_name.name} = dc.{dd_cols.year_week_name.name},
    d.{dd_cols.year_month_name.name} = dc.{dd_cols.year_month_name.name},
    d.{dd_cols.month_year_name.name} = dc.{dd_cols.month_year_name.name},
    d.{dd_cols.year_quarter_name.name} = dc.{dd_cols.year_quarter_name.name},
    d.{dd_cols.year.name} = dc.{dd_cols.year.name},
    d.{dd_cols.year_week.name} = dc.{dd_cols.year_week.name},
    d.{dd_cols.iso_year_week_code.name} = dc.{dd_cols.iso_year_week_code.name},
    d.{dd_cols.year_month.name} = dc.{dd_cols.year_month.name},
    d.{dd_cols.year_quarter.name} = dc.{dd_cols.year_quarter.name},
    d.{dd_cols.day_of_week_starting_monday.name} = dc.{dd_cols.day_of_week_starting_monday.name},
    d.{dd_cols.day_of_week.name} = dc.{dd_cols.day_of_week.name},
    d.{dd_cols.day_of_month.name} = dc.{dd_cols.day_of_month.name},
    d.{dd_cols.day_of_quarter.name} = dc.{dd_cols.day_of_quarter.name},
    d.{dd_cols.day_of_year.name} = dc.{dd_cols.day_of_year.name},
    d.{dd_cols.week_of_quarter.name} = dc.{dd_cols.week_of_quarter.name},
    d.{dd_cols.week_of_year.name} = dc.{dd_cols.week_of_year.name},
    d.{dd_cols.iso_week_of_year.name} = dc.{dd_cols.iso_week_of_year.name},
    d.{dd_cols.month.name} = dc.{dd_cols.month.name},
    d.{dd_cols.month_of_quarter.name} = dc.{dd_cols.month_of_quarter.name},
    d.{dd_cols.quarter.name} = dc.{dd_cols.quarter.name},
    d.{dd_cols.days_in_month.name} = dc.{dd_cols.days_in_month.name},
    d.{dd_cols.days_in_quarter.name} = dc.{dd_cols.days_in_quarter.name},
    d.{dd_cols.days_in_year.name} = dc.{dd_cols.days_in_year.name},
    d.{dd_cols.day_offset_from_today.name} = dc.{dd_cols.day_offset_from_today.name},
    d.{dd_cols.month_offset_from_today.name} = dc.{dd_cols.month_offset_from_today.name},
    d.{dd_cols.quarter_offset_from_today.name} = dc.{dd_cols.quarter_offset_from_today.name},
    d.{dd_cols.year_offset_from_today.name} = dc.{dd_cols.year_offset_from_today.name},
    d.{dd_cols.today_flag.name} = dc.{dd_cols.today_flag.name},
    d.{dd_cols.current_week_starting_monday_flag.name} = dc.{dd_cols.current_week_starting_monday_flag.name},
    d.{dd_cols.current_week_flag.name} = dc.{dd_cols.current_week_flag.name},
    d.{dd_cols.prior_week_flag.name} = dc.{dd_cols.prior_week_flag.name},
    d.{dd_cols.next_week_flag.name} = dc.{dd_cols.next_week_flag.name},
    d.{dd_cols.current_month_flag.name} = dc.{dd_cols.current_month_flag.name},
    d.{dd_cols.prior_month_flag.name} = dc.{dd_cols.prior_month_flag.name},
    d.{dd_cols.next_month_flag.name} = dc.{dd_cols.next_month_flag.name},
    d.{dd_cols.current_quarter_flag.name} = dc.{dd_cols.current_quarter_flag.name},
    d.{dd_cols.prior_quarter_flag.name} = dc.{dd_cols.prior_quarter_flag.name},
    d.{dd_cols.next_quarter_flag.name} = dc.{dd_cols.next_quarter_flag.name},
    d.{dd_cols.current_year_flag.name} = dc.{dd_cols.current_year_flag.name},
    d.{dd_cols.prior_year_flag.name} = dc.{dd_cols.prior_year_flag.name},
    d.{dd_cols.next_year_flag.name} = dc.{dd_cols.next_year_flag.name},
    d.{dd_cols.weekday_flag.name} = dc.{dd_cols.weekday_flag.name},
    d.{dd_cols.business_day_flag.name} = dc.{dd_cols.business_day_flag.name},
    d.{dd_cols.first_day_of_month_flag.name} = dc.{dd_cols.first_day_of_month_flag.name},
    d.{dd_cols.last_day_of_month_flag.name} = dc.{dd_cols.last_day_of_month_flag.name},
    d.{dd_cols.first_day_of_quarter_flag.name} = dc.{dd_cols.first_day_of_quarter_flag.name},
    d.{dd_cols.last_day_of_quarter_flag.name} = dc.{dd_cols.last_day_of_quarter_flag.name},
    d.{dd_cols.first_day_of_year_flag.name} = dc.{dd_cols.first_day_of_year_flag.name},
    d.{dd_cols.last_day_of_year_flag.name} = dc.{dd_cols.last_day_of_year_flag.name},
    d.{dd_cols.fraction_of_week.name} = dc.{dd_cols.fraction_of_week.name},
    d.{dd_cols.fraction_of_month.name} = dc.{dd_cols.fraction_of_month.name},
    d.{dd_cols.fraction_of_quarter.name} = dc.{dd_cols.fraction_of_quarter.name},
    d.{dd_cols.fraction_of_year.name} = dc.{dd_cols.fraction_of_year.name},
    d.{dd_cols.prior_day.name} = dc.{dd_cols.prior_day.name},
    d.{dd_cols.next_day.name} = dc.{dd_cols.next_day.name},
    d.{dd_cols.same_day_prior_week.name} = dc.{dd_cols.same_day_prior_week.name},
    d.{dd_cols.same_day_prior_month.name} = dc.{dd_cols.same_day_prior_month.name},
    d.{dd_cols.same_day_prior_quarter.name} = dc.{dd_cols.same_day_prior_quarter.name},
    d.{dd_cols.same_day_prior_year.name} = dc.{dd_cols.same_day_prior_year.name},
    d.{dd_cols.same_day_next_week.name} = dc.{dd_cols.same_day_next_week.name},
    d.{dd_cols.same_day_next_month.name} = dc.{dd_cols.same_day_next_month.name},
    d.{dd_cols.same_day_next_quarter.name} = dc.{dd_cols.same_day_next_quarter.name},
    d.{dd_cols.same_day_next_year.name} = dc.{dd_cols.same_day_next_year.name},
    d.{dd_cols.current_week_start.name} = dc.{dd_cols.current_week_start.name},
    d.{dd_cols.current_week_end.name} = dc.{dd_cols.current_week_end.name},
    d.{dd_cols.current_month_start.name} = dc.{dd_cols.current_month_start.name},
    d.{dd_cols.current_month_end.name} = dc.{dd_cols.current_month_end.name},
    d.{dd_cols.current_quarter_start.name} = dc.{dd_cols.current_quarter_start.name},
    d.{dd_cols.current_quarter_end.name} = dc.{dd_cols.current_quarter_end.name},
    d.{dd_cols.current_year_start.name} = dc.{dd_cols.current_year_start.name},
    d.{dd_cols.current_year_end.name} = dc.{dd_cols.current_year_end.name},
    d.{dd_cols.prior_week_start.name} = dc.{dd_cols.prior_week_start.name},
    d.{dd_cols.prior_week_end.name} = dc.{dd_cols.prior_week_end.name},
    d.{dd_cols.prior_month_start.name} = dc.{dd_cols.prior_month_start.name},
    d.{dd_cols.prior_month_end.name} = dc.{dd_cols.prior_month_end.name},
    d.{dd_cols.prior_quarter_start.name} = dc.{dd_cols.prior_quarter_start.name},
    d.{dd_cols.prior_quarter_end.name} = dc.{dd_cols.prior_quarter_end.name},
    d.{dd_cols.prior_year_start.name} = dc.{dd_cols.prior_year_start.name},
    d.{dd_cols.prior_year_end.name} = dc.{dd_cols.prior_year_end.name},
    d.{dd_cols.next_week_start.name} = dc.{dd_cols.next_week_start.name},
    d.{dd_cols.next_week_end.name} = dc.{dd_cols.next_week_end.name},
    d.{dd_cols.next_month_start.name} = dc.{dd_cols.next_month_start.name},
    d.{dd_cols.next_month_end.name} = dc.{dd_cols.next_month_end.name},
    d.{dd_cols.next_quarter_start.name} = dc.{dd_cols.next_quarter_start.name},
    d.{dd_cols.next_quarter_end.name} = dc.{dd_cols.next_quarter_end.name},
    d.{dd_cols.next_year_start.name} = dc.{dd_cols.next_year_start.name},
    d.{dd_cols.next_year_end.name} = dc.{dd_cols.next_year_end.name},
    d.{dd_cols.weekly_burnup_starting_monday.name} = dc.{dd_cols.weekly_burnup_starting_monday.name},
    d.{dd_cols.weekly_burnup.name} = dc.{dd_cols.weekly_burnup.name},
    d.{dd_cols.monthly_burnup.name} = dc.{dd_cols.monthly_burnup.name},
    d.{dd_cols.quarterly_burnup.name} = dc.{dd_cols.quarterly_burnup.name},
    d.{dd_cols.yearly_burnup.name} = dc.{dd_cols.yearly_burnup.name},
    d.{dd_cols.fiscal_month_name.name} = dc.{dd_cols.fiscal_month_name.name},
    d.{dd_cols.fiscal_month_abbrev.name} = dc.{dd_cols.fiscal_month_abbrev.name},
    d.{dd_cols.fiscal_year_week_name.name} = dc.{dd_cols.fiscal_year_week_name.name},
    d.{dd_cols.fiscal_year_month_name.name} = dc.{dd_cols.fiscal_year_month_name.name},
    d.{dd_cols.fiscal_month_year_name.name} = dc.{dd_cols.fiscal_month_year_name.name},
    d.{dd_cols.fiscal_year_quarter_name.name} = dc.{dd_cols.fiscal_year_quarter_name.name},
    d.{dd_cols.fiscal_year.name} = dc.{dd_cols.fiscal_year.name},
    d.{dd_cols.fiscal_year_week.name} = dc.{dd_cols.fiscal_year_week.name},
    d.{dd_cols.fiscal_year_month.name} = dc.{dd_cols.fiscal_year_month.name},
    d.{dd_cols.fiscal_year_quarter.name} = dc.{dd_cols.fiscal_year_quarter.name},
    d.{dd_cols.fiscal_day_of_month.name} = dc.{dd_cols.fiscal_day_of_month.name},
    d.{dd_cols.fiscal_day_of_quarter.name} = dc.{dd_cols.fiscal_day_of_quarter.name},
    d.{dd_cols.fiscal_day_of_year.name} = dc.{dd_cols.fiscal_day_of_year.name},
    d.{dd_cols.fiscal_week_of_quarter.name} = dc.{dd_cols.fiscal_week_of_quarter.name},
    d.{dd_cols.fiscal_week_of_year.name} = dc.{dd_cols.fiscal_week_of_year.name},
    d.{dd_cols.fiscal_month.name} = dc.{dd_cols.fiscal_month.name},
    d.{dd_cols.fiscal_month_of_quarter.name} = dc.{dd_cols.fiscal_month_of_quarter.name},
    d.{dd_cols.fiscal_quarter.name} = dc.{dd_cols.fiscal_quarter.name},
    d.{dd_cols.fiscal_days_in_month.name} = dc.{dd_cols.fiscal_days_in_month.name},
    d.{dd_cols.fiscal_days_in_quarter.name} = dc.{dd_cols.fiscal_days_in_quarter.name},
    d.{dd_cols.fiscal_days_in_year.name} = dc.{dd_cols.fiscal_days_in_year.name},
    d.{dd_cols.fiscal_current_month_flag.name} = dc.{dd_cols.fiscal_current_month_flag.name},
    d.{dd_cols.fiscal_prior_month_flag.name} = dc.{dd_cols.fiscal_prior_month_flag.name},
    d.{dd_cols.fiscal_next_month_flag.name} = dc.{dd_cols.fiscal_next_month_flag.name},
    d.{dd_cols.fiscal_current_quarter_flag.name} = dc.{dd_cols.fiscal_current_quarter_flag.name},
    d.{dd_cols.fiscal_prior_quarter_flag.name} = dc.{dd_cols.fiscal_prior_quarter_flag.name},
    d.{dd_cols.fiscal_next_quarter_flag.name} = dc.{dd_cols.fiscal_next_quarter_flag.name},
    d.{dd_cols.fiscal_current_year_flag.name} = dc.{dd_cols.fiscal_current_year_flag.name},
    d.{dd_cols.fiscal_prior_year_flag.name} = dc.{dd_cols.fiscal_prior_year_flag.name},
    d.{dd_cols.fiscal_next_year_flag.name} = dc.{dd_cols.fiscal_next_year_flag.name},
    d.{dd_cols.fiscal_first_day_of_month_flag.name} = dc.{dd_cols.fiscal_first_day_of_month_flag.name},
    d.{dd_cols.fiscal_last_day_of_month_flag.name} = dc.{dd_cols.fiscal_last_day_of_month_flag.name},
    d.{dd_cols.fiscal_first_day_of_quarter_flag.name} = dc.{dd_cols.fiscal_first_day_of_quarter_flag.name},
    d.{dd_cols.fiscal_last_day_of_quarter_flag.name} = dc.{dd_cols.fiscal_last_day_of_quarter_flag.name},
    d.{dd_cols.fiscal_first_day_of_year_flag.name} = dc.{dd_cols.fiscal_first_day_of_year_flag.name},
    d.{dd_cols.fiscal_last_day_of_year_flag.name} = dc.{dd_cols.fiscal_last_day_of_year_flag.name},
    d.{dd_cols.fiscal_fraction_of_month.name} = dc.{dd_cols.fiscal_fraction_of_month.name},
    d.{dd_cols.fiscal_fraction_of_quarter.name} = dc.{dd_cols.fiscal_fraction_of_quarter.name},
    d.{dd_cols.fiscal_fraction_of_year.name} = dc.{dd_cols.fiscal_fraction_of_year.name},
    d.{dd_cols.fiscal_current_month_start.name} = dc.{dd_cols.fiscal_current_month_start.name},
    d.{dd_cols.fiscal_current_month_end.name} = dc.{dd_cols.fiscal_current_month_end.name},
    d.{dd_cols.fiscal_current_quarter_start.name} = dc.{dd_cols.fiscal_current_quarter_start.name},
    d.{dd_cols.fiscal_current_quarter_end.name} = dc.{dd_cols.fiscal_current_quarter_end.name},
    d.{dd_cols.fiscal_current_year_start.name} = dc.{dd_cols.fiscal_current_year_start.name},
    d.{dd_cols.fiscal_current_year_end.name} = dc.{dd_cols.fiscal_current_year_end.name},
    d.{dd_cols.fiscal_prior_month_start.name} = dc.{dd_cols.fiscal_prior_month_start.name},
    d.{dd_cols.fiscal_prior_month_end.name} = dc.{dd_cols.fiscal_prior_month_end.name},
    d.{dd_cols.fiscal_prior_quarter_start.name} = dc.{dd_cols.fiscal_prior_quarter_start.name},
    d.{dd_cols.fiscal_prior_quarter_end.name} = dc.{dd_cols.fiscal_prior_quarter_end.name},
    d.{dd_cols.fiscal_prior_year_start.name} = dc.{dd_cols.fiscal_prior_year_start.name},
    d.{dd_cols.fiscal_prior_year_end.name} = dc.{dd_cols.fiscal_prior_year_end.name},
    d.{dd_cols.fiscal_next_month_start.name} = dc.{dd_cols.fiscal_next_month_start.name},
    d.{dd_cols.fiscal_next_month_end.name} = dc.{dd_cols.fiscal_next_month_end.name},
    d.{dd_cols.fiscal_next_quarter_start.name} = dc.{dd_cols.fiscal_next_quarter_start.name},
    d.{dd_cols.fiscal_next_quarter_end.name} = dc.{dd_cols.fiscal_next_quarter_end.name},
    d.{dd_cols.fiscal_next_year_start.name} = dc.{dd_cols.fiscal_next_year_start.name},
    d.{dd_cols.fiscal_next_year_end.name} = dc.{dd_cols.fiscal_next_year_end.name},
    d.{dd_cols.fiscal_monthly_burnup.name} = dc.{dd_cols.fiscal_monthly_burnup.name},
    d.{dd_cols.fiscal_quarterly_burnup.name} = dc.{dd_cols.fiscal_quarterly_burnup.name},
    d.{dd_cols.fiscal_yearly_burnup.name} = dc.{dd_cols.fiscal_yearly_burnup.name},
{holiday_columns}
  FROM
    {dd_conf.table_schema}.{dd_conf.table_name} AS d
    INNER JOIN DateCalculations AS dc
      ON d.{dd_cols.date_key.name} = dc.{dd_cols.date_key.name}
END
GO
"""
