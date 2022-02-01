from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from awesome_date_dimension.config import Column, Config, DimDateColumns, DimFiscalMonthColumns, DimCalendarMonthColumns
from awesome_date_dimension.generators._tsql_templates.dim_date_setup_template import dim_date_setup_template


@dataclass
class TSQLColumn(Column):
    sql_datatype: str
    nullable: bool
    constraint: str = None


@dataclass
class TSQLDimDateColumns(DimDateColumns):
    def __post_init__(self):
        # Extend column definitions with required SQL info
        self.self.date_key = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.date_key))
        self.the_date = TSQLColumn(sql_datatype='date',
                                   nullable=False, **asdict(self.the_date))
        self.iso_date_name = TSQLColumn(
            sql_datatype='varchar(10)', nullable=False, **asdict(self.iso_date_name))
        self.american_date_name = TSQLColumn(
            sql_datatype='varchar(10)', nullable=False, **asdict(self.american_date_name))
        self.day_of_week_name = TSQLColumn(
            sql_datatype='varchar(9)', nullable=False, **asdict(self.day_of_week_name))
        self.day_of_week_abbrev = TSQLColumn(
            sql_datatype='varchar(3)', nullable=False, **asdict(self.day_of_week_abbrev))
        self.month_name = TSQLColumn(sql_datatype='varchar(9)',
                                     nullable=False, **asdict(self.month_name))
        self.month_abbrev = TSQLColumn(
            sql_datatype='varchar(3)', nullable=False, **asdict(self.month_abbrev))
        self.year_week_name = TSQLColumn(
            sql_datatype='varchar(8)', nullable=False, **asdict(self.year_week_name))
        self.year_month_name = TSQLColumn(
            sql_datatype='varchar(7)', nullable=False, **asdict(self.year_month_name))
        self.month_year_name = TSQLColumn(
            sql_datatype='varchar(8)', nullable=False, **asdict(self.month_year_name))
        self.year_quarter_name = TSQLColumn(
            sql_datatype='varchar(6)', nullable=False, **asdict(self.year_quarter_name))
        self.year = TSQLColumn(sql_datatype='int', nullable=False,
                               **asdict(self.year))
        self.year_week = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.year_week))
        self.iso_year_week_code = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.iso_year_week_code))
        self.year_month = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.year_month))
        self.year_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.year_quarter))
        self.day_of_week_starting_monday = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.day_of_week_starting_monday))
        self.day_of_week = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.day_of_week))
        self.day_of_month = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.day_of_month))
        self.day_of_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.day_of_quarter))
        self.day_of_year = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.day_of_year))
        self.week_of_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.week_of_quarter))
        self.week_of_year = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.week_of_year))
        self.iso_week_of_year = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.iso_week_of_year))
        self.month = TSQLColumn(sql_datatype='int',
                                nullable=False, **asdict(self.month))
        self.month_of_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.month_of_quarter))
        self.quarter = TSQLColumn(sql_datatype='int',
                                  nullable=False, **asdict(self.quarter))
        self.days_in_month = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.days_in_month))
        self.days_in_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.days_in_quarter))
        self.days_in_year = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.days_in_year))
        self.day_offset_from_today = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.day_offset_from_today))
        self.month_offset_from_today = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.month_offset_from_today))
        self.quarter_offset_from_today = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.quarter_offset_from_today))
        self.year_offset_from_today = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.year_offset_from_today))
        self.today_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.today_flag))
        self.current_week_starting_monday_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.current_week_starting_monday_flag))
        self.current_week_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.current_week_flag))
        self.prior_week_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.prior_week_flag))
        self.next_week_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.next_week_flag))
        self.current_month_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.current_month_flag))
        self.prior_month_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.prior_month_flag))
        self.next_month_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.next_month_flag))
        self.current_quarter_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.current_quarter_flag))
        self.prior_quarter_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.prior_quarter_flag))
        self.next_quarter_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.next_quarter_flag))
        self.current_year_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.current_year_flag))
        self.prior_year_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.prior_year_flag))
        self.next_year_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.next_year_flag))
        self.weekday_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.weekday_flag))
        self.business_day_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.business_day_flag))
        self.first_day_of_month_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.first_day_of_month_flag))
        self.last_day_of_month_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.last_day_of_month_flag))
        self.first_day_of_quarter_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.first_day_of_quarter_flag))
        self.last_day_of_quarter_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.last_day_of_quarter_flag))
        self.first_day_of_year_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.first_day_of_year_flag))
        self.last_day_of_year_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.last_day_of_year_flag))
        self.fraction_of_week = TSQLColumn(
            sql_datatype='decimal(5,4)', nullable=False, constraint=f'chk_DimDate_{self.fraction_of_week.name} CHECK ({self.fraction_of_week.name} BETWEEN 0 AND 1)', **asdict(self.fraction_of_week))
        self.fraction_of_month = TSQLColumn(
            sql_datatype='decimal(5,4)', nullable=False, constraint=f'chk_DimDate_{self.fraction_of_month.name} CHECK ({self.fraction_of_month.name} BETWEEN 0 AND 1)', **asdict(self.fraction_of_month))
        self.fraction_of_quarter = TSQLColumn(
            sql_datatype='decimal(5,4)', nullable=False, constraint=f'chk_DimDate_{self.fraction_of_quarter.name} CHECK ({self.fraction_of_quarter.name} BETWEEN 0 AND 1)', **asdict(self.fraction_of_quarter))
        self.fraction_of_year = TSQLColumn(
            sql_datatype='decimal(5,4)', nullable=False, constraint=f'chk_DimDate_{self.fraction_of_year.name} CHECK ({self.fraction_of_year.name} BETWEEN 0 AND 1)', **asdict(self.fraction_of_year))
        self.prior_day = TSQLColumn(sql_datatype='date',
                                    nullable=False, **asdict(self.prior_day))
        self.next_day = TSQLColumn(sql_datatype='date',
                                   nullable=False, **asdict(self.next_day))
        self.same_day_prior_week = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.same_day_prior_week))
        self.same_day_prior_month = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.same_day_prior_month))
        self.same_day_prior_quarter = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.same_day_prior_quarter))
        self.same_day_prior_year = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.same_day_prior_year))
        self.same_day_next_week = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.same_day_next_week))
        self.same_day_next_month = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.same_day_next_month))
        self.same_day_next_quarter = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.same_day_next_quarter))
        self.same_day_next_year = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.same_day_next_year))
        self.current_week_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.current_week_start))
        self.current_week_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.current_week_end))
        self.current_month_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.current_month_start))
        self.current_month_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.current_month_end))
        self.current_quarter_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.current_quarter_start))
        self.current_quarter_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.current_quarter_end))
        self.current_year_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.current_year_start))
        self.current_year_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.current_year_end))
        self.prior_week_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.prior_week_start))
        self.prior_week_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.prior_week_end))
        self.prior_month_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.prior_month_start))
        self.prior_month_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.prior_month_end))
        self.prior_quarter_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.prior_quarter_start))
        self.prior_quarter_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.prior_quarter_end))
        self.prior_year_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.prior_year_start))
        self.prior_year_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.prior_year_end))
        self.next_week_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.next_week_start))
        self.next_week_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.next_week_end))
        self.next_month_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.next_month_start))
        self.next_month_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.next_month_end))
        self.next_quarter_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.next_quarter_start))
        self.next_quarter_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.next_quarter_end))
        self.next_year_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.next_year_start))
        self.next_year_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.next_year_end))
        self.weekly_burnup_starting_monday = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.weekly_burnup_starting_monday))
        self.weekly_burnup = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.weekly_burnup))
        self.monthly_burnup = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.monthly_burnup))
        self.quarterly_burnup = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.quarterly_burnup))
        self.yearly_burnup = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.yearly_burnup))
        self.fiscal_month_name = TSQLColumn(
            sql_datatype='varchar(9)', nullable=False, **asdict(self.fiscal_month_name))
        self.fiscal_month_abbrev = TSQLColumn(
            sql_datatype='varchar(3)', nullable=False, **asdict(self.fiscal_month_abbrev))
        self.fiscal_year_name = TSQLColumn(
            sql_datatype='varchar(8)', nullable=False, **asdict(self.fiscal_year_name))
        self.fiscal_year_month_name = TSQLColumn(
            sql_datatype='varchar(7)', nullable=False, **asdict(self.fiscal_year_month_name))
        self.fiscal_month_year_name = TSQLColumn(
            sql_datatype='varchar(8)', nullable=False, **asdict(self.fiscal_month_year_name))
        self.fiscal_year_quarter_name = TSQLColumn(
            sql_datatype='varchar(6)', nullable=False, **asdict(self.fiscal_year_quarter_name))
        self.fiscal_year = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_year))
        self.fiscal_year_week = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_year_week))
        self.fiscal_year_month = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_year_month))
        self.fiscal_year_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_year_quarter))
        self.fiscal_day_of_month = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_day_of_month))
        self.fiscal_day_of_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_day_of_quarter))
        self.fiscal_day_of_year = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_day_of_year))
        self.fiscal_week_of_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_week_of_quarter))
        self.fiscal_week_of_year = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_week_of_year))
        self.fiscal_month = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.fiscal_month))
        self.fiscal_month_of_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_month_of_quarter))
        self.fiscal_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_quarter))
        self.fiscal_days_in_month = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_days_in_month))
        self.fiscal_days_in_quarter = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_days_in_quarter))
        self.fiscal_days_in_year = TSQLColumn(
            sql_datatype='int', nullable=False, **asdict(self.fiscal_days_in_year))
        self.fiscal_current_month_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_current_month_flag))
        self.fiscal_prior_month_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_prior_month_flag))
        self.fiscal_next_month_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_next_month_flag))
        self.fiscal_current_quarter_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_current_quarter_flag))
        self.fiscal_prior_quarter_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_prior_quarter_flag))
        self.fiscal_next_quarter_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_next_quarter_flag))
        self.fiscal_current_year_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_current_year_flag))
        self.fiscal_prior_year_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_prior_year_flag))
        self.fiscal_next_year_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_next_year_flag))
        self.fiscal_first_day_of_month_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_first_day_of_month_flag))
        self.fiscal_last_day_of_month_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_last_day_of_month_flag))
        self.fiscal_first_day_of_quarter_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_first_day_of_quarter_flag))
        self.fiscal_last_day_of_quarter_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_last_day_of_quarter_flag))
        self.fiscal_first_day_of_year_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_first_day_of_year_flag))
        self.fiscal_last_day_of_year_flag = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_last_day_of_year_flag))
        self.fiscal_fraction_of_month = TSQLColumn(
            sql_datatype='decimal(5,4)', nullable=False, constraint=f'chk_DimDate_{self.fiscal_fraction_of_month.name} CHECK ({self.fiscal_fraction_of_month.name} BETWEEN 0 AND 1)', **asdict(self.fiscal_fraction_of_month))
        self.fiscal_fraction_of_quarter = TSQLColumn(
            sql_datatype='decimal(5,4)', nullable=False, constraint=f'chk_DimDate_{self.fiscal_fraction_of_quarter.name} CHECK ({self.fiscal_fraction_of_quarter.name} BETWEEN 0 AND 1)', **asdict(self.fiscal_fraction_of_quarter))
        self.fiscal_fraction_of_year = TSQLColumn(
            sql_datatype='decimal(5,4)', nullable=False, constraint=f'chk_DimDate_{self.fiscal_fraction_of_year.name} CHECK ({self.fiscal_fraction_of_year.name} BETWEEN 0 AND 1)', **asdict(self.fiscal_fraction_of_year))
        self.fiscal_current_month_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_current_month_start))
        self.fiscal_current_month_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_current_month_end))
        self.fiscal_current_quarter_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_current_quarter_start))
        self.fiscal_current_quarter_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_current_quarter_end))
        self.fiscal_current_year_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_current_year_start))
        self.fiscal_current_year_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_current_year_end))
        self.fiscal_prior_month_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_prior_month_start))
        self.fiscal_prior_month_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_prior_month_end))
        self.fiscal_prior_quarter_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_prior_quarter_start))
        self.fiscal_prior_quarter_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_prior_quarter_end))
        self.fiscal_prior_year_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_prior_year_start))
        self.fiscal_prior_year_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_prior_year_end))
        self.fiscal_next_month_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_next_month_start))
        self.fiscal_next_month_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_next_month_end))
        self.fiscal_next_quarter_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_next_quarter_start))
        self.fiscal_next_quarter_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_next_quarter_end))
        self.fiscal_next_year_start = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_next_year_start))
        self.fiscal_next_year_end = TSQLColumn(
            sql_datatype='date', nullable=False, **asdict(self.fiscal_next_year_end))
        self.fiscal_monthly_burnup = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_monthly_burnup))
        self.fiscal_quarterly_burnup = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_quarterly_burnup))
        self.fiscal_yearly_burnup = TSQLColumn(
            sql_datatype='bit', nullable=False, **asdict(self.fiscal_yearly_burnup))


@dataclass
class TSQLDimFiscalMonthColumns(DimFiscalMonthColumns):
    def __post_init__(self):
        # Extend column definitions with required SQL info
        self.month_start_key = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_key))
        self.month_end_key = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_key))
        self.month_start_date = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_date))
        self.month_end_date = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_date))
        self.month_start_iso_date_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_iso_date_name))
        self.month_end_iso_date_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_iso_date_name))
        self.month_start_american_date_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_american_date_name))
        self.month_end_american_date_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_american_date_name))
        self.month_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_name))
        self.month_abbrev = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_abbrev))
        self.month_start_year_week_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_year_week_name))
        self.month_end_year_week_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_year_week_name))
        self.year_month_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.year_month_name))
        self.month_year_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_year_name))
        self.year_quarter_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.year_quarter_name))
        self.year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.year))
        self.month_start_year_week = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_year_week))
        self.month_end_year_week = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_year_week))
        self.year_month = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.year_month))
        self.year_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.year_quarter))
        self.month_start_day_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_day_of_quarter))
        self.month_end_day_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_day_of_quarter))
        self.month_start_day_of_year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_day_of_year))
        self.month_end_day_of_year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_day_of_year))
        self.month_start_week_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_week_of_quarter))
        self.month_end_week_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_week_of_quarter))
        self.month_start_week_of_year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_week_of_year))
        self.month_end_week_of_year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_week_of_year))
        self.month_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_of_quarter))
        self.quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.quarter))
        self.days_in_month = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.days_in_month))
        self.days_in_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.days_in_quarter))
        self.days_in_year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.days_in_year))
        self.current_month_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.current_month_flag))
        self.prior_month_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.prior_month_flag))
        self.next_month_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.next_month_flag))
        self.current_quarter_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.current_quarter_flag))
        self.prior_quarter_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.prior_quarter_flag))
        self.next_quarter_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.next_quarter_flag))
        self.current_year_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.current_year_flag))
        self.prior_year_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.prior_year_flag))
        self.next_year_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.next_year_flag))
        self.first_day_of_month_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.first_day_of_month_flag))
        self.last_day_of_month_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.last_day_of_month_flag))
        self.first_day_of_quarter_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.first_day_of_quarter_flag))
        self.last_day_of_quarter_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.last_day_of_quarter_flag))
        self.first_day_of_year_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.first_day_of_year_flag))
        self.last_day_of_year_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.last_day_of_year_flag))
        self.month_start_fraction_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, constraint=f'chk_DimFiscalMonth_{self.month_start_fraction_of_quarter.name} CHECK ({self.month_start_fraction_of_quarter.name} BETWEEN 0 AND 1)', **asdict(self.month_start_fraction_of_quarter))
        self.month_end_fraction_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, constraint=f'chk_DimFiscalMonth_{self.month_end_fraction_of_quarter.name} CHECK ({self.month_end_fraction_of_quarter.name} BETWEEN 0 AND 1)', **asdict(self.month_end_fraction_of_quarter))
        self.month_start_fraction_of_year = TSQLColumn(
            sql_datatype='', nullable=False, constraint=f'chk_DimFiscalMonth_{self.month_start_fraction_of_year.name} CHECK ({self.month_start_fraction_of_year.name} BETWEEN 0 AND 1)', **asdict(self.month_start_fraction_of_year))
        self.month_end_fraction_of_year = TSQLColumn(
            sql_datatype='', nullable=False, constraint=f'chk_DimFiscalMonth_{self.month_end_fraction_of_year.name} CHECK ({self.month_end_fraction_of_year.name} BETWEEN 0 AND 1)', **asdict(self.month_end_fraction_of_year))
        self.month_start_current_quarter_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_current_quarter_start))
        self.month_start_current_quarter_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_current_quarter_end))
        self.month_start_current_year_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_current_year_start))
        self.month_start_current_year_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_current_year_end))
        self.month_start_prior_month_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_month_start))
        self.month_start_prior_month_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_month_end))
        self.month_start_prior_quarter_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_quarter_start))
        self.month_start_prior_quarter_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_quarter_end))
        self.month_start_prior_year_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_year_start))
        self.month_start_prior_year_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_year_end))
        self.month_start_next_month_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_month_start))
        self.month_start_next_month_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_month_end))
        self.month_start_next_quarter_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_quarter_start))
        self.month_start_next_quarter_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_quarter_end))
        self.month_start_next_year_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_year_start))
        self.month_start_next_year_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_year_end))
        self.month_start_quarterly_burnup = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_quarterly_burnup))
        self.month_end_quarterly_burnup = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_quarterly_burnup))
        self.month_start_yearly_burnup = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_yearly_burnup))
        self.month_end_yearly_burnup = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_yearly_burnup))


@dataclass
class TSQLDimCalendarMonthColumns(DimCalendarMonthColumns):
    def __post_init__(self):
        # Extend column definitions with required SQL info
        self.month_start_key = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_key))
        self.month_end_key = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_key))
        self.month_start_date = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_date))
        self.month_end_date = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_date))
        self.month_start_iso_date_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_iso_date_name))
        self.month_end_iso_date_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_iso_date_name))
        self.month_start_american_date_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_american_date_name))
        self.month_end_american_date_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_american_date_name))
        self.month_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_name))
        self.month_abbrev = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_abbrev))
        self.month_start_year_week_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_year_week_name))
        self.month_end_year_week_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_year_week_name))
        self.year_month_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.year_month_name))
        self.month_year_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_year_name))
        self.year_quarter_name = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.year_quarter_name))
        self.year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.year))
        self.month_start_year_week = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_year_week))
        self.month_end_year_week = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_year_week))
        self.year_month = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.year_month))
        self.year_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.year_quarter))
        self.month_start_day_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_day_of_quarter))
        self.month_end_day_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_day_of_quarter))
        self.month_start_day_of_year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_day_of_year))
        self.month_end_day_of_year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_day_of_year))
        self.month_start_week_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_week_of_quarter))
        self.month_end_week_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_week_of_quarter))
        self.month_start_week_of_year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_week_of_year))
        self.month_end_week_of_year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_week_of_year))
        self.month_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_of_quarter))
        self.quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.quarter))
        self.days_in_month = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.days_in_month))
        self.days_in_quarter = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.days_in_quarter))
        self.days_in_year = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.days_in_year))
        self.current_month_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.current_month_flag))
        self.prior_month_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.prior_month_flag))
        self.next_month_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.next_month_flag))
        self.current_quarter_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.current_quarter_flag))
        self.prior_quarter_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.prior_quarter_flag))
        self.next_quarter_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.next_quarter_flag))
        self.current_year_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.current_year_flag))
        self.prior_year_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.prior_year_flag))
        self.next_year_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.next_year_flag))
        self.first_day_of_month_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.first_day_of_month_flag))
        self.last_day_of_month_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.last_day_of_month_flag))
        self.first_day_of_quarter_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.first_day_of_quarter_flag))
        self.last_day_of_quarter_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.last_day_of_quarter_flag))
        self.first_day_of_year_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.first_day_of_year_flag))
        self.last_day_of_year_flag = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.last_day_of_year_flag))
        self.month_start_fraction_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, constraint=f'chk_DimCalendarMonth_{self.month_start_fraction_of_quarter.name} CHECK ({self.month_start_fraction_of_quarter.name} BETWEEN 0 AND 1)', **asdict(self.month_start_fraction_of_quarter))
        self.month_end_fraction_of_quarter = TSQLColumn(
            sql_datatype='', nullable=False, constraint=f'chk_DimCalendarMonth_{self.month_end_fraction_of_quarter.name} CHECK ({self.month_end_fraction_of_quarter.name} BETWEEN 0 AND 1)', **asdict(self.month_end_fraction_of_quarter))
        self.month_start_fraction_of_year = TSQLColumn(
            sql_datatype='', nullable=False, constraint=f'chk_DimCalendarMonth_{self.month_start_fraction_of_year.name} CHECK ({self.month_start_fraction_of_year.name} BETWEEN 0 AND 1)', **asdict(self.month_start_fraction_of_year))
        self.month_end_fraction_of_year = TSQLColumn(
            sql_datatype='', nullable=False, constraint=f'chk_DimCalendarMonth_{self.month_end_fraction_of_year.name} CHECK ({self.month_end_fraction_of_year.name} BETWEEN 0 AND 1)', **asdict(self.month_end_fraction_of_year))
        self.month_start_current_quarter_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_current_quarter_start))
        self.month_start_current_quarter_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_current_quarter_end))
        self.month_start_current_year_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_current_year_start))
        self.month_start_current_year_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_current_year_end))
        self.month_start_prior_month_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_month_start))
        self.month_start_prior_month_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_month_end))
        self.month_start_prior_quarter_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_quarter_start))
        self.month_start_prior_quarter_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_quarter_end))
        self.month_start_prior_year_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_year_start))
        self.month_start_prior_year_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_prior_year_end))
        self.month_start_next_month_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_month_start))
        self.month_start_next_month_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_month_end))
        self.month_start_next_quarter_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_quarter_start))
        self.month_start_next_quarter_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_quarter_end))
        self.month_start_next_year_start = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_year_start))
        self.month_start_next_year_end = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_next_year_end))
        self.month_start_quarterly_burnup = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_quarterly_burnup))
        self.month_end_quarterly_burnup = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_quarterly_burnup))
        self.month_start_yearly_burnup = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_start_yearly_burnup))
        self.month_end_yearly_burnup = TSQLColumn(
            sql_datatype='', nullable=False, **asdict(self.month_end_yearly_burnup))


class TSQLGenerator():
    def __init__(self, config: Config):
        self._config = config

    def generate_scripts(self) -> None:
        folder_no = 0
        folder_no = self._generate_setup_scripts(folder_no)
        folder_no = self._generate_build_scripts(folder_no)
        folder_no = self._generate_refresh_procs(folder_no)
        folder_no = self._generate_table_constraints(folder_no)

    def _generate_setup_scripts(self, folder_no: int) -> int:
        file_no = 0
        base_path = self._generate_folder_path(folder_no, 'initial-build')
        file_no = self._generate_dim_date_setup_scripts(file_no, base_path)
        file_no = self._generate_dim_fiscal_month_setup_scripts(
            file_no, base_path)
        file_no = self._generate_dim_calendar_month_setup_scripts(
            file_no, base_path)
        if self._config.holiday_config.generate_holidays:
            file_no = self._generate_holiday_setup_scripts(file_no, base_path)
        return folder_no + 1

    def _generate_dim_date_setup_scripts(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_dim_fiscal_month_setup_scripts(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_dim_calendar_month_setup_scripts(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_holiday_setup_scripts(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_build_scripts(self, folder_no: int) -> int:
        file_no = 0
        base_path = self._generate_folder_path(folder_no, 'initial-build')
        if self._config.holiday_config.generate_holidays:
            file_no = self._generate_holiday_build_scripts(file_no, base_path)
        file_no = self._generate_dim_date_build_scripts(file_no, base_path)
        file_no = self._generate_dim_fiscal_month_build_scripts(
            file_no, base_path)
        file_no = self._generate_dim_calendar_month_build_scripts(
            file_no, base_path)
        return folder_no + 1

    def _generate_holiday_build_scripts(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_dim_date_build_scripts(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_dim_fiscal_month_build_scripts(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_dim_calendar_month_build_scripts(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_refresh_procs(self, folder_no: int) -> int:
        file_no = 0
        base_path = self._generate_folder_path(folder_no, 'refresh-procs')
        file_no = self._generate_dim_date_refresh_procs(file_no, base_path)
        file_no = self._generate_dim_fiscal_month_refresh_procs(
            file_no, base_path)
        file_no = self._generate_dim_calendar_month_refresh_procs(
            file_no, base_path)
        return folder_no + 1

    def _generate_dim_date_refresh_procs(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_dim_fiscal_month_refresh_procs(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_dim_calendar_month_refresh_procs(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_table_constraints(self, folder_no: int) -> int:
        file_no = 0
        base_path = self._generate_folder_path(folder_no, 'table-constraints')
        file_no = self._generate_dim_date_table_constraints(file_no, base_path)
        file_no = self._generate_dim_fiscal_month_table_constraints(
            file_no, base_path)
        file_no = self._generate_dim_calendar_month_table_constraints(
            file_no, base_path)
        if self._config.holiday_config.generate_holidays:
            file_no = self._generate_holiday_table_constraints(
                file_no, base_path)
        return folder_no + 1

    def _generate_dim_date_table_constraints(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_dim_fiscal_month_table_constraints(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_dim_calendar_month_table_constraints(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_holiday_table_constraints(self, file_no: int, base_path: Path) -> int:
        raise NotImplementedError()

    def _generate_folder_path(self, folder_no: int, name: str) -> Path:
        # note: Internal use. Does not attempt to sanitize folder name.
        if folder_no < 0 or folder_no > 99:
            raise ValueError('folder_no must be between 0 and 99 inclusive.')

        return self._config.outdir_base / f'{str(folder_no).zfill(2)}-{name}'
