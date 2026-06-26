from psychopy import core, visual
from psychopy.hardware import keyboard

win = visual.Window([800, 600], fullscr=False)
kb = keyboard.Keyboard()

movie_path = "stimuli/movies/laughing_baby_no_audio_grey.mp4"

for i in range(5):
    print("movie", i, flush=True)
    mov = visual.MovieStim(win, filename=movie_path, loop=True)
    mov.play()

    timer = core.Clock()
    while timer.getTime() < 1:
        kb.getState("space")
        mov.draw()
        win.flip()

    mov.stop()
    try:
        mov._unload()
    except Exception:
        pass

win.close()
print("before core.quit", flush=True)
core.quit()