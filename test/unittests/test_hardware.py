import unittest


class TestLed(unittest.TestCase):
    def test_color(self):
        from ovos_color_parser import color_from_description
        from ovos_color_parser.models import Color, sRGBAColor


        # Check types
        color = color_from_description("Mycroft Blue")
        self.assertIsInstance(color, Color)

        # from_description
        self.assertEqual(color.name, "Mycroft Blue")
        with self.assertRaises(ValueError):
            color_from_description('not a color')

        # from_hex
        self.assertEqual(sRGBAColor.from_hex_str('#ffffff'), sRGBAColor.from_hex_str("#FFFFFF"))

    def test_abstract_led(self):
        from ovos_hardware_helpers.led import AbstractLed
        # TODO

    def test_led_animation(self):
        from ovos_hardware_helpers.led.animations import LedAnimation
        # TODO

    def test_breathe_led_animation(self):
        from ovos_hardware_helpers.led.animations import \
            BreatheLedAnimation
        # TODO

    def test_chase_led_animation(self):
        from ovos_hardware_helpers.led.animations import \
            ChaseLedAnimation
        # TODO

    def test_fill_led_animation(self):
        from ovos_hardware_helpers.led.animations import FillLedAnimation
        # TODO

    def test_refill_led_animation(self):
        from ovos_hardware_helpers.led.animations import \
            RefillLedAnimation
        # TODO

    def test_bounce_led_animation(self):
        from ovos_hardware_helpers.led.animations import \
            BounceLedAnimation
        # TODO

    def test_Blink_led_animation(self):
        from ovos_hardware_helpers.led.animations import \
            BlinkLedAnimation
        # TODO

    def test_alternating_led_animation(self):
        from ovos_hardware_helpers.led.animations import \
            AlternatingLedAnimation
        # TODO

    def test_animations(self):
        from ovos_hardware_helpers.led.animations import animations, \
            LedAnimation
        for key, val in animations.items():
            self.assertIsInstance(key, str)
            self.assertTrue(issubclass(val, LedAnimation))


class TestFan(unittest.TestCase):
    from ovos_hardware_helpers.fan import AbstractFan
    # TODO


class TestSwitches(unittest.TestCase):
    from ovos_hardware_helpers.switches import AbstractSwitches
    # TODO
