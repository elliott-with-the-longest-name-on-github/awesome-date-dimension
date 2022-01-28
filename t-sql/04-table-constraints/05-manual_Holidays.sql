ALTER TABLE integration.manual_Holidays 
ADD PRIMARY KEY CLUSTERED (DateKey ASC, HolidayTypeKey ASC) WITH (
  PAD_INDEX = OFF,
  STATISTICS_NORECOMPUTE = OFF,
  IGNORE_DUP_KEY = OFF,
  ALLOW_ROW_LOCKS = ON,
  ALLOW_PAGE_LOCKS = ON
);

ALTER TABLE integration.manual_Holidays
ADD CONSTRAINT FK_manual_Holidays_HolidayType FOREIGN KEY (HolidayTypeKey)
  REFERENCES integration.manual_HolidayTypes (HolidayTypeKey)
  ON DELETE CASCADE
  ON UPDATE CASCADE;
