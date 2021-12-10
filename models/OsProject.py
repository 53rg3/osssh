import os
from dataclasses import dataclass, field

from models import Constants
from models.Keys import Keys
from utils import Utils


@dataclass
class OsProject:

    id: str
    pathToSshKey: str
    userAtJumpHost: str
    targetUser: str
    env: dict
    instanceList: list

    allowSelfSignedCert: bool = False

    def __init__(self, osProjectsDict: dict):
        # Mandatory
        self.id = Utils.getMandatoryKeyFromDict(Keys.id, osProjectsDict)
        self.env = Utils.getMandatoryKeyFromDict(Keys.env, osProjectsDict)
        self.pathToSshKey = Utils.getMandatoryKeyFromDict(Keys.pathToSshKey, osProjectsDict)
        self.targetUser = Utils.getMandatoryKeyFromDict(Keys.targetUser, osProjectsDict)
        self.userAtJumpHost = Utils.getMandatoryKeyFromDict(Keys.userAtJumpHost, osProjectsDict)
        self.userAtJumpHost = Utils.getMandatoryKeyFromDict(Keys.userAtJumpHost, osProjectsDict)
        self.instanceList = []

        # Optional
        self.allowSelfSignedCert = Utils.getOptionalKeyFromDict(Keys.allowSelfSignedCert, osProjectsDict)

    def envWithSystemEnv(self) -> dict:
        return {
            **os.environ,
            **self.env
        }

    def getPathToCacheFile(self):
        return f"{Constants.cacheDir}/{self.id}"
