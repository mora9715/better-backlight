from configparser import ConfigParser
from dataclasses import dataclass, field


@dataclass
class GeneralConfig:
    idle_time_seconds: int = 60
    event_throttle_interval_seconds: int = 1
    management_loop_interval_seconds: int = 1


@dataclass
class LoggingConfig:
    level: str = "warning"
    file: str = "/var/log/better-backlight.log"


@dataclass
class ServiceConfig:
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    general: GeneralConfig = field(default_factory=GeneralConfig)


def load_config(file_path: str = "/etc/better-backlight.conf") -> ServiceConfig:
    parser = ConfigParser()
    parser.read(file_path)

    general_config = GeneralConfig(
        idle_time_seconds=parser.getint(
            "General", "idle_time_seconds", fallback=GeneralConfig.idle_time_seconds
        ),
        event_throttle_interval_seconds=parser.getint(
            "General",
            "event_throttle_interval_seconds",
            fallback=GeneralConfig.event_throttle_interval_seconds,
        ),
        management_loop_interval_seconds=parser.getint(
            "General",
            "management_loop_interval_seconds",
            fallback=GeneralConfig.management_loop_interval_seconds,
        ),
    )

    logging_config = LoggingConfig(
        level=parser.get("Logging", "level", fallback=LoggingConfig.level),
        file=parser.get("Logging", "file", fallback=LoggingConfig.file),
    )

    return ServiceConfig(general=general_config, logging=logging_config)
