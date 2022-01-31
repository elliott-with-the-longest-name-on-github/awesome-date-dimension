from pathlib import Path
from awesome_date_dimension.config import Config


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
