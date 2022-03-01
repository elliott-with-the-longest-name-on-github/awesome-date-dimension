from dataclasses import asdict, dataclass

from ...config import (
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
            TSQLColumn.from_column("varchar(10)", False, columns.iso_week_date_name),
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
                "varchar(10)", False, columns.month_start_iso_week_date_name
            ),
            TSQLColumn.from_column(
                "varchar(10)", False, columns.month_end_iso_week_date_name
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
                "varchar(10)", False, columns.month_start_iso_week_date_name
            ),
            TSQLColumn.from_column(
                "varchar(10)", False, columns.month_end_iso_week_date_name
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
                f"chk_DimCalendarMonth_{columns.month_start_fraction_of_quarter.name} CHECK ({columns.month_start_fraction_of_quarter.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_end_fraction_of_quarter,
                f"chk_DimCalendarMonth_{columns.month_end_fraction_of_quarter.name} CHECK ({columns.month_end_fraction_of_quarter.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_start_fraction_of_year,
                f"chk_DimCalendarMonth_{columns.month_start_fraction_of_year.name} CHECK ({columns.month_start_fraction_of_year.name} BETWEEN 0 AND 1)",
            ),
            TSQLColumn.from_column(
                "decimal(5,4)",
                False,
                columns.month_end_fraction_of_year,
                f"chk_DimCalendarMonth_{columns.month_end_fraction_of_year.name} CHECK ({columns.month_end_fraction_of_year.name} BETWEEN 0 AND 1)",
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
