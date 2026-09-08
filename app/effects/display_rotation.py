import os
import json
import shutil
import subprocess
import time

TOTAL_DURATION = 120  # 2 minutes en secondes
INTERVAL = 10  # Intervalle de 10 secondes


class DisplayRotator:
    @staticmethod
    def _outputs_wlr_randr():
        try:
            result = subprocess.run(
                ["wlr-randr"],
                check=True,
                capture_output=True,
                text=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []

        outputs = []
        for line in result.stdout.splitlines():
            if not line.strip():
                continue
            if line.startswith((" ", "\t")):
                continue
            outputs.append(line.split()[0])
        return outputs

    @staticmethod
    def _set_rotation_x11(mode):
        subprocess.run(["xrandr", "-o", mode], check=True)

    @staticmethod
    def _set_rotation_wayland(mode):
        outputs = DisplayRotator._outputs_wlr_randr()
        if not outputs:
            raise RuntimeError(
                "Aucun output Wayland detecte via wlr-randr."
            )
        for output in outputs:
            subprocess.run(
                ["wlr-randr", "--output", output, "--transform", mode],
                check=True,
            )

    @staticmethod
    def _set_rotation_sway(mode):
        subprocess.run(
            ["swaymsg", "output", "*", "transform", mode],
            check=True,
        )

    @staticmethod
    def _set_rotation_hypr(mode):
        # 0 = normal, 2 = 180 degres
        hypr_mode = "2" if mode == "180" else "0"
        result = subprocess.run(
            ["hyprctl", "monitors", "-j"],
            check=True,
            capture_output=True,
            text=True,
        )
        monitors = []
        try:
            monitors = json.loads(result.stdout)
        except Exception as e:
            raise RuntimeError(
                "Impossible de lire la liste des moniteurs Hyprland"
            ) from e

        if not monitors:
            raise RuntimeError("Aucun moniteur detecte par hyprctl")

        for monitor in monitors:
            name = monitor.get("name")
            if not name:
                continue
            subprocess.run(
                [
                    "hyprctl",
                    "keyword",
                    "monitor",
                    f"{name},preferred,auto,1,transform,{hypr_mode}",
                ],
                check=True,
            )

    @staticmethod
    def roll():
        elapsed = 0  # Compteur de temps passe 
        session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
        wayland_backend = None
        if session_type == "wayland":
            if shutil.which("wlr-randr"):
                wayland_backend = DisplayRotator._set_rotation_wayland
            elif shutil.which("swaymsg"):
                wayland_backend = DisplayRotator._set_rotation_sway
            elif shutil.which("hyprctl"):
                wayland_backend = DisplayRotator._set_rotation_hypr
            else:
                print(
                    "\nErreur : session Wayland detectee, aucun backend "
                    "de rotation trouve."
                )
                print(
                    "Installe wlr-randr, ou utilise Sway/Hyprland, "
                    "ou passe en Xorg."
                )
                return

        set_rotation = (
            wayland_backend
            if wayland_backend
            else DisplayRotator._set_rotation_x11
        )
        inverted_mode = "180" if session_type == "wayland" else "inverted"
        normal_mode = "normal"

        try:
            while elapsed < TOTAL_DURATION:
                # 1. Retourne l'écran à l'envers (inverted)
                set_rotation(inverted_mode)
                time.sleep(INTERVAL)

                # 2. Remet l'écran à la normale
                set_rotation(normal_mode)
                time.sleep(INTERVAL)
                # Chaque cycle complet prend 20 secondes.
                elapsed += (INTERVAL * 2)

        except subprocess.CalledProcessError:
            if session_type == "wayland":
                print(
                    "\nErreur : echec de la rotation sur Wayland "
                    "avec le backend detecte."
                )
                print(
                    "GNOME/KDE Wayland bloquent souvent cette action "
                    "par securite."
                )
            else:
                print("\nErreur : Impossible d'utiliser xrandr.")
                print("Verifie que tu es bien sur une session graphique Xorg.")
        except RuntimeError as e:
            print(f"\nErreur : {e}")
        except KeyboardInterrupt:
            print("\nScript interrompu par l'utilisateur.")
        finally:
            # Remettre l'écran à l'endroit, même en cas d'erreur.
            try:
                set_rotation(normal_mode)
            except (subprocess.CalledProcessError, RuntimeError):
                pass
            print("Fin du programme. Écran réinitialisé à l'endroit.")


if __name__ == "__main__":
    DisplayRotator.roll()
