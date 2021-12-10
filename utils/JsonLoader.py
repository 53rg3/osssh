import json
from pathlib import PurePath

from utils import Utils


def asList(path: PurePath) -> list:
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except Exception as e:
        Utils.exitWithException(f"Failed to load {path}", e)
