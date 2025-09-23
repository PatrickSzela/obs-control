import sys
import obsws_python as obsws  # type: ignore
import time
from notify import notify, notify_file


def is_active(obs: obsws.ReqClient):
    return bool(obs.get_replay_buffer_status().output_active)  # type: ignore


def error_if_off(obs: obsws.ReqClient):
    if not is_active(obs):
        notify("Replay Buffer error", "Replay Buffer hasn't been started!", "critical")
        sys.exit(0)


def start(obs: obsws.ReqClient):
    if not is_active(obs):
        obs.start_replay_buffer()
        notify("Replay Buffer started")


def stop(obs: obsws.ReqClient):
    error_if_off(obs)

    obs.stop_replay_buffer()
    notify("Replay Buffer stopped")


def toggle(obs: obsws.ReqClient):
    if not is_active(obs):
        start(obs)
    else:
        stop(obs)


def save(obs: obsws.ReqClient):
    error_if_off(obs)

    def last_replay_buffer_saved():
        return str(obs.get_last_replay_buffer_replay().saved_replay_path)  # type: ignore

    old_file = last_replay_buffer_saved()

    obs.save_replay_buffer()

    while old_file == last_replay_buffer_saved():
        time.sleep(0.1)

    path = last_replay_buffer_saved()
    notify_file(path, "Replay Buffer saved", "Replay Buffer was saved as {}")
