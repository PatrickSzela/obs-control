import sys
import os
import json
from notify import notify_file

CONFIG_PATH = os.path.realpath("./config.json")


class Config:
    def __init__(self):
        self.host: str = "localhost"
        self.port: int = 4455
        self.password: str = ""
        self.timeout: int = 3

    def load(self):
        if not os.path.isfile(CONFIG_PATH):
            self.save()
            notify_file(
                CONFIG_PATH,
                "Config file not found",
                "A new config file has been created, please fill it out with WebSocket server settings from OBS Studio",
                "critical",
            )
            sys.exit(0)

        with open(CONFIG_PATH, "r") as file:
            obj = json.load(file)
            file.close()
            self.__dict__.update(obj)

    def save(self):
        with open(CONFIG_PATH, "w") as file:
            obj = self.__dict__.copy()
            file.write(json.dumps(obj, indent=4))
            file.close()
