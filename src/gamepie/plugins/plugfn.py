import os
import shutil
import json
import tempfile
import subprocess
from gamepie.core import _gp_log
from urllib.parse import urlparse
import platform

protected_plugins = ["GUIassets","SoundsAssets"]

def install(input_path):
    current_folder = os.path.dirname(os.path.abspath(__file__))
    plugins_folder = os.path.join(current_folder, "")

    if not os.path.exists(plugins_folder):
        os.makedirs(plugins_folder)

    if input_path.startswith("http://") or input_path.startswith("https://"):
        parsed_url = urlparse(input_path)
        folder_name = os.path.basename(parsed_url.path).replace(".git", "")
        temp_dir = tempfile.mkdtemp()
        try:
            subprocess.check_call(["git", "clone", input_path, os.path.join(temp_dir, folder_name)])
            input_path = os.path.join(temp_dir, folder_name)
        except Exception as e:
            _gp_log(f"[plugin warning]: Failed to clone repository: {e}")
            return
    else:
        folder_name = os.path.basename(input_path)

    has_gpplug = [
        f for f in os.listdir(input_path)
        if f.endswith(".gpplugin") and os.path.isfile(os.path.join(input_path, f))
    ]

    author = "Unknown"
    if has_gpplug:
        gp_file = os.path.join(input_path, has_gpplug[0])
        try:
            with open(gp_file, "r", encoding="utf-8") as f:
                gp_data = json.load(f)
            author = gp_data.get("author", "Unknown")
        except Exception as e:
            _gp_log(f"[plugin warning]: Failed to read .gpplugin file: {e}")

    answer = input(f"\nAre you sure you want to install plugin:\n\tName: '{folder_name}'\n\tCreated by: {author}\n\tFrom: {input_path}\n\033[91mbe careful (Y/n): \033[0m")
    if answer.lower() not in ["y", "yes", ""]:
        _gp_log("[plugin warning]: Installation canceled by user.")
        return

    if has_gpplug:
        gp_file = os.path.join(input_path, has_gpplug[0])
        try:
            with open(gp_file, "r", encoding="utf-8") as f:
                gp_data = json.load(f)

            plugin_os = gp_data.get("os", "any")
            _gp_log(f"[plugin info]: Plugin '{folder_name}' is created by {author}.")

            current_os = platform.system()
            if plugin_os != "any" and plugin_os.lower() != current_os.lower():
                _gp_log(f"[plugin warning]: This plugin is built for {plugin_os}, do you really want to install it on {current_os}? (Y/n): ")
                answer = input()
                if answer.lower() not in ["y", "yes", ""]:
                    _gp_log("[plugin warning]: Installation canceled by user.")
                    return
                else:
                    _gp_log("[plugin info]: Installation confirmed by user.")

        except Exception as e:
            _gp_log(f"[plugin warning]: Failed to read .gpplugin file: {e}")

        destination = os.path.join(plugins_folder, folder_name)
        if os.path.exists(destination):
            shutil.rmtree(destination)
        shutil.copytree(input_path, destination)
        _gp_log(f"[plugin info]: Plugin '{folder_name}' has been installed in 'plugins/'.")
    else:
        _gp_log("[plugin warning]: This folder is not a Gamepie plugin (to make it a plugin, create a .gpplugin file in the first level of the folder).")

def uninstall(name):
    current_folder = os.path.dirname(os.path.abspath(__file__))
    plugins_folder = os.path.join(current_folder, "")
    target_folder = os.path.join(plugins_folder, name)

    if not os.path.isdir(target_folder):
        _gp_log(f"[plugin warning]: Plugin folder '{name}' was not found in 'plugins/'.")
        return

    gpplug_files = [
        f for f in os.listdir(target_folder)
        if f.endswith(".gpplugin") and os.path.isfile(os.path.join(target_folder, f))
    ]

    if gpplug_files:
        if name in protected_plugins:
            _gp_log(f"[plugin warning]: Plugin folder '{name}' is protected and cannot be removed.")
            return

    shutil.rmtree(target_folder)
    _gp_log(f"[plugin info]: Plugin folder '{name}' has been removed from 'plugins'.")
