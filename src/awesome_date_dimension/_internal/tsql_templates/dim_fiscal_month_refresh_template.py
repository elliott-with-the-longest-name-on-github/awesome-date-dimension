from ...config import Config
from .dim_fiscal_month_insert_template import dim_fiscal_month_insert_template


def dim_fiscal_month_refresh_template(config: Config) -> str:
    indentation_level = "    "
    insert_script = dim_fiscal_month_insert_template(config)
    indented_script = "\n".join(
        map(lambda line: indentation_level + line, insert_script.split("\n"))
    )
    return f"""CREATE PROCEDURE dbo.sp_build_DimFiscalMonth AS BEGIN
  SET XACT_ABORT ON;
  BEGIN TRY
    BEGIN TRANSACTION;

    TRUNCATE TABLE dbo.DimFiscalMonth;

{indented_script}

    COMMIT TRANSACTION;
  END TRY
  BEGIN CATCH
    EXEC sp_GetErrorInfo;
    IF @@TRANCOUNT > 0
      ROLLBACK TRANSACTION;
    THROW;
  END CATCH;
END
GO
"""
