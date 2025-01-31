import asyncio
import logging
from datetime import datetime, timedelta
from typing import Iterator

import evdev
from evdev import ecodes

from better_backlight.backlight_controller import BacklightControllerProtocol
from better_backlight.config import ServiceConfig
from better_backlight.state import SharedState

logger = logging.getLogger(__name__)


def get_input_devices() -> Iterator[evdev.InputDevice]:
    """Yields input devices that have keys.
    This includes keyboards, mice power buttons usr."""
    for fn in evdev.list_devices():
        dev = evdev.InputDevice(fn)
        cap = dev.capabilities()
        if ecodes.EV_KEY in cap:
            logger.debug(f"Found input device: {dev.name}")
            yield dev


async def handle_device_events(
    config: ServiceConfig, device: evdev.InputDevice, state: SharedState
):
    events = list(await device.async_read())
    for event in events:
        if event.type in (ecodes.EV_KEY, ecodes.EV_REL):
            state.last_input_activity_at = datetime.now()
            break
    await asyncio.sleep(config.general.event_throttle_interval_seconds)


async def device_event_handler(
    config: ServiceConfig, device: evdev.InputDevice, state: SharedState
):
    while True:
        await handle_device_events(config, device, state)


def manage_backlight_state(
    config: ServiceConfig, state: SharedState, backlight_controller: BacklightControllerProtocol
):
    if not state.last_input_activity_at:
        return

    current_brightness = backlight_controller.get_brightness()

    if current_brightness != state.last_brightness:
        logger.debug(
            f"Detected manual brightness change "
            f"from {state.last_brightness} to {current_brightness}."
        )
        state.last_brightness = current_brightness
        state.max_brightness = current_brightness
        state.last_input_activity_at = datetime.now()

    if datetime.now() - state.last_input_activity_at > timedelta(
        seconds=config.general.idle_time_seconds
    ):
        if state.enabled:
            logger.info("Turning off the backlight due to inactivity.")
            backlight_controller.set_brightness(0)
            state.last_brightness = 0
    else:
        if not state.enabled and not state.disabled_by_user:
            logger.info("Turning on the backlight due to activity.")
            backlight_controller.set_brightness(state.max_brightness)
            state.last_brightness = state.max_brightness


async def manage_backlight(
    config: ServiceConfig, state: SharedState, backlight_controller: BacklightControllerProtocol
):
    while True:
        manage_backlight_state(config, state, backlight_controller)
        await asyncio.sleep(config.general.management_loop_interval_seconds)
