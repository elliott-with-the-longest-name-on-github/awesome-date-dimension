CREATE PROCEDURE dbo.sp_build_DimDate AS BEGIN
  DECLARE @TodayInLocal date;
  DECLARE @FiscalMonthStartDay int;
  DECLARE @FiscalYearStartMonth int;

  -- customize-fiscalperiods START
  SET @FiscalMonthStartDay=26;
  SET @FiscalYearStartMonth=12;
  -- customize-fiscalperiods END

  -- customize-todayinlocal START
  SET @TodayInLocal = CONVERT(
    date, 
    GETUTCDATE() AT TIME ZONE 'UTC' AT TIME ZONE 'Mountain Standard Time'
  );
  -- customize-todayinlocal END

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
      d.DateKey,
      DayOffsetFromToday = DATEDIFF(
        day,
        @TodayInLocal,
        TheDate
      ),
      MonthOffsetFromToday = DATEDIFF(
        month,
        @TodayInLocal,
        TheDate
      ),
      QuarterOffsetFromToday = DATEDIFF(
        quarter,
        @TodayInLocal,
        TheDate
      ),
      YearOffsetFromToday = DATEDIFF(
        year,
        @TodayInLocal,
        TheDate
      ),
      TodayFlag = IIF(
        TheDate = @TodayInLocal,
        1,
        0
      ),
      CurrentWeekStartingMondayFlag = IIF(
        DATEDIFF(
          week,
          CONVERT(date, GETDATE()),
          DATEADD(day, -1, TheDate)
        ) = 0,
        1,
        0
      ),
      CurrentWeekFlag = IIF(
        DATEDIFF(week, @TodayInLocal, TheDate) = 0,
        1,
        0
      ),
      PriorWeekFlag = IIF(
        DATEDIFF(week, @TodayInLocal, TheDate) = -1,
        1,
        0
      ),
      NextWeekFlag = IIF(
        DATEDIFF(week, @TodayInLocal, TheDate) = 1,
        1,
        0
      ),
      CurrentMonthFlag = IIF(
        DATEDIFF(month, @TodayInLocal, TheDate) = 0,
        1,
        0
      ),
      PriorMonthFlag = IIF(
        DATEDIFF(month, @TodayInLocal, TheDate) = -1,
        1,
        0
      ),
      NextMonthFlag = IIF(
        DATEDIFF(month, @TodayInLocal, TheDate) = 1,
        1,
        0
      ),
      CurrentQuarterFlag = IIF(
        DATEDIFF(quarter, @TodayInLocal, TheDate) = 0,
        1,
        0
      ),
      PriorQuarterFlag = IIF(
        DATEDIFF(quarter, @TodayInLocal, TheDate) = -1,
        1,
        0
      ),
      NextQuarterFlag = IIF(
        DATEDIFF(quarter, @TodayInLocal, TheDate) = 1,
        1,
        0
      ),
      CurrentYearFlag = IIF(
        DATEDIFF(year, @TodayInLocal, TheDate) = 0,
        1,
        0
      ),
      PriorYearFlag = IIF(
        DATEDIFF(year, @TodayInLocal, TheDate) = -1,
        1,
        0
      ),
      NextYearFlag = IIF(
        DATEDIFF(year, @TodayInLocal, TheDate) = 1,
        1,
        0
      ),
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
        DayOfWeek <= DayOfWeekToday,
        1,
        0
      ),
      MonthlyBurnup = IIF(
        DayOfMonth <= DayOfMonthToday,
        1,
        0
      ),
      QuarterlyBurnup = IIF(
        DayOfQuarter <= DayOfQuarterToday,
        1,
        0
      ),
      YearlyBurnup = IIF(
        DayOfYear <= DayOfYearToday,
        1,
        0
      ),
      FiscalCurrentMonthFlag = IIF(
        @TodayInLocal BETWEEN 
          FiscalCurrentMonthStart AND FiscalCurrentMonthEnd,
        1,
        0
      ),
      FiscalPriorMonthFlag = IIF(
        @TodayInLocal BETWEEN 
          FiscalPriorMonthStart AND FiscalPriorMonthEnd,
        1,
        0
      ),
      FiscalNextMonthFlag = IIF(
        @TodayInLocal BETWEEN 
          FiscalNextMonthStart AND FiscalNextMonthEnd,
        1,
        0
      ),
      FiscalCurrentQuarterFlag = IIF(
        @TodayInLocal BETWEEN 
          FiscalCurrentQuarterStart AND FiscalCurrentQuarterEnd,
        1,
        0
      ),
      FiscalPriorQuarterFlag = IIF(
        @TodayInLocal BETWEEN 
          FiscalPriorQuarterStart AND FiscalPriorQuarterEnd,
        1,
        0
      ),
      FiscalNextQuarterFlag = IIF(
        @TodayInLocal BETWEEN 
          FiscalNextQuarterStart AND FiscalNextQuarterEnd,
        1,
        0
      ),
      FiscalCurrentYearFlag = IIF(
        @TodayInLocal BETWEEN 
          FiscalCurrentYearStart AND FiscalCurrentYearEnd,
        1,
        0
      ),
      FiscalPriorYearFlag = IIF(
        @TodayInLocal BETWEEN 
          FiscalPriorYearStart AND FiscalPriorYearEnd,
        1,
        0
      ),
      FiscalNextYearFlag = IIF(
        @TodayInLocal BETWEEN 
          FiscalNextYearStart AND FiscalNextYearEnd,
        1,
        0
      ),
      FiscalMonthlyBurnup = IIF(
        FiscalDayOfMonth <= FiscalDayOfMonthToday,
        1,
        0
      ),
      FiscalQuarterlyBurnup = IIF(
      FiscalDayOfQuarter <= FiscalDayOfQuarterToday,
        1,
        0
      ),
      FiscalYearlyBurnup = IIF(
        FiscalDayOfYear <= FiscalDayOfyearToday,
        1,
        0
      ),
      BusinessDayFlag = IIF(
        ch.DateKey IS NOT NULL
        OR DATEPART(
          weekday,
          TheDate
        ) IN (1, 7),
        0,
        1
      ),
      CompanyHolidayFlag = IIF(
        ch.DateKey IS NOT NULL,
        1,
        0
      ),
      USPublicHolidayFlag = IIF(
        ph.DateKey IS NOT NULL,
        1,
        0
      ),
      CompanyHolidayName = ch.HolidayName,
      USPublicHolidayName = ph.HolidayName
    FROM
      dbo.DimDate AS d
      CROSS JOIN BurnupsAsOfToday AS r
      -- customize-holidays JOIN START
      LEFT OUTER JOIN integration.manual_Holidays AS ch -- Company Holidays
        ON d.DateKey = ch.DateKey AND ch.HolidayTypeKey = 1
      LEFT OUTER JOIN integration.manual_Holidays AS ph -- Public Holidays
        ON d.DateKey = ph.DateKey AND ph.HolidayTypeKey = 2
      -- customize-holidays JOIN END
  )

  UPDATE d
  SET
    d.DayOffsetFromToday = dc.DayOffsetFromToday,
    d.MonthOffsetFromToday = dc.MonthOffsetFromToday,
    d.QuarterOffsetFromToday = dc.QuarterOffsetFromToday,
    d.YearOffsetFromToday = dc.YearOffsetFromToday,
    d.TodayFlag = dc.TodayFlag,
    d.CurrentWeekStartingMondayFlag = dc.CurrentWeekStartingMondayFlag,
    d.CurrentWeekFlag = dc.CurrentWeekFlag,
    d.PriorWeekFlag = dc.PriorWeekFlag,
    d.NextWeekFlag = dc.NextWeekFlag,
    d.CurrentMonthFlag = dc.CurrentMonthFlag,
    d.PriorMonthFlag = dc.PriorMonthFlag,
    d.NextMonthFlag = dc.NextMonthFlag,
    d.CurrentQuarterFlag = dc.CurrentQuarterFlag,
    d.PriorQuarterFlag = dc.PriorQuarterFlag,
    d.NextQuarterFlag = dc.NextQuarterFlag,
    d.CurrentYearFlag = dc.CurrentYearFlag,
    d.PriorYearFlag = dc.PriorYearFlag,
    d.NextYearFlag = dc.NextYearFlag,
    d.WeeklyBurnupStartingMonday = dc.WeeklyBurnupStartingMonday,
    d.WeeklyBurnup = dc.WeeklyBurnup,
    d.MonthlyBurnup = dc.MonthlyBurnup,
    d.QuarterlyBurnup = dc.QuarterlyBurnup,
    d.YearlyBurnup = dc.YearlyBurnup,
    d.FiscalCurrentMonthFlag = dc.FiscalCurrentMonthFlag,
    d.FiscalPriorMonthFlag = dc.FiscalPriorMonthFlag,
    d.FiscalNextMonthFlag = dc.FiscalNextMonthFlag,
    d.FiscalCurrentQuarterFlag = dc.FiscalCurrentQuarterFlag,
    d.FiscalPriorQuarterFlag = dc.FiscalPriorQuarterFlag,
    d.FiscalNextQuarterFlag = dc.FiscalNextQuarterFlag,
    d.FiscalCurrentYearFlag = dc.FiscalCurrentYearFlag,
    d.FiscalPriorYearFlag = dc.FiscalPriorYearFlag,
    d.FiscalNextYearFlag = dc.FiscalNextYearFlag,
    d.FiscalMonthlyBurnup = dc.FiscalMonthlyBurnup,
    d.FiscalQuarterlyBurnup = dc.FiscalQuarterlyBurnup,
    d.FiscalYearlyBurnup = dc.FiscalYearlyBurnup,
    d.CompanyHolidayFlag = dc.CompanyHolidayFlag,
    d.USPublicHolidayFlag = dc.USPublicHolidayFlag,
    d.CompanyHolidayName = dc.CompanyHolidayName,
    d.USPublicHolidayName = dc.USPublicHolidayName
  FROM
    dbo.DimDate AS d
    INNER JOIN DateCalculations AS dc
      ON d.DateKey = dc.DateKey
END
GO
