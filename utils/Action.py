import os

from models.SshData import SshData
from utils import Utils
from utils.Shell import Shell


def ssh(sshData: SshData):
    sh = Shell(os.getcwd())

    cmd = f"""
    ssh -i {sshData.pathToSshKey} \
        -t {sshData.userAtJumpHost} \
        "ssh -t {sshData.targetUser}@{sshData.targetIp}"
    """.strip()

    Utils.printInfo(f"> Running SSH with: \n{cmd}\n")
    sh.run(cmd, env=os.environ)

    if sh.getExitCode() != 0:
        Utils.exitWithError(f"{sh.getStdErr()}\n"
                            f"Command `{cmd}` produced error code: {sh.getExitCode()}")


def scp(source: str, target: str, sshData: SshData):
    sh = Shell(os.getcwd())

    cmd = f"""
    scp -r \
        -i {sshData.pathToSshKey} \
        -oProxyCommand="ssh -i {sshData.pathToSshKey} -W %h:%p {sshData.userAtJumpHost}" \
        {source} \
        {target}
    """.strip()

    Utils.printInfo(f"> Running SCP with: \n{cmd}\n")
    sh.run(cmd, env=os.environ)

    if sh.getExitCode() != 0:
        Utils.exitWithError(f"{sh.getStdErr()}\n"
                            f"Command `{cmd}` produced error code: {sh.getExitCode()}")
