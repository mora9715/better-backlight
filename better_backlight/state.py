from dataclasses import dataclass
from datetime import datetime


@dataclass
class SharedState:
    """Used to track the state of the backlight and input devices."""

    last_input_activity_at: datetime | None
    last_brightness: int
    max_brightness: int

    @property
    def enabled(self) -> bool:
        return self.last_brightness > 0

    @property
    def disabled_by_user(self) -> bool:
        return self.max_brightness == 0
