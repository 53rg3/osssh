import os

import click
from prompt_toolkit import prompt

from models import Constants
from models.OsProject import OsProject
from utils import Utils, FileUtils
from utils.Shell import Shell
from utils.StopWatch import StopWatch


def updateCachePrompt(osProjectList: list):
    Utils.printInfo("> Choose OpenStack project to update (done via `openstack server list`):")
    i = 1
    selection = "[0] All"
    choiceMap = {}
    for osProject in osProjectList:
        choiceMap[str(i)] = osProject
        selection += f"      [{i}] {osProject.id}"
        i = i + 1

    click.secho(selection)
    choice = prompt("Choice: ")
    if choice == '0':
        loadAll(osProjectList)
    else:
        if choice not in choiceMap:
            Utils.exitWithError(f"Choice not recognized. Got '{choice}', need one of {['0'] + list(choiceMap.keys())}")
        loadSingle(choiceMap[choice])


def loadAll(osProjectList: list):
    for osProject in osProjectList:
        loadSingle(osProject)


def loadSingle(osProject: OsProject):
    if not os.path.exists(Constants.cacheDir):
        os.makedirs(Constants.cacheDir)
    Utils.printInfo(f"Loading {osProject.id}...")

    stopWatch = StopWatch()
    sh = Shell(os.getcwd())

    cmd = "openstack server list -f json"
    if osProject.allowSelfSignedCert:
        cmd = "openstack --insecure server list -f json"

    sh.run(cmd, captureOutput=True, env=osProject.envWithSystemEnv())
    if sh.getExitCode() != 0:
        Utils.exitWithError(f"{sh.getStdErr()}\n"
                            f"Command `{cmd}` produced error code: {sh.getExitCode()}")

    FileUtils.writeToFile(osProject.getPathToCacheFile(), sh.getStdOut())
    Utils.printInfo(f"Took {stopWatch.getElapsedSeconds()}s")


