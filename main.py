#!/usr/bin/python3

import obsws_python as obsws  # type: ignore
import sys
import argparse
from collections.abc import Callable
from typing import Any
import notify as ntfy
import recording
import replay_buffer
from notify import notify, SUPPORTED_NOTIFICATIONS
from config import Config

# TODO: possibly convert it into an OBS script (more info here: https://github.com/obsproject/obs-studio/wiki/Getting-Started-With-OBS-Scripting) or implement it as a systemd service
# TODO: use GlobalShortcuts portal:
# - https://github.com/Aviana/Global-Shortcuts-OBS
# - https://gist.github.com/Aviana/a3a0368172e326d6ccc57cb254c1e569

SUPPORTED_ACTIONS: dict[str, dict[str, Callable[[obsws.ReqClient], None]]] = {
    "connection": {
        "test": lambda obs: notify(
            "Connection test", "Successfully connected to OBS", "normal"
        ),
    },
    "recording": {
        "start": recording.start,
        "stop": recording.stop,
        "toggle": recording.toggle,
        "pause": recording.pause,
        "resume": recording.resume,
        "toggle-pause": recording.toggle_pause,
    },
    "replay-buffer": {
        "start": replay_buffer.start,
        "stop": replay_buffer.stop,
        "toggle": replay_buffer.toggle,
        "save": replay_buffer.save,
    },
}


def get_all_nested_keys(d: dict[str, dict[str, Any]]):
    keys: list[str] = []

    for _key, value in d.items():
        for key, _value in value.items():
            if key not in keys:
                keys.append(key)

    return keys


def main():
    parser = argparse.ArgumentParser(
        prog="obs-control",
        description="Control OBS Studio from the command line and, optionally, display an interactive notification after an action has been executed.",
    )
    parser.add_argument(
        "scope",
        nargs="?",
        choices=list(SUPPORTED_ACTIONS.keys()),
        default=list(SUPPORTED_ACTIONS.keys())[0],
        help="action's scope",
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=get_all_nested_keys(SUPPORTED_ACTIONS),
        default=get_all_nested_keys(SUPPORTED_ACTIONS)[0],
        help="action to perform; not every action is supported for every scope",
    )
    parser.add_argument(
        "-n",
        "--notification-type",
        choices=list(SUPPORTED_NOTIFICATIONS.keys()),
        default=list(SUPPORTED_NOTIFICATIONS.keys())[0],
        help="notification type",
    )

    args = parser.parse_args()
    [scope, action, notification_type] = [
        args.scope,
        args.action,
        args.notification_type,
    ]

    if scope not in SUPPORTED_ACTIONS or action not in SUPPORTED_ACTIONS[scope]:
        notify(
            "Script error",
            "Invalid combination of scope and action has been passed!",
            "critical",
        )
        sys.exit(0)

    if notification_type not in SUPPORTED_NOTIFICATIONS:
        notify("Script error", "Invalid notification type has been passed!", "critical")
        sys.exit(0)

    ntfy.NOTIFY_TYPE = notification_type

    try:
        config = Config()
        config.load()

        obs = obsws.ReqClient(
            host=config.host,
            port=config.port,
            password=config.password,
            timeout=config.timeout,
        )
    except Exception as e:
        notify(
            "Connection error",
            f"Couldn't connect to the OBS WebSocket!\nError: {str(e)}",
            "critical",
        )
        sys.exit(0)

    SUPPORTED_ACTIONS[scope][action](obs)


if __name__ == "__main__":
    main()
