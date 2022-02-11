import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable

from ._internal.tsql_templates.dim_calendar_month_insert_template import (
    dim_calendar_month_insert_template,
)
from ._internal.tsql_templates.dim_calendar_month_refresh_template import (
    dim_calendar_month_refresh_template,
)
from ._internal.tsql_templates.dim_date_insert_template import dim_date_insert_template
from ._internal.tsql_templates.dim_date_refresh_template import (
    dim_date_refresh_template,
)
from ._internal.tsql_templates.dim_fiscal_month_insert_template import (
    dim_fiscal_month_insert_template,
)
from ._internal.tsql_templates.dim_fiscal_month_refresh_template import (
    dim_fiscal_month_refresh_template,
)
from ._internal.tsql_templates.holiday_types_insert_template import (
    holiday_types_insert_template,
)
from ._internal.tsql_templates.holidays_insert_template import holidays_insert_template
from ._internal.tsql_templates.table_setup_template import table_setup_template
from .config import (
    Column,
    Config,
    DimCalendarMonthColumns,
    DimDateColumns,
    DimFiscalMonthColumns,
    HolidayConfig,
)


@dataclass
class TSQLColumn:
    name: str
    include: bool
    sort_index: int
    sql_datatype: str
    nullable: bool
    constraint: str = None

    @classmethod
    def from_column(
        cls, sql_datatype: str, nullable: bool, column: Column, constraint: str = None
    ):
        return cls(
            sql_datatype=sql_datatype,
            nullable=nullable,
            constraint=constraint,
            **asdict(column),
        )


class TSQLDimDateColumns:
    def __init__(self, columns: DimDateColumns):
        self._columns: list[TSQLColumn] = [
            TSQLColumn.from_column("int", False, columns.date_key),
            TSQLColumn.from_column("date", False, columns.the_date),
            TSQLColumn.from_column("varchar(10)", False, columns.iso_date_name),
            TSQLColumn.from_column("varchar(10)", False, columns.american_date_name),
            TSQLColumn.from_column("varchar(9)", False, columns.day_of_week_name),
            TSQLColumn.from_column("varchar(3)", False, columns.day_of_week_abbrev),
            TSQLColumn.from_column("varchar(9)", False, columns.month_name),
            TSQLColumn.from_column("varchar(3)", False, columns.month_abbrev),
            TSQLColumn.from_column("varchar(8)", False, columns.year_week_name),
            TSQLColumn.from_column("varchar(7)", False, columns.year_month_name),
            TSQLColumn.from_column("varchar(8)", False, columns.month_year_name),
            TSQLColumn.from_column("varchar(6)", False, columns.year_quarter_name),
            TSQLColumn.from_column("int", False, columns.year),
            TSQLColumn.from_column("int", False, columns.year_week),
            TSQLColumn.from_column("int", False, columns.iso_year_week_code),
            TSQLColumn.from_column("int", False, columns.year_month),
            TSQLColumn.from_column("int", False, columns.year_quarter),
            TSQLColumn.from_column("int", False, columns.day_of_week_starting_monday),
            TSQLColumn.from_column("int", False, columns.day_of_week),
            TSQLColumn.from_column("int", False, columns.day_of_month),
            TSQLColumn.from_column("int", False, columns.day_of_quarter),
            TSQLColumn.from_column("int", False, columns.day_of_year),
            TSQLColumn.from_column("int", False, columns.week_of_quarter),
            TSQLColumn.from_column("int", False, columns.week_of_year),
            TSQLColumn.from_column("int", False, columns.iso_week_of_year),
            TSQLColumn.from_column("int", False, columns.month),
            TSQLColumn.from_column("int", False, columns.month_of_quarter),
            TSQLColumn.from_column("int", False, columns.quarter),
            TSQLColumn.from_column("int", False, columns.days_in_month),
            TSQLColumn.from_column("int", False, columns.days_in_quarter),
            TSQLColumn.from_column("int", False, columns.days_in_year),
            TSQLColumn.from_column("int", False, columns.day_offset_from_today),
            TSQLColumn.from_column("int", False, columns.month_offset_from_today),
            TSQLColumn.from_column("int", False, columns.quarter_offset_from_today),
            TSQLColumn.from_column("int", False, columns.year_offset_from_today),
            TSQLColumn.from_column("bit", False, columns.today_flag),
            TSQLColumn.from_column(
                "bit", False, columns.current_week_starting_monday_flag
            ),
            TSQLColumn.from_column("bit", False, columns.current_week_flag),
            TSQLColumn.from_column("bit", False, columns.prior_week_flag),
            TSQLColumn.from_column("bit", False, columns.next_week_flag),
            TSQLColumn.from_column("bit", False, columns.current_month_flag),
            TSQLColumn.from_column("bit", False, columns.prior_month_flag),
            TSQLColumn.from_column("bit", False, columns.next_month_flag),
            TSQLColumn.from_column("bit", False, columns.current_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.prior_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.next_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.current_year_flag),
            TSQLColumn.from_column("bit", False, columns.prior_year_flag),
            TSQLColumn.from_column("bit", False, columns.next_year_flag),
            TSQLColumn.from_column("bit", False, columns.weekday_flag),
            TSQLColumn.from_column("bit", False, columns.business_day_flag),
            TSQLColumn.from_column("bit", False, columns.first_day_of_month_flag),
            TSQLColumn.from_column("bit", False, columns.last_day_of_month_flag),
            TSQLColumn.from_column("bit", False, columns.first_day_of_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.last_day_of_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.first_day_of_year_flag),
            TSQLColumn.from_column("bit", False, columns.last_day_of_year_flag),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.fraction_of_week,
                f"chk_DimDate_{columns.fraction_of_week.name} CHECK ({columns.fraction_of_week.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.fraction_of_month,
                f"chk_DimDate_{columns.fraction_of_month.name} CHECK ({columns.fraction_of_month.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.fraction_of_quarter,
                f"chk_DimDate_{columns.fraction_of_quarter.name} CHECK ({columns.fraction_of_quarter.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.fraction_of_year,
                f"chk_DimDate_{columns.fraction_of_year.name} CHECK ({columns.fraction_of_year.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column("date", False, columns.prior_day),
            TSQLColumn.from_column("date", False, columns.next_day),
            TSQLColumn.from_column("date", False, columns.same_day_prior_week),
            TSQLColumn.from_column("date", False, columns.same_day_prior_month),
            TSQLColumn.from_column("date", False, columns.same_day_prior_quarter),
            TSQLColumn.from_column("date", False, columns.same_day_prior_year),
            TSQLColumn.from_column("date", False, columns.same_day_next_week),
            TSQLColumn.from_column("date", False, columns.same_day_next_month),
            TSQLColumn.from_column("date", False, columns.same_day_next_quarter),
            TSQLColumn.from_column("date", False, columns.same_day_next_year),
            TSQLColumn.from_column("date", False, columns.current_week_start),
            TSQLColumn.from_column("date", False, columns.current_week_end),
            TSQLColumn.from_column("date", False, columns.current_month_start),
            TSQLColumn.from_column("date", False, columns.current_month_end),
            TSQLColumn.from_column("date", False, columns.current_quarter_start),
            TSQLColumn.from_column("date", False, columns.current_quarter_end),
            TSQLColumn.from_column("date", False, columns.current_year_start),
            TSQLColumn.from_column("date", False, columns.current_year_end),
            TSQLColumn.from_column("date", False, columns.prior_week_start),
            TSQLColumn.from_column("date", False, columns.prior_week_end),
            TSQLColumn.from_column("date", False, columns.prior_month_start),
            TSQLColumn.from_column("date", False, columns.prior_month_end),
            TSQLColumn.from_column("date", False, columns.prior_quarter_start),
            TSQLColumn.from_column("date", False, columns.prior_quarter_end),
            TSQLColumn.from_column("date", False, columns.prior_year_start),
            TSQLColumn.from_column("date", False, columns.prior_year_end),
            TSQLColumn.from_column("date", False, columns.next_week_start),
            TSQLColumn.from_column("date", False, columns.next_week_end),
            TSQLColumn.from_column("date", False, columns.next_month_start),
            TSQLColumn.from_column("date", False, columns.next_month_end),
            TSQLColumn.from_column("date", False, columns.next_quarter_start),
            TSQLColumn.from_column("date", False, columns.next_quarter_end),
            TSQLColumn.from_column("date", False, columns.next_year_start),
            TSQLColumn.from_column("date", False, columns.next_year_end),
            TSQLColumn.from_column("bit", False, columns.weekly_burnup_starting_monday),
            TSQLColumn.from_column("bit", False, columns.weekly_burnup),
            TSQLColumn.from_column("bit", False, columns.monthly_burnup),
            TSQLColumn.from_column("bit", False, columns.quarterly_burnup),
            TSQLColumn.from_column("bit", False, columns.yearly_burnup),
            TSQLColumn.from_column("varchar(9)", False, columns.fiscal_month_name),
            TSQLColumn.from_column("varchar(3)", False, columns.fiscal_month_abbrev),
            TSQLColumn.from_column("varchar(8)", False, columns.fiscal_year_week_name),
            TSQLColumn.from_column("varchar(7)", False, columns.fiscal_year_month_name),
            TSQLColumn.from_column("varchar(8)", False, columns.fiscal_month_year_name),
            TSQLColumn.from_column(
                "varchar(6)", False, columns.fiscal_year_quarter_name
            ),
            TSQLColumn.from_column("int", False, columns.fiscal_year),
            TSQLColumn.from_column("int", False, columns.fiscal_year_week),
            TSQLColumn.from_column("int", False, columns.fiscal_year_month),
            TSQLColumn.from_column("int", False, columns.fiscal_year_quarter),
            TSQLColumn.from_column("int", False, columns.fiscal_day_of_month),
            TSQLColumn.from_column("int", False, columns.fiscal_day_of_quarter),
            TSQLColumn.from_column("int", False, columns.fiscal_day_of_year),
            TSQLColumn.from_column("int", False, columns.fiscal_week_of_quarter),
            TSQLColumn.from_column("int", False, columns.fiscal_week_of_year),
            TSQLColumn.from_column("int", False, columns.fiscal_month),
            TSQLColumn.from_column("int", False, columns.fiscal_month_of_quarter),
            TSQLColumn.from_column("int", False, columns.fiscal_quarter),
            TSQLColumn.from_column("int", False, columns.fiscal_days_in_month),
            TSQLColumn.from_column("int", False, columns.fiscal_days_in_quarter),
            TSQLColumn.from_column("int", False, columns.fiscal_days_in_year),
            TSQLColumn.from_column("bit", False, columns.fiscal_current_month_flag),
            TSQLColumn.from_column("bit", False, columns.fiscal_prior_month_flag),
            TSQLColumn.from_column("bit", False, columns.fiscal_next_month_flag),
            TSQLColumn.from_column("bit", False, columns.fiscal_current_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.fiscal_prior_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.fiscal_next_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.fiscal_current_year_flag),
            TSQLColumn.from_column("bit", False, columns.fiscal_prior_year_flag),
            TSQLColumn.from_column("bit", False, columns.fiscal_next_year_flag),
            TSQLColumn.from_column(
                "bit", False, columns.fiscal_first_day_of_month_flag
            ),
            TSQLColumn.from_column("bit", False, columns.fiscal_last_day_of_month_flag),
            TSQLColumn.from_column(
                "bit", False, columns.fiscal_first_day_of_quarter_flag
            ),
            TSQLColumn.from_column(
                "bit", False, columns.fiscal_last_day_of_quarter_flag
            ),
            TSQLColumn.from_column("bit", False, columns.fiscal_first_day_of_year_flag),
            TSQLColumn.from_column("bit", False, columns.fiscal_last_day_of_year_flag),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.fiscal_fraction_of_month,
                f"chk_DimDate_{columns.fiscal_fraction_of_month.name} CHECK ({columns.fiscal_fraction_of_month.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.fiscal_fraction_of_quarter,
                f"chk_DimDate_{columns.fiscal_fraction_of_quarter.name} CHECK ({columns.fiscal_fraction_of_quarter.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.fiscal_fraction_of_year,
                f"chk_DimDate_{columns.fiscal_fraction_of_year.name} CHECK ({columns.fiscal_fraction_of_year.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column("date", False, columns.fiscal_current_month_start),
            TSQLColumn.from_column("date", False, columns.fiscal_current_month_end),
            TSQLColumn.from_column("date", False, columns.fiscal_current_quarter_start),
            TSQLColumn.from_column("date", False, columns.fiscal_current_quarter_end),
            TSQLColumn.from_column("date", False, columns.fiscal_current_year_start),
            TSQLColumn.from_column("date", False, columns.fiscal_current_year_end),
            TSQLColumn.from_column("date", False, columns.fiscal_prior_month_start),
            TSQLColumn.from_column("date", False, columns.fiscal_prior_month_end),
            TSQLColumn.from_column("date", False, columns.fiscal_prior_quarter_start),
            TSQLColumn.from_column("date", False, columns.fiscal_prior_quarter_end),
            TSQLColumn.from_column("date", False, columns.fiscal_prior_year_start),
            TSQLColumn.from_column("date", False, columns.fiscal_prior_year_end),
            TSQLColumn.from_column("date", False, columns.fiscal_next_month_start),
            TSQLColumn.from_column("date", False, columns.fiscal_next_month_end),
            TSQLColumn.from_column("date", False, columns.fiscal_next_quarter_start),
            TSQLColumn.from_column("date", False, columns.fiscal_next_quarter_end),
            TSQLColumn.from_column("date", False, columns.fiscal_next_year_start),
            TSQLColumn.from_column("date", False, columns.fiscal_next_year_end),
            TSQLColumn.from_column("bit", False, columns.fiscal_monthly_burnup),
            TSQLColumn.from_column("bit", False, columns.fiscal_quarterly_burnup),
            TSQLColumn.from_column("bit", False, columns.fiscal_yearly_burnup),
        ]
        self._columns = list(filter(lambda c: c.include, self._columns))
        self._columns.sort(key=lambda c: c.sort_index)

    def __iter__(self):
        return iter(self._columns)

    def add_holiday_columns(self, holiday_config: HolidayConfig):
        idx = self._columns[-1].sort_index + 1
        if holiday_config.generate_holidays:
            for t in holiday_config.holiday_types:
                self._columns.append(
                    TSQLColumn(
                        f"{t.generated_column_prefix}{t.generated_flag_column_postfix}",
                        True,
                        idx,
                        "bit",
                        False,
                    )
                )
                idx += 1
                self._columns.append(
                    TSQLColumn(
                        f"{t.generated_column_prefix}{t.generated_name_column_postfix}",
                        True,
                        idx,
                        "varchar(255)",
                        True,
                    )
                )
                idx += 1


class TSQLDimFiscalMonthColumns:
    def __init__(self, columns: DimFiscalMonthColumns):
        self._columns: list[TSQLColumn] = [
            TSQLColumn.from_column("int", False, columns.month_start_key),
            TSQLColumn.from_column("int", False, columns.month_end_key),
            TSQLColumn.from_column("date", False, columns.month_start_date),
            TSQLColumn.from_column("date", False, columns.month_end_date),
            TSQLColumn.from_column(
                "varchar(10)", False, columns.month_start_iso_date_name
            ),
            TSQLColumn.from_column(
                "varchar(10)", False, columns.month_end_iso_date_name
            ),
            TSQLColumn.from_column(
                "varchar(10)", False, columns.month_start_american_date_name
            ),
            TSQLColumn.from_column(
                "varchar(10)", False, columns.month_end_american_date_name
            ),
            TSQLColumn.from_column("varchar(9)", False, columns.month_name),
            TSQLColumn.from_column("varchar(3)", False, columns.month_abbrev),
            TSQLColumn.from_column(
                "varchar(8)", False, columns.month_start_year_week_name
            ),
            TSQLColumn.from_column(
                "varchar(8)", False, columns.month_end_year_week_name
            ),
            TSQLColumn.from_column("varchar(7)", False, columns.year_month_name),
            TSQLColumn.from_column("varchar(8)", False, columns.month_year_name),
            TSQLColumn.from_column("varchar(6)", False, columns.year_quarter_name),
            TSQLColumn.from_column("int", False, columns.year),
            TSQLColumn.from_column("int", False, columns.month_start_year_week),
            TSQLColumn.from_column("int", False, columns.month_end_year_week),
            TSQLColumn.from_column("int", False, columns.year_month),
            TSQLColumn.from_column("int", False, columns.year_quarter),
            TSQLColumn.from_column("int", False, columns.month_start_day_of_quarter),
            TSQLColumn.from_column("int", False, columns.month_end_day_of_quarter),
            TSQLColumn.from_column("int", False, columns.month_start_day_of_year),
            TSQLColumn.from_column("int", False, columns.month_end_day_of_year),
            TSQLColumn.from_column("int", False, columns.month_start_week_of_quarter),
            TSQLColumn.from_column("int", False, columns.month_end_week_of_quarter),
            TSQLColumn.from_column("int", False, columns.month_start_week_of_year),
            TSQLColumn.from_column("int", False, columns.month_end_week_of_year),
            TSQLColumn.from_column("int", False, columns.month_of_quarter),
            TSQLColumn.from_column("int", False, columns.quarter),
            TSQLColumn.from_column("int", False, columns.days_in_month),
            TSQLColumn.from_column("int", False, columns.days_in_quarter),
            TSQLColumn.from_column("int", False, columns.days_in_year),
            TSQLColumn.from_column("bit", False, columns.current_month_flag),
            TSQLColumn.from_column("bit", False, columns.prior_month_flag),
            TSQLColumn.from_column("bit", False, columns.next_month_flag),
            TSQLColumn.from_column("bit", False, columns.current_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.prior_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.next_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.current_year_flag),
            TSQLColumn.from_column("bit", False, columns.prior_year_flag),
            TSQLColumn.from_column("bit", False, columns.next_year_flag),
            TSQLColumn.from_column("bit", False, columns.first_day_of_month_flag),
            TSQLColumn.from_column("bit", False, columns.last_day_of_month_flag),
            TSQLColumn.from_column("bit", False, columns.first_day_of_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.last_day_of_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.first_day_of_year_flag),
            TSQLColumn.from_column("bit", False, columns.last_day_of_year_flag),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_start_fraction_of_quarter,
                f"chk_DimFiscalMonth_{columns.month_start_fraction_of_quarter.name} CHECK ({columns.month_start_fraction_of_quarter.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_end_fraction_of_quarter,
                f"chk_DimFiscalMonth_{columns.month_end_fraction_of_quarter.name} CHECK ({columns.month_end_fraction_of_quarter.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_start_fraction_of_year,
                f"chk_DimFiscalMonth_{columns.month_start_fraction_of_year.name} CHECK ({columns.month_start_fraction_of_year.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_end_fraction_of_year,
                f"chk_DimFiscalMonth_{columns.month_end_fraction_of_year.name} CHECK ({columns.month_end_fraction_of_year.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column("date", False, columns.current_quarter_start),
            TSQLColumn.from_column("date", False, columns.current_quarter_end),
            TSQLColumn.from_column("date", False, columns.current_year_start),
            TSQLColumn.from_column("date", False, columns.current_year_end),
            TSQLColumn.from_column("date", False, columns.prior_month_start),
            TSQLColumn.from_column("date", False, columns.prior_month_end),
            TSQLColumn.from_column("date", False, columns.prior_quarter_start),
            TSQLColumn.from_column("date", False, columns.prior_quarter_end),
            TSQLColumn.from_column("date", False, columns.prior_year_start),
            TSQLColumn.from_column("date", False, columns.prior_year_end),
            TSQLColumn.from_column("date", False, columns.next_month_start),
            TSQLColumn.from_column("date", False, columns.next_month_end),
            TSQLColumn.from_column("date", False, columns.next_quarter_start),
            TSQLColumn.from_column("date", False, columns.next_quarter_end),
            TSQLColumn.from_column("date", False, columns.next_year_start),
            TSQLColumn.from_column("date", False, columns.next_year_end),
            TSQLColumn.from_column("bit", False, columns.month_start_quarterly_burnup),
            TSQLColumn.from_column("bit", False, columns.month_end_quarterly_burnup),
            TSQLColumn.from_column("bit", False, columns.month_start_yearly_burnup),
            TSQLColumn.from_column("bit", False, columns.month_end_yearly_burnup),
        ]
        self._columns = list(filter(lambda c: c.include, self._columns))
        self._columns.sort(key=lambda c: c.sort_index)

    def __iter__(self):
        return iter(self._columns)

    def add_holiday_columns(self, holiday_config: HolidayConfig):
        idx = self._columns[-1].sort_index + 1
        if holiday_config.generate_holidays:
            for t in holiday_config.holiday_types:
                self._columns.append(
                    TSQLColumn(
                        f"{t.generated_column_prefix}{t.generated_monthly_count_column_postfix}",
                        True,
                        idx,
                        "int",
                        False,
                    )
                )
                idx += 1


class TSQLDimCalendarMonthColumns:
    def __init__(self, columns: DimCalendarMonthColumns):
        self._columns: list[TSQLColumn] = [
            TSQLColumn.from_column("int", False, columns.month_start_key),
            TSQLColumn.from_column("int", False, columns.month_end_key),
            TSQLColumn.from_column("date", False, columns.month_start_date),
            TSQLColumn.from_column("date", False, columns.month_end_date),
            TSQLColumn.from_column(
                "varchar(10)", False, columns.month_start_iso_date_name
            ),
            TSQLColumn.from_column(
                "varchar(10)", False, columns.month_end_iso_date_name
            ),
            TSQLColumn.from_column(
                "varchar(10)", False, columns.month_start_american_date_name
            ),
            TSQLColumn.from_column(
                "varchar(10)", False, columns.month_end_american_date_name
            ),
            TSQLColumn.from_column("varchar(9)", False, columns.month_name),
            TSQLColumn.from_column("varchar(3)", False, columns.month_abbrev),
            TSQLColumn.from_column(
                "varchar(8)", False, columns.month_start_year_week_name
            ),
            TSQLColumn.from_column(
                "varchar(8)", False, columns.month_end_year_week_name
            ),
            TSQLColumn.from_column("varchar(7)", False, columns.year_month_name),
            TSQLColumn.from_column("varchar(8)", False, columns.month_year_name),
            TSQLColumn.from_column("varchar(6)", False, columns.year_quarter_name),
            TSQLColumn.from_column("int", False, columns.year),
            TSQLColumn.from_column("int", False, columns.month_start_year_week),
            TSQLColumn.from_column("int", False, columns.month_end_year_week),
            TSQLColumn.from_column("int", False, columns.year_month),
            TSQLColumn.from_column("int", False, columns.year_quarter),
            TSQLColumn.from_column("int", False, columns.month_start_day_of_quarter),
            TSQLColumn.from_column("int", False, columns.month_end_day_of_quarter),
            TSQLColumn.from_column("int", False, columns.month_start_day_of_year),
            TSQLColumn.from_column("int", False, columns.month_end_day_of_year),
            TSQLColumn.from_column("int", False, columns.month_start_week_of_quarter),
            TSQLColumn.from_column("int", False, columns.month_end_week_of_quarter),
            TSQLColumn.from_column("int", False, columns.month_start_week_of_year),
            TSQLColumn.from_column("int", False, columns.month_end_week_of_year),
            TSQLColumn.from_column("int", False, columns.month_of_quarter),
            TSQLColumn.from_column("int", False, columns.quarter),
            TSQLColumn.from_column("int", False, columns.days_in_month),
            TSQLColumn.from_column("int", False, columns.days_in_quarter),
            TSQLColumn.from_column("int", False, columns.days_in_year),
            TSQLColumn.from_column("bit", False, columns.current_month_flag),
            TSQLColumn.from_column("bit", False, columns.prior_month_flag),
            TSQLColumn.from_column("bit", False, columns.next_month_flag),
            TSQLColumn.from_column("bit", False, columns.current_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.prior_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.next_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.current_year_flag),
            TSQLColumn.from_column("bit", False, columns.prior_year_flag),
            TSQLColumn.from_column("bit", False, columns.next_year_flag),
            TSQLColumn.from_column("bit", False, columns.first_day_of_month_flag),
            TSQLColumn.from_column("bit", False, columns.last_day_of_month_flag),
            TSQLColumn.from_column("bit", False, columns.first_day_of_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.last_day_of_quarter_flag),
            TSQLColumn.from_column("bit", False, columns.first_day_of_year_flag),
            TSQLColumn.from_column("bit", False, columns.last_day_of_year_flag),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_start_fraction_of_quarter,
                f"chk_DimFiscalMonth_{columns.month_start_fraction_of_quarter.name} CHECK ({columns.month_start_fraction_of_quarter.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_end_fraction_of_quarter,
                f"chk_DimFiscalMonth_{columns.month_end_fraction_of_quarter.name} CHECK ({columns.month_end_fraction_of_quarter.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_start_fraction_of_year,
                f"chk_DimFiscalMonth_{columns.month_start_fraction_of_year.name} CHECK ({columns.month_start_fraction_of_year.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_end_fraction_of_year,
                f"chk_DimFiscalMonth_{columns.month_end_fraction_of_year.name} CHECK ({columns.month_end_fraction_of_year.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column("date", False, columns.current_quarter_start),
            TSQLColumn.from_column("date", False, columns.current_quarter_end),
            TSQLColumn.from_column("date", False, columns.current_year_start),
            TSQLColumn.from_column("date", False, columns.current_year_end),
            TSQLColumn.from_column("date", False, columns.prior_month_start),
            TSQLColumn.from_column("date", False, columns.prior_month_end),
            TSQLColumn.from_column("date", False, columns.prior_quarter_start),
            TSQLColumn.from_column("date", False, columns.prior_quarter_end),
            TSQLColumn.from_column("date", False, columns.prior_year_start),
            TSQLColumn.from_column("date", False, columns.prior_year_end),
            TSQLColumn.from_column("date", False, columns.next_month_start),
            TSQLColumn.from_column("date", False, columns.next_month_end),
            TSQLColumn.from_column("date", False, columns.next_quarter_start),
            TSQLColumn.from_column("date", False, columns.next_quarter_end),
            TSQLColumn.from_column("date", False, columns.next_year_start),
            TSQLColumn.from_column("date", False, columns.next_year_end),
            TSQLColumn.from_column("bit", False, columns.month_start_quarterly_burnup),
            TSQLColumn.from_column("bit", False, columns.month_end_quarterly_burnup),
            TSQLColumn.from_column("bit", False, columns.month_start_yearly_burnup),
            TSQLColumn.from_column("bit", False, columns.month_end_yearly_burnup),
        ]
        self._columns = list(filter(lambda c: c.include, self._columns))
        self._columns.sort(key=lambda c: c.sort_index)

    def __iter__(self):
        return iter(self._columns)

    def add_holiday_columns(self, holiday_config: HolidayConfig):
        idx = self._columns[-1].sort_index + 1
        if holiday_config.generate_holidays:
            for t in holiday_config.holiday_types:
                self._columns.append(
                    TSQLColumn(
                        f"{t.generated_column_prefix}{t.generated_monthly_count_column_postfix}",
                        True,
                        idx,
                        "int",
                        False,
                    )
                )
                idx += 1


class TSQLGenerator:
    def __init__(self, config: Config):
        self._config = config
        self._dim_date_columns = TSQLDimDateColumns(config.dim_date.columns)
        self._dim_fiscal_month_columns = TSQLDimFiscalMonthColumns(
            config.dim_fiscal_month.columns
        )
        self._dim_calendar_month_columns = TSQLDimCalendarMonthColumns(
            config.dim_calendar_month.columns
        )

        self._dim_date_columns.add_holiday_columns(config.holidays)
        self._dim_fiscal_month_columns.add_holiday_columns(config.holidays)
        self._dim_calendar_month_columns.add_holiday_columns(config.holidays)

        dir_exists = config.output_dir.exists()
        if dir_exists and config.clear_output_dir:
            shutil.rmtree(config.output_dir)
            config.output_dir.mkdir()
        elif not dir_exists:
            config.output_dir.mkdir()

    def generate_scripts(self) -> None:
        folder_no = 0
        folder_no = self._generate_setup_scripts(folder_no)
        folder_no = self._generate_build_scripts(folder_no)
        folder_no = self._generate_refresh_procs(folder_no)
        folder_no = self._generate_table_constraints(folder_no)

    def _generate_setup_scripts(self, folder_no: int) -> int:
        file_no = 0
        base_path = self._generate_folder_path(folder_no, "initial-build")
        if not base_path.exists():
            base_path.mkdir()
        file_no = self._generate_dim_date_setup_scripts(file_no, base_path)
        file_no = self._generate_dim_fiscal_month_setup_scripts(file_no, base_path)
        file_no = self._generate_dim_calendar_month_setup_scripts(file_no, base_path)
        file_no = self._generate_holiday_setup_scripts(file_no, base_path)
        return folder_no + 1

    def _generate_dim_date_setup_scripts(self, file_no: int, base_path: Path) -> int:
        cfg = self._config.dim_date
        table_gen = lambda config: TSQLGenerator._get_table_definition(
            cfg.table_schema, cfg.table_name, self._dim_date_columns
        )
        return TSQLGenerator._generate_file(
            file_no, cfg.table_name, base_path, self._config, table_gen
        )

    def _generate_dim_fiscal_month_setup_scripts(
        self, file_no: int, base_path: Path
    ) -> int:
        cfg = self._config.dim_fiscal_month
        table_gen = lambda config: TSQLGenerator._get_table_definition(
            cfg.table_schema, cfg.table_name, self._dim_fiscal_month_columns
        )
        return TSQLGenerator._generate_file(
            file_no, cfg.table_name, base_path, self._config, table_gen
        )

    def _generate_dim_calendar_month_setup_scripts(
        self, file_no: int, base_path: Path
    ) -> int:
        cfg = self._config.dim_calendar_month
        table_gen = lambda config: TSQLGenerator._get_table_definition(
            cfg.table_schema, cfg.table_name, self._dim_calendar_month_columns
        )
        return TSQLGenerator._generate_file(
            file_no, cfg.table_name, base_path, self._config, table_gen
        )

    def _generate_holiday_setup_scripts(self, file_no: int, base_path: Path) -> int:
        if self._config.holidays.generate_holidays:
            # Honestly, not worth it to create templates for these since they're so simple.
            # I'll take points off for "bad software", I suppose.

            # Holiday Types
            ht_tabledef = [
                f"CREATE TABLE {self._config.holidays.holiday_types_schema_name}.{self._config.holidays.holiday_types_table_name} (",
                f"  {self._config.holidays.holiday_types_columns.holiday_type_key.name} int IDENTITY(1,1) NOT NULL,",
                f"  {self._config.holidays.holiday_types_columns.holiday_type_name.name} varchar(255) UNIQUE NOT NULL",
                ");",
            ]
            file_path = base_path / TSQLGenerator._get_sql_filename(
                file_no, self._config.holidays.holiday_types_table_name
            )
            TSQLGenerator._assert_filepath_available(file_path)
            file_path.write_text("\n".join(ht_tabledef))

            file_no += 1

            # Holidays
            h_tabledef = [
                f"CREATE TABLE {self._config.holidays.holidays_schema_name}.{self._config.holidays.holidays_table_name} (",
                f"  {self._config.holidays.holidays_columns.date_key.name} int NOT NULL,",
                f"  {self._config.holidays.holidays_columns.holiday_name.name} varchar(255) NOT NULL,",
                f"  {self._config.holidays.holidays_columns.holiday_type_key.name} int NOT NULL",
                ");",
            ]
            file_path = base_path / TSQLGenerator._get_sql_filename(
                file_no, self._config.holidays.holidays_table_name
            )
            TSQLGenerator._assert_filepath_available(file_path)
            file_path.write_text("\n".join(h_tabledef))
            return file_no + 1
        return file_no

    def _generate_build_scripts(self, folder_no: int) -> int:
        file_no = 0
        base_path = self._generate_folder_path(folder_no, "initial-build")
        if not base_path.exists():
            base_path.mkdir()
        file_no = self._generate_holiday_build_scripts(file_no, base_path)
        file_no = self._generate_dim_date_build_scripts(file_no, base_path)
        file_no = self._generate_dim_fiscal_month_build_scripts(file_no, base_path)
        file_no = self._generate_dim_calendar_month_build_scripts(file_no, base_path)
        return folder_no + 1

    def _generate_holiday_type_build_script(self, file_no: int, base_path: Path) -> int:
        return TSQLGenerator._generate_file(
            file_no,
            self._config.holidays.holiday_types_table_name,
            base_path,
            self._config,
            holiday_types_insert_template,
        )

    def _generate_holidays_build_script(self, file_no: int, base_path: Path) -> int:
        return TSQLGenerator._generate_file(
            file_no,
            self._config.holidays.holidays_table_name,
            base_path,
            self._config,
            holidays_insert_template,
        )

    def _generate_holiday_build_scripts(self, file_no: int, base_path: Path) -> int:
        if self._config.holidays.generate_holidays:
            file_no = self._generate_holiday_type_build_script(file_no, base_path)
            file_no = self._generate_holidays_build_script(file_no, base_path)
        return file_no

    def _generate_dim_date_build_scripts(self, file_no: int, base_path: Path) -> int:
        return TSQLGenerator._generate_file(
            file_no,
            self._config.dim_date.table_name,
            base_path,
            self._config,
            dim_date_insert_template,
        )

    def _generate_dim_fiscal_month_build_scripts(
        self, file_no: int, base_path: Path
    ) -> int:
        return TSQLGenerator._generate_file(
            file_no,
            self._config.dim_fiscal_month.table_name,
            base_path,
            self._config,
            dim_fiscal_month_insert_template,
        )

    def _generate_dim_calendar_month_build_scripts(
        self, file_no: int, base_path: Path
    ) -> int:
        return TSQLGenerator._generate_file(
            file_no,
            self._config.dim_calendar_month.table_name,
            base_path,
            self._config,
            dim_calendar_month_insert_template,
        )

    def _generate_refresh_procs(self, folder_no: int) -> int:
        file_no = 0
        base_path = self._generate_folder_path(folder_no, "refresh-procs")
        if not base_path.exists():
            base_path.mkdir()
        file_no = self._generate_dim_date_refresh_procs(file_no, base_path)
        file_no = self._generate_dim_fiscal_month_refresh_procs(file_no, base_path)
        file_no = self._generate_dim_calendar_month_refresh_procs(file_no, base_path)
        return folder_no + 1

    def _generate_dim_date_refresh_procs(self, file_no: int, base_path: Path) -> int:
        return TSQLGenerator._generate_file(
            file_no,
            self._config.dim_date.table_name,
            base_path,
            self._config,
            dim_date_refresh_template,
        )

    def _generate_dim_fiscal_month_refresh_procs(
        self, file_no: int, base_path: Path
    ) -> int:
        return TSQLGenerator._generate_file(
            file_no,
            self._config.dim_fiscal_month.table_name,
            base_path,
            self._config,
            dim_fiscal_month_refresh_template,
        )

    def _generate_dim_calendar_month_refresh_procs(
        self, file_no: int, base_path: Path
    ) -> int:
        return TSQLGenerator._generate_file(
            file_no,
            self._config.dim_calendar_month.table_name,
            base_path,
            self._config,
            dim_calendar_month_refresh_template,
        )

    def _generate_table_constraints(self, folder_no: int) -> int:
        file_no = 0
        base_path = self._generate_folder_path(folder_no, "table-constraints")
        if not base_path.exists():
            base_path.mkdir()
        file_no = self._generate_dim_date_table_constraints(file_no, base_path)
        file_no = self._generate_dim_fiscal_month_table_constraints(file_no, base_path)
        file_no = self._generate_dim_calendar_month_table_constraints(
            file_no, base_path
        )
        file_no = self._generate_holiday_table_constraints(file_no, base_path)
        return folder_no + 1

    def _generate_dim_date_table_constraints(
        self, file_no: int, base_path: Path
    ) -> int:
        # raise NotImplementedError()
        pass

    def _generate_dim_fiscal_month_table_constraints(
        self, file_no: int, base_path: Path
    ) -> int:
        # raise NotImplementedError()
        pass

    def _generate_dim_calendar_month_table_constraints(
        self, file_no: int, base_path: Path
    ) -> int:
        # raise NotImplementedError()
        pass

    def _generate_holiday_table_constraints(self, file_no: int, base_path: Path) -> int:
        # raise NotImplementedError()
        pass

    def _generate_folder_path(self, folder_no: int, name: str) -> Path:
        # note: Internal use. Does not attempt to sanitize folder name.
        if folder_no < 0 or folder_no > 99:
            raise ValueError("folder_no must be between 0 and 99 inclusive.")

        return self._config.output_dir / f"{str(folder_no).zfill(2)}-{name}"

    @staticmethod
    def _get_sql_filename(file_no: int, file_name: str):
        if file_no < 0 or file_no > 99:
            raise ValueError("file_no must be between 0 and 99 inclusive")
        return f"{str(file_no).zfill(2)}-{file_name}.sql"

    @staticmethod
    def _generate_file(
        file_no: int,
        table_name: str,
        base_path: Path,
        config: Config,
        script_gen_func: Callable[[Config], str],
    ) -> int:
        scriptdef = script_gen_func(config)
        file_path = base_path / TSQLGenerator._get_sql_filename(file_no, table_name)
        TSQLGenerator._assert_filepath_available(file_path)
        file_path.write_text(scriptdef)
        return file_no + 1

    @staticmethod
    def _get_constraint_str(constraint_def: str) -> str:
        return f"CONSTRAINT {constraint_def} " if constraint_def is not None else ""

    @staticmethod
    def _get_column_def(tsql_column: TSQLColumn) -> str:
        return f'{tsql_column.name} {tsql_column.sql_datatype} {TSQLGenerator._get_constraint_str(tsql_column.constraint)}{"NULL" if tsql_column.nullable else "NOT NULL"}'

    @staticmethod
    def _get_table_definition(
        table_schema: str, table_name: str, columns: Iterable[TSQLColumn]
    ) -> str:
        column_def = []
        for col in columns:
            column_def.append(TSQLGenerator._get_column_def(col))
        return table_setup_template(table_schema, table_name, column_def)

    @staticmethod
    def _generate_table_setup_scripts(
        table_schema: str,
        table_name: str,
        columns: Iterable[TSQLColumn],
        file_path: Path,
    ):
        table_def = TSQLGenerator._get_table_definition(
            table_name, table_schema, columns
        )
        TSQLGenerator._assert_filepath_available(file_path)
        file_path.write_text(table_def)

    @staticmethod
    def _assert_filepath_available(path: Path) -> None:
        if path.exists():
            TSQLGenerator._raise_fileexistserror(path)

    @staticmethod
    def _raise_fileexistserror(file_name: str) -> None:
        raise FileExistsError(
            f"The file {file_name} already exists. Please delete it and try again."
        )
