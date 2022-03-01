import pickle
import unittest

from awesome_date_dimension.config import Config


class TestConfig(unittest.TestCase):
    def test_defaults_are_immutable(self):
        with open("./tests/files/default_config.pickle", "rb") as file:
            saved_defaults = pickle.load(file)

        self.assertEqual(Config(), saved_defaults)


if __name__ == "main":
    unittest.main()
