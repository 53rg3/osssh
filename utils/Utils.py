import click


def exitWithError(errorMessage: str):
    click.secho(f"{errorMessage}", fg="red")
    exit(1)


def exitWithException(errorMessage: str, exception: Exception):
    click.secho(f"{exception}", fg="red")
    click.secho(f"{errorMessage}", fg="red")
    exit(1)


def printInfo(message: str):
    click.secho(f"{message}", fg="yellow")


def throwIfNoneOrEmpty(value: str, errorMessage):
    if not value or value == "":
        exitWithError(errorMessage)


def getMandatoryKeyFromDict(key: str, dictionary: dict):
    try:
        return dictionary[key]
    except Exception as e:
        exitWithException(f"Failed to get key from dict, need: '{key}'.", e)


def getOptionalKeyFromDict(key: str, dictionary: dict):
    try:
        return dictionary[key]
    except (Exception, ):
        return None
