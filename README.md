# GamePie Documentation
Developed since June 15, 2025

## Description

GamePie is a simple library for creating 2D games using the pygame library.  
It works on MS Windows and Linux (possibly macOS).

---

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Modules & Objects](#modules--objects)
  - [Main Objects](#main-objects)
    - [Window](#window)
    - [Camera](#camera)
    - [Objects](#objects)
    - [Namespace](#namespace)
  - [Loading](#loading)
    - [Load Texture](#texture)
    - [Load Frames](#frames)
    - [Font](#font)
  - [Rendering objects](#rendering)
    - [Animation](#animation)
    - [Label](#label)
    - [Image](#image)
    - [Rectangle](#rectangle)
    - [Ellipse](#ellipse)
    - [Polygon](#polygon)
    - [Line](#line)
  - [Sound & Mixer](#sound--mixer)
    - [Sound](#sound)
- [Example](#example)
- [Plugin System](#plugin-system)
- [More](#more)

## Installation

1. Download the library files.
2. Open the folder in your terminal. ( cd /home/ruda/Dokumenty/Python/gamepie )
3. Install using:

```bash
pip install .
```

### For Linux (with virtual environment):

```bash
python -m venv venv
source venv/bin/activate
pip install .
```

### Run (with virtual environment)
```bash
python -m venv venv
source venv/bin/activate
python <name>.py
```

---

## Modules & Objects

### Window

**`gamepie.Window`**  
Creates the main game window.  
**Arguments:**  
- `title`: Window title  
- `flags`: Window flags (e.g., `gamepie.utils.RESIZABLE`)

### Camera

**`gamepie.Camera`**  
Handles camera position, zoom, and anchor for rendering.

### Load texture

**`gamepie.load.Texture(path)`**  
Loads an image texture from assets.

### Load frames

**`gamepie.load.Frames(path)`**  
Loads animation frames from assets.

### Animation

**`gamepie.draw.Animation`**  
Rendering object
Draws and animates a sprite on the surface.  
**Arguments:**  
- `surface`: Target window  
- `position`: (x, y) coordinates  
- `frames`: Animation frames  
- `ms`: Frame duration in ms  
- `size`: (width, height)  
- `camera`: Camera object  
- `anchor`: Anchor position

### Label

**`gamepie.draw.gui.Label`**  
Rendering object
Draws a text label on the surface.  
**Arguments:**  
- `surface`: Target window  
- `position`: (x, y)  
- `font`: Font object  
- `text`: String to display  
- `background_color`: Background color  
- `anti_aliasing`: Boolean  
- `camera`: Camera object  
- `anchor`: Anchor position  
- `visible`: Boolean

### Image

**`gamepie.draw.Image`**  
Rendering object
Draws an image on the surface.  
**Arguments:**  
- `surface`: Target window  
- `texture`: Texture object  
- `position`: (x, y)  
- `size`: (width, height)  
- `camera`: Camera object  
- `anchor`: Anchor position

### Rectangle

**`gamepie.draw.Rectangle`** 
Rendering object
Draws a rectangle.  
**Arguments:**  
- `surface`: Target window  
- `position`: (x, y)  
- `size`: (width, height)  
- `color`: RGB tuple  
- `camera`: Camera object  
- `anchor`: Anchor position

### Ellipse

**`gamepie.draw.Ellipse`**  
Rendering object
Draws an ellipse.  
**Arguments:**  
- `surface`: Target window  
- `position`: (x, y)  
- `size`: (width, height)  
- `color`: RGB tuple  
- `anchor`: Anchor position

### Polygon

**`gamepie.draw.polygon`**  
Rendering funcion
Draws a polygon.  
**Arguments:**  
- `surface`: Target surface  
- `color`: RGB tuple  
- `points`: List of (x, y) tuples  
- `width`: Line thickness (0 = filled)  
- `angle`: Rotation angle  
- `flip`: (flip_x, flip_y)

### Line

**`gamepie.draw.line`**  
Rendering funcion
Draws a line.  
**Arguments:**  
- `surface`: Target surface  
- `color`: RGB tuple  
- `start_pos`: (x, y)  
- `end_pos`: (x, y)  
- `width`: Line thickness  
- `anti_aliasing`: Boolean  
- `blend`: Boolean  
- `angle`: Rotation angle

### Objects

**`gamepie.utils.Objects`**  
Groups multiple drawable objects for batch operations.

### Namespace

**`gamepie.utils.Namespace`**  
Stores and manages game state variables.

### Sound & Mixer

**`gamepie.mixer.Sound`**  
Loads and plays sound effects.

### Font

**`gamepie.load.Font`**  
Loads a font for text rendering.

---

## Example

```python
import gamepie

surface = gamepie.Window(title="Test", flags=gamepie.utils.RESIZABLE)
fps = gamepie.Clock(60)

pie_texture = gamepie.load.Texture("pie")
pie = gamepie.draw.Image(surface, texture=pie_texture)

def update():
    dt = fps.tick()
    speed = 0.1 * dt
    pie.x += speed
    surface.fill(gamepie.WHITE)
    pie.draw()
    surface.flip()

surface.run()
gamepie.quit()
```
**Quick use:**
```python
import gamepie

# Direct access to main objects
win = gamepie.Window(...)
cam = gamepie.Camera(...)
rect = gamepie.draw.Rectangle(...)
img = gamepie.draw.Image(...)
label = gamepie.draw.gui.Label(...)
controller = gamepie.plugins.Controllers.PlatformController(...)
sound = gamepie.mixer.Sound(...)
font = gamepie.load.Font(...)
objects = gamepie.utils.Objects(...)
namespace = gamepie.utils.Namespace(...)
color = gamepie.utils.Color("SKY")()
```
---

## Commands
- for more informacion write in terminal 
  ```bash
  python -m gamepie.commands.help
  ```

## Plugin System

- Install plugins from local folders or git URLs using `install(path_or_url)`.
- Uninstall plugins by name using `uninstall(name)`.
- Plugins must contain a `.gpplugin` file at the top level.

---

## More

For more examples, see the `src/` folder and the `examples.py` file.

Made by Rudolf Mueller

