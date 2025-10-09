import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ['SDL_VIDEO_CENTERED'] = '1'

GAMEPIE_LOG = os.environ.get('GAMEPIE_LOG', '1') == '1'

def _gp_log(msg: str,start="", end="\n", flush=False):
    if GAMEPIE_LOG:
        print(start,f"[gamepie]: {msg}", end=end, flush=flush)