# OBS Control

Control OBS Studio from the command line and, optionally, display an interactive notification after an action has been executed.

![Preview of notification created with `notify-send` notification type on KDE Plasma 6](./preview.png)

## Features

- Control OBS Studio over WebSocket
- Displays a notification after an action has been executed with, if applicable, options to open the saved file or the folder containing it
- Allows for control of OBS Studio with keyboard shortcuts on Wayland

## Requirements

- Linux operating system
- OBS Studio 28 or higher
- Python 3.13 or higher <small>(could work on lower versions, but hasn't been tested)</small>
- For notification support:
  - `notify-send` for the `notify-send` notification type
  - KDE Plasma 6 for the `osd` notification type

## Installation

1. Clone and enter this repository
2. Create a virtual environment: `python -m venv .venv`
3. Activate virtual environment: `source .venv/bin/activate`
4. Install required dependencies: `pip install -r requirements.txt`
5. Execute `obs-control` to generate the default configuration file `config.json`
6. Enable the WebSocket server in OBS Studio (_Tools_ → _WebSocket Server Settings_) and configure authentication settings
7. Fill out `config.json` with the appropriate WebSocket server settings
8. Execute `obs-control` again to test the connection

## Usage

`obs-control [-h] [-n NOTIFICATION_TYPE] SCOPE ACTION`

#### Supported combinations of scopes `SCOPE` and actions `ACTION`:

| `SCOPE`         | `ACTION`                                                     |
| --------------- | ------------------------------------------------------------ |
| `connection`    | `test`                                                       |
| `recording`     | `start`, `stop`, `toggle`, `pause`, `resume`, `toggle-pause` |
| `replay-buffer` | `start`, `stop`, `toggle`, `save`                            |

#### Supported notification types `NOTIFICATION_TYPE`:

- `notify-send` (`notify-send` required, default)
- `osd` (KDE Plasma 6 required)
- `stdout`

## Notes

- The interactivity of the notifications depends on the used desktop environment. Testing was done only on KDE Plasma 6, but theoretically, most of the functionality should work in every environment.
- The `osd` notification type interacts directly with the D-Bus message system and uses a method exposed by KDE Plasma itself, so it's currently impossible to use it in other desktop environments. This type of notification is also not interactive and very limited on how much text can it display.

## FAQ

### How can I use this script to control OBS with keyboard shortcuts on Wayland?

This will depend on your desktop environment:

- On KDE Plasma 6:
  1. Open **System Settings** → **Keyboard** → **Shortcuts**
  2. Add the script by pressing **Add New** → **Command or Script...**
     - Set **Command:** to point at the `obs-control` script and set your desired arguments
     - Set **Name:** to be what you see fit
  3. Assign a keyboard shortcut

### Why was this script created?

As an avid Replay Buffer user, I needed a quick and simple way to save the replay with the ability to preview the file or open the directory where it was saved. Because OBS lacks an option to quickly open the most recently saved replay, and, on Wayland, currently doesn't support global hotkeys, this script was created.
