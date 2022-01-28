# awesome-date-dimension

A few months back, I had to create a date dimension. All of the scripts I could find publicly were missing a lot of the flags and other features I needed (especially around fiscal month handling) -- so I created one myself. This is written in T-SQL, but shouldn't be _too_ hard to port to another dialect of SQL.

This template also provides tables and refresh scripts for a `DimFiscalMonth` and a `DimCalendarMonth`. These roll up details from `DimDate` into a dimension you can use to join pre-aggregated tables together. This can be useful when trying to join fact tables that are at different date granularities or when trying to create a pre-aggregated model in Power BI.

If you're a corporation and want me to translate this to another dialect, send me a message. I'd be happy to do so inexpensively.

## Instructions

One of the few assumptions I made is around table names. I assume your table is called `dbo.DimDate`. If it's not, just do a find-and-replace across the whole project for whatever your table name is. 

Two tables are also required for the holiday mapping: `integration.manual_HolidayTypes` and `integration.manual_Holidays`. `HolidayTypes` just holds different type definitions for holidays (for example, "Company Holiday", "US Public Holiday", "Canadian Public Holiday"). The template script creates flags for `CompanyHoliday` and `USPublicHoliday` by default. You can add to or subtract from this by adding or removing columns and logic (see [Custom Holidays](#custom-holidays)).

All customizations should be performed _before_ executing the below steps. If you need to customize something, come back to this section after reading through the customization subheaders below. As a general rule, if you want to customize a behavior, I have provided easily-searchable comments in the code. For example, to customize holidays, perform a folder-wide search for "customize-holidays". Sections are delimited with a starting comment of `-- customize-holidays START` and an ending comment of `--customize-holidays END`. Specific comments are listed in their sections. 

1. Choose a language. These are represented by the top-level folders. Currently, only T-SQL is supported.
2. Start from the top. The folders are ordered. Run all of the scripts from each folder before moving to the next.
3. Run the following scriptlet to make sure the refresh procs are working:
```sql
EXEC dbo.sp_build_DimDate;
EXEC dbo.sp_build_DimCalendarMonth;
EXEC dbo.sp_build_DimFiscalMonth;
```
4. Set the stored procedures to run daily with your chosen ETL software. The proc for `DimDate` should run prior to the procs for `DimFiscalMonth` and `DimCalendarMonth`, as they depend upon `DimDate` being up-to-date.

## Customization

See below for instructions around customizing specific behaviors.

### Generated Date Range

Comment name: `-- customize-daterange`

The date range generated is defined in `/{language}/02-initial-build/03-InsertDimDateRecords.sql`. Specifically, you're looking for the following two lines:
```sql
SET @FirstDate='2000-01-01';
SET @NumberOfYearsToGenerate=100;
```
By default, it will start on 2021-01-01 and run through 100 years.

### Fiscal Periods

Comment name: `-- customize-fiscalperiods`

I built this around having a very flexible set of fiscal periods. That being said, there are a few assumptions:

1. Your fiscal month runs from a constant numerical day to a numerical day. For example, a fiscal month of the 24th through the 23rd is valid; a fiscal month of "the first Sunday of the calendar month to the first Saturday of the next calendar month" is not.
2. Your fiscal month does not start after the 28th. Because February, the shortest month, has 28 days, anything over this causes _all sorts_ of horrifying edge cases.

The fiscal period settings are defined in `/{language}/02-initial-build/03-InsertDimDateRecords.sql`. They are also defined in `/{language}/03-refresh-procs/01-sp_build_DimDate.sql`. (The first file controls the initial build behavior; the second file controls the daily update behavior.)

There are five available settings:

1. `FiscalMonthStartDay` - This controls the first day of your fiscal month. For example, if your month ran from the 15th through the 14th, you'd set this to 15.
2. `FiscalYearStartMonth` - This controls the first month of your fiscal year. For example, if your fiscal year starts in November, you'd set this to 11.
3. `FiscalMonthPeriodEndMatchesCalendar` - This controls the behavior of fields like `FiscalMonthName` by allowing you to set which "end" of your fiscal month determines its name. For example, say your fiscal month starts on the 15th and runs through the 14th. For the dates of December 15-January 14, is that the fiscal month of December or January? Setting this flag to 1 indicates that the month presented in the example is called "January" (because the fiscal month end falls in the calendar month of January). Setting it to 0 indicates that it's called "December".
4. `FiscalQuarterPeriodEndMatchesCalendar` - Same as above, but for the quarter. If the quarter starts in December and runs through February, is that Q1 or Q4? `FiscalQuarterPeriodEndMatchesCalendar = 1` indicates that it's Q1, whereas `0` indicates it's Q4.
5. `FiscalYearPeriodEndMatchesCalendar` - Same as above, but for year. If your year runs from June 2020 through June 2021, is it the fiscal year of 2020 or 2021? `FiscalYearPeriodEndMatchesCalendar = 1` indicates that it's 2021, whereas `0` indicates it's 2020.

**Be sure to set the variables in both files!**

### TodayInLocal Behavior

Comment name: `-- customize-todayinlocal`

One of the variables central to the load scripts is called `TodayInLocal`. At runtime, it determines what the date is in your local timezone. By default, it's set to `Mountain Standard Time`. You can change this by searching for the comment and adjusting the timezone. Be careful -- timezones may be named different things on different operating systems. Make sure the name you use is correct for your runtime environment!

### Business Days

Comment name: `-- customize-businessdays`

Business days are based off of company holidays. The logic is pretty simple: If the date is a company holiday or a weekend, the `BusinessDayFlag` will be 0. If it's not, it's a 1. I didn't build much specific customization in for this behavior; If you'd like to change it, you can replace the logic (just search for the comment).


### Custom Holidays

Comment name: `-- customize-holidays`

Holidays are pretty easy to customize as long as you only need US Public Holidays and Company Holidays. If you need to add more categories, you'll have to start adding more columns. I'll cover as many use cases here as possible, but you're going to have to get your hands a little dirty for each of them.

#### Holiday Branding

Many companies may want to have their company holiday columns less generically-named. Currently, company holidays are just called "Company Holidays" everywhere. If you want to change this, you can pretty safely do a project-wide find and replace of "Company" to your company's name. (Just make sure whatever you replace "Company" with is a valid SQL identifier.)

#### Holiday Types

The default two holiday types are "Company Holiday" and "US Public Holiday". They're loaded to `integration.manual_HolidayTypes`. If you need to change one of these or add another, just adjust or add the record to `/{language}/02-initial-build/01-InsertHolidayTypes.sql`.

#### Holiday Days and Names

Holidays are loaded to the `integration.manual_Holidays` table. To add or remove, or update holidays at initial load time, adjust the rows in `/{language}/02-initial-build/01-InsertHolidays.sql`. Be sure that the keys you provide for `HolidayTypes` are present in `integration.manual_HolidayTypes`.

If you need to make updates after the initial build, just add, remove, or update the records in `integration.manual_Holidays`.

#### Holiday Columns

Here's where it gets tricky. There are a few holiday-related columns:

1. CompanyHolidayFlag
2. USPublicHolidayFlag
3. CompanyHolidayName
4. USPublicHolidayName
5. BusinessDayFlag
6. A couple of other derived columns in the month-aggregated tables

Company-holiday-related information is pulled from `integration.manual_Holidays` where `HolidayTypeKey = 1`. The same is true for US Public Holidays, except that `HolidayTypeKey = 2`. If you've added or removed holiday types, or if you need to add more holiday types, you're going to have to perform a few steps.

##### Removing Columns

1. Remove the holiday type (see above).
2. Remove the holidays (see above).
3. Track down the locations where the scripts join into the `integration.manual_Holidays` table. Search for the comment `-- customize-holidays JOIN START`. Remove the join you don't want.
4. Remove columns. I haven't commented where all of these columns are because it's relatively easy to remove references to them. For example, if you don't want US Public Holidays, just search for the US-public-holiday-related column names and remove them.

##### Adding Columns

1. Add a new holiday type (see above).
2. Add new holidays (see above).
3. Track down the locations where the scripts join into the `integration.manual_Holidays` table. Search for the comment `-- customize-holidays JOIN START`. Add a join (you can copy an existing one), substituting in your `HolidayTypeKey`.
4. Add column definitions to all of the tables' definitions.
5. Add logic to the scripts to load data to the new columns. You can probably copy one of the existing columns and just sub in a reference to your new join.

## Column Documentation

A decent level of documentation for each column by table. Note: Datatypes are accurate for T-SQL. For other dialects (if I ever end up adding them), the datatype will be the nearest match.

### DimDate

<table>
  <tr>
    <th>Column Name</th>
    <th>Data Type</th>
    <th>Format Example</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>DateKey</td>
    <td>int</td>
    <td>20210101</td>
    <td>The table key.</td>
  </tr>
  <tr>
    <td>TheDate</td>
    <td>date</td>
    <td>Locale specific</td>
    <td>The unique calendar date for this row. All other columns are based off of this date.</td>
  </tr>
  <tr>
    <td>ISODateName</td>
    <td>varchar(10)</td>
    <td>2021-12-31</td>
    <td>The ISO-formatted date as a string. (Ex: 2021-12-31)</td>
  </tr>
  <tr>
    <td>AmericanDateName</td>
    <td>varchar(10)</td>
    <td>12/31/2021</td>
    <td>The American-formatted date as a string. (Ex: 12/31/2021)</td>
  </tr>
  <tr>
    <td>DayOfWeekName</td>
    <td>varchar(9)</td>
    <td>Sunday</td>
    <td>The full day name. (Ex: Sunday)</td>
  </tr>
  <tr>
    <td>DayOfWeekAbbrev</td>
    <td>varchar(3)</td>
    <td>Sun</td>
    <td>The abbreviated (three-character) day name. (Ex: Sun)</td>
  </tr>
  <tr>
    <td>MonthName</td>
    <td>varchar(9)</td>
    <td>December</td>
    <td>The full month name. (Ex: December)</td>
  </tr>
  <tr>
    <td>MonthAbbrev</td>
    <td>varchar(3)</td>
    <td>Dec</td>
    <td>The abbreviated (three-character) month name. (Ex: Dec)</td>
  </tr>
  <tr>
    <td>YearWeekName</td>
    <td>varchar(8)</td>
    <td>2021W51</td>
    <td>The year-week as a string. (Ex: 2021W51)</td>
  </tr>
  <tr>
    <td>YearMonthName</td>
    <td>varchar(7)</td>
    <td>2021-12</td>
    <td>The year-month as a string. (Ex: 2021-12)</td>
  </tr>
  <tr>
    <td>MonthYearName</td>
    <td>varchar(8)</td>
    <td>Dec 2021</td>
    <td>The abbreviated month name followed by the year. (Ex: Dec 2021)</td>
  </tr>
  <tr>
    <td>YearQuarterName</td>
    <td>varchar(6)</td>
    <td>2021Q4</td>
    <td>The year followed by the quarter. (Ex: 2021Q4)</td>
  </tr>
  <tr>
    <td>Year</td>
    <td>int</td>
    <td>2021</td>
    <td>The year as a number. (Ex: 2021)</td>
  </tr>
  <tr>
    <td>YearWeek</td>
    <td>int</td>
    <td>202151</td>
    <td>The year-week as a number. (Ex: 202152)</td>
  </tr>
  <tr>
    <td>ISOYearWeekCode</td>
    <td>int</td>
    <td>202151</td>
    <td>The year-week as a number, with the week calculated according to the ISO standard. (Ex: 202151)</td>
  </tr>
  <tr>
    <td>YearMonth</td>
    <td>int</td>
    <td>202101</td>
    <td>The year-month as a number. (Ex: 202112)</td>
  </tr>
  <tr>
    <td>YearQuarter</td>
    <td>int</td>
    <td>202101</td>
    <td>The year-quarter as a number. (Ex: 202104)</td>
  </tr>
  <tr>
    <td>DayOfWeekStartingMonday</td>
    <td>int</td>
    <td>1</td>
    <td>The same as DayOfWeek, but with Monday=1.</td>
  </tr>
  <tr>
    <td>DayOfWeek</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical day of the week. Sunday is 1.</td>
  </tr>
  <tr>
    <td>DayOfMonth</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical day of the month.</td>
  </tr>
  <tr>
    <td>DayOfQuarter</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical day of the quarter.</td>
  </tr>
  <tr>
    <td>DayOfYear</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical day of the year.</td>
  </tr>
  <tr>
    <td>WeekOfQuarter</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical week of the quarter. Starts at 1 and counts up. Partial weeks do count.</td>
  </tr>
  <tr>
    <td>WeekOfYear</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical week of the year.</td>
  </tr>
  <tr>
    <td>ISOWeekOfYear</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical week of the year, calculated according to the ISO standard.</td>
  </tr>
  <tr>
    <td>Month</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical month. (Ex. Dec = 12)</td>
  </tr>
  <tr>
    <td>MonthOfQuarter</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical month of the quarter. For obvious reasons, 1-3.</td>
  </tr>
  <tr>
    <td>Quarter</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical quarter.</td>
  </tr>
  <tr>
    <td>DaysInMonth</td>
    <td>int</td>
    <td>31</td>
    <td>The number of days in the month.</td>
  </tr>
  <tr>
    <td>DaysInQuarter</td>
    <td>int</td>
    <td>62</td>
    <td>The number of days in the quarter.</td>
  </tr>
  <tr>
    <td>DaysInYear</td>
    <td>int</td>
    <td>365</td>
    <td>The number of days in the year.</td>
  </tr>
  <tr>
    <td>DayOffsetFromToday</td>
    <td>int</td>
    <td>-123</td>
    <td>The number of days the day on this row is offset from the current date. For example, yesterday is -1, and tomorrow is 1.</td>
  </tr>
  <tr>
    <td>MonthOffsetFromToday</td>
    <td>int</td>
    <td>-12</td>
    <td>The number of months the day on this row is offset from the current date. For example, last month is -1, and next month is 1.</td>
  </tr>
  <tr>
    <td>QuarterOffsetFromToday</td>
    <td>int</td>
    <td>-12</td>
    <td>The number of quarters the day on this row is offset from the current quarter. For example, last quarter is -1, and next quarter is 1.</td>
  </tr>
  <tr>
    <td>YearOffsetFromToday</td>
    <td>int</td>
    <td>-1</td>
    <td>The number of years the day on this row is offset from the current date. For example, last year is -1, and next year is 1.</td>
  </tr>
  <tr>
    <td>TodayFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date is the current date.</td>
  </tr>
  <tr>
    <td>CurrentWeekStartingMondayFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>The same as CurrentWeekFlag, but with Monday=1.</td>
  </tr>
  <tr>
    <td>CurrentWeekFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the current week.</td>
  </tr>
  <tr>
    <td>PriorWeekFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the prior week.</td>
  </tr>
  <tr>
    <td>NextWeekFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the next week.</td>
  </tr>
  <tr>
    <td>CurrentMonthFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the current month.</td>
  </tr>
  <tr>
    <td>PriorMonthFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the prior month.</td>
  </tr>
  <tr>
    <td>NextMonthFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the next month.</td>
  </tr>
  <tr>
    <td>CurrentQuarterFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the current quarter.</td>
  </tr>
  <tr>
    <td>PriorQuarterFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the prior quarter.</td>
  </tr>
  <tr>
    <td>NextQuarterFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the next quarter.</td>
  </tr>
  <tr>
    <td>CurrentYearFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the current year.</td>
  </tr>
  <tr>
    <td>PriorYearFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the prior year.</td>
  </tr>
  <tr>
    <td>NextYearFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the next year.</td>
  </tr>
  <tr>
    <td>WeekdayFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date is a weekday (Monday-Friday).</td>
  </tr>
  <tr>
    <td>BusinessDayFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date is a business day. (In reality, this means it is both a weekday and not a holiday.)</td>
  </tr>
  <tr>
    <td>CompanyHolidayFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date is a Company holiday. See CompanyHolidayName for the holiday name.</td>
  </tr>
  <tr>
    <td>USPublicHolidayFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date is a US public holiday. See USPublicHolidayName for the holiday name.</td>
  </tr>
  <tr>
    <td>FirstDayOfMonthFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the first day of the month.</td>
  </tr>
  <tr>
    <td>LastDayOfMonthFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the last day of the month.</td>
  </tr>
  <tr>
    <td>FirstDayOfQuarterFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the first day of the quarter.</td>
  </tr>
  <tr>
    <td>LastDayOfQuarterFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the last day of the quarter.</td>
  </tr>
  <tr>
    <td>FirstDayOfYearFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the first day of the year.</td>
  </tr>
  <tr>
    <td>LastDayOfYearFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the last day of the year.</td>
  </tr>
  <tr>
    <td>FractionOfWeek</td>
    <td>decimal(5,4)</td>
    <td>0.1429</td>
    <td>The decimal fraction of the week that has passed as of this row's date.</td>
  </tr>
  <tr>
    <td>FractionOfMonth</td>
    <td>decimal(5,4)</td>
    <td>0.323</td>
    <td>The decimal fraction of the month that has passed as of this row's date.</td>
  </tr>
  <tr>
    <td>FractionOfQuarter</td>
    <td>decimal(5,4)</td>
    <td>0.0110</td>
    <td>The decimal fraction of the quarter that has passed as of this row's date.</td>
  </tr>
  <tr>
    <td>FractionOfYear</td>
    <td>decimal(5,4)</td>
    <td>0.0027</td>
    <td>The decimal fraction of the year that has passed as of this row's date.</td>
  </tr>
  <tr>
    <td>PriorDay</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date one day before this row's date.</td>
  </tr>
  <tr>
    <td>NextDay</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date one day after this row's date.</td>
  </tr>
  <tr>
    <td>SameDayPriorWeek</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date one week before this row's date.</td>
  </tr>
  <tr>
    <td>SameDayPriorMonth</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date one month before this row's date. If this row's date falls outside of the range of last month's date, this will be the greatest date in the last month. For example, the row for March 31st would show a value of February 28th in non-leap years, and it would show February 29th in leap years.</td>
  </tr>
  <tr>
    <td>SameDayPriorQuarter</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date one quarter before this row's date. Behaves similarly to SameDayPriorMonth for overflow dates.</td>
  </tr>
  <tr>
    <td>SameDayPriorYear</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date one year before this row's date. Behaves similarly to SameDayPriorMonth for overflow dates (which could only occur on the 366th day of a leap year).</td>
  </tr>
  <tr>
    <td>SameDayNextWeek</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date one week after this row's date.</td>
  </tr>
  <tr>
    <td>SameDayNextMonth</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date one month after this row's date. If this row's date falls outside of the range of next month's date, this will be the greatest date in the next month. For example, the row for January 31st would show a value of February 28th in non-leap years, and it would show February 29th in leap years.</td>
  </tr>
  <tr>
    <td>SameDayNextQuarter</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date one quarter after this row's date. Behaves similarly to SameDayNextMonth for overflow dates.</td>
  </tr>
  <tr>
    <td>SameDayNextYear</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date one year after this row's date. Behaves similarly to SameDayNextMonth for overflow dates (which could only occur on the 366th day of a leap year).</td>
  </tr>
  <tr>
    <td>CurrentWeekStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's week starts (always a Sunday).</td>
  </tr>
  <tr>
    <td>CurrentWeekEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's week ends (always a Saturday).</td>
  </tr>
  <tr>
    <td>CurrentMonthStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's month starts.</td>
  </tr>
  <tr>
    <td>CurrentMonthEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's month ends.</td>
  </tr>
  <tr>
    <td>CurrentQuarterStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's quarter starts.</td>
  </tr>
  <tr>
    <td>CurrentQuarterEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's quarter ends.</td>
  </tr>
  <tr>
    <td>CurrentYearStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's year starts.</td>
  </tr>
  <tr>
    <td>CurrentYearEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's year ends.</td>
  </tr>
  <tr>
    <td>PriorWeekStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date week prior to this row's week starts.</td>
  </tr>
  <tr>
    <td>PriorWeekEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date week prior to this row's week ends.</td>
  </tr>
  <tr>
    <td>PriorMonthStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date month prior to this row's month starts.</td>
  </tr>
  <tr>
    <td>PriorMonthEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date month prior to this row's month ends.</td>
  </tr>
  <tr>
    <td>PriorQuarterStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date quarter prior to this row's quarter starts.</td>
  </tr>
  <tr>
    <td>PriorQuarterEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date quarter prior to this row's quarter ends.</td>
  </tr>
  <tr>
    <td>PriorYearStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date year prior to this row's year starts.</td>
  </tr>
  <tr>
    <td>PriorYearEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date year prior to this row's year ends.</td>
  </tr>
  <tr>
    <td>NextWeekStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date week after this row's week starts.</td>
  </tr>
  <tr>
    <td>NextWeekEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date week after this row's week ends.</td>
  </tr>
  <tr>
    <td>NextMonthStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date month after this row's month starts.</td>
  </tr>
  <tr>
    <td>NextMonthEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date month after this row's month ends.</td>
  </tr>
  <tr>
    <td>NextQuarterStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date quarter after this row's quarter starts.</td>
  </tr>
  <tr>
    <td>NextQuarterEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date quarter after this row's quarter ends.</td>
  </tr>
  <tr>
    <td>NextYearStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The year quarter after this row's year starts.</td>
  </tr>
  <tr>
    <td>NextYearEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The year quarter after this row's year ends.</td>
  </tr>
  <tr>
    <td>WeeklyBurnupStartingMonday</td>
    <td>bit</td>
    <td>1</td>
    <td>The same as WeeklyBurnup, but with Monday=1.</td>
  </tr>
  <tr>
    <td>WeeklyBurnup</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates the day of the week of this row's date is equal to or greater to the day of the week today. For example, if today is a Monday and the day on this row is a Tuesday, this would be FALSE. If the day on this row were a Monday or a Sunday, it would be TRUE. Useful for creating weekly burnup charts.</td>
  </tr>
  <tr>
    <td>MonthlyBurnup</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates the day of the month of this row's date is equal to or greater to the day of the month today. For example, if today is the 12th and the day of the month for this row is the 15th, this would be FALSE. If the day of the month on this row were the 12th or lower, it would be TRUE. Useful for creating monthly burnup charts.</td>
  </tr>
  <tr>
    <td>QuarterlyBurnup</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates the day of the quarter of this row's date is equal to or greater to the day of the quarter today. For example, if today is the 42nd day of the quarter and the day of the quarter for this row is the 60th, this would be FALSE. If the day of the quarter on this row were the 42nd or lower, it would be TRUE. Useful for creating quarterly burnup charts.</td>
  </tr>
  <tr>
    <td>YearlyBurnup</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates the day of the year of this row's date is equal to or greater to the day of the year today. For example, if today is the 42nd day of the year and the day of the year for this row is the 60th, this would be FALSE. If the day of the year on this row were the 42nd or lower, it would be TRUE. Useful for creating yearly burnup charts.</td>
  </tr>
  <tr>
    <td>FiscalMonthName</td>
    <td>varchar(9)</td>
    <td>December</td>
    <td>The full fiscal month name. (Ex: December)</td>
  </tr>
  <tr>
    <td>FiscalMonthAbbrev</td>
    <td>varchar(3)</td>
    <td>Dec</td>
    <td>The abbreviated (three-character) fiscal month name. (Ex: Dec)</td>
  </tr>
  <tr>
    <td>FiscalYearWeekName</td>
    <td>varchar(8)</td>
    <td>2021W51</td>
    <td>The fiscal year-week as a string. (Ex: 2021W51)</td>
  </tr>
  <tr>
    <td>FiscalYearMonthName</td>
    <td>varchar(7)</td>
    <td>2021-12</td>
    <td>The fiscal year-month as a string. (Ex: 2021-12)</td>
  </tr>
  <tr>
    <td>FiscalMonthYearName</td>
    <td>varchar(8)</td>
    <td>Dec 2021</td>
    <td>The abbreviated fiscal month name followed by the fiscal year. (Ex: Dec 2021)</td>
  </tr>
  <tr>
    <td>FiscalYearQuarterName</td>
    <td>varchar(6)</td>
    <td>2021Q4</td>
    <td>The fiscal year followed by the fiscal quarter. (Ex: 2021Q4)</td>
  </tr>
  <tr>
    <td>FiscalYear</td>
    <td>int</td>
    <td>2021</td>
    <td>The fiscal year as a number. (Ex: 2021)</td>
  </tr>
  <tr>
    <td>FiscalYearWeek</td>
    <td>int</td>
    <td>202152</td>
    <td>The fiscal year-week as a number. (Ex: 202152)</td>
  </tr>
  <tr>
    <td>FiscalYearMonth</td>
    <td>int</td>
    <td>202101</td>
    <td>The fiscal year-month as a number. (Ex: 202112)</td>
  </tr>
  <tr>
    <td>FiscalYearQuarter</td>
    <td>int</td>
    <td>202101</td>
    <td>The fiscal year-quarter as a number. (Ex: 202104)</td>
  </tr>
  <tr>
    <td>FiscalDayOfMonth</td>
    <td>int</td>
    <td>31</td>
    <td>The numerical day of the fiscal month.</td>
  </tr>
  <tr>
    <td>FiscalDayOfQuarter</td>
    <td>int</td>
    <td>31</td>
    <td>The numerical day of the fiscal quarter.</td>
  </tr>
  <tr>
    <td>FiscalDayOfYear</td>
    <td>int</td>
    <td>31</td>
    <td>The numerical day of the fiscal year.</td>
  </tr>
  <tr>
    <td>FiscalWeekOfQuarter</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical week of the fiscal quarter. Starts at 1 and counts up. Partial weeks do count.</td>
  </tr>
  <tr>
    <td>FiscalWeekOfYear</td>
    <td>int</td>
    <td>52</td>
    <td>The numerical week of the fiscal year.</td>
  </tr>
  <tr>
    <td>FiscalMonth</td>
    <td>int</td>
    <td>10</td>
    <td>The numerical fiscal month. (Ex. Dec = 12)</td>
  </tr>
  <tr>
    <td>FiscalMonthOfQuarter</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical fiscal month of the fiscal quarter. For obvious reasons, 1-3.</td>
  </tr>
  <tr>
    <td>FiscalQuarter</td>
    <td>int</td>
    <td>1</td>
    <td>The numerical fiscal quarter.</td>
  </tr>
  <tr>
    <td>FiscalDaysInMonth</td>
    <td>int</td>
    <td>31</td>
    <td>The number of days in the fiscal month.</td>
  </tr>
  <tr>
    <td>FiscalDaysInQuarter</td>
    <td>int</td>
    <td>62</td>
    <td>The number of days in the fiscal quarter.</td>
  </tr>
  <tr>
    <td>FiscalDaysInYear</td>
    <td>int</td>
    <td>365</td>
    <td>The number of days in the fiscal year.</td>
  </tr>
  <tr>
    <td>FiscalCurrentMonthFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the current fiscal month.</td>
  </tr>
  <tr>
    <td>FiscalPriorMonthFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the prior fiscal month.</td>
  </tr>
  <tr>
    <td>FiscalNextMonthFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the next fiscal month.</td>
  </tr>
  <tr>
    <td>FiscalCurrentQuarterFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the current fiscal quarter.</td>
  </tr>
  <tr>
    <td>FiscalPriorQuarterFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the prior fiscal quarter.</td>
  </tr>
  <tr>
    <td>FiscalNextQuarterFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the next fiscal quarter.</td>
  </tr>
  <tr>
    <td>FiscalCurrentYearFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the current fiscal year.</td>
  </tr>
  <tr>
    <td>FiscalPriorYearFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the prior fiscal year.</td>
  </tr>
  <tr>
    <td>FiscalNextYearFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls within the next fiscal year.</td>
  </tr>
  <tr>
    <td>FiscalFirstDayOfMonthFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the first day of the fiscal month.</td>
  </tr>
  <tr>
    <td>FiscalLastDayOfMonthFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the last day of the fiscal month.</td>
  </tr>
  <tr>
    <td>FiscalFirstDayOfQuarterFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the first day of the fiscal quarter.</td>
  </tr>
  <tr>
    <td>FiscalLastDayOfQuarterFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the last day of the fiscal quarter.</td>
  </tr>
  <tr>
    <td>FiscalFirstDayOfYearFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the first day of the fiscal year.</td>
  </tr>
  <tr>
    <td>FiscalLastDayOfYearFlag</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates this row's date falls on the last day of the fiscal year.</td>
  </tr>
  <tr>
    <td>FiscalFractionOfMonth</td>
    <td>decimal(5,4)</td>
    <td>0.2258</td>
    <td>The decimal fraction of the fiscal month that has passed as of this row's date.</td>
  </tr>
  <tr>
    <td>FiscalFractionOfQuarter</td>
    <td>decimal(5,4)</td>
    <td>0.0769</td>
    <td>The decimal fraction of the fiscal quarter that has passed as of this row's date.</td>
  </tr>
  <tr>
    <td>FiscalFractionOfYear</td>
    <td>decimal(5,4)</td>
    <td>0.0191</td>
    <td>The decimal fraction of the fiscal year that has passed as of this row's date.</td>
  </tr>
  <tr>
    <td>FiscalCurrentMonthStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's fiscal month starts.</td>
  </tr>
  <tr>
    <td>FiscalCurrentMonthEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's fiscal month ends.</td>
  </tr>
  <tr>
    <td>FiscalCurrentQuarterStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's fiscal quarter starts.</td>
  </tr>
  <tr>
    <td>FiscalCurrentQuarterEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's fiscal quarter ends.</td>
  </tr>
  <tr>
    <td>FiscalCurrentYearStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's fiscal year starts.</td>
  </tr>
  <tr>
    <td>FiscalCurrentYearEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date this row's fiscal year ends.</td>
  </tr>
  <tr>
    <td>FiscalPriorMonthStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date fiscal month prior to this row's fiscal month starts.</td>
  </tr>
  <tr>
    <td>FiscalPriorMonthEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date fiscal month prior to this row's fiscal month ends.</td>
  </tr>
  <tr>
    <td>FiscalPriorQuarterStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date fiscal quarter prior to this row's fiscal quarter starts.</td>
  </tr>
  <tr>
    <td>FiscalPriorQuarterEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date fiscal quarter prior to this row's fiscal quarter ends.</td>
  </tr>
  <tr>
    <td>FiscalPriorYearStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date fiscal year prior to this row's fiscal year starts.</td>
  </tr>
  <tr>
    <td>FiscalPriorYearEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date fiscal year prior to this row's fiscal year ends.</td>
  </tr>
  <tr>
    <td>FiscalNextMonthStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date fiscal month after this row's fiscal month starts.</td>
  </tr>
  <tr>
    <td>FiscalNextMonthEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date fiscal month after this row's fiscal month ends.</td>
  </tr>
  <tr>
    <td>FiscalNextQuarterStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date fiscal quarter after this row's fiscal quarter starts.</td>
  </tr>
  <tr>
    <td>FiscalNextQuarterEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The date fiscal quarter after this row's fiscal quarter ends.</td>
  </tr>
  <tr>
    <td>FiscalNextYearStart</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The fiscal year fiscal quarter after this row's fiscal year starts.</td>
  </tr>
  <tr>
    <td>FiscalNextYearEnd</td>
    <td>date</td>
    <td>Locale specific.</td>
    <td>The fiscal year fiscal quarter after this row's fiscal year ends.</td>
  </tr>
  <tr>
    <td>FiscalMonthlyBurnup</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates the day of the fiscal month of this row's date is equal to or greater to the day of the fiscal month today. For example, if today is the 12th of the fiscal month and the day of the fiscal month for this row is the 15th, this would be FALSE. If the day of the fiscal month on this row were the 12th or lower, it would be TRUE. Useful for creating fiscal monthly burnup charts.</td>
  </tr>
  <tr>
    <td>FiscalQuarterlyBurnup</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates the day of the fiscal quarter of this row's date is equal to or greater to the day of the fiscal quarter today. For example, if today is the 42nd day of the fiscal quarter and the day of the fiscal quarter for this row is the 60th, this would be FALSE. If the day of the fiscal quarter on this row were the 42nd or lower, it would be TRUE. Useful for creating fiscal quarterly burnup charts.</td>
  </tr>
  <tr>
    <td>FiscalYearlyBurnup</td>
    <td>bit</td>
    <td>1</td>
    <td>Indicates the day of the fiscal year of this row's date is equal to or greater to the day of the fiscal year today. For example, if today is the 42nd day of the fiscal year and the day of the fiscal year for this row is the 60th, this would be FALSE. If the day of the fiscal year on this row were the 42nd or lower, it would be TRUE. Useful for creating fiscal yearly burnup charts.</td>
  </tr>
  <tr>
    <td>CompanyHolidayName</td>
    <td>varchar(255)</td>
    <td>Christmas</td>
    <td>The name of the Company holiday, if applicable.</td>
  </tr>
  <tr>
    <td>USPublicHolidayName</td>
    <td>varchar(255)</td>
    <td>Christmas</td>
    <td>The name of the US public holiday, if applicable.</td>
  </tr>

</table>
