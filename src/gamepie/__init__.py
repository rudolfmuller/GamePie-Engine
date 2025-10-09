import os
import platform
from . import envs
from . import cmds
VERSION = 0.4
if os.environ.get('GAMEPIE_SHOW_WELCOME', '1') == '1':
    print(f"\n:: You use the \033[4m\033[33mGamePie\033[0m library to create 2d games\n:: Power by \033[4m\033[33mPygame\033[0m\n:: Version: {VERSION}")
    print(f":: Using: {platform.platform()}\n")

from .core import *
from . import plugins


