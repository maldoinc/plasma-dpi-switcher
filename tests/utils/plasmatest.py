import unittest

from utils.plasma import kconfig_generate_groups_params, config_write_get_params, config_read_get_params


class TestPlasma(unittest.TestCase):
    def test_kconfig_generate_groups_params(self):
        self.assertEqual([], kconfig_generate_groups_params(None))
        self.assertEqual([], kconfig_generate_groups_params([]))
        self.assertEqual(['--group', 'x'], kconfig_generate_groups_params(['x']))
        self.assertEqual(['--group', 'x', '--group', 'y'], kconfig_generate_groups_params(['x', 'y']))

    def test_config_write_get_params(self):
        self.assertEqual(['kwriteconfig5', '--file', 'x', '--key', 'Key', 'Val'],
                         config_write_get_params("x", None, "Key", "Val"))
        self.assertEqual(['kwriteconfig5', '--file', 'x', '--key', 'Key', '--group', 'G', 'Val'],
                         config_write_get_params("x", "G", "Key", "Val"))

    def test_config_read_get_params(self):
        self.assertEqual(['kreadconfig5', '--file', 'x', '--key', 'Key'],
                         config_read_get_params("x", None, "Key"))
        self.assertEqual(['kreadconfig5', '--file', 'x', '--key', 'Key', '--group', 'G'],
                         config_read_get_params("x", "G", "Key"))


if __name__ == '__main__':
    unittest.main()
