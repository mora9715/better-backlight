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

## Known Supported Devices

- ThinkPad laptops
- Dell laptops

## TODO's

| Feature          | Description                                                              | Status  |
|------------------|--------------------------------------------------------------------------|---------|
| Configuration    | Add configuration file to allow users to customize the behavior          | Pending |
| Power Management | Add ability to keep the backlight enabled when the system is on AC power | Pending |
| Debian Packaging | Configure .deb packages building for easier installation                 | Pending |