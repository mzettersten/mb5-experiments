from psychopy import core, visual
from psychopy.hardware import keyboard

win = visual.Window(fullscr=True, screen=2)
win2 = visual.Window([800, 800], screen=0)
win3 = visual.Window(fullscr=True, screen=1)

kb = keyboard.Keyboard()
timer = core.Clock()

while timer.getTime() < 5:
    kb.getState("space")
    win.flip()
    win2.flip()
    win3.flip()

win3.close()
win2.close()
win.close()

print("before core.quit", flush=True)
core.quit()