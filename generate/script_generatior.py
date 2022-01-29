from dataclasses import dataclass
from datetime import datetime
from holidays import default_holidays, Holiday
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
    holiday_types: tuple[str] = ("Company Holiday", "US Public Holiday")
    holiday_types_for_business_days: tuple[str] = ("Company Holiday")
    holidays: list[Holiday] = default_holidays

    def __post_init__(self):
        if self.generate_holidays:
            assert all((holiday.holiday_type in self.holiday_types for holiday in self.holidays)
                       ), 'found a holiday in holidays whose holiday_type does not exist in holiday_types'
            assert all(holiday_type in self.holiday_types for holiday_type in self.holiday_types_for_business_days), 'found a holiday type in holiday_types_for_business_days that is not present in holiday_types'


@dataclass(frozen=True)
class TableNameConfig:
    dim_date_schema_name: str = "dbo"
    dim_date_table_name: str = "DimDate"
    holiday_types_schema_name: str = "integration"
    holiday_types_table_name: str = "manual_HolidayTypes"
    holidays_schema_name: str = "integration"
    holidays_table_name: str = "manual_Holidays"


@dataclass
class ScriptGeneratorConfig:
    outdir_base: Path = Path('../output')
    date_range: DateRange = DateRange()
    fiscal_config: FiscalConfig = FiscalConfig()
    time_zone: str = "Mountain Standard Time"
    table_name_config: TableNameConfig = TableNameConfig()
    holiday_config: HolidayConfig = HolidayConfig()


class ScriptGenerator(ABC):
    @abstractmethod
    def __init__(self, config: ScriptGeneratorConfig = ScriptGeneratorConfig()):
        pass

    @abstractmethod
    def generate_scripts(self) -> None:
        pass
