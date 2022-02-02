from ...config import Config


# Note: Rather than trying to be "smart" and removing or adding columns based on whether or not they should be present,
# we just remove or rename them at the very end before the INSERT statement. The performance change is so negligible for a one-time-setup
# script that it doesn't make sense to take on the complication.
def dim_date_insert_template(config: Config) -> str:
    holiday_join = []
    business_day_list = []
    holiday_columndef = []
    holiday_column_list = []
    for i, t in enumerate(config.holidays.holiday_types):
        holiday_join.append(
            f'    LEFT OUTER JOIN {config.holidays.holidays_schema_name}.{config.holidays.holidays_table_name} AS h{i} -- {t.name}')
        holiday_join.append(
            f"      ON fh.DateKey = h{i}.DateKey AND h{i}.HolidayTypeKey = (SELECT HolidayTypeKey FROM {config.holidays.holiday_types_schema_name}.{config.holidays.holiday_types_table_name} WHERE HolidayTypeName = '{t.name}')")
        if t.included_in_business_day_calc:
            business_day_list.append(f'      h{i}.DateKey IS NOT NULL')

        holiday_columndef.append(
            f'      {t.generated_column_prefix}HolidayFlag = IIF(')
        holiday_columndef.append(f'        h{i}.DateKey IS NOT NULL,')
        holiday_columndef.append(f'        1,')
        holiday_columndef.append(f'        0')
        holiday_columndef.append(f'      ),')
        holiday_columndef.append('')
        holiday_columndef.append(
            f'      {t.generated_column_prefix}HolidayName = h{i}.HolidayName,')
        holiday_columndef.append('')

        holiday_column_list.append(
            f'  {t.generated_column_prefix}HolidayFlag,')
        holiday_column_list.append(
            f'  {t.generated_column_prefix}HolidayName,')

    holiday_join = '\n'.join(holiday_join)
    business_day_clause = '\n'.join(business_day_list) + '\n      OR '
    holiday_column_clause = '\n'.join(holiday_columndef)[:-2]
    holiday_columns = '\n'.join(holiday_column_list)[:-1]
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
-- The DateKey is 20210101
-- @TodayInLocal = 2021-07-29
-- @FiscalMonthStartDay=26;
-- @FiscalYearStartMonth=12;
-- @FiscalMonthPeriodEndMatchesCalendar=1;
-- @FiscalQuarterPeriodEndMatchesCalendar=1;
-- @FiscalYearPeriodEndMatchesCalendar=1;
WITH Recursion AS (
  SELECT
    DateKey = CONVERT(
      int,
      CONVERT(
        varchar(8),
        @FirstDate,
        @ISODatekeyFormatNumber
      )
    ),

    TheDate = @FirstDate
  UNION ALL
  SELECT
    CONVERT(
      int,
      CONVERT(
        varchar(8),
        DATEADD(DAY, 1, TheDate),
        @ISODatekeyFormatNumber
      )
    ),
    DATEADD(DAY, 1, TheDate)
  FROM Recursion
  WHERE TheDate < @LastDate
),

BaseDatesFirst AS (
  SELECT 
    DateKey,
    TheDate,
    CalendarYearStart = DATEFROMPARTS(
      YEAR(TheDate),
      01,
      01
    ),
    CalendarYearEnd = DATEFROMPARTS(
      YEAR(TheDate),
      12,
      31
    ),
    CalendarQuarterStart = CAST(
      DATEADD(
        quarter,
        DATEDIFF(quarter, 0, TheDate),
        0
      ) AS date
    ),
    CalendarQuarterEnd = CAST(
      DATEADD(
        day, 
        -1, 
        DATEADD(
          quarter, 
          DATEDIFF(quarter, 0, TheDate) + 1,
          0
        )
      ) AS date
    ),
    CalendarMonthStart = DATEFROMPARTS(
      YEAR(TheDate),
      MONTH(TheDate),
      01
    ),
    CalendarMonthEnd = EOMONTH(TheDate),
    CalendarWeekStart = DATEADD(
      day, 
      1-DATEPART(
        WEEKDAY, 
        TheDate
      ), 
      TheDate
    ),
    CalendarWeekEnd = DATEADD(
      day, 
      7-DATEPART(
        WEEKDAY, 
        TheDate
      ), 
      TheDate
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
    --     TheDate = '2021-01-01';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2020-12-26'
    -- For: 
    --     TheDate = '2020-12-26';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2020-12-26'
    -- For: 
    --     TheDate = '2020-12-25';
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
          DATEPART(year, TheDate), 
          @FiscalYearStartMonth,
          @FiscalMonthStartDay
        ),
        TheDate
      ) >= 0,
      DATEFROMPARTS(
        DATEPART(year, TheDate), 
        @FiscalYearStartMonth,
        @FiscalMonthStartDay
      ),
      DATEFROMPARTS(
          DATEPART(year, TheDate) - 1, 
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

    FiscalPeriodYearReferenceTotday = IIF(
      @FiscalYearPeriodEndMatchesCalendar = 0,
      FiscalYearStartToday,
      FiscalYearEndToday
    ),

    -- Same here. Here are some examples:
    -- For:
    --     TheDate = '2021-01-01';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2020-12-26'
    -- For: 
    --     TheDate = '2020-12-26';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2020-12-26'
    -- For: 
    --     TheDate = '2020-12-25';
    --     @FiscalYearStartMonth = 12;
    --     @FiscalMonthStartDay = 26;
    -- Output: 
    --     '2020-11-26'
    FiscalMonthStart = IIF(
      DATEPART(
        day,
        TheDate
      ) >= @FiscalMonthStartDay,
      DATEFROMPARTS(
        YEAR(TheDate),
        MONTH(TheDate),
        @FiscalMonthStartDay
      ),
      DATEFROMPARTS(
        YEAR(
          DATEADD(
            month,
            -1,
            TheDate
          )
        ),
        MONTH(
          DATEADD(
            month,
            -1,
            TheDate
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
        TheDate
      ) = DATEPART(
        quarter,
        FiscalMonthEnd
      ),
      DATEFROMPARTS(
        YEAR(
          DATEADD(
            month,
            -1,
            DATEADD(
                quarter,
                DATEDIFF(quarter, 0, TheDate),
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
                DATEDIFF(quarter, 0, TheDate),
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
                DATEDIFF(quarter, 0, TheDate) + 1,
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
                DATEDIFF(quarter, 0, TheDate) + 1,
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
    ISODateName = CONVERT(
      varchar(10),
      TheDate,
      @ISO8601DatestringFormatNumber
    ),

    -- '01/01/2021'
    AmericanDateName = CONVERT(
      varchar(10),
      TheDate,
      @USDatestringFormatNumber
    ),

    -- 'Friday'
    DayOfWeekName = DATENAME(
      weekday,
      TheDate
    ),

    -- 'Fri'
    DayOfWeekAbbrev = LEFT(
      DATENAME(
        weekday,
        TheDate
      ),
      3
    ),

    -- 'January'
    MonthName = DATENAME(
      month,
      TheDate
    ),

    -- 'Jan'
    MonthAbbrev = LEFT(
      DATENAME(
        month,
        TheDate
      ),
      3
    ),

    -- '2021W01'
    YearWeekName = CONCAT(
      DATENAME(
        year,
        TheDate
      ),
      'W',
      RIGHT(
        '0'+DATENAME(
          week,
          TheDate
        ),
        2
      )
    ),

    -- '2021-01'
    YearMonthName = CONCAT(
      DATENAME(
        year,
        TheDate
      ),
      '-',
      RIGHT(
        '0'+CONVERT(
          varchar(2),
          DATEPART(
            month,
            TheDate
          )
        ),
        2
      )
    ),

    -- 'Jan 2021'
    MonthYearName = CONCAT(
      LEFT(
        DATENAME(
          month,
          TheDate
        ),
        3
      ),
      ' ',
      DATENAME(
        year,
        TheDate
      )
    ),

    -- '2021Q1'
    YearQuarterName = CONCAT(
      DATENAME(
        year,
        TheDate
      ),
      'Q',
      DATENAME(
          quarter,
          TheDate
      )
    ),

    -- 2021
    Year = DATEPART(year, TheDate),

    -- 202101
    YearWeek = CONVERT(
      int,
      CONCAT(
        DATENAME(
          year,
          TheDate
        ),
        RIGHT(
          '0'+DATENAME(
            week,
            TheDate
          ),
          2
        )
      )
    ),

    -- 202101
    ISOYearWeekCode = CONVERT(
      int,
      CONCAT(
        DATENAME(
          year,
          TheDate
        ),
        RIGHT(
          '0'+CONVERT(
            varchar(2),
            DATEPART(
              iso_week,
              TheDate
            )
          ),
          2
        )
      )
    ),

    -- 202101
    YearMonth = CONVERT(
      int,
      CONCAT(
        DATENAME(
          year,
          TheDate
        ),
        RIGHT(
          '0'+CONVERT(
            varchar(2),
            DATEPART(
              month,
              TheDate
            )
          ),
          2
        )
      )
    ),

    -- 202101
    YearQuarter = CONVERT(
      int,
      CONCAT(
        DATENAME(
          year,
          TheDate
        ),
        RIGHT(
          '0'+DATENAME(
            quarter,
            TheDate
          ),
          2
        )
      )
    ),

    -- 5
    DayOfWeekStartingMonday = (
      DATEPART(
        weekday,
        TheDate
      ) + @@DATEFIRST + 6 - 1
    ) % 7 + 1,

    -- 6
    DayOfWeek = DATEPART(
      weekday,
      TheDate
    ),

    -- 1
    DayOfMonth = DATEPART(
      day,
      TheDate
    ),

    -- 1
    DayOfQuarter = DATEDIFF(
      day,
      DATEADD(
        quarter,
        DATEDIFF(quarter, 0, TheDate),
        0
      ),
      TheDate
    ) + 1,

    -- 1
    DayOfYear = DATEPART(
      dayofyear,
      TheDate
    ),

    -- 1
    WeekOfQuarter = DATEDIFF(
      week,
      CalendarQuarterStart,
      TheDate
    ) + 1,

    -- 1
    WeekOfYear = DATEPART(
      week,
      TheDate
    ),

    -- 1
    ISOWeekOfYear = DATEPART(
      iso_week,
      TheDate
    ),

    -- 1
    Month = DATEPART(
      month,
      TheDate
    ),

    -- 1
    MonthOfQuarter = DATEDIFF(
      month,
      CalendarQuarterStart,
      TheDate
    ) + 1,

    -- 1
    Quarter = DATEPART(
        quarter,
        TheDate
      ),
    
    -- 31
    DaysInMonth = DATEPART(
      day,
      EOMONTH(TheDate)
    ),

    -- 90
    DaysInQuarter = DATEDIFF(
      day,
      CalendarQuarterStart,
      NextCalendarQuarterStart
    ),

    -- 365
    DaysInYear = DATEDIFF(
      day,
      CalendarYearStart,
      NextCalendarYearStart
    ),

    -- -209
    DayOffsetFromToday = DATEDIFF(
      day,
      @TodayInLocal,
      TheDate
    ),

    -- -6
    MonthOffsetFromToday = DATEDIFF(
      month,
      @TodayInLocal,
      TheDate
    ),

    -- -2
    QuarterOffsetFromToday = DATEDIFF(
      quarter,
      @TodayInLocal,
      TheDate
    ),

    -- 0
    YearOffsetFromToday = DATEDIFF(
      year,
      @TodayInLocal,
      TheDate
    ),

    -- 0
    TodayFlag = IIF(
      TheDate = @TodayInLocal,
      1,
      0
    ),

    -- 0
    CurrentWeekStartingMondayFlag = IIF(
      DATEDIFF(
        week,
        CONVERT(date, GETDATE()),
        DATEADD(day, -1, TheDate)
      ) = 0,
      1,
      0
    ),

    -- 0
    CurrentWeekFlag = IIF(
      DATEDIFF(week, @TodayInLocal, TheDate) = 0,
      1,
      0
    ),

    -- 0
    PriorWeekFlag = IIF(
      DATEDIFF(week, @TodayInLocal, TheDate) = -1,
      1,
      0
    ),

    -- 0
    NextWeekFlag = IIF(
      DATEDIFF(week, @TodayInLocal, TheDate) = 1,
      1,
      0
    ),

    -- 0
    CurrentMonthFlag = IIF(
      DATEDIFF(month, @TodayInLocal, TheDate) = 0,
      1,
      0
    ),

    -- 0
    PriorMonthFlag = IIF(
      DATEDIFF(month, @TodayInLocal, TheDate) = -1,
      1,
      0
    ),

    -- 0
    NextMonthFlag = IIF(
      DATEDIFF(month, @TodayInLocal, TheDate) = 1,
      1,
      0
    ),

    -- 0
    CurrentQuarterFlag = IIF(
      DATEDIFF(quarter, @TodayInLocal, TheDate) = 0,
      1,
      0
    ),

    -- 0
    PriorQuarterFlag = IIF(
      DATEDIFF(quarter, @TodayInLocal, TheDate) = -1,
      1,
      0
    ),

    -- 0
    NextQuarterFlag = IIF(
      DATEDIFF(quarter, @TodayInLocal, TheDate) = 1,
      1,
      0
    ),

    -- 1
    CurrentYearFlag = IIF(
      DATEDIFF(year, @TodayInLocal, TheDate) = 0,
      1,
      0
    ),

    -- 0
    PriorYearFlag = IIF(
      DATEDIFF(year, @TodayInLocal, TheDate) = -1,
      1,
      0
    ),

    -- 0
    NextYearFlag = IIF(
      DATEDIFF(year, @TodayInLocal, TheDate) = 1,
      1,
      0
    ),

    -- 1
    WeekdayFlag = IIF(
      DATEPART(weekday, TheDate) NOT IN (1,7),
      1,
      0
    ),

    BusinessDayFlag = IIF(
      {business_day_clause if len(business_day_list) > 0 else ''}DATEPART(
        weekday,
        TheDate
      ) IN (1, 7),
      0,
      1
    ),

    -- 1
    FirstDayOfMonthFlag = IIF(
      CalendarMonthStart = TheDate,
      1,
      0
    ),

    -- 0
    LastDayOfMonthFlag = IIF(
      CalendarMonthEnd = TheDate,
      1,
      0
    ),

    -- 1
    FirstDayOfQuarterFlag = IIF(
      CalendarQuarterStart = TheDate,
      1,
      0
    ),
    
    -- 0
    LastDayOfQuarterFlag = IIF(
      CalendarQuarterEnd = TheDate,
      1,
      0
    ),

    -- 1
    FirstDayOfYearFlag = IIF(
      CalendarYearStart = TheDate,
      1,
      0
    ),

    -- 0
    LastDayOfYearFlag = IIF(
      CalendarYearEnd = TheDate,
      1,
      0
    ),

    -- 0.8571
    -- The fraction of the week, counted from Sunday to Saturday, that has passed as of
    -- 2021-01-01. In this case, 6 (Friday) / 7 (the total number of days in the week)
    FractionOfWeek = CAST(
      DATEPART(
        weekday,
        TheDate
      )
      AS decimal(8,4)
    ) / 7,

    -- 0.0323
    -- The fraction of the month, counted from the first day of the calendar month to the last
    -- that has passed as of 2021-01-01. 
    FractionOfMonth = CAST(
      DATEPART(
        day,
        TheDate
      ) 
      AS decimal(8,4)
    ) / DATEPART(
      day,
      CalendarMonthEnd
    ),

    -- 0.0111
    -- The fraction of the quarter, counted from the first day of the calendar quarter to the last
    -- that has passed as of 2021-01-01. 
    FractionOfQuarter = CAST(
      DATEDIFF(
        day,
        CalendarQuarterStart,
        TheDate
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
    FractionOfYear = CAST(
      DATEPART(
        dayofyear,
        TheDate
      )
      AS decimal(8,4)
    ) / (DATEDIFF(
      day,
      CalendarYearStart,
      CalendarYearEnd
    ) + 1),

    -- 2020-12-31
      PriorDay = DATEADD(
        day,
        -1,
        TheDate
      ),

      -- 2021-01-02
      NextDay = DATEADD(
        day,
        1,
        TheDate
      ),

      -- 2020-12-25
      SameDayPriorWeek = DATEADD(
        week,
        -1,
        TheDate
      ),

      -- 2020-12-01
      SameDayPriorMonth = DATEADD(
        month,
        -1,
        TheDate
      ),

      -- 2020-10-01
      SameDayPriorQuarter = DATEADD(
        quarter,
        -1,
        TheDate
      ),

      -- 2020-01-01
      SameDayPriorYear = DATEADD(
        year,
        -1,
        TheDate
      ),

      -- 2021-01-08
      SameDayNextWeek = DATEADD(
        week,
        1,
        TheDate
      ),

      -- 2021-02-01
      SameDayNextMonth = DATEADD(
        month,
        1,
        TheDate
      ),

      -- 2021-04-01
      SameDayNextQuarter = DATEADD(
        quarter,
        1,
        TheDate
      ),

      -- 2022-01-01
      SameDayNextYear = DATEADD(
        year,
        1,
        TheDate
      ),

      -- 2020-12-27 (week start is Sunday)
      CurrentWeekStart = CalendarWeekStart,

      -- 2021-01-02 (week end is Saturday)
      CurrentWeekEnd = CalendarWeekEnd,

      -- 2021-01-01
      CurrentMonthStart = CalendarMonthStart,

      -- 2021-01-31 (does take into account leap years)
      CurrentMonthEnd = CalendarMonthEnd,

      -- 2021-01-01
      CurrentQuarterStart = CalendarQuarterStart,

      -- 2021-03-31
      CurrentQuarterEnd = CalendarQuarterEnd,
      
      -- 2021-01-01
      CurrentYearStart = CalendarYearStart,

      -- 2021-12-31
      CurrentYearEnd = CalendarYearEnd,

      -- 2020-12-20
      PriorWeekStart = PriorCalendarWeekStart,

      -- 2020-12-26
      PriorWeekEnd = PriorCalendarWeekEnd,

      -- 2020-12-01
      PriorMonthStart = PriorCalendarMonthStart,

      -- 2020-12-31
      PriorMonthEnd = PriorCalendarMonthEnd,

      -- 2020-10-01
      PriorQuarterStart = PriorCalendarQuarterStart,

      -- 2020-12-31
      PriorQuarterEnd = PriorCalendarQuarterEnd,

      -- 2020-01-01
      PriorYearStart = PriorCalendarYearStart,

      -- 2020-12-31
      PriorYearEnd = PriorCalendarYearEnd,

      -- 2021-01-03
      NextWeekStart = NextCalendarWeekStart,

      -- 2021-01-09
      NextWeekEnd = NextCalendarWeekEnd,

      -- 2021-02-01
      NextMonthStart = NextCalendarMonthStart,

      -- 2021-02-28 (handles leap years)
      NextMonthEnd = NextCalendarMonthEnd,

      -- 2021-04-01
      NextQuarterStart = NextCalendarQuarterStart,

      -- 2021-06-30
      NextQuarterEnd = NextCalendarQuarterEnd,

      -- 2022-01-01
      NextYearStart = NextCalendarYearStart,

      -- 2022-12-31
      NextYearEnd = NextCalendarYearEnd,

      -- Hell starts here.
      -- Let me use a couple of examples. With our current settings, on Jan. 1:
      -- Year = 2021 (because the end of the fiscal year falls into CY2021)
      -- Month = January (name), 01 (number) 
      -- (because the end of the fiscal month, 01-26, falls into January)
      -- Here's the catch:
      -- Quarter and month numbers are always based off of the start of your fiscal year
      -- So if your fiscal year starts July 15, July 15-August 14 will always have a month 
      -- number of 1 (because it's the first month in your fiscal year), but the fiscal
      -- month NAME will depend on @@FiscalMonthPeriodEndMatchesCalendar. If it's set to 0,
      -- the name would be July. If it's set to 1, it would be August.

      -- 'January'
      FiscalMonthName = DATENAME(
        month,
        FiscalPeriodMonthReference
      ),

      -- 'Jan'
      FiscalMonthAbbrev = LEFT(
        DATENAME(
          month,
          FiscalPeriodMonthReference
        ),
        3
      ),

      -- '2021W02'
      FiscalYearWeekName = CONCAT(
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
              TheDate
            ) + 1
          ),
          2
        )
      ),

      -- '2021-01'
      FiscalYearMonthName = CONCAT(
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
      FiscalMonthYearName = CONCAT(
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
      FiscalYearQuarterName = CONCAT(
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
      FiscalYear = FiscalYearNum,

      -- 202102
      FiscalYearWeek = CONVERT(
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
                TheDate
              ) + 1
            ),
            2
          )
        )
      ),

      -- 202101
      FiscalYearMonth = CONVERT(
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
      FiscalYearQuarter = CONVERT(
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
      FiscalDayOfMonth = DATEDIFF(
        day,
        FiscalMonthStart,
        TheDate
      ) + 1,

      -- 7
      FiscalDayOfQuarter = DATEDIFF(
        day,
        FiscalQuarterStart,
        TheDate
      ) + 1,

      -- 7
      FiscalDayOfYear = DATEDIFF(
        day,
        FiscalYearStart,
        TheDate
      ) + 1,

      -- 2
      FiscalWeekOfQuarter = DATEDIFF(
        week,
        FiscalQuarterStart,
        TheDate
      ) + 1,

      -- 2
      FiscalWeekOfYear = DATEDIFF(
        week,
        FiscalYearStart,
        TheDate
      ) + 1,

      -- 1
      FiscalMonth = FiscalMonthNum,

      -- 1
      FiscalMonthOfQuarter = DATEDIFF(
        month,
        FiscalQuarterStart,
        TheDate
      ) + IIF(
        DATEPART(
          day,
          TheDate
        ) >= @FiscalMonthStartDay,
        1,
        0
      ),

      -- 1
      FiscalQuarter = FiscalQuarterNum,

      -- 31
      FiscalDaysInMonth = DATEDIFF(
        day,
        FiscalMonthStart,
        FiscalMonthEnd
      ) + 1,

      -- 90
      FiscalDaysInQuarter = DATEDIFF(
        day,
        FiscalQuarterStart,
        FiscalQuarterEnd
      ) + 1,

      -- 365
      FiscalDaysInYear = DATEDIFF(
        day,
        FiscalYearStart,
        FiscalYearEnd
      ) + 1,

      -- 0
      FiscalCurrentMonthFlag = IIF(
        @TodayInLocal BETWEEN FiscalMonthStart AND FiscalMonthEnd,
        1,
        0
      ),

      -- 0
      FiscalPriorMonthFlag = IIF(
        @TodayInLocal BETWEEN 
          PriorFiscalMonthStart AND PriorFiscalMonthEnd,
        1,
        0
      ),

      -- 0
      FiscalNextMonthFlag = IIF(
        @TodayInLocal BETWEEN 
          NextFiscalMonthStart AND NextFiscalMonthEnd,
        1,
        0
      ),
      
      -- 0
      FiscalCurrentQuarterFlag = IIF(
        @TodayInLocal BETWEEN FiscalQuarterStart AND FiscalQuarterEnd,
        1,
        0
      ),
      
      -- 0
      FiscalPriorQuarterFlag = IIF(
        @TodayInLocal BETWEEN 
          PriorFiscalQuarterStart AND PriorFiscalQuarterEnd,
        1,
        0
      ),
      
      -- 0
      FiscalNextQuarterFlag = IIF(
        @TodayInLocal BETWEEN 
          NextFiscalQuarterStart AND NextFiscalQuarterEnd,
        1,
        0
      ),
      
      -- 1
      FiscalCurrentYearFlag = IIF(
        @TodayInLocal BETWEEN FiscalYearStart AND FiscalYearEnd,
        1,
        0
      ),
      
      -- 0
      FiscalPriorYearFlag = IIF(
        @TodayInLocal BETWEEN 
          PriorFiscalYearStart AND PriorFiscalYearEnd,
        1,
        0
      ),

      -- 0
      FiscalNextYearFlag = IIF(
        @TodayInLocal BETWEEN 
          NextFiscalYearStart AND NextFiscalYearEnd,
        1,
        0
      ),
      
      -- 0
      FiscalFirstDayOfMonthFlag = IIF(
        TheDate = FiscalMonthStart,
        1,
        0
      ),
      
      -- 0
      FiscalLastDayOfMonthFlag = IIF(
        TheDate = FiscalMonthEnd,
        1,
        0
      ),
      
      -- 0
      FiscalFirstDayOfQuarterFlag = IIF(
        TheDate = FiscalQuarterStart,
        1,
        0
      ),
      
      -- 0
      FiscalLastDayOfQuarterFlag = IIF(
        TheDate = FiscalQuarterEnd,
        1,
        0
      ),
      
      -- 0
      FiscalFirstDayOfYearFlag = IIF(
        TheDate = FiscalYearStart,
        1,
        0
      ),
      
      -- 0
      FiscalLastDayOfYearFlag = IIF(
        TheDate = FiscalYearEnd,
        1,
        0
      ),
      
      -- 0.2258
      FiscalFractionOfMonth = CAST(
        DATEDIFF(
          day,
          FiscalMonthStart,
          TheDate
        ) + 1 AS decimal(8,4)
      ) / (DATEDIFF(
        day,
        FiscalMonthStart,
        FiscalMonthEnd
      ) + 1),

      -- 0.0778
      FiscalFractionOfQuarter = CAST(
        DATEDIFF(
          day,
          FiscalQuarterStart,
          TheDate
        ) + 1 AS decimal(8,4)
      ) / (DATEDIFF(
        day,
        FiscalQuarterStart,
        FiscalQuarterEnd
      ) + 1),

      -- 0.0192
      FiscalFractionOfYear = CAST(
        DATEDIFF(
          day,
          FiscalYearStart,
          TheDate
        ) + 1 AS decimal(8,4)
      ) / (DATEDIFF(
        day,
        FiscalYearStart,
        FiscalYearEnd
      ) + 1),

      -- 2020-12-26
      FiscalCurrentMonthStart = FiscalMonthStart,

      -- 2021-01-25
      FiscalCurrentMonthEnd = FiscalMonthEnd,

      -- 2020-12-26
      FiscalCurrentQuarterStart = FiscalQuarterStart,

      -- 2021-03-25
      FiscalCurrentQuarterEnd = FiscalQuarterEnd,

      -- 2020-12-26
      FiscalCurrentYearStart = FiscalYearStart,

      -- 2021-12-25
      FiscalCurrentYearEnd = FiscalYearEnd,

      -- 2020-11-26
      FiscalPriorMonthStart = PriorFiscalMonthStart,

      -- 2020-12-25
      FiscalPriorMonthEnd = PriorFiscalMonthEnd,

      -- 2020-09-26
      FiscalPriorQuarterStart = PriorFiscalQuarterStart,

      -- 2020-12-25
      FiscalPriorQuarterEnd = PriorFiscalQuarterEnd,

      -- 2019-12-26
      FiscalPriorYearStart = PriorFiscalYearStart,

      -- 2020-12-25
      FiscalPriorYearEnd = PriorFiscalYearEnd,

      -- 2021-01-26
      FiscalNextMonthStart = NextFiscalMonthStart,

      -- 2021-02-25
      FiscalNextMonthEnd = NextFiscalMonthEnd,

      -- 2021-03-26
      FiscalNextQuarterStart = NextFiscalQuarterStart,

      -- 2021-06-25
      FiscalNextQuarterEnd = NextFiscalQuarterEnd,

      -- 2021-12-26
      FiscalNextYearStart = NextFiscalYearStart,

      -- 2022-12-25
      FiscalNextYearEnd = NextFiscalYearEnd,

{holiday_column_clause}
  FROM 
    FiscalHelpers AS fh
{holiday_join}
),

Burnups AS (
  SELECT 
    *,

    -- 1 - This is useful for dashboards. You can check 1 and see
    -- week-to-date for every week simultaneously. Same for mon/qtr/year.
    WeeklyBurnupStartingMonday = IIF(
      DayOfWeekStartingMonday <= (
        DATEPART(
          weekday,
          @TodayInLocal
        ) + @@DATEFIRST + 6 - 1
      ) % 7 + 1,
      1,
      0
    ),

    WeeklyBurnup = IIF(
      DayOfWeek <= DATEPART(
        weekday,
        @TodayInLocal
      ),
      1,
      0
    ),

    -- 1
    MonthlyBurnup = IIF(
      DayOfMonth <= DATEPART(
        day,
        @TodayInLocal
      ),
      1,
      0
    ),

    -- 1
    QuarterlyBurnup = IIF(
      DayOfQuarter <= DATEDIFF(
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
    YearlyBurnup = IIF(
      DayOfYear <= DATEPART(
        dayofyear,
        @TodayInLocal
      ),
      1,
      0
    ),

    -- 0
    FiscalMonthlyBurnup = IIF(
      FiscalDayOfMonth <= DATEDIFF(
        day,
        FiscalMonthStartToday,
        @TodayInLocal
      ) + 1,
      1,
      0
    ),

    -- 1
    FiscalQuarterlyBurnup = IIF(
      FiscalDayOfQuarter <= DATEDIFF(
        day,
        FiscalQuarterStartToday,
        @TodayInLocal
      ) + 1,
      1,
      0
    ),

    -- 1
    FiscalYearlyBurnup = IIF(
      FiscalDayOfYear <= DATEDIFF(
        day,
        FiscalYearStartToday,
        @TodayInLocal
      ) + 1,
      1,
      0
    )
  FROM Main
)

INSERT INTO dbo.DimDate
SELECT 
  {config.dim_date.columns.date_key.name} = DateKey,
  {config.dim_date.columns.the_date.name} = TheDate,
  {config.dim_date.columns.iso_date_name.name} = ISODateName,
  {config.dim_date.columns.american_date_name.name} = AmericanDateName,
  {config.dim_date.columns.day_of_week_name.name} = DayOfWeekName,
  {config.dim_date.columns.day_of_week_abbrev.name} = DayOfWeekAbbrev,
  {config.dim_date.columns.month_name.name} = MonthName,
  {config.dim_date.columns.month_abbrev.name} = MonthAbbrev,
  {config.dim_date.columns.year_week_name.name} = YearWeekName,
  {config.dim_date.columns.year_month_name.name} = YearMonthName,
  {config.dim_date.columns.month_year_name.name} = MonthYearName,
  {config.dim_date.columns.year_quarter_name.name} = YearQuarterName,
  {config.dim_date.columns.year.name} = Year,
  {config.dim_date.columns.year_week.name} = YearWeek,
  {config.dim_date.columns.iso_year_week_code.name} = ISOYearWeekCode,
  {config.dim_date.columns.year_month.name} = YearMonth,
  {config.dim_date.columns.year_quarter.name} = YearQuarter,
  {config.dim_date.columns.day_of_week_starting_monday.name} = DayOfWeekStartingMonday,
  {config.dim_date.columns.day_of_week.name} = DayOfWeek,
  {config.dim_date.columns.day_of_month.name} = DayOfMonth,
  {config.dim_date.columns.day_of_quarter.name} = DayOfQuarter,
  {config.dim_date.columns.day_of_year.name} = DayOfYear,
  {config.dim_date.columns.week_of_quarter.name} = WeekOfQuarter,
  {config.dim_date.columns.week_of_year.name} = WeekOfYear,
  {config.dim_date.columns.iso_week_of_year.name} = ISOWeekOfYear,
  {config.dim_date.columns.month.name} = Month,
  {config.dim_date.columns.month_of_quarter.name} = MonthOfQuarter,
  {config.dim_date.columns.quarter.name} = Quarter,
  {config.dim_date.columns.days_in_month.name} = DaysInMonth,
  {config.dim_date.columns.days_in_quarter.name} = DaysInQuarter,
  {config.dim_date.columns.days_in_year.name} = DaysInYear,
  {config.dim_date.columns.day_offset_from_today.name} = DayOffsetFromToday,
  {config.dim_date.columns.month_offset_from_today.name} = MonthOffsetFromToday,
  {config.dim_date.columns.quarter_offset_from_today.name} = QuarterOffsetFromToday,
  {config.dim_date.columns.year_offset_from_today.name} = YearOffsetFromToday,
  {config.dim_date.columns.today_flag.name} = TodayFlag,
  {config.dim_date.columns.current_week_starting_monday_flag.name} = CurrentWeekStartingMondayFlag,
  {config.dim_date.columns.current_week_flag.name} = CurrentWeekFlag,
  {config.dim_date.columns.prior_week_flag.name} = PriorWeekFlag,
  {config.dim_date.columns.next_week_flag.name} = NextWeekFlag,
  {config.dim_date.columns.current_month_flag.name} = CurrentMonthFlag,
  {config.dim_date.columns.prior_month_flag.name} = PriorMonthFlag,
  {config.dim_date.columns.next_month_flag.name} = NextMonthFlag,
  {config.dim_date.columns.current_quarter_flag.name} = CurrentQuarterFlag,
  {config.dim_date.columns.prior_quarter_flag.name} = PriorQuarterFlag,
  {config.dim_date.columns.next_quarter_flag.name} = NextQuarterFlag,
  {config.dim_date.columns.current_year_flag.name} = CurrentYearFlag,
  {config.dim_date.columns.prior_year_flag.name} = PriorYearFlag,
  {config.dim_date.columns.next_year_flag.name} = NextYearFlag,
  {config.dim_date.columns.weekday_flag.name} = WeekdayFlag,
  {config.dim_date.columns.business_day_flag.name} = BusinessDayFlag,
  {config.dim_date.columns.first_day_of_month_flag.name} = FirstDayOfMonthFlag,
  {config.dim_date.columns.last_day_of_month_flag.name} = LastDayOfMonthFlag,
  {config.dim_date.columns.first_day_of_quarter_flag.name} = FirstDayOfQuarterFlag,
  {config.dim_date.columns.last_day_of_quarter_flag.name} = LastDayOfQuarterFlag,
  {config.dim_date.columns.first_day_of_year_flag.name} = FirstDayOfYearFlag,
  {config.dim_date.columns.last_day_of_year_flag.name} = LastDayOfYearFlag,
  {config.dim_date.columns.fraction_of_week.name} = FractionOfWeek,
  {config.dim_date.columns.fraction_of_month.name} = FractionOfMonth,
  {config.dim_date.columns.fraction_of_quarter.name} = FractionOfQuarter,
  {config.dim_date.columns.fraction_of_year.name} = FractionOfYear,
  {config.dim_date.columns.prior_day.name} = PriorDay,
  {config.dim_date.columns.next_day.name} = NextDay,
  {config.dim_date.columns.same_day_prior_week.name} = SameDayPriorWeek,
  {config.dim_date.columns.same_day_prior_month.name} = SameDayPriorMonth,
  {config.dim_date.columns.same_day_prior_quarter.name} = SameDayPriorQuarter,
  {config.dim_date.columns.same_day_prior_year.name} = SameDayPriorYear,
  {config.dim_date.columns.same_day_next_week.name} = SameDayNextWeek,
  {config.dim_date.columns.same_day_next_month.name} = SameDayNextMonth,
  {config.dim_date.columns.same_day_next_quarter.name} = SameDayNextQuarter,
  {config.dim_date.columns.same_day_next_year.name} = SameDayNextYear,
  {config.dim_date.columns.current_week_start.name} = CurrentWeekStart,
  {config.dim_date.columns.current_week_end.name} = CurrentWeekEnd,
  {config.dim_date.columns.current_month_start.name} = CurrentMonthStart,
  {config.dim_date.columns.current_month_end.name} = CurrentMonthEnd,
  {config.dim_date.columns.current_quarter_start.name} = CurrentQuarterStart,
  {config.dim_date.columns.current_quarter_end.name} = CurrentQuarterEnd,
  {config.dim_date.columns.current_year_start.name} = CurrentYearStart,
  {config.dim_date.columns.current_year_end.name} = CurrentYearEnd,
  {config.dim_date.columns.prior_week_start.name} = PriorWeekStart,
  {config.dim_date.columns.prior_week_end.name} = PriorWeekEnd,
  {config.dim_date.columns.prior_month_start.name} = PriorMonthStart,
  {config.dim_date.columns.prior_month_end.name} = PriorMonthEnd,
  {config.dim_date.columns.prior_quarter_start.name} = PriorQuarterStart,
  {config.dim_date.columns.prior_quarter_end.name} = PriorQuarterEnd,
  {config.dim_date.columns.prior_year_start.name} = PriorYearStart,
  {config.dim_date.columns.prior_year_end.name} = PriorYearEnd,
  {config.dim_date.columns.next_week_start.name} = NextWeekStart,
  {config.dim_date.columns.next_week_end.name} = NextWeekEnd,
  {config.dim_date.columns.next_month_start.name} = NextMonthStart,
  {config.dim_date.columns.next_month_end.name} = NextMonthEnd,
  {config.dim_date.columns.next_quarter_start.name} = NextQuarterStart,
  {config.dim_date.columns.next_quarter_end.name} = NextQuarterEnd,
  {config.dim_date.columns.next_year_start.name} = NextYearStart,
  {config.dim_date.columns.next_year_end.name} = NextYearEnd,
  {config.dim_date.columns.weekly_burnup_starting_monday.name} = WeeklyBurnupStartingMonday,
  {config.dim_date.columns.weekly_burnup.name} = WeeklyBurnup,
  {config.dim_date.columns.monthly_burnup.name} = MonthlyBurnup,
  {config.dim_date.columns.quarterly_burnup.name} = QuarterlyBurnup,
  {config.dim_date.columns.yearly_burnup.name} = YearlyBurnup,
  {config.dim_date.columns.fiscal_month_name.name} = FiscalMonthName,
  {config.dim_date.columns.fiscal_month_abbrev.name} = FiscalMonthAbbrev,
  {config.dim_date.columns.fiscal_year_week_name.name} = FiscalYearWeekName,
  {config.dim_date.columns.fiscal_year_month_name.name} = FiscalYearMonthName,
  {config.dim_date.columns.fiscal_month_year_name.name} = FiscalMonthYearName,
  {config.dim_date.columns.fiscal_year_quarter_name.name} = FiscalYearQuarterName,
  {config.dim_date.columns.fiscal_year.name} = FiscalYear,
  {config.dim_date.columns.fiscal_year_week.name} = FiscalYearWeek,
  {config.dim_date.columns.fiscal_year_month.name} = FiscalYearMonth,
  {config.dim_date.columns.fiscal_year_quarter.name} = FiscalYearQuarter,
  {config.dim_date.columns.fiscal_day_of_month.name} = FiscalDayOfMonth,
  {config.dim_date.columns.fiscal_day_of_quarter.name} = FiscalDayOfQuarter,
  {config.dim_date.columns.fiscal_day_of_year.name} = FiscalDayOfYear,
  {config.dim_date.columns.fiscal_week_of_quarter.name} = FiscalWeekOfQuarter,
  {config.dim_date.columns.fiscal_week_of_year.name} = FiscalWeekOfYear,
  {config.dim_date.columns.fiscal_month.name} = FiscalMonth,
  {config.dim_date.columns.fiscal_month_of_quarter.name} = FiscalMonthOfQuarter,
  {config.dim_date.columns.fiscal_quarter.name} = FiscalQuarter,
  {config.dim_date.columns.fiscal_days_in_month.name} = FiscalDaysInMonth,
  {config.dim_date.columns.fiscal_days_in_quarter.name} = FiscalDaysInQuarter,
  {config.dim_date.columns.fiscal_days_in_year.name} = FiscalDaysInYear,
  {config.dim_date.columns.fiscal_current_month_flag.name} = FiscalCurrentMonthFlag,
  {config.dim_date.columns.fiscal_prior_month_flag.name} = FiscalPriorMonthFlag,
  {config.dim_date.columns.fiscal_next_month_flag.name} = FiscalNextMonthFlag,
  {config.dim_date.columns.fiscal_current_quarter_flag.name} = FiscalCurrentQuarterFlag,
  {config.dim_date.columns.fiscal_prior_quarter_flag.name} = FiscalPriorQuarterFlag,
  {config.dim_date.columns.fiscal_next_quarter_flag.name} = FiscalNextQuarterFlag,
  {config.dim_date.columns.fiscal_current_year_flag.name} = FiscalCurrentYearFlag,
  {config.dim_date.columns.fiscal_prior_year_flag.name} = FiscalPriorYearFlag,
  {config.dim_date.columns.fiscal_next_year_flag.name} = FiscalNextYearFlag,
  {config.dim_date.columns.fiscal_first_day_of_month_flag.name} = FiscalFirstDayOfMonthFlag,
  {config.dim_date.columns.fiscal_last_day_of_month_flag.name} = FiscalLastDayOfMonthFlag,
  {config.dim_date.columns.fiscal_first_day_of_quarter_flag.name} = FiscalFirstDayOfQuarterFlag,
  {config.dim_date.columns.fiscal_last_day_of_quarter_flag.name} = FiscalLastDayOfQuarterFlag,
  {config.dim_date.columns.fiscal_first_day_of_year_flag.name} = FiscalFirstDayOfYearFlag,
  {config.dim_date.columns.fiscal_last_day_of_year_flag.name} = FiscalLastDayOfYearFlag,
  {config.dim_date.columns.fiscal_fraction_of_month.name} = FiscalFractionOfMonth,
  {config.dim_date.columns.fiscal_fraction_of_quarter.name} = FiscalFractionOfQuarter,
  {config.dim_date.columns.fiscal_fraction_of_year.name} = FiscalFractionOfYear,
  {config.dim_date.columns.fiscal_current_month_start.name} = FiscalCurrentMonthStart,
  {config.dim_date.columns.fiscal_current_month_end.name} = FiscalCurrentMonthEnd,
  {config.dim_date.columns.fiscal_current_quarter_start.name} = FiscalCurrentQuarterStart,
  {config.dim_date.columns.fiscal_current_quarter_end.name} = FiscalCurrentQuarterEnd,
  {config.dim_date.columns.fiscal_current_year_start.name} = FiscalCurrentYearStart,
  {config.dim_date.columns.fiscal_current_year_end.name} = FiscalCurrentYearEnd,
  {config.dim_date.columns.fiscal_prior_month_start.name} = FiscalPriorMonthStart,
  {config.dim_date.columns.fiscal_prior_month_end.name} = FiscalPriorMonthEnd,
  {config.dim_date.columns.fiscal_prior_quarter_start.name} = FiscalPriorQuarterStart,
  {config.dim_date.columns.fiscal_prior_quarter_end.name} = FiscalPriorQuarterEnd,
  {config.dim_date.columns.fiscal_prior_year_start.name} = FiscalPriorYearStart,
  {config.dim_date.columns.fiscal_prior_year_end.name} = FiscalPriorYearEnd,
  {config.dim_date.columns.fiscal_next_month_start.name} = FiscalNextMonthStart,
  {config.dim_date.columns.fiscal_next_month_end.name} = FiscalNextMonthEnd,
  {config.dim_date.columns.fiscal_next_quarter_start.name} = FiscalNextQuarterStart,
  {config.dim_date.columns.fiscal_next_quarter_end.name} = FiscalNextQuarterEnd,
  {config.dim_date.columns.fiscal_next_year_start.name} = FiscalNextYearStart,
  {config.dim_date.columns.fiscal_next_year_end.name} = FiscalNextYearEnd,
  {config.dim_date.columns.fiscal_monthly_burnup.name} = FiscalMonthlyBurnup,
  {config.dim_date.columns.fiscal_quarterly_burnup.name} = FiscalQuarterlyBurnup,
  {config.dim_date.columns.fiscal_yearly_burnup.name} = FiscalYearlyBurnup,
{holiday_columns}
FROM Burnups
ORDER BY DateKey ASC
OPTION (MAXRECURSION 0)
"""
