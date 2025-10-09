_colors = {
    "WHITE"      : (255, 255, 255),
    "BLACK"      : (0, 0, 0),
    "RED"        : (255, 0, 0),
    "GREEN"      : (0, 255, 0),
    "BLUE"       : (0, 0, 255),
    "YELLOW"     : (255, 255, 0),
    "CYAN"       : (0, 255, 255),
    "MAGENTA"    : (255, 0, 255),
    "GRAY"       : (128, 128, 128),
    "GRAY1"      : (30, 30, 30),
    "LIGHTGRAY"  : (200, 200, 200),
    "DARKGRAY"   : (50, 50, 50),
    "ORANGE"     : (255, 165, 0),
    "PURPLE"     : (128, 0, 128),
    "PINK"       : (255, 192, 203),
    "BROWN"      : (139, 69, 19),
    "BEIGE"      : (245, 245, 220),
    "IVORY"      : (255, 255, 240),
    "TAN"        : (210, 180, 140),
    "OLIVE"      : (128, 128, 0),
    "NAVY"       : (0, 0, 128),
    "TEAL"       : (0, 128, 128),
    "MAROON"     : (128, 0, 0),
    "LIGHTBLUE"  : (173, 216, 230),
    "LIGHTGREEN" : (144, 238, 144),
    "LIGHTPINK"  : (255, 182, 193),
    "LIGHTYELLOW": (255, 255, 224),
    "DARKRED"    : (139, 0, 0),
    "DARKGREEN"  : (0, 100, 0),
    "DARKBLUE"   : (0, 0, 139),
    "DARKORANGE" : (255, 140, 0),
    "SKY"        : (0, 135, 215),
    "FOREST"     : (34, 139, 34),
    "GOLD"       : (255, 215, 0),
    "SILVER"     : (192, 192, 192),
    "TURQUOISE"  : (64, 224, 208),
}

def mycolor(colorcode: str = "RED-Lx5"):
    try:
        parts = colorcode.split("-")
        color = parts[0].upper()
        edit = parts[1].split("x")[0].upper()
        steps = int(parts[1].split("x")[1])
        
        base = _colors[color]
        r, g, b = base

        if edit == "L":  # Lighten
            factor = 10 * steps
            r = min(255, r + factor)
            g = min(255, g + factor)
            b = min(255, b + factor)
        elif edit == "D":  # Darken
            factor = 10 * steps
            r = max(0, r - factor)
            g = max(0, g - factor)
            b = max(0, b - factor)

        return (r, g, b)
    except Exception as e:
        raise Exception(f"error parsing color: {e}")


class _Color:
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
