from psychopy import core, visual
from psychopy.hardware import keyboard

print("creating window", flush=True)
win = visual.Window([800, 600], fullscr=False)

print("creating keyboard", flush=True)
kb = keyboard.Keyboard()

print("starting loop", flush=True)
timer = core.Clock()

while timer.getTime() < 5:
    keys = kb.getKeys(["space", "escape"], clear=True, waitRelease=False)
    states = kb.getState("space")
    if keys:
        print(keys, flush=True)
    win.flip()

print("loop done", flush=True)

print("closing window", flush=True)
win.close()

print("before core.quit", flush=True)
core.quit()