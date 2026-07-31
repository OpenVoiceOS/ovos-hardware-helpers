# ovos-hardware-helpers

`ovos-hardware-helpers` defines the abstract base classes that OVOS (OpenVoiceOS) PHAL plugins implement for LEDs, fans, and switches. It also provides a set of ready-to-use LED animation classes. It replaces the hardware interfaces previously in [ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager/tree/dev/ovos_plugin_manager/hardware) and uses [ovos-color-parser](https://github.com/OpenVoiceOS/ovos-color-parser) to handle colors.

## Install

```bash
pip install ovos_hardware_helpers
```

## Usage

Subclass `AbstractLed`, `AbstractFan`, or `AbstractSwitches` to expose a hardware component to OVOS:

```python
from ovos_hardware_helpers.led import AbstractLed

class MyNeopixelLed(AbstractLed):
    def __init__(self, pin, count):
        import neopixel
        self._strip = neopixel.NeoPixel(pin, count)

    @property
    def num_leds(self) -> int:
        return len(self._strip)

    @property
    def capabilities(self) -> dict:
        return {"num_leds": self.num_leds}

    def set_led(self, led_idx: int, color: tuple, immediate: bool = True):
        self._strip[led_idx] = color
        if immediate:
            self._strip.show()

    def fill(self, color: tuple):
        self._strip.fill(color)
        self._strip.show()

    def show(self):
        self._strip.show()

    def shutdown(self):
        self.fill((0, 0, 0))
```

Run one of the built-in LED animations against any `AbstractLed` implementation:

```python
from ovos_hardware_helpers.led.animations import BreatheLedAnimation
from ovos_color_parser import color_from_description

leds = MyNeopixelLed(board.D18, 12)
color = color_from_description("Mycroft Blue")
anim = BreatheLedAnimation(leds, color)
anim.start(timeout=10)  # runs for 10 seconds
```

See [docs/index.md](docs/index.md) for the full list of animations and the fan and switches interfaces, and [docs/api.md](docs/api.md) for the complete API reference.

## Related projects

- [ovos-PHAL](https://github.com/OpenVoiceOS/ovos-PHAL): the plugin framework that loads hardware plugins implementing these interfaces
- [ovos-color-parser](https://github.com/OpenVoiceOS/ovos-color-parser): required dependency for color handling
- [ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager): previous home of the hardware interfaces this library replaces

## License

Apache-2.0. See [LICENSE](LICENSE).
