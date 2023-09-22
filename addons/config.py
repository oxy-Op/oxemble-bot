from json import load
import os

config_path = os.path.join(os.getcwd(), "discordBot", "config", "config.json")


def config(config_path=config_path):
    try:
        if os.path.isfile(config_path):
            with open(config_path, "r") as file:
                config = load(file)
                return config
        else:
            print("config.json file not found.")

    except Exception as e:
        return e
