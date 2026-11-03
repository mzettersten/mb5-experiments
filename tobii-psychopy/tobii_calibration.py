"""Infant-friendly Tobii calibration, run from the Calibration routine in Builder.
Uses Builder's window; positioning screen, then 5-point calibration.
Library: https://github.com/yh-luo/psychopy_tobii_infant"""
import os
import glob
import atexit
from psychopy import visual, sound
from psychopy_tobii_infant import TobiiInfantController
from psychopy.visual.movies import MovieStim as _MovieStim

_original_unload = _MovieStim.unload


def _patched_unload(self):
    if not hasattr(self, '_freePlayer'):
        self._freePlayer = lambda: None
    _original_unload(self)


_MovieStim.unload = _patched_unload

HERE = os.path.dirname(os.path.abspath(__file__))
STIM_DIR = os.path.join(HERE, "CalibrationStim")

# fraction of screen width/height from center
CALI_POINTS = [(-0.4, 0.4), (-0.4, -0.4), (0.0, 0.0), (0.4, 0.4), (0.4, -0.4)]


def run_infant_calibration(win):
    aspect = win.size[0] / win.size[1]
    points = [(x * 2 * aspect, y) for x, y in CALI_POINTS]  # to height units
    stims = sorted(glob.glob(os.path.join(STIM_DIR, "*.png")))
    grabber = visual.MovieStim(win, os.path.join(STIM_DIR, "Attentiongrabber.mp4"),
                               loop=True, size=(0.741, 0.417), units="height",
                               volume=0.4)
    chime = sound.Sound(os.path.join(STIM_DIR, "upchime1.wav"))

    et = TobiiInfantController(win)
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
