import click
from prompt_toolkit import prompt

from models import Mode
from utils import Utils


def selectModePrompt() -> str:
    Utils.printInfo("> What do you want to do?")
    selection = "[1] SSH (default)      [2] Download      [3] Upload"
    choiceMap = {
        "1": Mode.ssh,
        "2": Mode.download,
        "3": Mode.upload
    }
    click.secho(selection)
    choice = prompt('Choice: ')

    if choice == '':
        choice = "1"
    if choice not in choiceMap:
        Utils.exitWithError(f"Choice not recognized. Got '{choice}', need one of {list(choiceMap.keys())}")

    return choiceMap[choice]
