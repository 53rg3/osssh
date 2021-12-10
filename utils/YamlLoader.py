from pathlib import PurePath

from ruamel.yaml import YAML

from utils import Utils

yaml = YAML(typ='safe')


def fromFile(path: PurePath) -> dict:
    try:
        with open(path, 'r') as yamlFile:
            return yaml.load(yamlFile)
    except Exception as e:
        Utils.exitWithException(f"Failed to load {path}", e)
