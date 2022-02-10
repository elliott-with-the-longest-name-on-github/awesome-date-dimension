def dim_fiscal_month_insert_template() -> str:
    return """WITH DistinctMonths AS (
  SELECT
  MonthStartKey = CONVERT(
    int,
    CONVERT(
    varchar(8),
    FiscalCurrentMonthStart,
    112
    )
  ),
  MonthEndKey = CONVERT(
    int,
    CONVERT(
    varchar(8),
    FiscalCurrentMonthEnd,
    112
    )
  ),
  CompanyHolidaysInMonth = SUM(CompanyHolidayFlag * 1),
  USPublicHolidaysInMonth = SUM(USPublicHolidayFlag * 1)
  FROM
    dbo.DimDate
    GROUP BY FiscalCurrentMonthStart, FiscalCurrentMonthEnd
)

INSERT INTO dbo.DimFiscalMonth
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
  MonthName = startdate.FiscalMonthName,
  MonthAbbrev = startdate.FiscalMonthAbbrev,
  MonthStartYearWeekName = startdate.FiscalYearWeekName,
  MonthEndYearWeekName = enddate.FiscalYearWeekName,
  YearMonthName = startdate.FiscalYearMonthName,
  MonthYearName = startdate.FiscalMonthYearName,
  YearQuarterName = startdate.FiscalYearQuarterName,
  Year = startdate.FiscalYear,
  MonthStartYearWeek = startdate.FiscalYearWeek,
  MonthEndYearWeek = enddate.FiscalYearWeek,
  YearMonth = startdate.FiscalYearMonth,
  YearQuarter = startdate.FiscalYearQuarter,
  MonthStartDayOfQuarter = startdate.FiscalDayOfQuarter,
  MonthEndDayOfQuarter = enddate.FiscalDayOfQuarter,
  MonthStartDayOfYear = startdate.FiscalDayOfYear,
  MonthEndDayOfYear = enddate.FiscalDayOfYear,
  MonthStartWeekOfQuarter = startdate.FiscalWeekOfQuarter,
  MonthEndWeekOfQuarter = enddate.FiscalWeekOfQuarter,
  MonthStartWeekOfYear = startdate.FiscalWeekOfYear,
  MonthEndWeekOfYear = enddate.FiscalWeekOfYear,
  MonthOfQuarter = startdate.FiscalMonthOfQuarter,
  Quarter = startdate.FiscalQuarter,
  DaysInMonth = startdate.FiscalDaysInMonth,
  DaysInQuarter = startdate.FiscalDaysInQuarter,
  DaysInYear = startdate.FiscalDaysInYear,
  CurrentMonthFlag = startdate.FiscalCurrentMonthFlag,
  PriorMonthFlag = startdate.FiscalPriorMonthFlag,
  NextMonthFlag = startdate.FiscalNextMonthFlag,
  CurrentQuarterFlag = startdate.FiscalCurrentQuarterFlag,
  PriorQuarterFlag = startdate.FiscalPriorQuarterFlag,
  NextQuarterFlag = startdate.FiscalNextQuarterFlag,
  CurrentYearFlag = startdate.FiscalCurrentYearFlag,
  PriorYearFlag = startdate.FiscalPriorYearFlag,
  NextYearFlag = startdate.FiscalNextYearFlag,
  FirstDayOfMonthFlag = startdate.FiscalFirstDayOfMonthFlag,
  LastDayOfMonthFlag = startdate.FiscalLastDayOfMonthFlag,
  FirstDayOfQuarterFlag = startdate.FiscalFirstDayOfQuarterFlag,
  LastDayOfQuarterFlag = startdate.FiscalLastDayOfQuarterFlag,
  FirstDayOfYearFlag = startdate.FiscalFirstDayOfYearFlag,
  LastDayOfYearFlag = startdate.FiscalLastDayOfYearFlag,
  MonthStartFractionOfQuarter = startdate.FiscalFractionOfQuarter,
  MonthEndFractionOfQuarter = enddate.FiscalFractionOfQuarter,
  MonthStartFractionOfYear = startdate.FiscalFractionOfYear,
  MonthEndFractionOfYear = enddate.FiscalFractionOfYear,
  CurrentQuarterStart = startdate.FiscalCurrentQuarterStart,
  CurrentQuarterEnd = startdate.FiscalCurrentQuarterEnd,
  CurrentYearStart = startdate.FiscalCurrentYearStart,
  CurrentYearEnd = startdate.FiscalCurrentYearEnd,
  PriorMonthStart = startdate.FiscalPriorMonthStart,
  PriorMonthEnd = startdate.FiscalPriorMonthEnd,
  PriorQuarterStart = startdate.FiscalPriorQuarterStart,
  PriorQuarterEnd = startdate.FiscalPriorQuarterEnd,
  PriorYearStart = startdate.FiscalPriorYearStart,
  PriorYearEnd = startdate.FiscalPriorYearEnd,
  NextMonthStart = startdate.FiscalNextMonthStart,
  NextMonthEnd = startdate.FiscalNextMonthEnd,
  NextQuarterStart = startdate.FiscalNextQuarterStart,
  NextQuarterEnd = startdate.FiscalNextQuarterEnd,
  NextYearStart = startdate.FiscalNextYearStart,
  NextYearEnd = startdate.FiscalNextYearEnd,
  MonthStartQuarterlyBurnup = startdate.FiscalQuarterlyBurnup,
  MonthEndQuarterlyBurnup = enddate.FiscalQuarterlyBurnup,
  MonthStartYearlyBurnup = startdate.FiscalYearlyBurnup,
  MonthEndQuarterlyBurnup = enddate.FiscalYearlyBurnup,
  base.CompanyHolidaysInMonth,
  base.USPublicHolidaysInMonth
FROM
  DistinctMonths AS base
  INNER JOIN dbo.DimDate AS startdate
    ON base.MonthStartKey = startdate.DateKey
  INNER JOIN dbo.DimDate AS enddate
    ON base.MonthEndKey = enddate.DateKey;"""
