from better_backlight.backlight_controller.factory import (
    SysfsBacklightController,
    get_backlight_controller,
)


def test_get_backlight_controller(fake_fs):
    fake_fs.create_file("/sys/class/leds/tpacpi::kbd_backlight/max_brightness", contents="2")

    assert isinstance(get_backlight_controller(), SysfsBacklightController)
