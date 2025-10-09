import os

codes = {
    "main.py": """
import gamepie 

screen = gamepie.Window()

def update():
    screen.fill("sky")
    screen.flip()

screen.run()
""",

    "gp.toml": """
[plugins]
use = ["gamepie.plugins.SoundsAssets","gamepie.plugins.Controllers",]
"""
}

def main():
    dst = os.getcwd()
    for key, value in codes.items():
        path = os.path.join(dst, key)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as pf:
                pf.write(value.strip() + "\n")
            print(f"created: {key}")
        else:
            print(f"skipped (already exists): {key}")

    print("\nthe gamepie project was successfully created.")

if __name__ == "__main__":
    main()
