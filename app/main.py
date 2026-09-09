import subprocess
import sys

from pynput import keyboard

roue_deja_lancee = False


def lancer_programme():
    global roue_deja_lancee

    if roue_deja_lancee:
        return

    print("Touche détectée : lancement de la roue")
    subprocess.Popen(
        [sys.executable, "-m", "app.wheel"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
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
