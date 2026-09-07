#!/usr/bin/env python3
"""
Roue de la fortune - tkinter
-----------------------------
Appuie sur ESPACE (ou clique sur le bouton "Tourner") pour faire tourner
la roue. Elle ralentit progressivement et s'arrête sur un événement
choisi aléatoirement.

Pour personnaliser : modifie la liste EVENEMENTS ci-dessous.
Tu peux donner un "poids" (probabilité) différent à chaque événement
via la liste POIDS (même longueur que EVENEMENTS). Laisse POIDS = None
pour une probabilité égale entre tous les événements.
"""

import math
import random
import tkinter as tk
from tkinter import messagebox

# ---------------------------------------------------------------------
# CONFIGURATION - modifie ces listes selon tes besoins
# ---------------------------------------------------------------------
EVENEMENTS = [
    "do a barel roll",
    "log ton screen",
    "une beau fond d'ecrant",
    "F14",
    "parot invation",
    "rick roll",
    "kiss",
    "how train dragon",
    "shrek surprise"
]

# Mets des nombres ici pour pondérer (ex: [3, 1, 1, 2, 1, 1, 1, 0.5])
# ou laisse None pour un tirage équiprobable.
POIDS = None

COULEURS = [
    "#e74c3c",
    "#3498db",
    "#2ecc71",
    "#f1c40f",
    "#9b59b6",
    "#1abc9c",
    "#e67e22",
    "#34495e",
]

LARGEUR, HAUTEUR = 1500, 1560
CENTRE_X, CENTRE_Y = LARGEUR // 2, 750
RAYON = 700


class RoueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roue des événements")
        self.root.resizable(False, False)

        self.angle = 0.0  # angle actuel de la roue (degrés)
        self.vitesse = 0.0  # vitesse de rotation (degrés / frame)
        self.en_rotation = False
        self.angle_cible = None  # angle final calculé au démarrage du spin

        n = len(EVENEMENTS)
        self.poids = POIDS if POIDS else [1] * n
        if len(self.poids) != n:
            raise ValueError("POIDS doit avoir la même longueur que EVENEMENTS")

        # --- Interface ---
        self.canvas = tk.Canvas(
            root, width=LARGEUR, height=HAUTEUR, bg="#f5f5f5", highlightthickness=0
        )
        self.canvas.pack()

        self.label_resultat = tk.Label(
            root,
            text="Appuie sur ESPACE pour tourner",
            font=("Helvetica", 12, "bold"),
            pady=10,
        )
        self.label_resultat.pack()

        self.bouton = tk.Button(
            root,
            text="Tourner la roue",
            font=("Helvetica", 12),
            command=self.lancer_rotation,
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            relief="flat",
            padx=10,
            pady=5,
        )
        self.bouton.pack(pady=(0, 15))

        self.dessiner_roue()

        # Raccourci clavier : barre espace pour lancer la roue
        self.root.bind("<space>", lambda e: self.lancer_rotation())
        self.root.focus_set()

    # -------------------------------------------------------------
    def dessiner_roue(self):
        self.canvas.delete("roue")
        n = len(EVENEMENTS)
        angle_par_secteur = 360 / n

        for i in range(n):
            debut = self.angle + i * angle_par_secteur
            self.canvas.create_arc(
                CENTRE_X - RAYON,
                CENTRE_Y - RAYON,
                CENTRE_X + RAYON,
                CENTRE_Y + RAYON,
                start=debut,
                extent=angle_par_secteur,
                fill=COULEURS[i % len(COULEURS)],
                outline="white",
                width=2,
                tags="roue",
            )
            # Texte au milieu du secteur
            angle_texte_deg = debut + angle_par_secteur / 2
            angle_texte_rad = math.radians(angle_texte_deg)
            rx = CENTRE_X + (RAYON * 0.65) * math.cos(angle_texte_rad)
            ry = CENTRE_Y - (RAYON * 0.65) * math.sin(angle_texte_rad)
            self.canvas.create_text(
                rx,
                ry,
                text=EVENEMENTS[i],
                fill="white",
                font=("Helvetica", 10, "bold"),
                tags="roue",
                angle=(
                    -angle_texte_deg + 90 if False else 0
                ),  # texte horizontal, plus lisible
            )

        # Moyeu central
        self.canvas.create_oval(
            CENTRE_X - 15,
            CENTRE_Y - 15,
            CENTRE_X + 15,
            CENTRE_Y + 15,
            fill="#2c3e50",
            outline="white",
            width=2,
            tags="roue",
        )

        # Flèche/pointeur fixe en haut
        self.canvas.create_polygon(
            CENTRE_X - 15,
            CENTRE_Y - RAYON - 5,
            CENTRE_X + 15,
            CENTRE_Y - RAYON - 5,
            CENTRE_X,
            CENTRE_Y - RAYON + 20,
            fill="#c0392b",
            outline="black",
            tags="roue",
        )

    # -------------------------------------------------------------
    def lancer_rotation(self):
        if self.en_rotation:
            return  # ignore si une rotation est déjà en cours

        self.en_rotation = True
        self.bouton.config(state="disabled")
        self.label_resultat.config(text="La roue tourne...")

        # 1. Choisir le gagnant à l'avance (selon les poids)
        n = len(EVENEMENTS)
        index_gagnant = random.choices(range(n), weights=self.poids, k=1)[0]
        angle_par_secteur = 360 / n

        # 2. Calculer l'angle final pour que ce secteur s'arrête sous la flèche (en haut, 90°)
        # Le secteur i est dessiné de (angle + i*sect) à (angle + (i+1)*sect)
        # On veut que le milieu du secteur gagnant tombe à 90° (position de la flèche)
        milieu_secteur = index_gagnant * angle_par_secteur + angle_par_secteur / 2
        tours_supplementaires = (
            random.randint(4, 7) * 360
        )  # plusieurs tours pour l'effet
        # angle final tel que (angle_final + milieu_secteur) % 360 == 90
        angle_final = (90 - milieu_secteur) % 360 + tours_supplementaires

        self.angle_cible = angle_final
        self.index_gagnant = index_gagnant
        self._animer()

    # -------------------------------------------------------------
    def _animer(self):
        distance_restante = self.angle_cible - self.angle

        if distance_restante <= 0:
            self.angle = self.angle_cible % 360
            self.dessiner_roue()
            self._fin_rotation()
            return

        # Vitesse proportionnelle à la distance restante (effet de ralentissement)
        pas = max(2, distance_restante * 0.04)
        self.angle += pas
        self.dessiner_roue()

        self.root.after(16, self._animer)  # ~60 fps

    # -------------------------------------------------------------
    def _fin_rotation(self):
        self.en_rotation = False
        self.bouton.config(state="normal")
        resultat = EVENEMENTS[self.index_gagnant]
        self.label_resultat.config(text=f"Résultat : {resultat}")
        messagebox.showinfo("Résultat", f"La roue s'est arrêtée sur :\n\n{resultat}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RoueApp(root)
    root.mainloop()
