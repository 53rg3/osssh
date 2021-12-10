from prompt_toolkit.styles import Style

from utils import Utils

configFile = f"{Utils.getProjectRoot()}/config.yml"
cacheDir = f"{Utils.getProjectRoot()}/.cache"

promptStyle = Style.from_dict({
    "yellow": "ansiyellow"
})
