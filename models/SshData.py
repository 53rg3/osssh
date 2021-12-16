from dataclasses import dataclass

from models.OsProject import OsProject


@dataclass
class SshData:
    hostName: str
    targetIp: str
    targetUser: str
    pathToSshKey: str
    userAtJumpHost: str

    def __init__(self, targetIp: str, hostName: str, osProject: OsProject):
        self.hostName = hostName
        self.targetIp = targetIp
        self.targetUser = osProject.targetUser
        self.pathToSshKey = osProject.pathToSshKey
        self.userAtJumpHost = osProject.userAtJumpHost



