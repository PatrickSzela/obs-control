import sys
import obsws_python as obsws  # type: ignore
from notify import notify, notify_file


def is_active(obs: obsws.ReqClient):
    return bool(obs.get_record_status().output_active)  # type: ignore


def error_if_not_active(obs: obsws.ReqClient):
    if not is_active(obs):
        notify("Recording error", "Recording hasn't been started!", "critical")
        sys.exit(0)


def start(obs: obsws.ReqClient):
    if not is_active(obs):
        obs.start_record()
        notify("Recording started")


def stop(obs: obsws.ReqClient):
    error_if_not_active(obs)

    path = str(obs.stop_record().output_path)  # type: ignore
    notify_file(path, "Recording stopped", "Recording was saved as {}")


def toggle(obs: obsws.ReqClient):
    if not is_active(obs):
        start(obs)
    else:
        stop(obs)


def is_paused(obs: obsws.ReqClient):
    return bool(obs.get_record_status().output_paused)  # type: ignore


def pause(obs: obsws.ReqClient):
    error_if_not_active(obs)
    if not is_paused(obs):
        obs.pause_record()
        notify("Recording paused")


def resume(obs: obsws.ReqClient):
    error_if_not_active(obs)
    if is_paused(obs):
        obs.resume_record()
        notify("Recording resumed")


def toggle_pause(obs: obsws.ReqClient):
    error_if_not_active(obs)

    if is_paused(obs):
        resume(obs)
    else:
        pause(obs)
