# betise-piscine

## Organisation

```text
app/
├── main.py                    # écoute le clavier et ouvre la roue
├── wheel.py                   # interface Tkinter et dispatch des événements
└── effects/
	├── animation.py           # animation dans le terminal
	├── background.py           # changement de fond d'écran
	└── display_rotation.py    # rotation de l'écran
```

`RoueApp` porte l'état et le comportement de l'interface graphique. Les effets
système restent séparés de l'interface. `DisplayRotator` regroupe la logique
de rotation et choisit le backend adapté à la session graphique.

## Lancer

```sh
make run
```

Ou directement depuis la racine du projet :

```sh
python3 -m app.main
```