"""Infant-friendly Tobii calibration, run from the Calibration routine in Builder.
Uses Builder's window; positioning screen, then 5-point calibration.
Saves a screenshot each time the calibration results screen appears.
Library: https://github.com/yh-luo/psychopy_tobii_infant"""
import os
import glob
import atexit
from pathlib import Path
import pyglet
from PIL import ImageGrab
from psychopy import visual, sound, logging
from psychopy_tobii_infant import TobiiInfantController

HERE = os.path.dirname(os.path.abspath(__file__))
STIM_DIR = os.path.join(HERE, "CalibrationStim")
SCREENSHOT_DIR = os.path.join(HERE, "calibration_screenshots")

# fraction of screen width/height from center
CALI_POINTS = [(-0.4, 0.4), (-0.4, -0.4), (0.0, 0.0), (0.4, 0.4), (0.4, -0.4)]


def screenshot(screen=0, folder=".", name=None, ext=".png"):
    """Capture a monitor (0 = first, 1 = second, ...) and save it as folder/name + ext.
    If that file already exists, a number is appended (name_1, name_2, ...)."""
    display_mod = getattr(pyglet, "canvas", None) or pyglet.display  # pyglet 1.x / 2.x
    s = display_mod.get_display().get_screens()[screen]
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


class ScreenshotInfantController(TobiiInfantController):
    """Takes a screenshot the first time each results screen is shown."""

    def __init__(self, win, shot_folder, shot_name):
        super().__init__(win)
        self.shot_folder = shot_folder
        self.shot_name = shot_name

    def _show_calibration_result(self):
        img = super()._show_calibration_result()
        self.win.callOnFlip(self._save_shot)  # fires after results are drawn
        return img

    def _save_shot(self):
        try:
            path = screenshot(self.win.screen, self.shot_folder, self.shot_name)
            logging.exp(f"Calibration screenshot saved: {path}")
        except Exception as e:  # never crash calibration over a screenshot
            logging.warning(f"Calibration screenshot failed: {e}")


def run_infant_calibration(win, name="calibration", folder=SCREENSHOT_DIR):
    aspect = win.size[0] / win.size[1]
    points = [(x * aspect, y) for x, y in CALI_POINTS]  # to height units
    stims = sorted(glob.glob(os.path.join(STIM_DIR, "*.png")))
    grabber = visual.MovieStim(win, os.path.join(STIM_DIR, "Attentiongrabber.mp4"),
                               loop=True, size=(0.741, 0.417), units="height",
                               volume=0.4)
    chime = sound.Sound(os.path.join(STIM_DIR, "upchime1.wav"))

    et = ScreenshotInfantController(win, folder, name)
    atexit.unregister(et.close)  # no data file opened, skip close at exit

    # positioning, space to continue
    grabber.setAutoDraw(True)
    grabber.play()
    et.show_status()
    grabber.setAutoDraw(False)
    grabber.stop()

    ok = et.run_calibration(points, stims, audio=chime)
    win.flip()
    return ok
