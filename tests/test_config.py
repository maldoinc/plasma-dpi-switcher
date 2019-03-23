import os
import unittest

from dpiswitchutils.config import get_default_config_filename


class TestConfig(unittest.TestCase):
    def test_get_default_config_filename(self):
        env_xdg = {"XDG_CONFIG_HOME": "/opt/config"}

        self.assertEqual(os.path.expanduser('~/.config/maldoinc/dpiswitch/profile.json'),
                         get_default_config_filename({}))
        self.assertEqual('/opt/config/maldoinc/dpiswitch/profile.json', get_default_config_filename(env_xdg))


if __name__ == '__main__':
    unittest.main()
