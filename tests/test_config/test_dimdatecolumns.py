import pickle
import unittest

from awesome_date_dimension.config import Column, DimDateColumns


class TestDimDateColumns(unittest.TestCase):
    def test_failure_when_key_column_is_excluded(self):
        with self.assertRaises(AssertionError):
            DimDateColumns(date_key=Column("DateKey", False, 1000))

    def test_failure_when_duplicate_colnames(self):
        with self.assertRaises(AssertionError):
            DimDateColumns(Column("Dupe", True, 1000), Column("Dupe", True, 2000))

    def test_failure_when_duplicate_sortkeys(self):
        with self.assertRaises(AssertionError):
            DimDateColumns(
                Column("DateKey", True, 1000),
                Column("DateKey", True, 1000),
            )

    def test_defaults_are_immutable(self):
        with open("./tests/files/default_dim_date_columns.pickle", "rb") as file:
            saved_defaults = pickle.load(file)

        self.assertEqual(DimDateColumns(), saved_defaults)


if __name__ == "main":
    unittest.main()
