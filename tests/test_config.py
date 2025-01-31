from better_backlight.config import (
    GeneralConfig,
    LoggingConfig,
    load_config,
)


def test_load_default_config(fake_fs):
    # Given
    config_file_path = "/etc/better-backlight.conf"
    fake_fs.create_file(config_file_path, contents="")

    # When
    config = load_config(config_file_path)

    # Then
    assert config.general == GeneralConfig()
    assert config.logging == LoggingConfig()


def test_load_custom_config(fake_fs):
    # Given
    config_file_path = "/etc/better-backlight.conf"
    custom_config = """
    [General]
    idle_time_seconds = 120
    event_throttle_interval_seconds = 2
    management_loop_interval_seconds = 3

    [Logging]
    level = info
    file = /tmp/custom.log
    """
    fake_fs.create_file(config_file_path, contents=custom_config)

    # When
    config = load_config(config_file_path)

    # Then
    assert config.general.idle_time_seconds == 120
    assert config.general.event_throttle_interval_seconds == 2
    assert config.general.management_loop_interval_seconds == 3
    assert config.logging.level == "info"
    assert config.logging.file == "/tmp/custom.log"
