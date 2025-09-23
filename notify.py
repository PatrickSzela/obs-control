import os
import subprocess
import dbus  # type: ignore
from typing import Literal, Any
from collections.abc import Callable

Urgency = Literal["low", "normal", "critical"]

global NOTIFY_TYPE
NOTIFY_TYPE = "notify-send"

session_bus = dbus.SessionBus()


class Action:
    def __init__(self, label: str, callback: Callable[[], Any]):
        self.label = label
        self.callback = callback


def dbus_get_method(name: str, path: str, method: str, interface: str | None = None):
    object = session_bus.get_object(name, path)  # type: ignore
    return object.get_dbus_method(method, interface)  # type: ignore


def highlight_in_file_manager(path: str):
    showItems = dbus_get_method(
        "org.freedesktop.FileManager1",
        "/org/freedesktop/FileManager1",
        "ShowItems",
    )
    showItems(dbus.Array([f"file://{path}"]), "")  # type: ignore


def notify_send(
    title: str,
    message: str,
    urgency: Urgency = "normal",
    timeout: int = -1,
    actions: dict[str, Action] = {},
    hints: list[str] = [],
):
    command = ["notify-send"]

    if timeout != -1:
        command += ["-t", str(timeout)]

    command += ["-u", urgency]
    command += ["-i", "com.obsproject.Studio", "-a", "OBS Studio"]

    for key, value in actions.items():
        command += ["-A", f"{key}={value.label}"]

    hints.append("string:desktop-entry:com.obsproject.Studio")

    for hint in hints:
        command += ["-h", hint]

    command += [title, message]

    if len(actions):
        result = subprocess.check_output(command).decode("utf-8").splitlines()
        result = result[0] if len(result) else result

        if result and result in actions:
            actions[result].callback()
    else:
        subprocess.run(command)


def osd(
    title: str,
    message: str,
    urgency: Urgency = "normal",
    timeout: int = -1,
    actions: dict[str, Action] = {},
    hints: list[str] = [],
):
    showText = dbus_get_method("org.kde.plasmashell", "/org/kde/osdService", "showText")
    showText("com.obsproject.Studio", title)

    # os.system(
    #     # f'qdbus6 org.kde.plasmashell /org/kde/osdService org.kde.osdService.showText com.obsproject.Studio "{message if message else title}"'
    #     f'dbus-send --session --dest=org.kde.plasmashell --type=method_call /org/kde/osdService org.kde.osdService.showText string:"com.obsproject.Studio" string:"{title}"'
    # )


def stdout(
    title: str,
    message: str,
    urgency: Urgency = "normal",
    timeout: int = -1,
    actions: dict[str, Action] = {},
    hints: list[str] = [],
):
    print(f"{title}: {message}")


SUPPORTED_NOTIFICATIONS: dict[
    str,
    Callable[[str, str, Urgency, int, dict[str, Action], list[str]], None],
] = {"notify-send": notify_send, "osd": osd, "stdout": stdout}


def notify(
    title: str,
    message: str = "",
    urgency: Urgency = "normal",
    timeout: int = -1,
    actions: dict[str, Action] = {},
    hints: list[str] = [],
):
    SUPPORTED_NOTIFICATIONS[NOTIFY_TYPE](
        title, message, urgency, timeout, actions, hints
    )


def notify_file(
    file_path: str,
    title: str,
    message: str,
    urgency: Urgency = "normal",
    timeout: int = -1,
):
    [_path, filename] = os.path.split(file_path)

    actions = {
        "default": Action(
            "default",
            lambda: os.system(f'xdg-open "{file_path}" > /dev/null 2>&1'),
        ),
        "folder": Action(
            "Open Containing Folder",
            # lambda: os.system(f'xdg-open "{path}" > /dev/null 2>&1'),
            # lambda: os.system(
            #     f'dbus-send --session --dest=org.freedesktop.FileManager1 --type=method_call /org/freedesktop/FileManager1 org.freedesktop.FileManager1.ShowItems array:string:"file://{file_path}" string:""'
            # ),
            lambda: highlight_in_file_manager(file_path),
        ),
    }

    notify(
        title,
        message.format(filename),
        urgency,
        timeout,
        actions,
        [f"string:x-kde-urls:file://{file_path}"],
    )
