
# ovos-hardware-helpers

A Python library providing abstract base classes for hardware components used in OVOS (OpenVoiceOS) devices. It defines the contracts that hardware-specific PHAL plugins must implement for LEDs, fans, and input switches. The library also provides a full suite of ready-to-use LED animation classes.

- PyPI package: `ovos_hardware_helpers`
- License: Apache-2.0
- Repository: https://github.com/OpenVoiceOS/ovos_hardware_helpers
- Designed as a drop-in replacement for the hardware interfaces previously embedded in `ovos-plugin-manager`

## What It Provides

`ovos-hardware-helpers` does not talk to hardware directly. It defines Python abstract base classes (ABCs) that hardware PHAL plugins subclass and implement. It also provides concrete LED animation classes that work against any `AbstractLed` implementation.

Three hardware domains are covered:

| Domain | Abstract Class | Module |
|--------|---------------|--------|
| LED ring / pixel strip | `AbstractLed` | `ovos_hardware_helpers.led` |
| Cooling fan | `AbstractFan` | `ovos_hardware_helpers.fan` |
| Physical buttons/switches | `AbstractSwitches` | `ovos_hardware_helpers.switches` |

Color handling is delegated to `ovos-color-parser`, which supports hex strings, CSS color names, fuzzy name matching, and RGB tuples.

## Installation

```bash
pip install ovos_hardware_helpers
```

Dependency: `ovos-color-parser`

## AbstractLed — `ovos_hardware_helpers/led/__init__.py`

```python
class AbstractLed:
    @property
    @abstractmethod
    def num_leds(self) -> int: ...

    @property
    @abstractmethod
    def capabilities(self) -> dict: ...

    @abstractmethod
    def set_led(self, led_idx: int, color: tuple, immediate: bool = True): ...

    @abstractmethod
    def fill(self, color: tuple): ...

    @abstractmethod
    def show(self): ...

    @abstractmethod
    def shutdown(self): ...

    @staticmethod
    def scale_brightness(color_val: int, bright_val: float) -> float: ...

    def get_capabilities(self) -> dict: ...  # backwards-compat alias for .capabilities
```

`eval_color(color)` is a module-level helper that normalises a color argument to an `ovos_color_parser.models.Color` object. It accepts:

- A `Color` instance — returned as-is
- A hex string like `"#ff0000"` — parsed via `sRGBAColor.from_hex_str()`
- A CSS color name string — resolved via `color_from_description()`, with fuzzy fallback
- An RGB or RGBA tuple of 3–4 ints — wrapped in `sRGBAColor`
- Anything else — falls back to "Mycroft Blue"

## AbstractFan — `ovos_hardware_helpers/fan.py`

```python
class AbstractFan:
    @abstractmethod
    def set_fan_speed(self, percent: int): ...
    # percent: 0–100

    @abstractmethod
    def get_fan_speed(self) -> int: ...
    # returns 0–100

    @abstractmethod
    def get_cpu_temp(self) -> float: ...
    # returns celsius, or -1.0 if unavailable

    @abstractmethod
    def shutdown(self): ...
    # cleanup and set to a reasonable speed
```

## AbstractSwitches — `ovos_hardware_helpers/switches.py`

```python
class AbstractSwitches:
    @property
    @abstractmethod
    def capabilities(self) -> dict: ...

    @abstractmethod
    def on_action(self): ...

    @abstractmethod
    def on_vol_up(self): ...

    @abstractmethod
    def on_vol_down(self): ...

    @abstractmethod
    def on_mute(self): ...

    @abstractmethod
    def on_unmute(self): ...

    @abstractmethod
    def shutdown(self): ...

    def get_capabilities(self) -> dict: ...  # backwards-compat alias for .capabilities
```

## LED Animations — `ovos_hardware_helpers/led/animations.py`

All animation classes inherit from `LedAnimation`. The `start()` method runs synchronously (blocking) until the animation ends or `stop()` is called. Animations use `threading.Event` for delays so they can be interrupted cleanly.

```python
BLACK = sRGBAColor.from_hex_str("#000000")

class LedAnimation:
    def __init__(self, leds: AbstractLed, **kwargs): ...

    @abstractmethod
    def start(self, timeout: Optional[int] = None, one_shot: bool = False): ...

    @abstractmethod
    def stop(self): ...
```

### Concrete Animation Classes

| Class | Constructor arguments | Behaviour |
|-------|-----------------------|-----------|
| `BreatheLedAnimation` | `leds, color` | All LEDs pulse dim/bright. `step=0.05`, `step_delay=0.05 s` |
| `ChaseLedAnimation` | `leds, foreground_color, background_color=BLACK` | One lit LED chases around the ring at `step_delay=0.1 s` |
| `FillLedAnimation` | `leds, fill_color, reverse=False` | LEDs turn on in sequence and stay on. `one_shot` only |
| `RefillLedAnimation` | `leds, fill_color, reverse=False` | Repeating fill-on then fill-off cycle |
| `BounceLedAnimation` | `leds, fill_color, reverse=False` | Fill forward then reverse-fill to black, repeat |
| `BlinkLedAnimation` | `leds, color, num_blinks=2, repeat=False` | Blink `num_blinks` times; optionally repeat with 0.5 s pause |
| `AlternatingLedAnimation` | `leds, color` | Even/odd LEDs alternate at 0.5 s intervals |

The module exposes a registry dict:

```python
animations = {
    'breathe': BreatheLedAnimation,
    'chase': ChaseLedAnimation,
    'fill': FillLedAnimation,
    'refill': RefillLedAnimation,
    'bounce': BounceLedAnimation,
    'blink': BlinkLedAnimation,
    'alternating': AlternatingLedAnimation
}
```

## Usage Examples

### Implementing a custom LED ring

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

### Running an animation

```python
from ovos_hardware_helpers.led.animations import BreatheLedAnimation
from ovos_color_parser import color_from_description

leds = MyNeopixelLed(board.D18, 12)
color = color_from_description("Mycroft Blue")
anim = BreatheLedAnimation(leds, color)
anim.start(timeout=10)   # run for 10 seconds
```

### Using the animations registry

```python
from ovos_hardware_helpers.led.animations import animations

AnimClass = animations['chase']
anim = AnimClass(leds, foreground_color=color)
anim.start(one_shot=True)
```

### Implementing a fan controller

```python
from ovos_hardware_helpers.fan import AbstractFan

class GpioPwmFan(AbstractFan):
    def set_fan_speed(self, percent: int):
        # write PWM duty cycle
        ...

    def get_fan_speed(self) -> int:
        return self._current_percent

    def get_cpu_temp(self) -> float:
        with open("/sys/class/thermal/thermal_zone0/temp") as f:
            return int(f.read()) / 1000.0

    def shutdown(self):
        self.set_fan_speed(30)
```

## Cross-References

- **ovos-PHAL** — PHAL plugins implement `AbstractLed`, `AbstractFan`, and `AbstractSwitches` to expose hardware to OVOS core
- **ovos-plugin-manager** — previous home of equivalent hardware interfaces; `ovos-hardware-helpers` is the replacement
- **ovos-color-parser** — required dependency for all color handling
- PHAL plugin examples: `ovos-PHAL-plugin-mk2`, hardware-specific plugins for SJ201 board
