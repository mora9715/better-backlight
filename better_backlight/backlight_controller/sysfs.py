import logging
from pathlib import Path

KNOWN_LED_NAMES = [
    "tpacpi::kbd_backlight",  # ThinkPad laptops
    "dell::kbd_backlight",  # Dell laptops
    "asus::kbd_backlight",  # ASUS laptops. Untested
    "asus::lightbar",  # Some ASUS gaming laptops. Untested
    "hp::kbd_backlight",  # HP laptops. Untested
    "samsung::kbd_backlight",  # Samsung laptops. Untested
    "toshiba::kbd_backlight",  # Toshiba laptops. Untested
    "clevo::kbd_backlight",  # Clevo laptops (often used by custom brands like System76). Untested
    "msi::kbd_backlight",  # MSI gaming laptops. Untested
    "acer::kbd_backlight",  # Acer laptops. Untested
    "gigabyte::kbd_backlight",  # Gigabyte laptops. Untested
    "alienware::kbd_backlight",  # Alienware laptops (Dell brand). Untested
    "apple::kbd_backlight",  # Apple MacBook laptops. Untested
    "surface::kbd_backlight",  # Microsoft Surface devices. Untested
]

logger = logging.getLogger(__name__)


class SysfsBacklightController:
    brightness_filename = "brightness"
    max_brightness_filename = "max_brightness"
    leds_path = Path("/sys/class/leds")

    def __init__(self, led_name: str | None = None):
        led_name = led_name or self._guess_led_name()

        logger.debug(f"Using LED: {led_name}")

        self.sysfs_path = self.leds_path / led_name

    def get_max_brightness(self) -> int:
        with open(self.sysfs_path / self.max_brightness_filename, "r", encoding="utf-8") as f:
            return int(f.read().strip())

    def get_brightness(self) -> int:
        with open(self.sysfs_path / self.brightness_filename, "r", encoding="utf-8") as f:
            return int(f.read().strip())

    def set_brightness(self, level: int) -> None:
        with open(self.sysfs_path / self.brightness_filename, "w", encoding="utf-8") as f:
            f.write(str(level))

    def _guess_led_name(self) -> str:
        for led_name in KNOWN_LED_NAMES:
            if (self.leds_path / led_name).exists():
                return led_name
        raise ValueError("Your device is not supported by this controller.")
