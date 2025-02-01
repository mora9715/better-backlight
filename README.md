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

The service is provided as RPM/DEB packages. The latest release can be found in
the [Releases](https://github.com/mora9715/better-backlight/releases) page.

To install the package, run the following command:

### Debian-based systems

```shell
wget https://github.com/mora9715/better-backlight/releases/latest/download/better-backlight-<version>.deb
sudo apt install ./better-backlight-<version>.rpm
```

### RedHat-based systems

```shell
wget https://github.com/mora9715/better-backlight/releases/latest/download/better-backlight-<version>.rpm
sudo dnf install ./better-backlight-<version>.rpm
```

## Service Management

After installing, you can manage the service using `systemctl`:

```bash
sudo systemctl enable better-backlight   # Enable service at boot
sudo systemctl start better-backlight    # Start service immediately
sudo systemctl status better-backlight   # Check current status
```

## Configuration

The configuration file is located at `/etc/better-backlight.conf`.

1. Modify the configuration:

```shell
sudo nano /etc/better-backlight.conf
```

2. Restart the service:

```shell
sudo systemctl restart better-backlight
```

A sample configuration file with detailed descriptions can be found [here](packaging/etc/better-backlight.conf).

## Troubleshooting

If the service is not working as expected, you can check the logs for more information:

```shell
journalctl -u better-backlight
# OR
tail -f /var/log/better-backlight.log
```

## TODO List

The following features are planned for the first stable release:

| Item               | Description                                                              | Status |
|--------------------|--------------------------------------------------------------------------|:------:|
| Configuration      | Add configuration file to allow users to customize the behavior          |   ✅    |
| Debian Packaging   | Configure .deb packages building for easier installation                 |   ✅    |
| Tests              | Add unit tests to ensure the service works as expected                   |   ✅    |
| Power Management   | Add ability to keep the backlight enabled when the system is on AC power |   ❌    |
| Security Hardening | Add SELinux and/or AppArmor policies for enhanced security               |   ❌    |
