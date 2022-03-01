from ...config import Config
from .tsql_columns import TSQLDimDateColumns


# Note: Rather than trying to be "smart" and removing or adding columns based on whether or not they should be present,
# we just remove or rename them at the very end before the INSERT statement. The performance change is so negligible for a one-time-setup
# script that it doesn't make sense to take on the complication.
def dim_date_insert_template(config: Config, columns: TSQLDimDateColumns) -> str:
    holiday_join = []
    business_day_list = []
    holiday_columndef = []
    if config.holidays.generate_holidays:
        for i, t in enumerate(config.holidays.holiday_types):
            holiday_join.append(
                f"    LEFT OUTER JOIN {config.holidays.holidays_schema_name}.{config.holidays.holidays_table_name} AS h{i} -- {t.name}"
            )
            holiday_join.append(
                f"      ON fh.DateKey = h{i}.{config.holidays.holidays_columns.date_key.name} AND h{i}.{config.holidays.holidays_columns.holiday_type_key.name} = (SELECT {config.holidays.holiday_types_columns.holiday_type_key.name} FROM {config.holidays.holiday_types_schema_name}.{config.holidays.holiday_types_table_name} WHERE {config.holidays.holiday_types_columns.holiday_type_name.name} = '{t.name}')"
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
            holiday_columndef.append("")
            holiday_columndef.append(
                f"      {t.generated_column_prefix}{t.generated_name_column_postfix} = h{i}.{config.holidays.holidays_columns.holiday_name.name},"
            )
            holiday_columndef.append("")

        holiday_join = "\n".join(holiday_join)
        business_day_clause = "\n".join(business_day_list) + "\n      OR "
        holiday_column_clause = ",\n\n" + "\n".join(holiday_columndef)[:-2]
    else:
        holiday_join = ""
        business_day_clause = ""
        holiday_column_clause = ""

    insert_column_clause = ",\n  ".join(map(lambda c: c.name, columns))

    return f"""SET DATEFIRST 7;

DECLARE @TodayInLocal date;
DECLARE @FirstDate date;
DECLARE @NumberOfYearsToGenerate int;
DECLARE @LastDate date;
DECLARE @FiscalMonthStartDay int;
DECLARE @FiscalYearStartMonth int;
DECLARE @FiscalMonthPeriodEndMatchesCalendar bit;
DECLARE @FiscalQuarterPeriodEndMatchesCalendar bit;
DECLARE @FiscalYearPeriodEndMatchesCalendar bit;
DECLARE @ISODatekeyFormatNumber int;
DECLARE @ISO8601DatestringFormatNumber int;
DECLARE @USDatestringFormatNumber int;

SET @FirstDate='{config.date_range.start_date.isoformat()}';
SET @NumberOfYearsToGenerate={config.date_range.num_years};


SET @FiscalMonthStartDay={config.fiscal.month_start_day}; -- Cannot be >28 or you'll blow up
SET @FiscalYearStartMonth={config.fiscal.year_start_month};

-- Set @FiscalPeriodEndMatchesCalendar to 1 if
-- your fiscal calendar takes on the month/quarter of
-- the fiscal period end date rather than the start date.
-- For example, if your month runs the 26th through the 25th,
-- and Dec 25-Jan 26 is considered "January", set it to 1.
-- If Dec 25-Jan 26 is considered "December", set to 0.
SET @FiscalMonthPeriodEndMatchesCalendar={1 if config.fiscal.month_end_matches_calendar else 0};
SET @FiscalQuarterPeriodEndMatchesCalendar={1 if config.fiscal.quarter_end_matches_calendar else 0};
SET @FiscalYearPeriodEndMatchesCalendar={1 if config.fiscal.year_end_matches_calendar else 0};


-- If you need to change what timezone you want to base your relative flags on
-- be sure to make sure your target system recognizes the timezone
SET @TodayInLocal = CONVERT(
  date, 
  -- You need to figure out what your local TZ is called in your server host's registry.
  -- See https://docs.microsoft.com/en-us/sql/t-sql/queries/at-time-zone-transact-sql?view=sql-server-ver15
  -- for more info.
  -- For example, on my machine, for MST, the following line would be:
  -- GETUTCDATE() AT TIME ZONE 'UTC' AT TIME ZONE 'Mountain Standard Time'
  GETUTCDATE() AT TIME ZONE 'UTC' AT TIME ZONE IntentionallyCrashScriptIfItTriesToRun
);

-- No touchie these lines; adjust the above instead
SET @LastDate=DATEADD(YEAR,@NumberOfYearsToGenerate,@FirstDate);
SET @ISODatekeyFormatNumber=112;
SET @ISO8601DatestringFormatNumber=23;
SET @USDatestringFormatNumber=101;

-- For all comments, assume:
-- The {config.dim_date.columns.date_key.name} is 20210101
-- @TodayInLocal = 2021-07-29
-- @FiscalMonthStartDay=26;
-- @FiscalYearStartMonth=12;
-- @FiscalMonthPeriodEndMatchesCalendar=1;
-- @FiscalQuarterPeriodEndMatchesCalendar=1;
-- @FiscalYearPeriodEndMatchesCalendar=1;
WITH Recursion AS (
  SELECT
    {config.dim_date.columns.date_key.name} = CONVERT(
      int,
      CONVERT(
        varchar(8),
        @FirstDate,
        @ISODatekeyFormatNumber
      )
    ),

    {config.dim_date.columns.the_date.name} = @FirstDate
  UNION ALL
  SELECT
    CONVERT(
      int,
      CONVERT(
        varchar(8),
        DATEADD(DAY, 1, {config.dim_date.columns.the_date.name}),
        @ISODatekeyFormatNumber
      )
    ),
    DATEADD(DAY, 1, {config.dim_date.columns.the_date.name})
  FROM Recursion
  WHERE {config.dim_date.columns.the_date.name} < @LastDate
),

BaseDatesFirst AS (
  SELECT 
    {config.dim_date.columns.date_key.name},
    {config.dim_date.columns.the_date.name},
    CalendarYearStart = DATEFROMPARTS(
      YEAR({config.dim_date.columns.the_date.name}),
      01,
      01
    ),
    CalendarYearEnd = DATEFROMPARTS(
      YEAR({config.dim_date.columns.the_date.name}),
      12,
      31
    ),
    CalendarQuarterStart = CAST(
      DATEADD(
        quarter,
        DATEDIFF(quarter, 0, {config.dim_date.columns.the_date.name}),
        0
      ) AS date
    ),
    CalendarQuarterEnd = CAST(
      DATEADD(
        day, 
        -1, 
        DATEADD(
          quarter, 
          DATEDIFF(quarter, 0, {config.dim_date.columns.the_date.name}) + 1,
          0
        )
      ) AS date
    ),
    CalendarMonthStart = DATEFROMPARTS(
      YEAR({config.dim_date.columns.the_date.name}),
      MONTH({config.dim_date.columns.the_date.name}),
      01
    ),
    CalendarMonthEnd = EOMONTH({config.dim_date.columns.the_date.name}),
    CalendarWeekStart = DATEADD(
      day, 
      1-DATEPART(
        WEEKDAY, 
        {config.dim_date.columns.the_date.name}
      ), 
      {config.dim_date.columns.the_date.name}
    ),
    CalendarWeekEnd = DATEADD(
      day, 
      7-DATEPART(
        WEEKDAY, 
        {config.dim_date.columns.the_date.name}
      ), 
      {config.dim_date.columns.the_date.name}
    ),

    CalendarYearStartToday = DATEFROMPARTS(
      YEAR(@TodayInLocal),
      01,
      01
    ),
    CalendarYearEndToday = DATEFROMPARTS(
      YEAR(@TodayInLocal),
      12,
      31
    ),
    CalendarQuarterStartToday = CAST(
      DATEADD(
        quarter,
        DATEDIFF(quarter, 0, @TodayInLocal),
        0
      ) AS date
    ),
    CalendarQuarterEndToday = CAST(
      DATEADD(
        day, 
        -1, 
        DATEADD(
          quarter, 
          DATEDIFF(quarter, 0, @TodayInLocal) + 1,
          0
        )
      ) AS date
    ),
    CalendarMonthStartToday = DATEFROMPARTS(
      YEAR(@TodayInLocal),
      MONTH(@TodayInLocal),
      01
    ),
    CalendarMonthEndToday = EOMONTH(@TodayInLocal),
    CalendarWeekStartToday = DATEADD(
      day, 
      1-DATEPART(
        WEEKDAY, 
        @TodayInLocal
      ), 
      @TodayInLocal
    ),
    CalendarWeekEndToday = DATEADD(
      day, 
      7-DATEPART(
        WEEKDAY, 
        @TodayInLocal
      ), 
      @TodayInLocal
    ),

    -- This looks insane, but it's not too complicated. Examples:
    -- For:
    --     {config.dim_date.columns.the_date.name} = '2021-01-01';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2020-12-26'
    -- For: 
    --     {config.dim_date.columns.the_date.name} = '2020-12-26';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2020-12-26'
    -- For: 
    --     {config.dim_date.columns.the_date.name} = '2020-12-25';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2019-12-26'
    --
    -- You can work out implementation details yourself if you'd like.
    FiscalYearStart = IIF(
      DATEDIFF(
        day, 
        DATEFROMPARTS(
          DATEPART(year, {config.dim_date.columns.the_date.name}), 
          @FiscalYearStartMonth,
          @FiscalMonthStartDay
        ),
        {config.dim_date.columns.the_date.name}
      ) >= 0,
      DATEFROMPARTS(
        DATEPART(year, {config.dim_date.columns.the_date.name}), 
        @FiscalYearStartMonth,
        @FiscalMonthStartDay
      ),
      DATEFROMPARTS(
          DATEPART(year, {config.dim_date.columns.the_date.name}) - 1, 
          @FiscalYearStartMonth,
          @FiscalMonthStartDay
        )
    ),

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
    )
  FROM Recursion
),

-- Much easier to reuse some values calculated in
-- BaseDates than to do it in BaseDates
BaseDatesSecond AS (
  SELECT 
    *,
    FiscalYearEnd = DATEADD(
      day,
      -1,
      DATEADD(
        year,
        1,
        FiscalYearStart
      )
    ),

    FiscalYearEndToday = DATEADD(
      day,
      -1,
      DATEADD(
        year,
        1,
        FiscalYearStartToday
      )
    )
  FROM BaseDatesFirst
),

BaseDatesThird AS (
  SELECT 
    *,
         
    FiscalPeriodYearReference = IIF(
      @FiscalYearPeriodEndMatchesCalendar = 0,
      FiscalYearStart,
      FiscalYearEnd
    ),

    FiscalPeriodYearReferenceToday = IIF(
      @FiscalYearPeriodEndMatchesCalendar = 0,
      FiscalYearStartToday,
      FiscalYearEndToday
    ),

    -- Same here. Here are some examples:
    -- For:
    --     {config.dim_date.columns.the_date.name} = '2021-01-01';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2020-12-26'
    -- For: 
    --     {config.dim_date.columns.the_date.name} = '2020-12-26';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2020-12-26'
    -- For: 
    --     {config.dim_date.columns.the_date.name} = '2020-12-25';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2020-11-26'
    FiscalMonthStart = IIF(
      DATEPART(
        day,
        {config.dim_date.columns.the_date.name}
      ) >= @FiscalMonthStartDay,
      DATEFROMPARTS(
        YEAR({config.dim_date.columns.the_date.name}),
        MONTH({config.dim_date.columns.the_date.name}),
        @FiscalMonthStartDay
      ),
      DATEFROMPARTS(
        YEAR(
          DATEADD(
            month,
            -1,
            {config.dim_date.columns.the_date.name}
          )
        ),
        MONTH(
          DATEADD(
            month,
            -1,
            {config.dim_date.columns.the_date.name}
          )
        ),
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
  FROM
    BaseDatesSecond
),

BaseDatesFourth AS (
  SELECT 
    *,

    FiscalMonthEnd = DATEADD(
      day,
      -1,
      DATEADD(
        month,
        1,
        FiscalMonthStart
      )
    ),

    FiscalMonthEndToday = DATEADD(
      day,
      -1,
      DATEADD(
        month,
        1,
        FiscalMonthStartToday
      )
    )
  FROM 
    BaseDatesThird
),

BaseDatesFifth AS (
  SELECT 
    *,
    
    FiscalPeriodMonthReference = IIF(
      @FiscalMonthPeriodEndMatchesCalendar = 0,
      FiscalMonthStart,
      FiscalMonthEnd
    ),

    FiscalPeriodMonthReferenceToday = IIF(
      @FiscalMonthPeriodEndMatchesCalendar = 0,
      FiscalMonthStartToday,
      FiscalMonthEndToday
    ),

    FiscalQuarterStart = IIF(
      DATEPART(
        quarter,
        {config.dim_date.columns.the_date.name}
      ) = DATEPART(
        quarter,
        FiscalMonthEnd
      ),
      DATEFROMPARTS(
        YEAR(
          DATEADD(
            month,
            IIF(@FiscalMonthStartDay = 1, 0, -1),
            DATEADD(
                quarter,
                DATEDIFF(quarter, 0, {config.dim_date.columns.the_date.name}),
                0
            )
          )
        ),
        MONTH(
          DATEADD(
            month,
            IIF(@FiscalMonthStartDay = 1, 0, -1),
            DATEADD(
                quarter,
                DATEDIFF(quarter, 0, {config.dim_date.columns.the_date.name}),
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
            IIF(@FiscalMonthStartDay = 1, 0, -1),
            DATEADD(
                quarter,
                DATEDIFF(quarter, 0, {config.dim_date.columns.the_date.name}) + 1,
                0
            )
          )
        ),
        MONTH(
          DATEADD(
            month,
            IIF(@FiscalMonthStartDay = 1, 0, -1),
            DATEADD(
                quarter,
                DATEDIFF(quarter, 0, {config.dim_date.columns.the_date.name}) + 1,
                0
            )
          )
        ),
        @FiscalMonthStartDay
      )
    ),

    FiscalQuarterStartToday = IIF(
      DATEPART(
        quarter,
        @TodayInLocal
      ) = DATEPART(
        quarter,
        FiscalMonthEndToday
      ),
      DATEFROMPARTS(
        YEAR(
          DATEADD(
            month,
            IIF(@FiscalMonthStartDay = 1, 0, -1),
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
            IIF(@FiscalMonthStartDay = 1, 0, -1),
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
            IIF(@FiscalMonthStartDay = 1, 0, -1),
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
            IIF(@FiscalMonthStartDay = 1, 0, -1),
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
    BaseDatesFourth
),

BaseDatesSixth AS (
  SELECT
    *,

    FiscalQuarterEnd = DATEADD(
      day,
      -1,
      DATEADD(
        quarter,
        1,
        FiscalQuarterStart
      )
    ),

    FiscalQuarterEndToday = DATEADD(
      day,
      -1,
      DATEADD(
        quarter,
        1,
        FiscalQuarterStartToday
      )
    )
  FROM
    BaseDatesFifth
),

BaseDatesSeventh AS (
  SELECT
    *,
     
    FiscalPeriodQuarterReference = IIF(
      @FiscalQuarterPeriodEndMatchesCalendar = 0,
      FiscalQuarterStart,
      FiscalQuarterEnd
    ),

    FiscalPeriodQuarterReferenceToday = IIF(
      @FiscalQuarterPeriodEndMatchesCalendar = 0,
      FiscalQuarterStartToday,
      FiscalQuarterEndToday
    )
  FROM 
    BaseDatesSixth
),

-- Generate "Prior" and "Next" dates for all above created dates
RelativeDates AS (
  SELECT
    *,
    PriorCalendarYearStart = DATEADD(
      year,
      -1,
      CalendarYearStart
    ),
    PriorCalendarYearEnd = DATEADD(
      day,
      -1,
      CalendarYearStart
    ),
    PriorCalendarQuarterStart = DATEADD(
      quarter,
      -1,
      CalendarQuarterStart
    ),
    PriorCalendarQuarterEnd = DATEADD(
      day,
      -1,
      CalendarQuarterStart
    ),
    PriorCalendarMonthStart = DATEADD(
      month,
      -1,
      CalendarMonthStart
    ),
    PriorCalendarMonthEnd = DATEADD(
      day,
      -1,
      CalendarMonthStart
    ),
    PriorCalendarWeekStart = DATEADD(
      week,
      -1,
      CalendarWeekStart
    ),
    PriorCalendarWeekEnd = DATEADD(
      day,
      -1,
      CalendarWeekStart
    ),
    NextCalendarYearStart = DATEADD(
      day,
      1,
      CalendarYearEnd
    ),
    NextCalendarYearEnd = DATEFROMPARTS(
      YEAR(CalendarYearStart) + 1,
      12,
      31
    ),
    NextCalendarQuarterStart = DATEADD(
      day,
      1,
      CalendarQuarterEnd
    ),
    NextCalendarQuarterEnd = DATEADD(
      day,
      -1,
      DATEADD(
        quarter,
        2,
        CalendarQuarterStart
      )
    ),
    NextCalendarMonthStart = DATEADD(
      day,
      1,
      CalendarMonthEnd
    ),
    NextCalendarMonthEnd = DATEADD(
      day,
      -1,
      DATEADD(
        month,
        2,
        CalendarMonthStart
      )
    ),
    NextCalendarWeekStart = DATEADD(
      week,
      1,
      CalendarWeekStart
    ),
    NextCalendarWeekEnd = DATEADD(
      week,
      1,
      CalendarWeekEnd
    ),
    PriorFiscalYearStart = DATEADD(
      year,
      -1,
      FiscalYearStart
    ),
    PriorFiscalYearEnd = DATEADD(
      day,
      -1,
      FiscalYearStart
    ),
    PriorFiscalQuarterStart = DATEADD(
      quarter,
      -1,
      FiscalQuarterStart
    ),
    PriorFiscalQuarterEnd = DATEADD(
      day,
      -1,
      FiscalQuarterStart
    ),
    PriorFiscalMonthStart = DATEADD(
      month,
      -1,
      FiscalMonthStart
    ),
    PriorFiscalMonthEnd = DATEADD(
      day,
      -1,
      FiscalMonthStart
    ),
    NextFiscalYearStart = DATEADD(
      day,
      1,
      FiscalYearEnd
    ),
    -- We can do the below because fiscal month
    -- start dates aren't allowed to be >28, meaning
    -- it's impossible for the year end to be on a different
    -- date depending on the number of days in the month
    NextFiscalYearEnd = DATEADD(
      year,
      1,
      FiscalYearEnd
    ),
    NextFiscalQuarterStart = DATEADD(
      day,
      1,
      FiscalQuarterEnd
    ),
    NextFiscalQuarterEnd = DATEADD(
      day,
      -1,
      DATEADD(
        quarter,
        2,
        FiscalQuarterStart
      )
    ),
    NextFiscalMonthStart = DATEADD(
      day,
      1,
      FiscalMonthEnd
    ),
    NextFiscalMonthEnd = DATEADD(
      day,
      -1,
      DATEADD(
        month,
        2,
        FiscalMonthStart
      )
    )
  FROM
    BaseDatesSeventh
),

-- Some things are just hard to calculate and I don't want to do it
-- repeatedly
FiscalHelpers AS (
  SELECT
    *,
    FiscalMonthNum = IIF(
      MONTH(FiscalPeriodMonthReference) - MONTH(FiscalPeriodYearReference) - @FiscalMonthPeriodEndMatchesCalendar >= 0,
      1 + MONTH(FiscalPeriodMonthReference) - MONTH(FiscalPeriodYearReference)  - @FiscalMonthPeriodEndMatchesCalendar,
      13 + MONTH(FiscalPeriodMonthReference) - MONTH(FiscalPeriodYearReference) - @FiscalMonthPeriodEndMatchesCalendar
    ),
    FiscalQuarterNum = IIF(
      DATEPART(quarter, FiscalPeriodQuarterReference) - DATEPART(quarter, FiscalPeriodYearReference) - @FiscalQuarterPeriodEndMatchesCalendar >= 0,
      1 + DATEPART(quarter, FiscalPeriodQuarterReference) - DATEPART(quarter, FiscalPeriodYearReference) - @FiscalQuarterPeriodEndMatchesCalendar,
      5 + DATEPART(quarter, FiscalPeriodQuarterReference) - DATEPART(quarter, FiscalPeriodYearReference) - @FiscalQuarterPeriodEndMatchesCalendar
    ),
    FiscalYearNum = YEAR(FiscalPeriodYearReference)
  FROM RelativeDates
),

Main AS (
  SELECT
    fh.*,

    -- '2021-01-01'
    {config.dim_date.columns.iso_date_name.name} = CONVERT(
      varchar(10),
      {config.dim_date.columns.the_date.name},
      @ISO8601DatestringFormatNumber
    ),

    -- '2020-W53-5'
    -- This is gross, but it works for
    -- every value I tested for (which was a lot).
    -- The "{config.dim_date.columns.year.name}" part is from https://stackoverflow.com/questions/26926271/sql-get-iso-year-for-iso-week
    ISOWeekDateName = CONCAT(
      DATENAME(
        year,
        DATEADD(
          day,
          26-DATEPART(
            iso_week,
            {config.dim_date.columns.the_date.name}
          ),
          {config.dim_date.columns.the_date.name}
        )
      ),
      '-W',
      RIGHT(
        '0'+CONVERT(
          varchar(2),
          DATEPART(
            iso_week,
            {config.dim_date.columns.the_date.name}
          )
        ),
        2
      ),
      '-',
      CONVERT(
        varchar(1),
        (
          DATEPART(
            weekday,
            {config.dim_date.columns.the_date.name}
          ) + @@DATEFIRST + 6 - 1
        ) % 7 + 1
      )
    ),

    -- '01/01/2021'
    {config.dim_date.columns.american_date_name.name} = CONVERT(
      varchar(10),
      {config.dim_date.columns.the_date.name},
      @USDatestringFormatNumber
    ),

    -- 'Friday'
    {config.dim_date.columns.day_of_week_name.name} = DATENAME(
      weekday,
      {config.dim_date.columns.the_date.name}
    ),

    -- 'Fri'
    {config.dim_date.columns.day_of_week_abbrev.name} = LEFT(
      DATENAME(
        weekday,
        {config.dim_date.columns.the_date.name}
      ),
      3
    ),

    -- 'January'
    {config.dim_date.columns.month_name.name} = DATENAME(
      month,
      {config.dim_date.columns.the_date.name}
    ),

    -- 'Jan'
    {config.dim_date.columns.month_abbrev.name} = LEFT(
      DATENAME(
        month,
        {config.dim_date.columns.the_date.name}
      ),
      3
    ),

    -- '2021W01'
    {config.dim_date.columns.year_week_name.name} = CONCAT(
      DATENAME(
        year,
        {config.dim_date.columns.the_date.name}
      ),
      'W',
      RIGHT(
        '0'+DATENAME(
          week,
          {config.dim_date.columns.the_date.name}
        ),
        2
      )
    ),

    -- '2021-01'
    {config.dim_date.columns.year_month_name.name} = CONCAT(
      DATENAME(
        year,
        {config.dim_date.columns.the_date.name}
      ),
      '-',
      RIGHT(
        '0'+CONVERT(
          varchar(2),
          DATEPART(
            month,
            {config.dim_date.columns.the_date.name}
          )
        ),
        2
      )
    ),

    -- 'Jan 2021'
    {config.dim_date.columns.month_year_name.name} = CONCAT(
      LEFT(
        DATENAME(
          month,
          {config.dim_date.columns.the_date.name}
        ),
        3
      ),
      ' ',
      DATENAME(
        year,
        {config.dim_date.columns.the_date.name}
      )
    ),

    -- '2021Q1'
    {config.dim_date.columns.year_quarter_name.name} = CONCAT(
      DATENAME(
        year,
        {config.dim_date.columns.the_date.name}
      ),
      'Q',
      DATENAME(
          quarter,
          {config.dim_date.columns.the_date.name}
      )
    ),

    -- 2021
    {config.dim_date.columns.year.name} = DATEPART(year, {config.dim_date.columns.the_date.name}),

    -- 202101
    {config.dim_date.columns.year_week.name} = CONVERT(
      int,
      CONCAT(
        DATENAME(
          year,
          {config.dim_date.columns.the_date.name}
        ),
        RIGHT(
          '0'+DATENAME(
            week,
            {config.dim_date.columns.the_date.name}
          ),
          2
        )
      )
    ),

    -- 202101
    {config.dim_date.columns.iso_year_week_code.name} = CONVERT(
      int,
      CONCAT(
        DATENAME(
          year,
          DATEADD(
            day,
            26-DATEPART(
              iso_week,
              {config.dim_date.columns.the_date.name}
            ),
            {config.dim_date.columns.the_date.name}
          )
        ),
        RIGHT(
          '0'+CONVERT(
            varchar(2),
            DATEPART(
              iso_week,
              {config.dim_date.columns.the_date.name}
            )
          ),
          2
        )
      )
    ),

    -- 202101
    {config.dim_date.columns.year_month.name} = CONVERT(
      int,
      CONCAT(
        DATENAME(
          year,
          {config.dim_date.columns.the_date.name}
        ),
        RIGHT(
          '0'+CONVERT(
            varchar(2),
            DATEPART(
              month,
              {config.dim_date.columns.the_date.name}
            )
          ),
          2
        )
      )
    ),

    -- 202101
    {config.dim_date.columns.year_quarter.name} = CONVERT(
      int,
      CONCAT(
        DATENAME(
          year,
          {config.dim_date.columns.the_date.name}
        ),
        RIGHT(
          '0'+DATENAME(
            quarter,
            {config.dim_date.columns.the_date.name}
          ),
          2
        )
      )
    ),

    -- 5
    {config.dim_date.columns.day_of_week_starting_monday.name} = (
      DATEPART(
        weekday,
        {config.dim_date.columns.the_date.name}
      ) + @@DATEFIRST + 6 - 1
    ) % 7 + 1,

    -- 6
    {config.dim_date.columns.day_of_week.name} = DATEPART(
      weekday,
      {config.dim_date.columns.the_date.name}
    ),

    -- 1
    {config.dim_date.columns.day_of_month.name} = DATEPART(
      day,
      {config.dim_date.columns.the_date.name}
    ),

    -- 1
    {config.dim_date.columns.day_of_quarter.name} = DATEDIFF(
      day,
      DATEADD(
        quarter,
        DATEDIFF(quarter, 0, {config.dim_date.columns.the_date.name}),
        0
      ),
      {config.dim_date.columns.the_date.name}
    ) + 1,

    -- 1
    {config.dim_date.columns.day_of_year.name} = DATEPART(
      dayofyear,
      {config.dim_date.columns.the_date.name}
    ),

    -- 1
    {config.dim_date.columns.week_of_quarter.name} = DATEDIFF(
      week,
      CalendarQuarterStart,
      {config.dim_date.columns.the_date.name}
    ) + 1,

    -- 1
    {config.dim_date.columns.week_of_year.name} = DATEPART(
      week,
      {config.dim_date.columns.the_date.name}
    ),

    -- 1
    {config.dim_date.columns.iso_week_of_year.name} = DATEPART(
      iso_week,
      {config.dim_date.columns.the_date.name}
    ),

    -- 1
    {config.dim_date.columns.month.name} = DATEPART(
      month,
      {config.dim_date.columns.the_date.name}
    ),

    -- 1
    {config.dim_date.columns.month_of_quarter.name} = DATEDIFF(
      month,
      CalendarQuarterStart,
      {config.dim_date.columns.the_date.name}
    ) + 1,

    -- 1
    {config.dim_date.columns.quarter.name} = DATEPART(
        quarter,
        {config.dim_date.columns.the_date.name}
      ),
    
    -- 31
    {config.dim_date.columns.days_in_month.name} = DATEPART(
      day,
      EOMONTH({config.dim_date.columns.the_date.name})
    ),

    -- 90
    {config.dim_date.columns.days_in_quarter.name} = DATEDIFF(
      day,
      CalendarQuarterStart,
      NextCalendarQuarterStart
    ),

    -- 365
    {config.dim_date.columns.days_in_year.name} = DATEDIFF(
      day,
      CalendarYearStart,
      NextCalendarYearStart
    ),

    -- -209
    {config.dim_date.columns.day_offset_from_today.name} = DATEDIFF(
      day,
      @TodayInLocal,
      {config.dim_date.columns.the_date.name}
    ),

    -- -6
    {config.dim_date.columns.month_offset_from_today.name} = DATEDIFF(
      month,
      @TodayInLocal,
      {config.dim_date.columns.the_date.name}
    ),

    -- -2
    {config.dim_date.columns.quarter_offset_from_today.name} = DATEDIFF(
      quarter,
      @TodayInLocal,
      {config.dim_date.columns.the_date.name}
    ),

    -- 0
    {config.dim_date.columns.year_offset_from_today.name} = DATEDIFF(
      year,
      @TodayInLocal,
      {config.dim_date.columns.the_date.name}
    ),

    -- 0
    {config.dim_date.columns.today_flag.name} = IIF(
      {config.dim_date.columns.the_date.name} = @TodayInLocal,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.current_week_starting_monday_flag.name} = IIF(
      DATEDIFF(
        week,
        CONVERT(date, GETDATE()),
        DATEADD(day, -1, {config.dim_date.columns.the_date.name})
      ) = 0,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.current_week_flag.name} = IIF(
      DATEDIFF(week, @TodayInLocal, {config.dim_date.columns.the_date.name}) = 0,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.prior_week_flag.name} = IIF(
      DATEDIFF(week, @TodayInLocal, {config.dim_date.columns.the_date.name}) = -1,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.next_week_flag.name} = IIF(
      DATEDIFF(week, @TodayInLocal, {config.dim_date.columns.the_date.name}) = 1,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.current_month_flag.name} = IIF(
      DATEDIFF(month, @TodayInLocal, {config.dim_date.columns.the_date.name}) = 0,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.prior_month_flag.name} = IIF(
      DATEDIFF(month, @TodayInLocal, {config.dim_date.columns.the_date.name}) = -1,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.next_month_flag.name} = IIF(
      DATEDIFF(month, @TodayInLocal, {config.dim_date.columns.the_date.name}) = 1,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.current_quarter_flag.name} = IIF(
      DATEDIFF(quarter, @TodayInLocal, {config.dim_date.columns.the_date.name}) = 0,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.prior_quarter_flag.name} = IIF(
      DATEDIFF(quarter, @TodayInLocal, {config.dim_date.columns.the_date.name}) = -1,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.next_quarter_flag.name} = IIF(
      DATEDIFF(quarter, @TodayInLocal, {config.dim_date.columns.the_date.name}) = 1,
      1,
      0
    ),

    -- 1
    {config.dim_date.columns.current_year_flag.name} = IIF(
      DATEDIFF(year, @TodayInLocal, {config.dim_date.columns.the_date.name}) = 0,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.prior_year_flag.name} = IIF(
      DATEDIFF(year, @TodayInLocal, {config.dim_date.columns.the_date.name}) = -1,
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.next_year_flag.name} = IIF(
      DATEDIFF(year, @TodayInLocal, {config.dim_date.columns.the_date.name}) = 1,
      1,
      0
    ),

    -- 1
    {config.dim_date.columns.weekday_flag.name} = IIF(
      DATEPART(weekday, {config.dim_date.columns.the_date.name}) NOT IN (1,7),
      1,
      0
    ),

    {config.dim_date.columns.business_day_flag.name} = IIF(
      {business_day_clause if len(business_day_list) > 0 else ''}DATEPART(
        weekday,
        {config.dim_date.columns.the_date.name}
      ) IN (1, 7),
      0,
      1
    ),

    -- 1
    {config.dim_date.columns.first_day_of_month_flag.name} = IIF(
      CalendarMonthStart = {config.dim_date.columns.the_date.name},
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.last_day_of_month_flag.name} = IIF(
      CalendarMonthEnd = {config.dim_date.columns.the_date.name},
      1,
      0
    ),

    -- 1
    {config.dim_date.columns.first_day_of_quarter_flag.name} = IIF(
      CalendarQuarterStart = {config.dim_date.columns.the_date.name},
      1,
      0
    ),
    
    -- 0
    {config.dim_date.columns.last_day_of_quarter_flag.name} = IIF(
      CalendarQuarterEnd = {config.dim_date.columns.the_date.name},
      1,
      0
    ),

    -- 1
    {config.dim_date.columns.first_day_of_year_flag.name} = IIF(
      CalendarYearStart = {config.dim_date.columns.the_date.name},
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.last_day_of_year_flag.name} = IIF(
      CalendarYearEnd = {config.dim_date.columns.the_date.name},
      1,
      0
    ),

    -- 0.8571
    -- The fraction of the week, counted from Sunday to Saturday, that has passed as of
    -- 2021-01-01. In this case, 6 (Friday) / 7 (the total number of days in the week)
    {config.dim_date.columns.fraction_of_week.name} = CAST(
      DATEPART(
        weekday,
        {config.dim_date.columns.the_date.name}
      )
      AS decimal(8,4)
    ) / 7,

    -- 0.0323
    -- The fraction of the month, counted from the first day of the calendar month to the last
    -- that has passed as of 2021-01-01. 
    {config.dim_date.columns.fraction_of_month.name} = CAST(
      DATEPART(
        day,
        {config.dim_date.columns.the_date.name}
      ) 
      AS decimal(8,4)
    ) / DATEPART(
      day,
      CalendarMonthEnd
    ),

    -- 0.0111
    -- The fraction of the quarter, counted from the first day of the calendar quarter to the last
    -- that has passed as of 2021-01-01. 
    {config.dim_date.columns.fraction_of_quarter.name} = CAST(
      DATEDIFF(
        day,
        CalendarQuarterStart,
        {config.dim_date.columns.the_date.name}
      ) + 1
      AS decimal(8,4)
    ) / (DATEDIFF(
      day,
      CalendarQuarterStart,
      CalendarQuarterEnd
    ) + 1),

    -- 0.0027
    -- The fraction of the year, counted from the first day of the calendar year to the last
    -- that has passed as of 2021-01-01. 
    {config.dim_date.columns.fraction_of_year.name} = CAST(
      DATEPART(
        dayofyear,
        {config.dim_date.columns.the_date.name}
      )
      AS decimal(8,4)
    ) / (DATEDIFF(
      day,
      CalendarYearStart,
      CalendarYearEnd
    ) + 1),

    -- 2020-12-31
      {config.dim_date.columns.prior_day.name} = DATEADD(
        day,
        -1,
        {config.dim_date.columns.the_date.name}
      ),

      -- 2021-01-02
      {config.dim_date.columns.next_day.name} = DATEADD(
        day,
        1,
        {config.dim_date.columns.the_date.name}
      ),

      -- 2020-12-25
      {config.dim_date.columns.same_day_prior_week.name} = DATEADD(
        week,
        -1,
        {config.dim_date.columns.the_date.name}
      ),

      -- 2020-12-01
      {config.dim_date.columns.same_day_prior_month.name} = DATEADD(
        month,
        -1,
        {config.dim_date.columns.the_date.name}
      ),

      -- 2020-10-01
      {config.dim_date.columns.same_day_prior_quarter.name} = DATEADD(
        quarter,
        -1,
        {config.dim_date.columns.the_date.name}
      ),

      -- 2020-01-01
      {config.dim_date.columns.same_day_prior_year.name} = DATEADD(
        year,
        -1,
        {config.dim_date.columns.the_date.name}
      ),

      -- 2021-01-08
      {config.dim_date.columns.same_day_next_week.name} = DATEADD(
        week,
        1,
        {config.dim_date.columns.the_date.name}
      ),

      -- 2021-02-01
      {config.dim_date.columns.same_day_next_month.name} = DATEADD(
        month,
        1,
        {config.dim_date.columns.the_date.name}
      ),

      -- 2021-04-01
      {config.dim_date.columns.same_day_next_quarter.name} = DATEADD(
        quarter,
        1,
        {config.dim_date.columns.the_date.name}
      ),

      -- 2022-01-01
      {config.dim_date.columns.same_day_next_year.name} = DATEADD(
        year,
        1,
        {config.dim_date.columns.the_date.name}
      ),

      -- 2020-12-27 (week start is Sunday)
      {config.dim_date.columns.current_week_start.name} = CalendarWeekStart,

      -- 2021-01-02 (week end is Saturday)
      {config.dim_date.columns.current_week_end.name} = CalendarWeekEnd,

      -- 2021-01-01
      {config.dim_date.columns.current_month_start.name} = CalendarMonthStart,

      -- 2021-01-31 (does take into account leap years)
      {config.dim_date.columns.current_month_end.name} = CalendarMonthEnd,

      -- 2021-01-01
      {config.dim_date.columns.current_quarter_start.name} = CalendarQuarterStart,

      -- 2021-03-31
      {config.dim_date.columns.current_quarter_end.name} = CalendarQuarterEnd,
      
      -- 2021-01-01
      {config.dim_date.columns.current_year_start.name} = CalendarYearStart,

      -- 2021-12-31
      {config.dim_date.columns.current_year_end.name} = CalendarYearEnd,

      -- 2020-12-20
      {config.dim_date.columns.prior_week_start.name} = PriorCalendarWeekStart,

      -- 2020-12-26
      {config.dim_date.columns.prior_week_end.name} = PriorCalendarWeekEnd,

      -- 2020-12-01
      {config.dim_date.columns.prior_month_start.name} = PriorCalendarMonthStart,

      -- 2020-12-31
      {config.dim_date.columns.prior_month_end.name} = PriorCalendarMonthEnd,

      -- 2020-10-01
      {config.dim_date.columns.prior_quarter_start.name} = PriorCalendarQuarterStart,

      -- 2020-12-31
      {config.dim_date.columns.prior_quarter_end.name} = PriorCalendarQuarterEnd,

      -- 2020-01-01
      {config.dim_date.columns.prior_year_start.name} = PriorCalendarYearStart,

      -- 2020-12-31
      {config.dim_date.columns.prior_year_end.name} = PriorCalendarYearEnd,

      -- 2021-01-03
      {config.dim_date.columns.next_week_start.name} = NextCalendarWeekStart,

      -- 2021-01-09
      {config.dim_date.columns.next_week_end.name} = NextCalendarWeekEnd,

      -- 2021-02-01
      {config.dim_date.columns.next_month_start.name} = NextCalendarMonthStart,

      -- 2021-02-28 (handles leap years)
      {config.dim_date.columns.next_month_end.name} = NextCalendarMonthEnd,

      -- 2021-04-01
      {config.dim_date.columns.next_quarter_start.name} = NextCalendarQuarterStart,

      -- 2021-06-30
      {config.dim_date.columns.next_quarter_end.name} = NextCalendarQuarterEnd,

      -- 2022-01-01
      {config.dim_date.columns.next_year_start.name} = NextCalendarYearStart,

      -- 2022-12-31
      {config.dim_date.columns.next_year_end.name} = NextCalendarYearEnd,

      -- Hell starts here.
      -- Let me use a couple of examples. With our current settings, on Jan. 1:
      -- {config.dim_date.columns.year.name} = 2021 (because the end of the fiscal year falls into CY2021)
      -- {config.dim_date.columns.month.name} = January (name), 01 (number) 
      -- (because the end of the fiscal month, 01-26, falls into January)
      -- Here's the catch:
      -- {config.dim_date.columns.quarter.name} and month numbers are always based off of the start of your fiscal year
      -- So if your fiscal year starts July 15, July 15-August 14 will always have a month 
      -- number of 1 (because it's the first month in your fiscal year), but the fiscal
      -- month NAME will depend on @@FiscalMonthPeriodEndMatchesCalendar. If it's set to 0,
      -- the name would be July. If it's set to 1, it would be August.

      -- 'January'
      {config.dim_date.columns.fiscal_month_name.name} = DATENAME(
        month,
        FiscalPeriodMonthReference
      ),

      -- 'Jan'
      {config.dim_date.columns.fiscal_month_abbrev.name} = LEFT(
        DATENAME(
          month,
          FiscalPeriodMonthReference
        ),
        3
      ),

      -- '2021W02'
      {config.dim_date.columns.fiscal_year_week_name.name} = CONCAT(
        DATENAME(
          year,
          FiscalPeriodYearReference
        ),
        'W',
        RIGHT(
          '0'+
          CONVERT(
            varchar(2),
              DATEDIFF(
              week,
              FiscalYearStart,
              {config.dim_date.columns.the_date.name}
            ) + 1
          ),
          2
        )
      ),

      -- '2021-01'
      {config.dim_date.columns.fiscal_year_month_name.name} = CONCAT(
        DATENAME(
          year,
          FiscalPeriodYearReference
        ),
        '-',
        RIGHT(
          '0'+CONVERT(
            varchar(2),
            FiscalMonthNum
          ),
          2
        )
      ),

      -- 'Jan 2021'
      {config.dim_date.columns.fiscal_month_year_name.name} = CONCAT(
        LEFT(
          DATENAME(
            month,
            FiscalPeriodMonthReference
          ),
          3
        ),
        ' ',
        DATENAME(
          year,
          FiscalPeriodYearReference
        )
      ),

      -- '2021Q1'
      {config.dim_date.columns.fiscal_year_quarter_name.name} = CONCAT(
        DATENAME(
          year,
          FiscalPeriodYearReference
        ),
        'Q',
        CONVERT(
          varchar(2),
          FiscalQuarterNum
        )
      ),

      -- 2021
      {config.dim_date.columns.fiscal_year.name} = FiscalYearNum,

      -- 202102
      {config.dim_date.columns.fiscal_year_week.name} = CONVERT(
        int,
        CONCAT(
          DATENAME(
            year,
            FiscalPeriodYearReference
          ),
          RIGHT(
            '0'+
            CONVERT(
              varchar(2),
              DATEDIFF(
                week,
                FiscalYearStart,
                {config.dim_date.columns.the_date.name}
              ) + 1
            ),
            2
          )
        )
      ),

      -- 202101
      {config.dim_date.columns.fiscal_year_month.name} = CONVERT(
        int,
        CONCAT(
          DATENAME(
            year,
            FiscalPeriodYearReference
          ),
          RIGHT(
            '0'+CONVERT(
              varchar(2),
              FiscalMonthNum
            ),
            2
          )
        )
      ),

      -- 202101
      {config.dim_date.columns.fiscal_year_quarter.name} = CONVERT(
        int,
        CONCAT(
          DATENAME(
            year,
            FiscalPeriodYearReference
          ),
          RIGHT(
            '0'+CONVERT(
              varchar(2),
              FiscalQuarterNum
            ),
            2
          )
        )
      ),

      -- 7
      {config.dim_date.columns.fiscal_day_of_month.name} = DATEDIFF(
        day,
        FiscalMonthStart,
        {config.dim_date.columns.the_date.name}
      ) + 1,

      -- 7
      {config.dim_date.columns.fiscal_day_of_quarter.name} = DATEDIFF(
        day,
        FiscalQuarterStart,
        {config.dim_date.columns.the_date.name}
      ) + 1,

      -- 7
      {config.dim_date.columns.fiscal_day_of_year.name} = DATEDIFF(
        day,
        FiscalYearStart,
        {config.dim_date.columns.the_date.name}
      ) + 1,

      -- 2
      {config.dim_date.columns.fiscal_week_of_quarter.name} = DATEDIFF(
        week,
        FiscalQuarterStart,
        {config.dim_date.columns.the_date.name}
      ) + 1,

      -- 2
      {config.dim_date.columns.fiscal_week_of_year.name} = DATEDIFF(
        week,
        FiscalYearStart,
        {config.dim_date.columns.the_date.name}
      ) + 1,

      -- 1
      {config.dim_date.columns.fiscal_month.name} = FiscalMonthNum,

      -- 1
      {config.dim_date.columns.fiscal_month_of_quarter.name} = DATEDIFF(
        month,
        FiscalQuarterStart,
        {config.dim_date.columns.the_date.name}
      ) + IIF(
        DATEPART(
          day,
          {config.dim_date.columns.the_date.name}
        ) >= @FiscalMonthStartDay,
        1,
        0
      ),

      -- 1
      {config.dim_date.columns.fiscal_quarter.name} = FiscalQuarterNum,

      -- 31
      {config.dim_date.columns.fiscal_days_in_month.name} = DATEDIFF(
        day,
        FiscalMonthStart,
        FiscalMonthEnd
      ) + 1,

      -- 90
      {config.dim_date.columns.fiscal_days_in_quarter.name} = DATEDIFF(
        day,
        FiscalQuarterStart,
        FiscalQuarterEnd
      ) + 1,

      -- 365
      {config.dim_date.columns.fiscal_days_in_year.name} = DATEDIFF(
        day,
        FiscalYearStart,
        FiscalYearEnd
      ) + 1,

      -- 0
      {config.dim_date.columns.fiscal_current_month_flag.name} = IIF(
        @TodayInLocal BETWEEN FiscalMonthStart AND FiscalMonthEnd,
        1,
        0
      ),

      -- 0
      {config.dim_date.columns.fiscal_prior_month_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          NextFiscalMonthStart AND NextFiscalMonthEnd,
        1,
        0
      ),

      -- 0
      {config.dim_date.columns.fiscal_next_month_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          PriorFiscalMonthStart AND PriorFiscalMonthEnd,
        1,
        0
      ),
      
      -- 0
      {config.dim_date.columns.fiscal_current_quarter_flag.name} = IIF(
        @TodayInLocal BETWEEN FiscalQuarterStart AND FiscalQuarterEnd,
        1,
        0
      ),
      
      -- 0
      {config.dim_date.columns.fiscal_prior_quarter_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          NextFiscalQuarterStart AND NextFiscalQuarterEnd,
        1,
        0
      ),
      
      -- 0
      {config.dim_date.columns.fiscal_next_quarter_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          PriorFiscalQuarterStart AND PriorFiscalQuarterEnd,
        1,
        0
      ),
      
      -- 1
      {config.dim_date.columns.fiscal_current_year_flag.name} = IIF(
        @TodayInLocal BETWEEN FiscalYearStart AND FiscalYearEnd,
        1,
        0
      ),
      
      -- 0
      {config.dim_date.columns.fiscal_prior_year_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          NextFiscalYearStart AND NextFiscalYearEnd,
        1,
        0
      ),

      -- 0
      {config.dim_date.columns.fiscal_next_year_flag.name} = IIF(
        @TodayInLocal BETWEEN 
          PriorFiscalYearStart AND PriorFiscalYearEnd,
        1,
        0
      ),
      
      -- 0
      {config.dim_date.columns.fiscal_first_day_of_month_flag.name} = IIF(
        {config.dim_date.columns.the_date.name} = FiscalMonthStart,
        1,
        0
      ),
      
      -- 0
      {config.dim_date.columns.fiscal_last_day_of_month_flag.name} = IIF(
        {config.dim_date.columns.the_date.name} = FiscalMonthEnd,
        1,
        0
      ),
      
      -- 0
      {config.dim_date.columns.fiscal_first_day_of_quarter_flag.name} = IIF(
        {config.dim_date.columns.the_date.name} = FiscalQuarterStart,
        1,
        0
      ),
      
      -- 0
      {config.dim_date.columns.fiscal_last_day_of_quarter_flag.name} = IIF(
        {config.dim_date.columns.the_date.name} = FiscalQuarterEnd,
        1,
        0
      ),
      
      -- 0
      {config.dim_date.columns.fiscal_first_day_of_year_flag.name} = IIF(
        {config.dim_date.columns.the_date.name} = FiscalYearStart,
        1,
        0
      ),
      
      -- 0
      {config.dim_date.columns.fiscal_last_day_of_year_flag.name} = IIF(
        {config.dim_date.columns.the_date.name} = FiscalYearEnd,
        1,
        0
      ),
      
      -- 0.2258
      {config.dim_date.columns.fiscal_fraction_of_month.name} = CAST(
        DATEDIFF(
          day,
          FiscalMonthStart,
          {config.dim_date.columns.the_date.name}
        ) + 1 AS decimal(8,4)
      ) / (DATEDIFF(
        day,
        FiscalMonthStart,
        FiscalMonthEnd
      ) + 1),

      -- 0.0778
      {config.dim_date.columns.fiscal_fraction_of_quarter.name} = CAST(
        DATEDIFF(
          day,
          FiscalQuarterStart,
          {config.dim_date.columns.the_date.name}
        ) + 1 AS decimal(8,4)
      ) / (DATEDIFF(
        day,
        FiscalQuarterStart,
        FiscalQuarterEnd
      ) + 1),

      -- 0.0192
      {config.dim_date.columns.fiscal_fraction_of_year.name} = CAST(
        DATEDIFF(
          day,
          FiscalYearStart,
          {config.dim_date.columns.the_date.name}
        ) + 1 AS decimal(8,4)
      ) / (DATEDIFF(
        day,
        FiscalYearStart,
        FiscalYearEnd
      ) + 1),

      -- 2020-12-26
      {config.dim_date.columns.fiscal_current_month_start.name} = FiscalMonthStart,

      -- 2021-01-25
      {config.dim_date.columns.fiscal_current_month_end.name} = FiscalMonthEnd,

      -- 2020-12-26
      {config.dim_date.columns.fiscal_current_quarter_start.name} = FiscalQuarterStart,

      -- 2021-03-25
      {config.dim_date.columns.fiscal_current_quarter_end.name} = FiscalQuarterEnd,

      -- 2020-12-26
      {config.dim_date.columns.fiscal_current_year_start.name} = FiscalYearStart,

      -- 2021-12-25
      {config.dim_date.columns.fiscal_current_year_end.name} = FiscalYearEnd,

      -- 2020-11-26
      {config.dim_date.columns.fiscal_prior_month_start.name} = PriorFiscalMonthStart,

      -- 2020-12-25
      {config.dim_date.columns.fiscal_prior_month_end.name} = PriorFiscalMonthEnd,

      -- 2020-09-26
      {config.dim_date.columns.fiscal_prior_quarter_start.name} = PriorFiscalQuarterStart,

      -- 2020-12-25
      {config.dim_date.columns.fiscal_prior_quarter_end.name} = PriorFiscalQuarterEnd,

      -- 2019-12-26
      {config.dim_date.columns.fiscal_prior_year_start.name} = PriorFiscalYearStart,

      -- 2020-12-25
      {config.dim_date.columns.fiscal_prior_year_end.name} = PriorFiscalYearEnd,

      -- 2021-01-26
      {config.dim_date.columns.fiscal_next_month_start.name} = NextFiscalMonthStart,

      -- 2021-02-25
      {config.dim_date.columns.fiscal_next_month_end.name} = NextFiscalMonthEnd,

      -- 2021-03-26
      {config.dim_date.columns.fiscal_next_quarter_start.name} = NextFiscalQuarterStart,

      -- 2021-06-25
      {config.dim_date.columns.fiscal_next_quarter_end.name} = NextFiscalQuarterEnd,

      -- 2021-12-26
      {config.dim_date.columns.fiscal_next_year_start.name} = NextFiscalYearStart,

      -- 2022-12-25
      {config.dim_date.columns.fiscal_next_year_end.name} = NextFiscalYearEnd{holiday_column_clause}
  FROM 
    FiscalHelpers AS fh
{holiday_join}
),

Burnups AS (
  SELECT 
    *,

    -- 1 - This is useful for dashboards. You can check 1 and see
    -- week-to-date for every week simultaneously. Same for mon/qtr/year.
    {config.dim_date.columns.weekly_burnup_starting_monday.name} = IIF(
      {config.dim_date.columns.day_of_week_starting_monday.name} <= (
        DATEPART(
          weekday,
          @TodayInLocal
        ) + @@DATEFIRST + 6 - 1
      ) % 7 + 1,
      1,
      0
    ),

    {config.dim_date.columns.weekly_burnup.name} = IIF(
      {config.dim_date.columns.day_of_week.name} <= DATEPART(
        weekday,
        @TodayInLocal
      ),
      1,
      0
    ),

    -- 1
    {config.dim_date.columns.monthly_burnup.name} = IIF(
      {config.dim_date.columns.day_of_month.name} <= DATEPART(
        day,
        @TodayInLocal
      ),
      1,
      0
    ),

    -- 1
    {config.dim_date.columns.quarterly_burnup.name} = IIF(
      {config.dim_date.columns.day_of_quarter.name} <= DATEDIFF(
        day,
        DATEADD(
          quarter,
          DATEDIFF(quarter, 0, @TodayInLocal),
          0
        ),
        @TodayInLocal
      ) + 1,
      1,
      0
    ),

    -- 1
    {config.dim_date.columns.yearly_burnup.name} = IIF(
      {config.dim_date.columns.day_of_year.name} <= DATEPART(
        dayofyear,
        @TodayInLocal
      ),
      1,
      0
    ),

    -- 0
    {config.dim_date.columns.fiscal_monthly_burnup.name} = IIF(
      {config.dim_date.columns.fiscal_day_of_month.name} <= DATEDIFF(
        day,
        FiscalMonthStartToday,
        @TodayInLocal
      ) + 1,
      1,
      0
    ),

    -- 1
    {config.dim_date.columns.fiscal_quarterly_burnup.name} = IIF(
      {config.dim_date.columns.fiscal_day_of_quarter.name} <= DATEDIFF(
        day,
        FiscalQuarterStartToday,
        @TodayInLocal
      ) + 1,
      1,
      0
    ),

    -- 1
    {config.dim_date.columns.fiscal_yearly_burnup.name} = IIF(
      {config.dim_date.columns.fiscal_day_of_year.name} <= DATEDIFF(
        day,
        FiscalYearStartToday,
        @TodayInLocal
      ) + 1,
      1,
      0
    )
  FROM Main
)

INSERT INTO {config.dim_date.table_schema}.{config.dim_date.table_name} (
  {insert_column_clause}
)
SELECT 
  {insert_column_clause}
FROM Burnups
ORDER BY {config.dim_date.columns.date_key.name} ASC
OPTION (MAXRECURSION 0)
"""
