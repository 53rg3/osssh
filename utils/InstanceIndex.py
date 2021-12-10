import os
import re
from pathlib import Path

import click

from models import Constants
from models.Keys import Keys
from models.OsProject import OsProject
from models.SshData import SshData
from utils import Utils, YamlLoader, JsonLoader


def create(shouldAddInstanceId=False) -> dict:
    osProjectsDict = loadFromConfig()
    osProjectList = getOsProjectList(osProjectsDict)
    appendCaches(osProjectList)
    return parseProjectList(osProjectList, shouldAddInstanceId)


def printList():
    index = create(True)
    for key in index:
        click.secho(key)


def printEnvs(osProjectId: str):
    osProjectsDict = loadFromConfig()
    isFound = False
    choices = []
    for osProject in osProjectsDict:
        choices.append(osProject[Keys.id])
        if osProject[Keys.id] == osProjectId:
            isFound = True
            envs = osProject[Keys.env]
            for key in envs:
                click.secho(f"export {key}=\"{envs[key]}\"")
    if not isFound:
        Utils.exitWithError(f"Failed to find OpenStack project id, need one of {choices}")


def loadOsProjectsListOnly():
    osProjectsDict = loadFromConfig()
    return getOsProjectList(osProjectsDict)


def loadFromConfig():
    config = YamlLoader.fromFile(Constants.configFile)
    osProjectsFilePath = getOsProjectsFilePath(config)
    return YamlLoader.fromFile(Path(osProjectsFilePath))


def getOsProjectsFilePath(config: dict) -> str:
    if Keys.pathToOpenStackProjectsYamlFile not in config:
        Utils.exitWithError(f"Failed to find {Keys.pathToOpenStackProjectsYamlFile} in config.yml")
    osProjectsFilePath = config[Keys.pathToOpenStackProjectsYamlFile]

    if not os.path.isfile(osProjectsFilePath):
        Utils.exitWithError(f"{osProjectsFilePath} does not exist or is not a file")

    return osProjectsFilePath


def getOsProjectList(osProjectsDict: dict) -> list:
    osProjectList = []
    uniqueIds = set([])
    for osp in osProjectsDict:
        osProject = OsProject(osp)
        if osProject.id in uniqueIds:
            Utils.exitWithError(
                f"Duplicate ID, OpenStack project ID already exists in configuration, check: {osProject.id}")
        else:
            uniqueIds.add(osProject.id)

        osProjectList.append(OsProject(osp))

    return osProjectList


def appendCaches(osProjectList: list):
    for osProject in osProjectList:
        cacheFilePath = f"{Constants.cacheDir}/{osProject.id}"
        if not os.path.isfile(cacheFilePath):
            Utils.exitWithError(f"Can't find '{cacheFilePath}', run with --update to load the cache")

        osProject.instanceList = osProject.instanceList + JsonLoader.asList(Path(cacheFilePath))


def parseProjectList(osProjectList: list, shouldAddInstanceId: bool) -> dict:
    index = {}
    formatTemplate = generateFormatTemplate(osProjectList, shouldAddInstanceId)
    uniqueIds = set([])
    for osProject in osProjectList:
        for instance in osProject.instanceList:
            if instance[Keys.ID] in uniqueIds:
                Utils.exitWithError(f"Duplicate ID for OpenStack instance, check:\n"
                                    f"  {osProject.id} - {instance[Keys.Name]} - {instance[Keys.ID]}\n"
                                    f"You likely have configured the same OpenStack project twice. Check your config and delete the files in `.cache/`")
            else:
                uniqueIds.add(instance[Keys.ID])

            if shouldAddInstanceId:
                key = formatTemplate.format(osProject.id, instance[Keys.Name], instance[Keys.Networks], instance[Keys.Flavor],
                                            instance[Keys.ID])
                index[key] = "NOT USED - Only used for --export"
            else:
                for ip in extractIPs(instance[Keys.Networks]):
                    key = formatTemplate.format(osProject.id, instance[Keys.Name], ip, instance[Keys.Flavor],
                                                instance[Keys.ID])
                    index[key] = SshData(ip, osProject)

    return index


def generateFormatTemplate(osProjectList: list, shouldAddInstanceId: bool):
    lengths = {
        "osProjectId": 0,
        "instanceName": 0,
        "ip": 0,
        "flavor": 0,
        "instanceId": 0
    }
    for osProject in osProjectList:
        for instance in osProject.instanceList:
            for ip in extractIPs(instance[Keys.Networks]):
                lengths["osProjectId"] = updateMaxLength(lengths["osProjectId"], osProject.id)
                lengths["instanceName"] = updateMaxLength(lengths["instanceName"], instance[Keys.Name])
                lengths["flavor"] = updateMaxLength(lengths["flavor"], instance[Keys.Flavor])
                lengths["instanceId"] = updateMaxLength(lengths["instanceId"], instance[Keys.ID])
                if shouldAddInstanceId:
                    lengths["ip"] = updateMaxLength(lengths["ip"], instance[Keys.Networks])
                else:
                    lengths["ip"] = updateMaxLength(lengths["ip"], ip)

    formatTemplate = "" + \
                     "{:<" + str(lengths['osProjectId']) + "} " + \
                     "| {:<" + str(lengths['instanceName']) + "} " + \
                     "| {:<" + str(lengths['ip']) + "} " + \
                     "| {:<" + str(lengths['flavor']) + "} "
    if shouldAddInstanceId:
        formatTemplate += "| {:<" + str(lengths['instanceId']) + "}"

    return formatTemplate


def updateMaxLength(maxLength: int, candidateString: str):
    if maxLength < len(candidateString):
        return len(candidateString)
    else:
        return maxLength


def extractIPs(networks: str):
    return re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', networks)
