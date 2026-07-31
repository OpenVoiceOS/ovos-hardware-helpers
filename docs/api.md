
# ovos-hardware-helpers: Complete API Reference

## Module: `ovos_hardware_helpers.led`

File: `ovos_hardware_helpers/led/__init__.py`

### `eval_color(color) -> Color`

Normalizes any color representation to an `ovos_color_parser.models.Color` object.

| Input type | Resolution strategy |
|------------|---------------------|
| `Color` instance | Returned unchanged |
| Hex string `"#rrggbb"` | `sRGBAColor.from_hex_str()` |
| Named string (exact) | `color_from_description(color, fuzzy=False)` |
| Named string (fuzzy) | `color_from_description(color)` on failure of exact |
| 3- or 4-tuple of ints | `sRGBAColor(color)` |
| Anything else | Falls back to `color_from_description("Mycroft blue", fuzzy=False)` |

Logs at DEBUG level while resolving. Logs WARNING on final fallback.

---

### `class AbstractLed` (ABC)

Abstract base class for addressable LED rings and pixel strips.

#### Properties

```python
@property
@abstractmethod
def num_leds(self) -> int
```
Return the logical count of addressable LEDs. Used by animation classes to iterate over indices.

```python
@property
@abstractmethod
def capabilities(self) -> dict
```
Return a dict describing what this LED object supports. Shape is implementation-defined.

#### Methods

```python
@abstractmethod
def set_led(self, led_idx: int, color: tuple, immediate: bool = True)
```
Set a single LED by index.
- `led_idx`: zero-based index
- `color`: `(R, G, B)` tuple of ints 0–255
- `immediate`: if `True`, push to hardware now. If `False`, wait for `show()`

```python
@abstractmethod
def fill(self, color: tuple)
```
Set all LEDs to the same color immediately.
- `color`: `(R, G, B)` tuple of ints 0–255

```python
@abstractmethod
def show(self)
```
Push buffered LED state to hardware. Called after a sequence of `set_led(..., immediate=False)` calls.

```python
@abstractmethod
def shutdown(self)
```
Clean up resources and turn off all LEDs. Must be idempotent.

```python
@staticmethod
def scale_brightness(color_val: int, bright_val: float) -> float
```
Scale one color channel by a brightness factor.
- `color_val`: 0–255 raw channel value
- `bright_val`: 0.0–1.0 scalar
- Returns: float ≤ 255.0

```python
def get_capabilities(self) -> dict
```
Backwards-compatible wrapper. Returns `self.capabilities`. Prefer the property in new code.

---

## Module: `ovos_hardware_helpers.fan`

File: `ovos_hardware_helpers/fan.py`

### `class AbstractFan` (ABC)

Abstract base class for cooling fan controllers.

```python
@abstractmethod
def set_fan_speed(self, percent: int)
```
Set fan speed. `percent` is 0 (off) to 100 (full speed).

```python
@abstractmethod
def get_fan_speed(self) -> int
```
Return current fan speed as 0–100.

```python
@abstractmethod
def get_cpu_temp(self) -> float
```
Return CPU temperature in degrees Celsius. Return `-1.0` when the reading is unavailable.

```python
@abstractmethod
def shutdown(self)
```
Perform cleanup and set fan to a safe idle speed.

---

## Module: `ovos_hardware_helpers.switches`

File: `ovos_hardware_helpers/switches.py`

### `class AbstractSwitches` (ABC)

Abstract base class for physical button/switch handlers.

#### Properties

```python
@property
@abstractmethod
def capabilities(self) -> dict
```
Return a dict of capabilities. Implementations declare which buttons/switches they support.

#### Event callbacks (all abstract)

```python
@abstractmethod
def on_action(self)
```
Called when the action button is pressed.

```python
@abstractmethod
def on_vol_up(self)
```
Called when the volume-up button is pressed.

```python
@abstractmethod
def on_vol_down(self)
```
Called when the volume-down button is pressed.

```python
@abstractmethod
def on_mute(self)
```
Called when mute switch is activated (mute on).

```python
@abstractmethod
def on_unmute(self)
```
Called when mute switch is deactivated (mute off).

```python
@abstractmethod
def shutdown(self)
```
Perform cleanup (e.g. unregister GPIO callbacks).

#### Utility

```python
def get_capabilities(self) -> dict
```
Backwards-compatible wrapper. Returns `self.capabilities`.

---

## Module: `ovos_hardware_helpers.led.animations`

File: `ovos_hardware_helpers/led/animations.py`

### `BLACK`

```python
BLACK = sRGBAColor.from_hex_str("#000000")
```
Module-level constant used by animations to reset LEDs. Defined explicitly because `ovos_color_parser` does not parse the name "black".

---

### `class LedAnimation` (ABC)

Base class for all LED animations.

```python
def __init__(self, leds: AbstractLed, **kwargs)
```
- `leds`: any `AbstractLed` implementation
- `self._delay`: `threading.Event` used for interruptible sleeps

```python
@abstractmethod
def start(self, timeout: Optional[int] = None, one_shot: bool = False)
```
Run the animation. Blocks until complete.
- `timeout`: stop after this many seconds (None = run until `stop()`)
- `one_shot`: if `True`, run one cycle and return

```python
@abstractmethod
def stop(self)
```
Signal the animation to stop. LEDs are reset to black.

---

### `class BreatheLedAnimation(LedAnimation)`

```python
def __init__(self, leds: AbstractLed, color: Color)
```
Brightness pulses from 0 → 1 → 0 continuously. Parameters:
- `self.step = 0.05`: brightness increment per tick
- `self.step_delay = 0.05`: seconds between ticks

Uses `leds.fill()` with brightness-scaled RGB values. After stopping, fills with BLACK.

---

### `class ChaseLedAnimation(LedAnimation)`

```python
def __init__(self, leds: AbstractLed, foreground_color: Color, background_color: Color = BLACK)
```
One foreground-colored LED advances through all indices. All other LEDs remain at `background_color`.
- `self.step_delay = 0.1`: seconds between LED advances

After stopping, fills with BLACK.

---

### `class FillLedAnimation(LedAnimation)`

```python
def __init__(self, leds: AbstractLed, fill_color: Color, reverse: bool = False)
```
Turns LEDs on one by one in index order (or reverse). LEDs stay on after the animation and do not reset to black.
- `self.step_delay = 0.05`: seconds between each LED
- Does not support `timeout` or persistent looping. Warns if `one_shot=False`

---

### `class RefillLedAnimation(LedAnimation)`

```python
def __init__(self, leds: AbstractLed, fill_color: Color, reverse: bool = False)
```
Repeating cycle: fill all LEDs with `fill_color`, then fill all with BLACK. Loops until `stop()` or `timeout`.

Internally composes two `FillLedAnimation` instances.

---

### `class BounceLedAnimation(LedAnimation)`

```python
def __init__(self, leds: AbstractLed, fill_color: Color, reverse: bool = False)
```
Fill LEDs forward, then reverse-fill to BLACK. Direction alternates each cycle. Loops until `stop()` or `timeout`.

---

### `class BlinkLedAnimation(LedAnimation)`

```python
def __init__(self, leds: AbstractLed, color: Color, num_blinks: int = 2, repeat: bool = False)
```
Blinks all LEDs `num_blinks` times (on 250 ms / off 250 ms per blink). If `repeat=True`, pauses 0.5 s and loops. Stops on `stop()` or `timeout`.

---

### `class AlternatingLedAnimation(LedAnimation)`

```python
def __init__(self, leds: AbstractLed, color: Color)
```
Alternates between even-indexed and odd-indexed LEDs being lit. `self.delay = 0.5` s between swaps. Uses `leds.set_led(..., False)` + `leds.show()`. Resets to BLACK after stopping.

---

### `animations` registry

```python
animations: dict[str, type[LedAnimation]] = {
    'breathe': BreatheLedAnimation,
    'chase': ChaseLedAnimation,
    'fill': FillLedAnimation,
    'refill': RefillLedAnimation,
    'bounce': BounceLedAnimation,
    'blink': BlinkLedAnimation,
    'alternating': AlternatingLedAnimation
}
```

Allows animation classes to be looked up by string name. Useful for configuration-driven animation selection.

---
[Home](index.md)
