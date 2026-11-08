from pathlib import Path
import pyglet
from PIL import ImageGrab

def screenshot(screen=0, folder=".", name=None, ext=".png"):
    """Capture a monitor (0 = first, 1 = second, ...) and save it as folder/name + ext.
    If that file already exists, a number is appended (name_1, name_2, ...)."""
    s = pyglet.canvas.get_display().get_screens()[screen]
    img = ImageGrab.grab(bbox=(s.x, s.y, s.x + s.width, s.y + s.height), all_screens=True)

    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    name = name or f"screen{screen}"

    path = folder / f"{name}{ext}"
    n = 1
    while path.exists():
        path = folder / f"{name}_{n}{ext}"
        n += 1

    img.save(path)
    return path

# example
# folder: relative path to folder for storing screenshots
# name: name for the image (e.g. the name of the participant being calibrated)
# if multiple screenshots are taken they will be numbered automatically
screenshot(1,"calibration_screenshots","test_participant")