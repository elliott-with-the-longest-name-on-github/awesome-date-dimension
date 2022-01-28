ALTER TABLE dbo.DimCalendarMonth
ADD PRIMARY KEY CLUSTERED (MonthStartKey, MonthEndKey ASC) WITH (
  PAD_INDEX = OFF,
  STATISTICS_NORECOMPUTE = OFF,
  IGNORE_DUP_KEY = OFF,
  ALLOW_ROW_LOCKS = ON,
  ALLOW_PAGE_LOCKS = ON
);

CREATE NONCLUSTERED INDEX IDX_NC_dbo_DimCalendarMonth_MonthStartDate ON dbo.DimCalendarMonth (MonthStartDate);
CREATE NONCLUSTERED INDEX IDX_NC_dbo_DimCalendarMonth_MonthEndDate ON dbo.DimCalendarMonth (MonthEndDate);