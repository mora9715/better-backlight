from .protocol import BacklightControllerProtocol
from .sysfs import SysfsBacklightController


def get_backlight_controller() -> BacklightControllerProtocol:
    return SysfsBacklightController()
