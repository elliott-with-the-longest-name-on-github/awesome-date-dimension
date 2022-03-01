import pickle
import unittest

from awesome_date_dimension.config import ConfigVersion, config_factory


class TestConfigFactory(unittest.TestCase):
    def test_invalid_version_raises_typeerror(self):
        with self.assertRaises(TypeError):
            config_factory("v-1")

    def test_defaults_are_immutable(self):
        for version in ConfigVersion:
            template = (
                "Defaults for a Config version have changed or were never stored. Did you forget to pickle "
                "defaults for a new version? version={version}"
            )
            with self.subTest(template.format(version=version)):
                with open(
                    f"./tests/files/config_factory_{version}.pickle", "rb"
                ) as file:
                    saved_defaults = pickle.load(file)
                    self.assertEqual(config_factory(version), saved_defaults)


if __name__ == "main":
    unittest.main()
