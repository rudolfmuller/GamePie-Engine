import subprocess
import platform
from ..pather import resource_path
from ..core.mixer import Sound
from ..core.load import Audio
# ai//t:my
class Messagebox:
    def __init__(self, msg, title=None):
        self._title = title
        self._msg = msg
        self.result = None 
        self.s = Sound(Audio(resource_path("assets/msgIco/music-box.mp3"), volume=10,msg=False))
        self.s.play()

    def _get_system_theme(self):
        system = platform.system()
        if system == "Windows":
            try:
                import winreg
                registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return "Light" if value == 1 else "Dark"
            except Exception:
                return "Unknown"
        elif system == "Darwin":
            try:
                result = subprocess.run(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"],
                    capture_output=True, text=True
                )
                return "Dark" if "Dark" in result.stdout else "Light"
            except Exception:
                return "Light"
        elif system == "Linux":
            try:
                result = subprocess.run(
                    ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                    capture_output=True, text=True
                )
                output = result.stdout.strip().lower()
                if "dark" in output:
                    return "Dark"
                elif "light" in output:
                    return "Light"
            except Exception:
                pass
            try:
                result = subprocess.run(
                    ["gsettings", "get", "org.cinnamon.desktop.interface", "gtk-theme"],
                    capture_output=True, text=True
                )
                theme = result.stdout.strip().strip("'").lower()
                if "dark" in theme:
                    return "Dark"
                else:
                    return "Light"
            except Exception:
                pass
            return "Unknown"
        else:
            return "Unknown"

    def showerror(self):
        self.show(type=0)

    def showwarning(self):
        self.show(type=1)

    def showinfo(self):
        self.show(type=2)

    def askquestion(self):
        return self.show(type=3) 

    def showask(self):
        self.show(type=4)

    def showscreenshot(self):
        self.show(type=5)

    def show(self, type=0):
        theme = self._get_system_theme()
        import tkinter as tk
        from PIL import Image, ImageTk
        from tkinter import ttk

        root = tk.Tk()
        bg_color = "#f0f0f0" if theme == "Light" else "#2e2e2e"
        fg_color = "#000000" if theme == "Light" else "#ffffff"
        root.config(bg=bg_color)

        type_str = str(type).zfill(2)
        icon_type = int(type_str[0])
        button_type = int(type_str[1])

        icons = {
            0: ("Error", resource_path("assets/msgIco/gperr.png")),
            1: ("Error", resource_path("assets/msgIco/gperr.png")),
            2: ("Warning", resource_path("assets/msgIco/gpwarn.png")),
            3: ("Info", resource_path("assets/msgIco/gpmsg.png")),
            4: ("Question", resource_path("assets/msgIco/gpqest.png")),
            5: ("Information", resource_path("assets/msgIco/gpinfo.png")),
            6: ("Screenshot", resource_path("assets/msgIco/gpscrshot.png")),
        }

        title, icon_path = icons.get(icon_type, icons[0])
        if self._title:
            root.title(self._title)
        else:
            root.title(title)

        img = Image.open(icon_path)

        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(
            root,
            image=photo,
            text=self._msg,
            compound="left",
            font=("Arial", 12),
            anchor="nw",
            justify="left",
            bg=bg_color,
            fg=fg_color
        )
        label.pack(padx=10, pady=2, fill="both")

        def set_result(value):
            self.result = value
            root.destroy()

        button_map = {
            0: [],  
            1: [("OK", lambda: set_result("ok"))],
            2: [("OK", lambda: set_result("ok")), ("Cancel", lambda: set_result("cancel"))],
            3: [("Yes", lambda: set_result("yes")), ("No", lambda: set_result("no")), ("Cancel", lambda: set_result("cancel"))],
            4: [("OK", lambda: set_result("ok"))], 
            5: [("Close", lambda: set_result("close"))],
        }

        if button_type in button_map and button_map[button_type]:
            button_frame = tk.Frame(root, bg=bg_color)
            button_frame.pack(pady=10, anchor="e")
            for text, cmd in button_map[button_type]:
                style = ttk.Style()
                style.configure("Custom.TButton", padding=2,font=("Arial", 11))
                btn = ttk.Button(button_frame, text=text, command=cmd, style="Custom.TButton",)
                btn.pack(side="right", padx=5)

        root.resizable(False, False)
        root.after(30000, lambda: root.destroy())
        root.mainloop()
        return self.result



def gpfile_dialog(typefiles=None, select=0):
    #ai//
    import ctypes
    from ctypes import wintypes
    system = platform.system()

    # --- WINDOWS ---
    if system == "Windows":
        GetOpenFileName = ctypes.windll.comdlg32.GetOpenFileNameW

        class OPENFILENAMEW(ctypes.Structure):
            _fields_ = [
                ("lStructSize", wintypes.DWORD),
                ("hwndOwner", wintypes.HWND),
                ("hInstance", wintypes.HINSTANCE),
                ("lpstrFilter", wintypes.LPCWSTR),
                ("lpstrCustomFilter", wintypes.LPWSTR),
                ("nMaxCustFilter", wintypes.DWORD),
                ("nFilterIndex", wintypes.DWORD),
                ("lpstrFile", wintypes.LPWSTR),
                ("nMaxFile", wintypes.DWORD),
                ("lpstrFileTitle", wintypes.LPWSTR),
                ("nMaxFileTitle", wintypes.DWORD),
                ("lpstrInitialDir", wintypes.LPCWSTR),
                ("lpstrTitle", wintypes.LPCWSTR),
                ("Flags", wintypes.DWORD),
                ("nFileOffset", wintypes.WORD),
                ("nFileExtension", wintypes.WORD),
                ("lpstrDefExt", wintypes.LPCWSTR),
                ("lCustData", wintypes.LPARAM),
                ("lpfnHook", wintypes.LPVOID),
                ("lpTemplateName", wintypes.LPCWSTR),
                ("pvReserved", wintypes.LPVOID),
                ("dwReserved", wintypes.DWORD),
                ("FlagsEx", wintypes.DWORD),
            ]

        def open_dialogWin():
            buffer = ctypes.create_unicode_buffer(260) 
            ofn = OPENFILENAMEW()
            ofn.lStructSize = ctypes.sizeof(ofn)
            ofn.lpstrFile = buffer
            ofn.nMaxFile = len(buffer)


            if typefiles is None:
                filter_str = "All files\0*.*\0"
            else:
                filter_str = ""
                for ext in typefiles:
                    filter_str += f"{ext.upper()} files\0*{ext}\0"
                filter_str += "All files\0*.*\0"

            ofn.lpstrFilter = filter_str
            ofn.nFilterIndex = 1
            ofn.Flags = 0x00001000 | 0x00000800  # FILEMUSTEXIST | PATHMUSTEXIST

            if GetOpenFileName(ctypes.byref(ofn)):
                return buffer.value
            return None

        return open_dialogWin()

    else:
        def open_dialogUnix():
            try:
                if select == 1:
                    cmd = ["zenity", "--file-selection", "--directory"]
                else:
                    cmd = ["zenity", "--file-selection"]
                    if typefiles is not None:
                        patterns = " ".join([f"*{ext}" for ext in typefiles])
                        cmd.append(f"--file-filter={patterns}")

                result = subprocess.check_output(cmd, text=True).strip()
                return result if result else None
            except (subprocess.CalledProcessError, FileNotFoundError):
                return None

        return open_dialogUnix()
