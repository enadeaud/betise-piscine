import os
import random
import subprocess
from urllib.parse import quote

# --- CONFIGURATION ---
# Assure-toi que ce dossier existe et contient des images
DOSSIER_IMAGES = os.path.expanduser(".media")

EXTENSIONS_VALIDES = (".jpg", ".jpeg", ".png", ".webp", ".bmp")


def changer_fond_ecran(chemin_image):
    chemin_abs = os.path.abspath(chemin_image)
    uri_image = f"file://{quote(chemin_abs)}"

    # Application sur le thème clair ET le thème sombre
    for key in ["picture-uri", "picture-uri-dark"]:
        subprocess.run(
            [
                "gsettings",
                "set",
                "org.gnome.desktop.background",
                key,
                uri_image,
            ],
            check=True,
        )


def lancer_diaporama():
    if not os.path.exists(DOSSIER_IMAGES):
        print(f"Erreur : Le dossier '{DOSSIER_IMAGES}' n'existe pas.")
        return

    images = [
        os.path.join(DOSSIER_IMAGES, f)
        for f in os.listdir(DOSSIER_IMAGES)
        if f.lower().endswith(EXTENSIONS_VALIDES)
    ]

    if not images:
        print(f"Aucune image valide trouvée dans '{DOSSIER_IMAGES}'.")
        return

    try:
        image_choisie = random.choice(images)
        changer_fond_ecran(image_choisie)
    except KeyboardInterrupt:
        print("\nDiaporama arrêté.")


if __name__ == "__main__":
    lancer_diaporama()
