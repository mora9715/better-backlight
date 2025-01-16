from pathlib import Path

KNOWN_LED_NAMES = [
    "tpacpi::kbd_backlight",  # ThinkPad laptops
    "dell::kbd_backlight",  # Dell laptops
]


class SysfsBacklightController:
    brightness_filename = "brightness"
    max_brightness_filename = "max_brightness"
    leds_path = Path("/sys/class/leds")

    def __init__(self, led_name: str | None = None):
        led_name = led_name or self._guess_led_name()

        self.sysfs_path = self.leds_path / led_name

    def get_max_brightness(self) -> int:
        with open(
            self.sysfs_path / self.max_brightness_filename, "r", encoding="utf-8"
        ) as f:
            return int(f.read().strip())

    def get_brightness(self) -> int:
        with open(
            self.sysfs_path / self.brightness_filename, "r", encoding="utf-8"
        ) as f:
            return int(f.read().strip())

    def set_brightness(self, level: int) -> None:
        with open(
            self.sysfs_path / self.brightness_filename, "w", encoding="utf-8"
        ) as f:
            f.write(str(level))

    def _guess_led_name(self) -> str:
        for led_name in KNOWN_LED_NAMES:
            if (self.leds_path / led_name).exists():
                return led_name
        raise ValueError("Your device is not supported by this controller.")
