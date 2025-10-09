_GITREPOURL = "https://github.com/ZeleznaRuda/GamePie-Engine.git"
import argparse
import tempfile
import subprocess
import os
import sys

def update():
    subprocess.run([sys.executable, "-m", "pip", "install", "git+" + _GITREPOURL], check=True)

def find_commits(n=1):
    with tempfile.TemporaryDirectory(prefix=f"gp_git_temp_{os.getpid()}_") as temp_dir:
        subprocess.run([
            "git", "clone", "--depth", str(n), "--no-checkout", _GITREPOURL, temp_dir
        ], check=True)
        result = subprocess.run(
            ["git", "-C", temp_dir, "log", "--oneline", f"-n{n}"],
            check=True,
            text=True,
            capture_output=True
        )
        
        print(result.stdout+"\n")

def main():
    import subprocess; subprocess.run(["cls" if subprocess.os.name == "nt" else "clear"])  
    parser = argparse.ArgumentParser(
        description="GamePie updater."
    )
    parser.add_argument(
        "--find","-f",
        help="Find all available updates.",
        type=int,
        default=None
    )
    parser.add_argument(
        "--upgrade","-u",
        help="Upgrade the GamePie installation.",
        default=None
    )

    args = parser.parse_args()

    if args.upgrade:
        update()
    if args.find:
        find_commits(args.find)


if __name__ == "__main__":
    main()
