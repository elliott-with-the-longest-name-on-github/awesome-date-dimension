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

A decent level of documentation for each column by table.

### DimDate

<table>
  <tr>
    <th>Column Name</th>
    <th>Data Type</th>
    <th>Format Example</th>
    <th>Description</th>
  </tr>
</table>
