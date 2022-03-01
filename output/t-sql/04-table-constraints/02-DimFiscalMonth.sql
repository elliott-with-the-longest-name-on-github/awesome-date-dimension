ALTER TABLE dbo.DimFiscalMonth
ADD PRIMARY KEY CLUSTERED (MonthStartKey, MonthEndKey ASC) WITH (
  PAD_INDEX = OFF,
  STATISTICS_NORECOMPUTE = OFF,
  IGNORE_DUP_KEY = OFF,
  ALLOW_ROW_LOCKS = ON,
  ALLOW_PAGE_LOCKS = ON
);

CREATE NONCLUSTERED INDEX IDX_NC_dbo_DimFiscalMonth_MonthStartDate ON dbo.DimFiscalMonth (MonthStartDate);
CREATE NONCLUSTERED INDEX IDX_NC_dbo_DimFiscalMonth_MonthEndDate ON dbo.DimFiscalMonth (MonthEndDate);