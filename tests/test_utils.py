import unittest
from dpiswitchutils.utils import display_get_scaling_str, scale_factor_to_font_dpi, font_dpi_to_scale_factor, \
    try_parse_int


class TestUtils(unittest.TestCase):
    def test_display_get_scaling_str(self):
        self.assertEqual('', display_get_scaling_str([], 1))
        self.assertEqual('a=1', display_get_scaling_str(['a'], 1))
        self.assertEqual('a=1.5;b=1.5', display_get_scaling_str(['a', 'b'], 1.5))

    def test_get_dpi(self):
        self.assertEqual(96, scale_factor_to_font_dpi(1))
        self.assertEqual(120, scale_factor_to_font_dpi(1.25))
        self.assertEqual(144, scale_factor_to_font_dpi(1.5))
        self.assertEqual(192, scale_factor_to_font_dpi(2))

    def test_font_dpi_to_scale_factor(self):
        self.assertEqual(1, font_dpi_to_scale_factor(0))
        self.assertEqual(1, font_dpi_to_scale_factor(96))
        self.assertEqual(1.5, font_dpi_to_scale_factor(144))

    def test_try_parse_int(self):
        self.assertEqual(10, try_parse_int('10'))
        self.assertEqual(None, try_parse_int('', None))
        self.assertEqual(1, try_parse_int('', 1))


if __name__ == '__main__':
    unittest.main()
