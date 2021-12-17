import os
import sys
import time
from threading import Timer

from models.SshData import SshData
from utils import Utils
from utils.Shell import Shell

keepRunning = True


def ssh(sshData: SshData, override_title: bool):
    sh = Shell(os.getcwd())

    cmd = f"""
    ssh -i {sshData.pathToSshKey} \
        -t {sshData.userAtJumpHost} \
        "ssh -t {sshData.targetUser}@{sshData.targetIp}"
    """.strip()

    if override_title:
        timer = Timer(0.1, overwriteTerminalTitle, args=[sshData.hostName, sshData.projectName])
        timer.start()

    Utils.printInfo(f"> Running SSH with: \n{cmd}\n")
    sh.run(cmd, env=os.environ)

    global keepRunning
    keepRunning = False
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


def overwriteTerminalTitle(hostName: str, projectName: str):
    global keepRunning
    try:
        while keepRunning:
            time.sleep(0.01)
            sys.stdout.write(f'\33]0;{hostName} ({projectName})\a')
            sys.stdout.flush()
    except (Exception,):
        pass
