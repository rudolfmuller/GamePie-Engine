import os
import sys
import importlib
import tomllib 
from ..envs import _gp_log
_base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
if _base_dir not in sys.path:
    sys.path.append(_base_dir)

gp_toml_path = os.path.join(_base_dir, "gp.toml")
plugins = []

if os.path.exists(gp_toml_path):
    with open(gp_toml_path, "rb") as f:
        toml_data = tomllib.load(f)
        plugins = toml_data.get("plugins", {}).get("use", [])
else:
    raise FileNotFoundError(f"the configuration file (gp.toml) was not found. (in '{_base_dir}')")

for plugin_name in plugins:
    try:
        module = importlib.import_module(plugin_name)
        globals()[plugin_name.split(".")[-1]] = module 
        _gp_log(f"plugin '{plugin_name}' loaded successfully")
    except Exception as e:
        _gp_log(f"failed to load {plugin_name}: {e}")
