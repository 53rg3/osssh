from utils import Utils


def writeToFile(path: str, content: str):
    with open(path, "w") as file:
        try:
            return file.write(content)
        except Exception as e:
            Utils.exitWithException(f"Failed write {path}", e)
