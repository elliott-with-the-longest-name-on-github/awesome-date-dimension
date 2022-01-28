CREATE PROCEDURE dbo.sp_build_DimCalendarMonth AS BEGIN
  SET XACT_ABORT ON;
  BEGIN TRY
    BEGIN TRANSACTION;

    TRUNCATE TABLE dbo.DimCalendarMonth;

    -- Get the distinct fiscal month start/ends from DimDate
    WITH DistinctMonths AS (
      SELECT
        MonthStartKey = CONVERT(
          int,
          CONVERT(
            varchar(8),
            CurrentMonthStart,
            112
          )
        ),
        MonthEndKey = CONVERT(
          int,
          CONVERT(
            varchar(8),
            CurrentMonthEnd,
            112
          )
        ),
        CompanyHolidaysInMonth = SUM(CompanyHolidayFlag * 1),
        USPublicHolidaysInMonth = SUM(USPublicHolidayFlag * 1)
      FROM
        dbo.DimDate
      GROUP BY CurrentMonthStart, CurrentMonthEnd
    )

    INSERT INTO dbo.DimCalendarMonth
    -- Yank the day-level stuff we need for both the start and end dates from dbo.DimDate
    SELECT  
      base.MonthStartKey,
      base.MonthEndKey,
      MonthStartDate = startdate.TheDate,
      MonthEndDate = enddate.TheDate,
      MonthStartISODateName = startdate.ISODateName,
      MonthEndISODateName = enddate.ISODateName,
      MonthStartAmericanDateName = startdate.AmericanDateName,
      MonthEndAmericanDateName = enddate.AmericanDateName,
      MonthName = startdate.MonthName,
      MonthAbbrev = startdate.MonthAbbrev,
      MonthStartYearWeekName = startdate.YearWeekName,
      MonthEndYearWeekName = enddate.YearWeekName,
      YearMonthName = startdate.YearMonthName,
      MonthYearName = startdate.MonthYearName,
      YearQuarterName = startdate.YearQuarterName,
      Year = startdate.Year,
      MonthStartYearWeek = startdate.YearWeek,
      MonthEndYearWeek = enddate.YearWeek,
      YearMonth = startdate.YearMonth,
      YearQuarter = startdate.YearQuarter,
      MonthStartDayOfQuarter = startdate.DayOfQuarter,
      MonthEndDayOfQuarter = enddate.DayOfQuarter,
      MonthStartDayOfYear = startdate.DayOfYear,
      MonthEndDayOfYear = enddate.DayOfYear,
      MonthStartWeekOfQuarter = startdate.WeekOfQuarter,
      MonthEndWeekOfQuarter = enddate.WeekOfQuarter,
      MonthStartWeekOfYear = startdate.WeekOfYear,
      MonthEndWeekOfYear = enddate.WeekOfYear,
      MonthOfQuarter = startdate.MonthOfQuarter,
      Quarter = startdate.Quarter,
      DaysInMonth = startdate.DaysInMonth,
      DaysInQuarter = startdate.DaysInQuarter,
      DaysInYear = startdate.DaysInYear,
      CurrentMonthFlag = startdate.CurrentMonthFlag,
      PriorMonthFlag = startdate.PriorMonthFlag,
      NextMonthFlag = startdate.NextMonthFlag,
      CurrentQuarterFlag = startdate.CurrentQuarterFlag,
      PriorQuarterFlag = startdate.PriorQuarterFlag,
      NextQuarterFlag = startdate.NextQuarterFlag,
      CurrentYearFlag = startdate.CurrentYearFlag,
      PriorYearFlag = startdate.PriorYearFlag,
      NextYearFlag = startdate.NextYearFlag,
      FirstDayOfMonthFlag = startdate.FirstDayOfMonthFlag,
      LastDayOfMonthFlag = startdate.LastDayOfMonthFlag,
      FirstDayOfQuarterFlag = startdate.FirstDayOfQuarterFlag,
      LastDayOfQuarterFlag = startdate.LastDayOfQuarterFlag,
      FirstDayOfYearFlag = startdate.FirstDayOfYearFlag,
      LastDayOfYearFlag = startdate.LastDayOfYearFlag,
      MonthStartFractionOfQuarter = startdate.FractionOfQuarter,
      MonthEndFractionOfQuarter = enddate.FractionOfQuarter,
      MonthStartFractionOfYear = startdate.FractionOfYear,
      MonthEndFractionOfYear = enddate.FractionOfYear,
      CurrentQuarterStart = startdate.CurrentQuarterStart,
      CurrentQuarterEnd = startdate.CurrentQuarterEnd,
      CurrentYearStart = startdate.CurrentYearStart,
      CurrentYearEnd = startdate.CurrentYearEnd,
      PriorMonthStart = startdate.PriorMonthStart,
      PriorMonthEnd = startdate.PriorMonthEnd,
      PriorQuarterStart = startdate.PriorQuarterStart,
      PriorQuarterEnd = startdate.PriorQuarterEnd,
      PriorYearStart = startdate.PriorYearStart,
      PriorYearEnd = startdate.PriorYearEnd,
      NextMonthStart = startdate.NextMonthStart,
      NextMonthEnd = startdate.NextMonthEnd,
      NextQuarterStart = startdate.NextQuarterStart,
      NextQuarterEnd = startdate.NextQuarterEnd,
      NextYearStart = startdate.NextYearStart,
      NextYearEnd = startdate.NextYearEnd,
      MonthStartQuarterlyBurnup = startdate.QuarterlyBurnup,
      MonthEndQuarterlyBurnup = enddate.QuarterlyBurnup,
      MonthStartYearlyBurnup = startdate.YearlyBurnup,
      MonthEndQuarterlyBurnup = enddate.YearlyBurnup,
      base.CompanyHolidaysInMonth,
      base.USPublicHolidaysInMonth
    FROM
      DistinctMonths AS base
      INNER JOIN dbo.DimDate AS startdate
        ON base.MonthStartKey = startdate.DateKey
      INNER JOIN dbo.DimDate AS enddate
        ON base.MonthEndKey = enddate.DateKey;

  COMMIT TRANSACTION;
  END TRY
  BEGIN CATCH
    EXEC sp_GetErrorInfo;
    IF @@TRANCOUNT > 0
      ROLLBACK TRANSACTION;
    THROW;
  END CATCH;
END
GO