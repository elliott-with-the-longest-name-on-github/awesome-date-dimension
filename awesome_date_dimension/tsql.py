import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable

from ._internal.tsql.dim_calendar_month_constraints_template import (
    dim_calendar_month_constraints_template,
)
from ._internal.tsql.dim_calendar_month_insert_template import (
    dim_calendar_month_insert_template,
)
from ._internal.tsql.dim_calendar_month_refresh_template import (
    dim_calendar_month_refresh_template,
)
from ._internal.tsql.dim_date_constraints_template import dim_date_constraints_template
from ._internal.tsql.dim_date_insert_template import dim_date_insert_template
from ._internal.tsql.dim_date_refresh_template import dim_date_refresh_template
from ._internal.tsql.dim_fiscal_month_constraints_template import (
    dim_fiscal_month_constraints_template,
)
from ._internal.tsql.dim_fiscal_month_insert_template import (
    dim_fiscal_month_insert_template,
)
from ._internal.tsql.dim_fiscal_month_refresh_template import (
    dim_fiscal_month_refresh_template,
)
from ._internal.tsql.holiday_types_constraints_template import (
    holiday_types_constraints_template,
)
from ._internal.tsql.holiday_types_insert_template import holiday_types_insert_template
from ._internal.tsql.holidays_constraints_template import holidays_constraints_template
from ._internal.tsql.holidays_insert_template import holidays_insert_template
from ._internal.tsql.table_setup_template import table_setup_template
from ._internal.tsql.tsql_columns import (
    TSQLColumn,
    TSQLDimCalendarMonthColumns,
    TSQLDimDateColumns,
    TSQLDimFiscalMonthColumns,
)
from .config import Config


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
        base_path = self._generate_folder_path(folder_no, "setup")
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
            columns=self._dim_date_columns,
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
            columns=self._dim_fiscal_month_columns,
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
            columns=self._dim_calendar_month_columns,
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
            columns=self._dim_date_columns,
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
            columns=self._dim_fiscal_month_columns,
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
            columns=self._dim_calendar_month_columns,
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
        return TSQLGenerator._generate_file(
            file_no,
            self._config.dim_date.table_name,
            base_path,
            self._config,
            dim_date_constraints_template,
        )

    def _generate_dim_fiscal_month_table_constraints(
        self, file_no: int, base_path: Path
    ) -> int:
        return TSQLGenerator._generate_file(
            file_no,
            self._config.dim_fiscal_month.table_name,
            base_path,
            self._config,
            dim_fiscal_month_constraints_template,
        )

    def _generate_dim_calendar_month_table_constraints(
        self, file_no: int, base_path: Path
    ) -> int:
        return TSQLGenerator._generate_file(
            file_no,
            self._config.dim_calendar_month.table_name,
            base_path,
            self._config,
            dim_calendar_month_constraints_template,
        )

    def _generate_holiday_table_constraints(self, file_no: int, base_path: Path) -> int:
        file_no = TSQLGenerator._generate_file(
            file_no,
            self._config.holidays.holiday_types_table_name,
            base_path,
            self._config,
            holiday_types_constraints_template,
        )
        return TSQLGenerator._generate_file(
            file_no,
            self._config.holidays.holidays_table_name,
            base_path,
            self._config,
            holidays_constraints_template,
        )

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
        **kwargs,
    ) -> int:
        scriptdef = script_gen_func(config, **kwargs)
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
