from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Callable
from columns import Column, DimCalendarMonthColumns, DimDateColumns, DimFiscalMonthColumns
from holidays import HolidayCalendar, HolidayType, default_company_holidays, default_us_public_holidays
from abc import ABC, abstractmethod
from pathlib import Path


@dataclass(frozen=True)
class DateRange:
    start_date: datetime.date = datetime.fromisoformat('2000-01-01').date()
    num_years: int = 100

    def __post_init__(self):
        assert self.num_years > 0, 'num_years must be greater than 0.'


@dataclass(frozen=True)
class FiscalConfig:
    fiscal_month_start_day: int = 1
    fiscal_year_start_month: int = 1
    fiscal_month_end_matches_calendar: bool = True
    fiscal_quarter_end_matches_calendar: bool = True
    fiscal_year_end_matches_calendar: bool = True

    def __post_init__(self):
        assert 1 <= self.fiscal_month_start_day <= 28, 'fiscal_month_start_day must be between 1 and 28.'
        assert 1 <= self.fiscal_year_start_month <= 12, 'fiscal_year_start_month must be between 1 and 12.'


@dataclass(frozen=True)
class HolidayConfig:
    generate_holidays: bool = True
    holiday_types_schema_name: str = 'integration'
    holiday_types_table_name: str = 'manual_HolidayTypes'
    holidays_schema_name: str = 'integration'
    holidays_table_name: str = 'manual_Holidays'
    holiday_calendars: list[HolidayCalendar] = [
        default_company_holidays, default_us_public_holidays]
    holiday_types: list[HolidayType] = field(init=False)

    def __post_init__(self):
        if self.generate_holidays:
            holiday_types = [
                cal.holiday_type for cal in self.holiday_calendars]
            holiday_type_names = [t.name for t in holiday_types]
            holiday_type_prefixes = [
                t.generated_column_prefix for t in holiday_types]
            assert len(holiday_type_names) == len(set(holiday_type_names)
                                                  ), 'detected a duplicate HolidayType name in HolidayConfig.'
            assert len(holiday_type_prefixes) == len(set(holiday_type_prefixes)
                                                     ), 'detected a duplicate HolidayTypePrefix in HolidayConfig.'
            self.holiday_types = holiday_types


@dataclass(frozen=True)
class DimDateConfig:
    table_schema: str = 'dbo'
    table_name: str = 'DimDate'
    columns: DimDateColumns = DimDateColumns()
    column_name_factory: Callable[[str], str] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v['sort_index']
                     for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys), 'there was a duplicate sort key in the column definitions for DimDateColumnConfig.'

        if self.column_name_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_cols[k] = Column(self.column_name_factory(
                    v['name']), v['include'], v['sort_index'])
            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass(frozen=True)
class DimFiscalMonthConfig:
    table_schema: str = 'dbo'
    table_name: str = 'DimFiscalMonth'
    columns: DimFiscalMonthColumns = DimFiscalMonthColumns()
    column_name_factory: Callable[[str], str] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v['sort_index']
                     for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys), 'there was a duplicate sort key in the column definitions for DimFiscalMonthColumnConfig.'

        if self.column_name_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_cols[k] = Column(self.column_name_factory(
                    v['name']), v['include'], v['sort_index'])
            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass(frozen=True)
class DimCalendarMonthConfig:
    table_schema: str = 'dbo'
    table_name: str = 'DimCalendarMonth'
    columns: DimCalendarMonthColumns = DimCalendarMonthColumns()
    column_name_factory: Callable[[str], str] = None

    def __post_init__(self):
        col_dict = asdict(self.columns)
        sort_keys = [v['sort_index']
                     for v in col_dict.values()]
        distinct_sort_keys = set(sort_keys)
        assert len(sort_keys) == len(
            distinct_sort_keys), 'there was a duplicate sort key in the column definitions for DimCalendarMonthColumnConfig.'

        if self.column_name_factory is not None:
            new_cols: dict[str, Column] = {}
            for k, v in col_dict.values():
                new_cols[k] = Column(self.column_name_factory(
                    v['name']), v['include'], v['sort_index'])
            self.columns = DimCalendarMonthColumns(**new_cols)


@dataclass
class ScriptGeneratorConfig:
    outdir_base: Path = Path('../output')
    date_range: DateRange = DateRange()
    fiscal_config: FiscalConfig = FiscalConfig()
    time_zone: str = "Mountain Standard Time"
    holiday_config: HolidayConfig = HolidayConfig()
    dim_date_config: DimDateConfig = DimDateConfig()
    dim_fiscal_month_config: DimFiscalMonthConfig = DimFiscalMonthConfig()
    dim_calendar_month_config: DimCalendarMonthConfig = DimCalendarMonthConfig()


class ScriptGenerator(ABC):
    @abstractmethod
    def __init__(self, config: ScriptGeneratorConfig = ScriptGeneratorConfig()):
        pass

    @abstractmethod
    def add_generator_specific_config(self, config: object) -> None:
        pass

    @abstractmethod
    def generate_scripts(self) -> None:
        pass
