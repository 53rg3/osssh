import click

from models import Mode
from prompts.CachePrompt import updateCachePrompt
from prompts.InstanceSelection import instanceSelectionPrompt
from prompts.ModeSelection import selectModePrompt
from prompts.ScpPrompt import uploadPrompt, downloadPrompt
from utils import InstanceIndex, Utils, Action


@click.command()
@click.option("-u", "--update", is_flag=True,
              help="Shows prompt to update the cache, sourced from `openstack server list`")
@click.option("-l", "--list", is_flag=True,
              help="Prints list of all service in the cache")
@click.option("-e", "--export", required=False,
              help="Prints the ENVs of the desired OpenStack project")
def main(update, list, export):
    if update:
        updateCachePrompt(InstanceIndex.loadOsProjectsListOnly())

    if list:
        InstanceIndex.printList()
        exit(0)

    if export:
        InstanceIndex.printEnvs(export)
        exit(0)

    # Prepare
    instanceIndex = InstanceIndex.create()
    sshData = instanceSelectionPrompt(instanceIndex)
    mode = selectModePrompt()

    # Execute
    if mode == Mode.ssh:
        Action.ssh(sshData)
    elif mode == Mode.download:
        downloadPrompt(sshData)
    elif mode == Mode.upload:
        uploadPrompt(sshData)
    else:
        Utils.exitWithError(f"Mode not recognized, got '{mode}'")


if __name__ == '__main__':
    main()
