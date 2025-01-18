# Better Backlight

Better Backlight aims to improve the keyboard backlight control on Linux systems.

It automatically disables the keyboard backlight after a period of inactivity and restores it when the user interacts
with the keyboard.

It respects user preferences. If the user disabled the keyboard backlight, Better Backlight will not enable it
automatically.
If the user set a specific brightness level, Better Backlight will not go beyond that level.

## Features

- Automatic keyboard backlight control.
- Automatic detection of supported backlit keyboard devices.

## How it works

The service listens to input device events through the `evdev` interface. When user activity is detected, the service
enables the keyboard backlight through sysfs led management interface.

If no user activity is detected for a period of time, the service disables the keyboard backlight.

## Installation

The service is provided as an RPM package. The latest release can be found in
the [Releases](https://github.com/mora9715/better-backlight/releases) page.

To install the package, run the following command:

```shell
sudo dnf install better-backlight-<version>.rpm
```

## Configuration

The service is configured using a configuration file located at `/etc/better-backlight.conf`.

A default configuration file with descriptions for each option is provided in the repository. It can be
found [here](packaging/etc/better-backlight.conf).

To modify the configuration, edit the file `etc/better-backlight.conf` and restart the service.

```shell
sudo systemctl restart better-backlight
```

## TODO's

| Item             | Description                                                              | Status |
|------------------|--------------------------------------------------------------------------|:------:|
| Configuration    | Add configuration file to allow users to customize the behavior          |   ✅    |
| Power Management | Add ability to keep the backlight enabled when the system is on AC power |   ❌    |
| Debian Packaging | Configure .deb packages building for easier installation                 |   ❌    |
| Tests            | Add unit tests to ensure the service works as expected                   |   ❌    |