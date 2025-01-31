from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from evdev import InputDevice, ecodes

from better_backlight.service import (
    get_input_devices,
    handle_device_events,
    manage_backlight_state,
)


def test_get_input_devices():
    with patch("evdev.list_devices", return_value=["/dev/input/event0", "/dev/input/event1"]):
        with patch(
            "evdev.InputDevice",
            return_value=MagicMock(spec=InputDevice, capabilities=lambda: {ecodes.EV_KEY: []}),
        ):

            devices = list(get_input_devices())
    assert len(devices) == 2


@pytest.mark.asyncio
async def test_device_event_handler(config, state, mock_device):
    # Given
    state.last_input_activity_at = None
    mock_device.async_read.return_value = [MagicMock(type=ecodes.EV_KEY)]

    # When
    await handle_device_events(config, mock_device, state)

    # Then
    assert state.last_input_activity_at is not None


def test_manage_backlight_no_activity(config, state, mock_backlight_controller):
    # Given
    state.last_input_activity_at = None

    # When
    manage_backlight_state(config, state, mock_backlight_controller)

    # Then
    mock_backlight_controller.set_brightness.assert_not_called()
    mock_backlight_controller.get_brightness.assert_not_called()


def test_manage_backlight_manual_change(config, state, mock_backlight_controller):
    # Given
    state.last_input_activity_at = datetime.now()
    state.last_brightness = 3
    mock_backlight_controller.get_brightness.return_value = 2

    # When
    manage_backlight_state(config, state, mock_backlight_controller)

    # Then
    mock_backlight_controller.set_brightness.assert_not_called()
    mock_backlight_controller.get_brightness.assert_called_once()

    assert state.last_brightness == 2
    assert state.max_brightness == 2


def test_manage_backlight_idle(config, state, mock_backlight_controller):
    # Given
    state.last_input_activity_at = datetime.now() - timedelta(seconds=600)
    state.last_brightness = 3

    mock_backlight_controller.get_brightness.return_value = 3

    # When
    manage_backlight_state(config, state, mock_backlight_controller)

    # Then
    mock_backlight_controller.set_brightness.assert_called_once_with(0)
    mock_backlight_controller.get_brightness.assert_called_once()

    assert state.last_brightness == 0
    assert state.max_brightness == 3
    assert state.last_input_activity_at is not None


def test_manage_backlight_active(config, state, mock_backlight_controller):
    # Given
    state.last_input_activity_at = datetime.now()
    state.last_brightness = 3

    mock_backlight_controller.get_brightness.return_value = 3

    # When
    manage_backlight_state(config, state, mock_backlight_controller)

    # Then
    mock_backlight_controller.set_brightness.assert_not_called()
    mock_backlight_controller.get_brightness.assert_called_once()

    assert state.last_brightness == 3
    assert state.max_brightness == 3
    assert state.last_input_activity_at is not None


def test_manage_backlight_disabled_by_user(config, state, mock_backlight_controller):
    # Given
    state.last_input_activity_at = datetime.now() - timedelta(seconds=600)
    state.last_brightness = 0
    state.max_brightness = 0

    mock_backlight_controller.get_brightness.return_value = 0

    # When
    manage_backlight_state(config, state, mock_backlight_controller)

    # Then
    mock_backlight_controller.set_brightness.assert_not_called()
    mock_backlight_controller.get_brightness.assert_called_once()

    assert state.last_brightness == 0
    assert state.max_brightness == 0
    assert state.last_input_activity_at is not None


def test_manage_backlight_enable_due_to_activity(config, state, mock_backlight_controller):
    # Given
    state.last_input_activity_at = datetime.now()
    state.last_brightness = 0
    state.max_brightness = 3

    mock_backlight_controller.get_brightness.return_value = 0

    # When
    manage_backlight_state(config, state, mock_backlight_controller)

    # Then
    mock_backlight_controller.set_brightness.assert_called_once_with(3)
    mock_backlight_controller.get_brightness.assert_called_once()

    assert state.last_brightness == 3
    assert state.max_brightness == 3
    assert state.last_input_activity_at is not None
