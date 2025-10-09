import os

def main():
    cmdsname = {"gp":"Game Pie specifications",
                "gpabout":"About Game Pie (aka command gp)",
                "gphelp":"Help for GamePie commands",
                "gpbuild":"Build GamePie project into executable (is in beta)",
                "gpupdater":"Update GamePie installation",
                "gpplug":"Plugin system for GamePie",
                "gphelp":"Command Help for GamePie"}
    import subprocess; subprocess.run(["cls" if subprocess.os.name == "nt" else "clear"])
    folder_path = os.path.dirname(os.path.abspath(__file__))
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print("Use commands:")
    print("\tpython -m gamepie.cmds.<command>")
    print(" "*4+"OR:")
    print("\tUse one of the commands listed below in the commands list.\n")
    print("Commands list:")
    for k,v in cmdsname.items():
        print(f"\t:: {k} -> {v}")

if __name__ == "__main__":
    main()
