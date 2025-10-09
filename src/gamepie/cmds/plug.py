
import argparse
from ..plugins import plugfn
import subprocess
def main():    
    import subprocess; subprocess.run(["cls" if subprocess.os.name == "nt" else "clear"])  
    parser = argparse.ArgumentParser(
        description="Menu for GamePie plugins."
    )
    parser.add_argument(
        "--install","-i",
        help="Install plugin from folder path or URL",
        default=None
    )
    parser.add_argument(
        "--uninstall","-u",
        help="Uninstall plugin by specifying the name",
        default=None
    )
    parser.add_argument(
        "--showprotectedplugins","--spp",
        help="Show protected plugins",
        default=None
    )
    args = parser.parse_args()

    if args.install:
        plugfn.install(args.install)

    if args.uninstall:
        plugfn.uninstall(args.uninstall)

    if args.showprotectedplugins:
        print(f"Protected plugins: '{plugfn.protected_plugins}'")

if __name__ == "__main__":
    main()
