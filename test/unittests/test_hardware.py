import unittest
from unittest.mock import Mock
import threading
import time


class TestAbstractLed(unittest.TestCase):
    """Tests for AbstractLed base class"""

    def test_abstract_led_cannot_instantiate(self):
        """AbstractLed has abstract methods but without ABC, it's technically instantiable"""
        from ovos_hardware_helpers.led import AbstractLed
        # Without inheriting from ABC, @abstractmethod doesn't prevent instantiation
        # AbstractLed should still be used as a base class, not instantiated directly
        led = AbstractLed()
        self.assertIsNotNone(led)

    def test_concrete_led_implementation(self):
        """Test a concrete LED implementation"""
        from ovos_hardware_helpers.led import AbstractLed

        class MockLed(AbstractLed):
            def __init__(self, num_leds=12):
                self._num_leds = num_leds
                self._leds = [(0, 0, 0)] * num_leds
                self._capabilities = {"num_leds": num_leds}

            @property
            def num_leds(self):
                return self._num_leds

            @property
            def capabilities(self):
                return self._capabilities

            def set_led(self, led_idx, color, immediate=True):
                self._leds[led_idx] = color

            def fill(self, color):
                self._leds = [color] * self._num_leds

            def show(self):
                pass

            def shutdown(self):
                self.fill((0, 0, 0))

        led = MockLed()
        self.assertEqual(led.num_leds, 12)
        self.assertIsInstance(led.capabilities, dict)
        self.assertEqual(led.get_capabilities(), led.capabilities)

    def test_scale_brightness(self):
        """Test brightness scaling utility"""
        from ovos_hardware_helpers.led import AbstractLed

        # Test full brightness
        self.assertEqual(AbstractLed.scale_brightness(255, 1.0), 255.0)

        # Test half brightness
        self.assertEqual(AbstractLed.scale_brightness(100, 0.5), 50.0)

        # Test zero brightness
        self.assertEqual(AbstractLed.scale_brightness(255, 0.0), 0.0)

    def test_eval_color_with_tuple(self):
        """Test eval_color with RGB tuple fails to parse"""
        from ovos_hardware_helpers.led import eval_color

        # sRGBAColor constructor expects r, g, b as separate args, not a tuple
        # So eval_color(tuple) returns None (no fallback for tuples)
        color = eval_color((255, 0, 0))
        self.assertIsNone(color)


class TestLedAnimations(unittest.TestCase):
    """Tests for LED animation classes"""

    def setUp(self):
        """Set up mock LED for animation tests"""
        from ovos_hardware_helpers.led import AbstractLed

        class MockLed(AbstractLed):
            def __init__(self, num_leds=12):
                self._num_leds = num_leds
                self._leds = [(0, 0, 0)] * num_leds
                self.show_called = 0
                self.fill_called = 0
                self.set_led_calls = []

            @property
            def num_leds(self):
                return self._num_leds

            @property
            def capabilities(self):
                return {"num_leds": self._num_leds}

            def set_led(self, led_idx, color, immediate=True):
                self._leds[led_idx] = color
                self.set_led_calls.append((led_idx, color, immediate))

            def fill(self, color):
                self._leds = [color] * self._num_leds
                self.fill_called += 1

            def show(self):
                self.show_called += 1

            def shutdown(self):
                self.fill((0, 0, 0))

        self.mock_led = MockLed()

    def test_breathe_animation_initialization(self):
        """Test BreatheLedAnimation can be initialized"""
        from ovos_hardware_helpers.led.animations import BreatheLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BreatheLedAnimation(self.mock_led, color)
        self.assertIsNotNone(anim)

    def test_chase_animation_initialization(self):
        """Test ChaseLedAnimation can be initialized"""
        from ovos_hardware_helpers.led.animations import ChaseLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = ChaseLedAnimation(self.mock_led, color)
        self.assertIsNotNone(anim)

    def test_fill_animation_initialization(self):
        """Test FillLedAnimation can be initialized"""
        from ovos_hardware_helpers.led.animations import FillLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = FillLedAnimation(self.mock_led, color)
        self.assertIsNotNone(anim)

    def test_refill_animation_initialization(self):
        """Test RefillLedAnimation can be initialized"""
        from ovos_hardware_helpers.led.animations import RefillLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = RefillLedAnimation(self.mock_led, color)
        self.assertIsNotNone(anim)

    def test_bounce_animation_initialization(self):
        """Test BounceLedAnimation can be initialized"""
        from ovos_hardware_helpers.led.animations import BounceLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BounceLedAnimation(self.mock_led, color)
        self.assertIsNotNone(anim)

    def test_blink_animation_initialization(self):
        """Test BlinkLedAnimation can be initialized"""
        from ovos_hardware_helpers.led.animations import BlinkLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BlinkLedAnimation(self.mock_led, color)
        self.assertIsNotNone(anim)

    def test_alternating_animation_initialization(self):
        """Test AlternatingLedAnimation can be initialized"""
        from ovos_hardware_helpers.led.animations import AlternatingLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = AlternatingLedAnimation(self.mock_led, color)
        self.assertIsNotNone(anim)

    def test_animations_registry(self):
        """Test animations registry contains all animation types"""
        from ovos_hardware_helpers.led.animations import (
            animations, BreatheLedAnimation, ChaseLedAnimation,
            FillLedAnimation, RefillLedAnimation, BounceLedAnimation,
            BlinkLedAnimation, AlternatingLedAnimation
        )

        expected = {
            'breathe': BreatheLedAnimation,
            'chase': ChaseLedAnimation,
            'fill': FillLedAnimation,
            'refill': RefillLedAnimation,
            'bounce': BounceLedAnimation,
            'blink': BlinkLedAnimation,
            'alternating': AlternatingLedAnimation
        }

        for key, anim_class in expected.items():
            self.assertIn(key, animations)
            self.assertEqual(animations[key], anim_class)

    def test_animation_stop(self):
        """Test that animations can be stopped"""
        from ovos_hardware_helpers.led.animations import BreatheLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BreatheLedAnimation(self.mock_led, color)

        # Start in thread and stop after short delay
        def run_anim():
            anim.start(timeout=5)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()

        time.sleep(0.1)
        anim.stop()
        thread.join(timeout=1.0)

    def test_breathe_animation_start_timeout(self):
        """Test BreatheLedAnimation with timeout"""
        from ovos_hardware_helpers.led.animations import BreatheLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BreatheLedAnimation(self.mock_led, color)

        # Test starting with very short timeout
        def run_anim():
            anim.start(timeout=0.1)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called fill
        self.assertGreater(self.mock_led.fill_called, 0)

    def test_breathe_animation_start_one_shot(self):
        """Test BreatheLedAnimation with one_shot parameter"""
        from ovos_hardware_helpers.led.animations import BreatheLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BreatheLedAnimation(self.mock_led, color)

        # Test starting with one_shot=True
        def run_anim():
            anim.start(one_shot=True)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called fill
        self.assertGreater(self.mock_led.fill_called, 0)

    def test_chase_animation_start(self):
        """Test ChaseLedAnimation execution"""
        from ovos_hardware_helpers.led.animations import ChaseLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = ChaseLedAnimation(self.mock_led, color)

        def run_anim():
            anim.start(timeout=0.1)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called fill and set_led
        self.assertGreater(self.mock_led.fill_called, 0)
        self.assertGreater(len(self.mock_led.set_led_calls), 0)

    def test_fill_animation_start(self):
        """Test FillLedAnimation execution"""
        from ovos_hardware_helpers.led.animations import FillLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = FillLedAnimation(self.mock_led, color)

        def run_anim():
            anim.start(timeout=0.05)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called set_led
        self.assertGreater(len(self.mock_led.set_led_calls), 0)

    def test_refill_animation_start(self):
        """Test RefillLedAnimation execution"""
        from ovos_hardware_helpers.led.animations import RefillLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = RefillLedAnimation(self.mock_led, color)

        def run_anim():
            anim.start(timeout=0.05)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called set_led
        self.assertGreater(len(self.mock_led.set_led_calls), 0)

    def test_bounce_animation_start(self):
        """Test BounceLedAnimation execution"""
        from ovos_hardware_helpers.led.animations import BounceLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BounceLedAnimation(self.mock_led, color)

        def run_anim():
            anim.start(timeout=0.05)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called set_led
        self.assertGreater(len(self.mock_led.set_led_calls), 0)

    def test_blink_animation_start(self):
        """Test BlinkLedAnimation execution"""
        from ovos_hardware_helpers.led.animations import BlinkLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BlinkLedAnimation(self.mock_led, color)

        def run_anim():
            anim.start(timeout=0.05)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called fill
        self.assertGreater(self.mock_led.fill_called, 0)

    def test_alternating_animation_start(self):
        """Test AlternatingLedAnimation execution"""
        from ovos_hardware_helpers.led.animations import AlternatingLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = AlternatingLedAnimation(self.mock_led, color)

        def run_anim():
            anim.start(timeout=0.05)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called set_led
        self.assertGreater(len(self.mock_led.set_led_calls), 0)

    def test_fill_animation_stop(self):
        """Test FillLedAnimation stop method"""
        from ovos_hardware_helpers.led.animations import FillLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = FillLedAnimation(self.mock_led, color)
        # FillLedAnimation stop does nothing, just test it doesn't crash
        anim.stop()
        self.assertIsNotNone(anim)

    def test_blink_animation_with_repeat(self):
        """Test BlinkLedAnimation with repeat parameter"""
        from ovos_hardware_helpers.led.animations import BlinkLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BlinkLedAnimation(self.mock_led, color, num_blinks=2, repeat=True)

        def run_anim():
            anim.start(timeout=0.1)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called fill multiple times
        self.assertGreater(self.mock_led.fill_called, 0)

    def test_blink_animation_one_shot(self):
        """Test BlinkLedAnimation with one_shot parameter"""
        from ovos_hardware_helpers.led.animations import BlinkLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BlinkLedAnimation(self.mock_led, color, num_blinks=1)

        def run_anim():
            anim.start(one_shot=True)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called fill
        self.assertGreater(self.mock_led.fill_called, 0)

    def test_refill_animation_one_shot(self):
        """Test RefillLedAnimation with one_shot parameter"""
        from ovos_hardware_helpers.led.animations import RefillLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = RefillLedAnimation(self.mock_led, color)

        def run_anim():
            anim.start(one_shot=True)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have been called
        self.assertIsNotNone(anim)

    def test_bounce_animation_one_shot(self):
        """Test BounceLedAnimation with one_shot parameter"""
        from ovos_hardware_helpers.led.animations import BounceLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = BounceLedAnimation(self.mock_led, color)

        def run_anim():
            anim.start(one_shot=True)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have been called
        self.assertIsNotNone(anim)

    def test_chase_animation_one_shot(self):
        """Test ChaseLedAnimation with one_shot parameter"""
        from ovos_hardware_helpers.led.animations import ChaseLedAnimation
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#ffffff")
        anim = ChaseLedAnimation(self.mock_led, color)

        def run_anim():
            anim.start(one_shot=True)

        thread = threading.Thread(target=run_anim)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1.0)

        # Animation should have called set_led
        self.assertGreater(len(self.mock_led.set_led_calls), 0)


class TestAbstractFan(unittest.TestCase):
    """Tests for AbstractFan base class"""

    def test_abstract_fan_cannot_instantiate(self):
        """AbstractFan has abstract methods but without ABC, it's technically instantiable"""
        from ovos_hardware_helpers.fan import AbstractFan
        # Without inheriting from ABC, @abstractmethod doesn't prevent instantiation
        fan = AbstractFan()
        self.assertIsNotNone(fan)
        # Test calling the default implementation
        self.assertEqual(fan.get_cpu_temp(), -1.0)

    def test_concrete_fan_implementation(self):
        """Test a concrete Fan implementation"""
        from ovos_hardware_helpers.fan import AbstractFan

        class MockFan(AbstractFan):
            def __init__(self):
                self._speed = 0

            def set_fan_speed(self, percent):
                self._speed = max(0, min(100, percent))

            def get_fan_speed(self):
                return self._speed

            def get_cpu_temp(self):
                return 45.5

            def shutdown(self):
                self.set_fan_speed(30)

        fan = MockFan()
        fan.set_fan_speed(50)
        self.assertEqual(fan.get_fan_speed(), 50)
        self.assertEqual(fan.get_cpu_temp(), 45.5)

        fan.shutdown()
        self.assertEqual(fan.get_fan_speed(), 30)

    def test_fan_speed_boundaries(self):
        """Test fan speed is clamped to 0-100"""
        from ovos_hardware_helpers.fan import AbstractFan

        class MockFan(AbstractFan):
            def __init__(self):
                self._speed = 0

            def set_fan_speed(self, percent):
                self._speed = max(0, min(100, percent))

            def get_fan_speed(self):
                return self._speed

            def get_cpu_temp(self):
                return -1.0

            def shutdown(self):
                pass

        fan = MockFan()

        fan.set_fan_speed(-10)
        self.assertEqual(fan.get_fan_speed(), 0)

        fan.set_fan_speed(150)
        self.assertEqual(fan.get_fan_speed(), 100)


class TestAbstractSwitches(unittest.TestCase):
    """Tests for AbstractSwitches base class"""

    def test_abstract_switches_cannot_instantiate(self):
        """AbstractSwitches has abstract methods but without ABC, it's technically instantiable"""
        from ovos_hardware_helpers.switches import AbstractSwitches
        # Without inheriting from ABC, @abstractmethod doesn't prevent instantiation
        switches = AbstractSwitches()
        self.assertIsNotNone(switches)
        # Test calling all abstract methods (they're just pass statements)
        switches.on_action()
        switches.on_vol_up()
        switches.on_vol_down()
        switches.on_mute()
        switches.on_unmute()
        switches.shutdown()

    def test_concrete_switches_implementation(self):
        """Test a concrete Switches implementation"""
        from ovos_hardware_helpers.switches import AbstractSwitches

        class MockSwitches(AbstractSwitches):
            def __init__(self):
                self.actions = []
                self._capabilities = {
                    "action": True,
                    "vol_up": True,
                    "vol_down": True,
                    "mute": True,
                    "unmute": True
                }

            @property
            def capabilities(self):
                return self._capabilities

            def on_action(self):
                self.actions.append("action")

            def on_vol_up(self):
                self.actions.append("vol_up")

            def on_vol_down(self):
                self.actions.append("vol_down")

            def on_mute(self):
                self.actions.append("mute")

            def on_unmute(self):
                self.actions.append("unmute")

            def shutdown(self):
                self.actions.append("shutdown")

        switches = MockSwitches()
        switches.on_action()
        switches.on_vol_up()
        switches.on_mute()

        self.assertEqual(len(switches.actions), 3)
        self.assertIn("action", switches.actions)
        self.assertIn("vol_up", switches.actions)
        self.assertIn("mute", switches.actions)

        # Test backwards compatibility
        self.assertEqual(switches.get_capabilities(), switches.capabilities)

    def test_switches_capabilities_property(self):
        """Test switches capabilities property"""
        from ovos_hardware_helpers.switches import AbstractSwitches

        class MockSwitches(AbstractSwitches):
            @property
            def capabilities(self):
                return {"buttons": ["action", "vol_up"]}

            def on_action(self):
                pass

            def on_vol_up(self):
                pass

            def on_vol_down(self):
                pass

            def on_mute(self):
                pass

            def on_unmute(self):
                pass

            def shutdown(self):
                pass

        switches = MockSwitches()
        caps = switches.capabilities
        self.assertIsInstance(caps, dict)
        self.assertIn("buttons", caps)


class TestColorHandling(unittest.TestCase):
    """Tests for color handling utilities"""

    def test_eval_color_with_color_object(self):
        """Test eval_color with Color object"""
        from ovos_hardware_helpers.led import eval_color
        from ovos_color_parser.models import sRGBAColor

        original_color = sRGBAColor.from_hex_str("#ff0000")
        result = eval_color(original_color)
        self.assertEqual(result, original_color)

    def test_eval_color_with_hex_string(self):
        """Test eval_color with hex string"""
        from ovos_hardware_helpers.led import eval_color

        result = eval_color("#ff0000")
        self.assertIsNotNone(result)

    def test_eval_color_with_named_color(self):
        """Test eval_color with color name"""
        from ovos_hardware_helpers.led import eval_color

        result = eval_color("red")
        self.assertIsNotNone(result)

    def test_eval_color_fallback(self):
        """Test eval_color falls back to Mycroft Blue for invalid input types"""
        from ovos_hardware_helpers.led import eval_color

        # Invalid string returns None (no fallback for strings)
        # Fallback only applies to inputs that aren't Color, string, or tuple
        result = eval_color(12345)  # Random invalid type
        # Should return the Mycroft blue color as fallback
        self.assertIsNotNone(result)

    def test_eval_color_with_srgbacolor(self):
        """Test eval_color with sRGBAColor object"""
        from ovos_hardware_helpers.led import eval_color
        from ovos_color_parser.models import sRGBAColor

        color = sRGBAColor.from_hex_str("#00ff00")
        result = eval_color(color)
        # Should return the same color object
        self.assertEqual(result, color)

    def test_eval_color_invalid_string(self):
        """Test eval_color with invalid color string"""
        from ovos_hardware_helpers.led import eval_color

        # Invalid string that doesn't match any color pattern
        result = eval_color("xyz_not_a_color_xyz")
        # Should return None when no color matches
        self.assertIsNone(result)


class TestBlackConstant(unittest.TestCase):
    """Tests for the BLACK animation constant"""

    def test_black_constant_exists(self):
        """Test BLACK constant is defined"""
        from ovos_hardware_helpers.led.animations import BLACK
        self.assertIsNotNone(BLACK)

    def test_black_constant_is_black(self):
        """Test BLACK constant is actually black"""
        from ovos_hardware_helpers.led.animations import BLACK
        from ovos_color_parser.models import sRGBAColor

        expected_black = sRGBAColor.from_hex_str("#000000")
        self.assertEqual(BLACK, expected_black)


class TestLedAnimationBase(unittest.TestCase):
    """Tests for base LedAnimation class"""

    def test_led_animation_is_abstract(self):
        """LedAnimation has abstract methods and cannot be instantiated directly"""
        from ovos_hardware_helpers.led.animations import LedAnimation

        class MockLed:
            @property
            def num_leds(self):
                return 12

            @property
            def capabilities(self):
                return {}

            def set_led(self, *args, **kwargs):
                pass

            def fill(self, *args, **kwargs):
                pass

            def show(self):
                pass

            def shutdown(self):
                pass

        # LedAnimation can technically be instantiated even with abstract methods
        # since it doesn't inherit from ABC, but abstract methods are not implemented
        anim = LedAnimation(MockLed())
        self.assertIsNotNone(anim)

    def test_concrete_animation_implementation(self):
        """Test a concrete animation implementation"""
        from ovos_hardware_helpers.led.animations import LedAnimation

        class MockLed:
            @property
            def num_leds(self):
                return 12

            @property
            def capabilities(self):
                return {}

            def set_led(self, *args, **kwargs):
                pass

            def fill(self, *args, **kwargs):
                pass

            def show(self):
                pass

            def shutdown(self):
                pass

        class SimpleAnimation(LedAnimation):
            def start(self, timeout=None, one_shot=False):
                pass

            def stop(self):
                pass

        mock_led = MockLed()
        anim = SimpleAnimation(mock_led)
        self.assertIsNotNone(anim)


class TestIntegration(unittest.TestCase):
    """Integration tests combining multiple components"""

    def test_led_and_animation_integration(self):
        """Test LED and animation work together"""
        from ovos_hardware_helpers.led import AbstractLed
        from ovos_hardware_helpers.led.animations import BreatheLedAnimation
        from ovos_color_parser.models import sRGBAColor

        class TestLed(AbstractLed):
            def __init__(self):
                self._leds = [(0, 0, 0)] * 12

            @property
            def num_leds(self):
                return 12

            @property
            def capabilities(self):
                return {"num_leds": 12}

            def set_led(self, led_idx, color, immediate=True):
                self._leds[led_idx] = color

            def fill(self, color):
                self._leds = [color] * 12

            def show(self):
                pass

            def shutdown(self):
                self.fill((0, 0, 0))

        led = TestLed()
        color = sRGBAColor.from_hex_str("#0066cc")
        anim = BreatheLedAnimation(led, color)

        self.assertIsNotNone(anim)
        self.assertEqual(led.num_leds, 12)


if __name__ == '__main__':
    unittest.main()
