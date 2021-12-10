import os.path

from prompt_toolkit import prompt

from models import Constants
from models.SshData import SshData
from utils import Utils, Action


def uploadPrompt(sshData: SshData):
    source = prompt(
        message=[("class:yellow", "> Path to upload (file or folder): ")],
        style=Constants.promptStyle
    )
    if not os.path.exists(source):
        Utils.exitWithError(f"Provided path doesn't exist, check '{source}'")

    target = prompt(
        message=[("class:yellow", "> Path on remote ( ~/ is allowed): ")],
        style=Constants.promptStyle
    )
    target = f"{sshData.targetUser}@{sshData.targetIp}:{target}"

    Action.scp(source, target, sshData)


def downloadPrompt(sshData: SshData):
    source = prompt(
        message=[("class:yellow", "> Path to download  (file or folder): ")],
        style=Constants.promptStyle
    )
    source = f"{sshData.targetUser}@{sshData.targetIp}:{source}"

    target = prompt(
        message=[("class:yellow", "> Path on localhost (file or folder): ")],
        style=Constants.promptStyle
    )
    if os.path.exists(target) and not os.path.isdir(target):
        Utils.exitWithError(f"Provided path already exists and is not a directory, check '{target}'")

    Action.scp(source, target, sshData)
