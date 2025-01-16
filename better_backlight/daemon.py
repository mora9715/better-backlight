import asyncio
from datetime import datetime, timedelta
from typing import Iterator

import evdev
from evdev import ecodes

from better_backlight.backlight_controller import (
    BacklightControllerProtocol,
    get_backlight_controller,
)
from better_backlight.state import SharedState

# TODO: Move to configuration
IDLE_TIME = 10
THROTTLE_INTERVAL = 1


def get_input_devices() -> Iterator[evdev.InputDevice]:
    """Yields input devices that have keys.
    This includes keyboards, mice power buttons usr."""
    for fn in evdev.list_devices():
        dev = evdev.InputDevice(fn)
        cap = dev.capabilities()
        if ecodes.EV_KEY in cap:
            yield dev


async def device_event_handler(device: evdev.InputDevice, state: SharedState):
    while True:
        events = list(await device.async_read())
        for event in events:
            if event.type in (
                ecodes.EV_KEY,
                ecodes.EV_REL,
            ):
                state.last_input_activity_at = datetime.now()
                break
        await asyncio.sleep(THROTTLE_INTERVAL)


async def manage_backlight(
    state: SharedState, backlight_controller: BacklightControllerProtocol
):
    while True:
        if not state.last_input_activity_at:
            # Nothing happened yet. Let's keep waiting.
            print(state)
            await asyncio.sleep(1)
            continue

        current_brightness = backlight_controller.get_brightness()

        if current_brightness != state.last_brightness:
            # Someone changed the brightness manually.
            # We treat as new max brightness level.
            state.last_brightness = current_brightness
            state.max_brightness = current_brightness
            state.last_input_activity_at = datetime.now()

        if datetime.now() - state.last_input_activity_at > timedelta(seconds=IDLE_TIME):
            # We're idle. Let's turn off the backlight.
            if state.enabled:
                backlight_controller.set_brightness(0)
                state.last_brightness = 0
        else:
            # We're not idle. Let's turn on the backlight if not already on.
            if not state.enabled and not state.disabled_by_user:
                backlight_controller.set_brightness(state.max_brightness)
                state.last_brightness = state.max_brightness
        await asyncio.sleep(1)


async def main():
    backlight_controller = get_backlight_controller()
    shared_state = SharedState(
        last_input_activity_at=datetime.now(),
        last_brightness=backlight_controller.get_brightness(),
        max_brightness=backlight_controller.get_brightness(),
    )

    for device in get_input_devices():
        asyncio.create_task(device_event_handler(device, shared_state))
    await manage_backlight(shared_state, backlight_controller)


if __name__ == "__main__":
    asyncio.run(main())
