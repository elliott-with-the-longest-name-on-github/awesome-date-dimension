import pickle
import unittest
from dataclasses import fields

from awesome_date_dimension.config import Column, DimDateConfig


class TestDimDateConfig(unittest.TestCase):
    def test_error_when_column_factory_returns_non_column_value(self):
        # This is the closest you can get to being correct: Returning a dictionary that LOOKS like a column.
        with self.assertRaises(AssertionError):
            DimDateConfig(
                column_factory=lambda name, c: {
                    "name": c.name,
                    "include": c.include,
                    "sort_index": c.sort_index,
                }
            )

    def test_creating_duplicate_column_names_with_column_factory_causes_error(self):
        def column_factory(field_name: str, column: Column) -> Column:
            return Column("dupe", column.include, column.sort_index)

        with self.assertRaises(AssertionError):
            DimDateConfig(column_factory=column_factory)

    def test_creating_duplicate_sort_keys_with_column_factory_causes_error(self):
        def column_factory(field_name: str, column: Column) -> Column:
            return Column(column.name, column.include, 1000)

        with self.assertRaises(AssertionError):
            DimDateConfig(column_factory=column_factory)

    def test_prefixing_with_column_factory(self):
        name_map: dict[str, str] = {}

        def column_factory(field_name: str, column: Column) -> Column:
            if "fiscal" in field_name:
                new_name = "CompanyName" + column.name
                name_map[field_name] = new_name
                return Column(new_name, column.include, column.sort_index)
            return column

        cfg = DimDateConfig(column_factory=column_factory)

        col_field_names = (f.name for f in fields(cfg.columns))
        for f_name in col_field_names:
            col: Column = cfg.columns.__dict__[f_name]
            with self.subTest(
                f"column name should be prefixed with 'CompanyName' if it previously contained 'fiscal': {col.name}"
            ):
                if "fiscal" in f_name:
                    self.assertEqual(name_map[f_name], col.name)

    def test_defaults_are_immutable(self):
        with open("./tests/files/default_dim_date_config.pickle", "rb") as file:
            saved_defaults = pickle.load(file)

        self.assertEqual(DimDateConfig(), saved_defaults)
