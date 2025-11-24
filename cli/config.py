import os
import json

CONFIG_PATH = os.path.expanduser("~/.my_own_cli/config.json")


def save_key(api_key: str):
    """Save the API key to ~/.my_own_cli/config.json"""
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

    with open(CONFIG_PATH, "w") as f:
        json.dump({"api_key": api_key}, f)


def load_key():
    """Load the API key"""
    if not os.path.exists(CONFIG_PATH):
        return None

    with open(CONFIG_PATH, "r") as f:
        return json.load(f).get("api_key")
