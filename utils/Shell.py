import os.path
import subprocess

from utils import Utils


class Shell:
    """
    This gives you a wrapper around subprocess.run(). The last command which was run() is stored in self.process and
    you have to manually handle the further processing. E.g. reading `stdout`, `stderr` or the exitCode. You can control
    this by passing run(your_command, captureOutput=False). Default is True.

    Note that a run() will never fail, i.e. produce a non-zero exit code. You have to decide what to do with the result.
    """
    runDir: str
    process: subprocess.CompletedProcess
    lastCommand: str

    def __init__(self, directoryToRunIn):
        if not directoryToRunIn:
            Utils.exitWithError(f"Provided 'directoryToRunIn' for Shell must not be None")
        if not os.path.isdir(directoryToRunIn):
            Utils.exitWithError(f"Provided 'directoryToRunIn' for Shell is not a directory, check: {directoryToRunIn}\n"
                                f"Script is being executed from: {os.getcwd()}")
        self.runDir = directoryToRunIn

    def run(self, commandToRun: str, captureOutput=False, env=None):
        if env is None:
            env = {}

        self.lastCommand = commandToRun
        try:
            self.process = subprocess.run(['bash', '-c', commandToRun], cwd=self.runDir, capture_output=captureOutput, env=env)
        except Exception as e:
            Utils.exitWithException(f"Failed to run command: {commandToRun}", e)

    def getStdOut(self) -> str:
        if self.process.stdout:
            return bytes.decode(self.process.stdout)
        return ""

    def getStdErr(self) -> str:
        if self.process.stderr:
            return bytes.decode(self.process.stderr)
        return ""

    def getExitCode(self) -> int:
        return self.process.returncode

    def throwIfNonZeroExitCode(self):
        if self.process.returncode != 0:
            Utils.exitWithError(f"{self.getStdErr()}\n\n"
                                f"Failed to run command: '{self.lastCommand}'. Exit code: {self.process.returncode}.")
