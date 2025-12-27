from abc import abstractmethod
from typing import Union

from ovos_utils.log import LOG

from ovos_color_parser.matching import color_from_description, is_hex_code_valid
from ovos_color_parser.models import Color, sRGBAColor

def eval_color(color):
    LOG.debug(f"evaluating color {color}")
    if isinstance(color, Color):
        return color
    elif isinstance(color, str):
        if is_hex_code_valid(color):
            try:
                return sRGBAColor.from_hex_str(color)
            except Exception as e:
                LOG.debug(f"Could not get color {color} from hex code: {e}")
        try:
            LOG.debug(f"Color is string, but not hex  {color}  {color_from_description(color, fuzzy=False)}")
            # Try an exact match of the color name
            return color_from_description(color, fuzzy=False)
        except Exception as e:
            LOG.debug(f"Could not get color {color} from description: {e}. Trying fuzzy match")
            try:
                return color_from_description(color)
            except Exception as e:
                LOG.debug(f"Could not get color {color}: {e}")
    elif isinstance(color, tuple) and 3 <= len(color) <= 4:
        try:
            color = sRGBAColor(color)
            return color
        except Exception as e:
            LOG.debug(f"Could not get color {color} from RGB: {e}")
    else:
        LOG.warning(f"Could not set color {color}: Defaulting to Mycroft Blue")
        return color_from_description("Mycroft blue", fuzzy=False)


class AbstractLed:
    @property
    @abstractmethod
    def num_leds(self) -> int:
        """
        Return the logical number of addressable LEDs.
        """

    @property
    @abstractmethod
    def capabilities(self) -> dict:
        """
        Return a dict of capabilities this object supports
        """

    @abstractmethod
    def set_led(self, led_idx: int, color: tuple, immediate: bool = True):
        """
        Set a specific LED to a particular color.
        :param led_idx: index of LED to modify
        :param color: RGB color value as ints
        :param immediate: If true, update LED immediately, else wait for `show`
        """

    # TODO: get_led?

    @abstractmethod
    def fill(self, color: tuple):
        """
        Set all LEDs to a particular color.
        :param color: RGB color value as a tuple of ints
        """

    @abstractmethod
    def show(self):
        """
        Update LEDs to match values set in this class.
        """

    @abstractmethod
    def shutdown(self):
        """
        Perform any cleanup and turn off LEDs.
        """

    @staticmethod
    def scale_brightness(color_val: int, bright_val: float) -> float:
        """
        Scale an individual color value by a specified brightness.
        :param color_val: 0-255 R, G, or B value
        :param bright_val: 0.0-1.0 brightness scalar value
        :returns: Float modified color value to account for brightness
        """
        return min(255.0, color_val * bright_val)

    def get_capabilities(self) -> dict:
        """
        Backwards-compatible method to return `self.capabilities`
        """
        return self.capabilities
