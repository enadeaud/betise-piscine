import os
import subprocess
import sys

from pynput import keyboard

ROUTE_DE_LA_ROUE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "log_tonscreen.py",
)
processus_roue = None
roue_deja_lancee = False


def lancer_programme():
    global processus_roue
    global roue_deja_lancee

    if roue_deja_lancee:
        return

    print("Touche détectée : lancement de la roue")
    processus_roue = subprocess.Popen([sys.executable, ROUTE_DE_LA_ROUE])
    roue_deja_lancee = True


def on_press(key):
    if roue_deja_lancee:
        return

    try:
        if key == keyboard.Key.esc:
            return False
    except AttributeError:
        pass

    lancer_programme()


def main():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
