import asyncio
from datetime import datetime

from better_backlight.backlight_controller import get_backlight_controller
from better_backlight.config import load_config
from better_backlight.logging import configure_logger
from better_backlight.service import (
    device_event_handler,
    get_input_devices,
    manage_backlight,
)
from better_backlight.state import SharedState


async def main():
    configuration = load_config()
    configure_logger(configuration)

    backlight_controller = get_backlight_controller()

    shared_state = SharedState(
        last_input_activity_at=datetime.now(),
        last_brightness=backlight_controller.get_brightness(),
        max_brightness=backlight_controller.get_brightness(),
    )

    for device in get_input_devices():
        asyncio.create_task(device_event_handler(configuration, device, shared_state))

    await manage_backlight(configuration, shared_state, backlight_controller)


if __name__ == "__main__":
    asyncio.run(main())
