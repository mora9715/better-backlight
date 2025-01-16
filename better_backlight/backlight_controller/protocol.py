from typing import Protocol


class BacklightControllerProtocol(Protocol):
    """Protocol for keyboard backlight controller."""

    def get_max_brightness(self) -> int: ...

    def set_brightness(self, level: int) -> None: ...

    def get_brightness(self) -> int: ...
