import sys
import pygame
import platform
import os
import subprocess
import inspect

def get_mypath():
    frame = inspect.stack()[1]
    caller_file = frame.filename
    return os.path.abspath(caller_file)
from ..core import _gp_log
        
def quit():
    _gp_log(f"program was quit")
    pygame.quit()
    sys.exit()
    
def hit_check(position,size , mouse_pos):
    x, y = position
    w, h = size
    mx, my = mouse_pos
    return x <= mx <= x + w and y <= my <= y + h

def fonts():
    from ..pather import BASE_DIR
    with open(f"{BASE_DIR}/fonts.txt", "r", encoding="utf-8") as f:
        con = f.read()

    return con

def look(obj, target_pos, smooth: float | None = None):
    import math
    def _shortest_angle_diff(target, current):
        diff = (target - current + 180) % 360 - 180
        return diff
    tx, ty = target_pos
    dx = tx - obj.x
    dy = ty - obj.y
    desired_angle = -math.degrees(math.atan2(dy, dx)) 

    if smooth is None:
        obj.angle = desired_angle
    else:
        current = obj.angle % 360
        delta = _shortest_angle_diff(desired_angle, current)
        obj.angle = current + delta * max(0.0, min(1.0, smooth))
        
def slide(obj, start_pos, end_pos, speed=2):
    x, y = start_pos
    dx = end_pos[0] - x
    dy = end_pos[1] - y
    dist = (dx**2 + dy**2) ** 0.5

    if dist > speed:
        x += dx / dist * speed
        y += dy / dist * speed
    else:
        x, y = end_pos

    if hasattr(obj, "pos"):
        obj.pos = (x, y)

    return (x, y)



def blit(surface, obj, position):
    surface().blit(obj, position)

def unpackobj(obj):
    x,y = obj.pos
    w,h = obj.size
    return x,y,w,h

def screenshot(surface, name=f"screenshot.jpg", msg=True):
    from .gpbox import Messagebox as msgbox
    surface = surface()
    pygame.image.save(surface, name)
    if msg:
        msgbox(f"Screenshot was save in \n'{name}' .").show(type=61)


import os
import inspect
import pickle
import json

def gpdata_save(objects, filename="objects.dat", type=""):
    # ai//t:my
    data = []

    for obj in objects:
        if isinstance(obj, dict):
            obj_data = obj.copy()
        elif hasattr(obj, "__dict__"):
            obj_data = obj.__dict__.copy()
            for name, attr in inspect.getmembers(type(obj), lambda o: isinstance(o, property)):
                try:
                    obj_data[name] = getattr(obj, name)
                except Exception:
                    pass
            obj_data['_class'] = type(obj).__name__
        else:

            obj_data = {"_value": obj}

        data.append(obj_data)

    ext = os.path.splitext(filename)[1].lower()
    file_type = type.lower() if type else (".json" if ext == ".json" else "bin")

    try:
        if file_type == "json" or ext == ".json":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        else:  # default pickle
            with open(filename, "wb") as f:
                pickle.dump(data, f)
        _gp_log(f"saved to '{filename}'")
    except Exception as e:
        _gp_log(f"[fatal error]: could not save objects '{e}'")


def gpdata_load(filename="objects.dat", type=""):
    # ai//t:my

    if not os.path.exists(filename):
        _gp_log("no saved file found.")
        return []

    if os.path.getsize(filename) == 0:
        _gp_log("saved file is empty.")
        return []

    ext = os.path.splitext(filename)[1].lower()
    file_type = type.lower() if type else (".json" if ext == ".json" else "bin")

    try:
        if file_type == "json" or ext == ".json":
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:  # default pickle
            with open(filename, "rb") as f:
                data = pickle.load(f)
        _gp_log(f"loaded from '{filename}'")
        return data
    except (json.JSONDecodeError, EOFError, Exception) as e:
        _gp_log(f"[fatal error]: file corrupted or invalid: {e}")
        return []


def build(script_path: str, icon=None, windowed=False, output_dir=None):
    import subprocess
    from pathlib import Path
    import platform
    from ..pather import paths, ICON70
    from ..core import _gp_log

    script_path = Path(script_path).resolve()
    sep = ";" if platform.system() == "Windows" else ":"
    base_dir = Path(__file__).resolve().parent.parent
    assets_dir = base_dir / "assets"
    plugins_dir = base_dir / "plugins"

    if not assets_dir.exists():
        print("[build]: 'assets' folder not found!",assets_dir)
        return

    if icon is None:
        icon = ICON70

    if output_dir is None:
        output_dir = script_path.parent
    else:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

    def collect_add_data(folder: Path, target_name: str):
        items = []
        for path in folder.rglob("*"):
            if path.is_file():
                rel_path = path.relative_to(folder)
                items.append(f"{path}{sep}{target_name}/{rel_path.as_posix()}")

        return items

    add_data = collect_add_data(assets_dir, "assets") + collect_add_data(plugins_dir, "plugins")

    command = [
        "pyinstaller",
        "--onefile",
        f"--distpath={output_dir}",
        str(script_path)
    ]

    if icon:
        command.append(f"--icon={icon}")
    if windowed:
        command.append("--noconsole")
    for data in add_data:
        command.append(f"--add-data={data}")

    _gp_log("[build]: running PyInstaller...")
    _gp_log("[build]: command:" + " ".join(command))

    result = subprocess.run(command, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    if result.returncode != 0:
        _gp_log("[build]: PyInstaller finished with an error!")
    else:
        _gp_log("[build]: Build completed successfully!")

  
def anchor(position=None, size=None, anchor="topleft", obj=None, reverse=False):
    # //ai
    if obj is not None:
        x = getattr(obj, "x", 0)
        y = getattr(obj, "y", 0)
        width = getattr(obj, "width", getattr(obj, "w", 0))
        height = getattr(obj, "height", getattr(obj, "h", 0))
    elif position is not None and size is not None:
        x, y = position
        width, height = size
    else:
        raise ValueError("You must provide either 'obj', or both 'position' and 'size'.")

    if not reverse:
        if anchor == "topleft":
            return x, y
        elif anchor == "topright":
            return x - width, y
        elif anchor == "bottomleft":
            return x, y - height
        elif anchor == "bottomright":
            return x - width, y - height
        elif anchor == "center":
            return x - width // 2, y - height // 2
        elif anchor == "midtop":
            return x - width // 2, y
        elif anchor == "midbottom":
            return x - width // 2, y - height
        elif anchor == "midleft":
            return x, y - height // 2
        elif anchor == "midright":
            return x - width, y - height // 2
        else:
            raise ValueError(f"Unknown anchor name: {anchor}")
    else:
        if anchor == "topleft":
            return x, y
        elif anchor == "topright":
            return x + width, y
        elif anchor == "bottomleft":
            return x, y + height
        elif anchor == "bottomright":
            return x + width, y + height
        elif anchor == "center":
            return x + width // 2, y + height // 2
        elif anchor == "midtop":
            return x + width // 2, y
        elif anchor == "midbottom":
            return x + width // 2, y + height
        elif anchor == "midleft":
            return x, y + height // 2
        elif anchor == "midright":
            return x + width, y + height // 2
        else:
            raise ValueError(f"Unknown anchor name: {anchor}")

_colors = {
"WHITE"  : (255, 255, 255),
"BLACK"  : (0, 0, 0),
"RED"  : (255, 0, 0),
"GREEN"  : (0, 255, 0),
"BLUE"  : (0, 0, 255),
"YELLOW"  : (255, 255, 0),
"CYAN"   : (0, 255, 255),
"MAGENTA" : (255, 0, 255),
"GRAY": (128, 128, 128),
"GRAY1" : (30, 30, 30),
"LIGHTGRAY"  : (200, 200, 200),
"DARKGRAY": (50, 50, 50),
"ORANGE" : (255, 165, 0),
"PURPLE"  : (128, 0, 128),
"PINK"   : (255, 192, 203),
"BROWN"    : (139, 69, 19),
"SKY"        : (0, 135, 215),
}

class Color:
    def __init__(self, color):
        if isinstance(color, str) and color.upper() in _colors:
            self._color = _colors[color.upper()]
        elif isinstance(color, tuple) and len(color) == 3:
            self._color = color
        else:
            raise ValueError(f"undefined color '{color}'")

    def __call__(self):
        return self._color

    def __repr__(self):
        return f"Color({self._color})"
    def __iter__(self):
        return iter(self._color)