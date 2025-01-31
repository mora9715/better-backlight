import pytest

from better_backlight.backlight_controller.sysfs import SysfsBacklightController


def test_get_max_brightness(fake_fs):
    # Given
    expected_max_brightness = 2
    fake_fs.create_file(
        "/sys/class/leds/test::kbd_backlight/max_brightness", contents=str(expected_max_brightness)
    )
    controller = SysfsBacklightController(led_name="test::kbd_backlight")

    # When
    actual_max_brightness = controller.get_max_brightness()

    # Then
    assert actual_max_brightness == expected_max_brightness


def test_get_brightness(fake_fs):
    # Given
    expected_brightness = 1
    fake_fs.create_file(
        "/sys/class/leds/test::kbd_backlight/brightness", contents=str(expected_brightness)
    )
    controller = SysfsBacklightController(led_name="test::kbd_backlight")

    # When
    actual_brightness = controller.get_brightness()

    # Then
    assert actual_brightness == expected_brightness


def test_set_brightness(fake_fs):
    # Given
    level = 1
    fake_fs.create_file("/sys/class/leds/test::kbd_backlight/brightness")
    controller = SysfsBacklightController(led_name="test::kbd_backlight")

    # When
    controller.set_brightness(level)

    # Then
    with open("/sys/class/leds/test::kbd_backlight/brightness", "r", encoding="utf-8") as f:
        assert f.read() == str(level)


def test_device_not_supported(fake_fs):  # pylint: disable=unused-argument
    with pytest.raises(ValueError):
        SysfsBacklightController()
