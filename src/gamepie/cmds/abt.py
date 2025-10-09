def main():
    import subprocess; subprocess.run(["cls" if subprocess.os.name == "nt" else "clear"])  
    asciiart = r"""                                      
                @@@@@%%%%%%%%%@@@@@                    
        @@%%@%#+=--::::::::::---=*#%@@@               
    @@@@*%*=-::::::-=**::::::::::::-=+%@@            
    @%==%%--:::::-+@@=:::::=%::::::::::-==%@@         
    @@+=+%==-::::=#+::::::-#@=::::*#:::#=:-==#@@
    @@+==@==--::::::::::::#@*:::::-%%-::=%*-===#@@@
    @%===#@*-=-:::::::::::#-:::::::=%%::::=%-===+@*%@  
    @@#===*%====-::::::::::::::::::-%-:::::-====#%*@  
    @@%===#%%#+==--:::::::::::::::::::::--====*@*+%@
    @%#@#======#%+--==----:::::::::::--==-===+%%+=%@
    @%++*%@@@#====*@@%%%#-==----==--=======+%@*=+%@@
    @@#+++*+*#%%+=========%%@@@%%%%%###%%*+=====#@@ 
        @@#+++++++*#%%%%%@%+-================+###%@@   
        @@#++++++*+++++**#%@%%%%@%%@%%%%%%@%#%@      
            @@%#++++++++++++++*****++*********%@       
            @@@@#*+++++++++*++++++********%@        
                @@@@%%#**++++++++*****#%%@@         
                        @@@@@@@@@@@@@@@@@@            
                                                    

                                                    """
    text = [
        "GamePie is a Python library for making 2D games and multimedia applications.",
        "Websites: https://github.com/ZeleznaRuda/GamePie-Engine :: https://www.youtube.com/@gamepieengine",
        "For help use command: gphelp",
    ]
    ascii_lines = asciiart.splitlines()
    text_lines = text
    max_lines = max(len(ascii_lines), len(text_lines))
    ascii_lines += [""] * (max_lines - len(ascii_lines))
    text_lines += [""] * (max_lines - len(text_lines))

    for left, right in zip(ascii_lines, text_lines):
        print(f"{left:55} {right}") 
if __name__ == "__main__":
    main()
