from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from models import Constants
from models.SshData import SshData
from utils import Utils


def instanceSelectionPrompt(instanceIndex: dict) -> SshData:
    instanceCompleter = WordCompleter(
        list(instanceIndex.keys()),
        ignore_case=True,
        match_middle=True)
    key = prompt(
        message=[("class:yellow", "> Where do you want to connect to?\n")],
        completer=instanceCompleter,
        style=Constants.promptStyle
    )
    if key not in instanceIndex:
        Utils.exitWithError(f"Failed to find entry '{key}'. Select entries via arrow keys.")

    return instanceIndex[key]
