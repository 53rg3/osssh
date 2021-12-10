from dataclasses import dataclass


@dataclass(frozen=True)
class Keys:

    # config.yml
    pathToOpenStackProjectsYamlFile: str = "pathToOpenStackProjectsYamlFile"

    # OsProject
    targetUser: str = "targetUser"
    pathToSshKey: str = "pathToSshKey"
    userAtJumpHost: str = "userAtJumpHost"
    allowSelfSignedCert: str = "allowSelfSignedCert"
    env: str = "env"
    id: str = "id"

    # OpenStack server list as JSON
    Name: str = "Name"
    ID: str = "ID"
    Flavor: str = "Flavor"
    Networks: str = "Networks"
    Status: str = "Status"
