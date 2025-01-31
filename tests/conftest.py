from unittest.mock import AsyncMock, MagicMock

import pytest
from evdev import InputDevice
from pyfakefs.fake_filesystem_unittest import Patcher

from better_backlight.config import GeneralConfig, LoggingConfig, ServiceConfig
from better_backlight.state import SharedState


@pytest.fixture
def fake_fs():
    with Patcher() as patcher:
        yield patcher.fs


@pytest.fixture
def config():
    return ServiceConfig(
        general=GeneralConfig(
            idle_time_seconds=60,
            event_throttle_interval_seconds=1,
            management_loop_interval_seconds=1,
        ),
        logging=LoggingConfig(
            level="info",
            file="/tmp/custom.log",
        ),
    )


@pytest.fixture
def state():
    return SharedState(
        last_input_activity_at=None,
        last_brightness=3,
        max_brightness=3,
    )


@pytest.fixture
def mock_device():
    device = MagicMock(spec=InputDevice)
    device.async_read = AsyncMock(return_value=[])
    return device


@pytest.fixture
def mock_backlight_controller():
    controller = MagicMock()
    controller.get_brightness = MagicMock(return_value=3)
    controller.set_brightness = MagicMock()
    return controller
