from pathlib import Path
from src.awesome_date_dimension.generators.tsql import TSQLGenerator
from src.awesome_date_dimension.config import Config

generator = TSQLGenerator(
    Config(output_dir=Path('./output/test'), clear_output_dir=True))
generator.generate_scripts()
