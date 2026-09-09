# betise-piscine

Une petite application Python volontairement absurde : elle attend une touche,
puis lance une fenêtre Shrek qui se déplace à l'écran et réagit aux clics.

## Prérequis

- Python 3
- `make`
- Tkinter installé au niveau du système
- Une session graphique pour afficher la fenêtre

Sur Debian ou Ubuntu, Tkinter peut être installé avec :

```sh
sudo apt install python3-tk
```

## Lancer le projet

Depuis la racine du dépôt :

```sh
make run
```

La commande :

1. crée l'environnement virtuel `.env` si nécessaire ;
2. installe ou met à jour la dépendance Python ;
3. tente de synchroniser le dépôt avec `git pull` ;
4. lance malgré tout l'application en arrière-plan si le pull échoue.

Le terminal n'est pas utilisé par le programme : la commande rend la main
immédiatement après le lancement.

Le lancement direct reste possible avec :

```sh
python3 -m app.main
```

## Organisation

```text
app/
├── main.py                    # écoute le clavier et ouvre la roue
├── wheel.py                   # fenêtre Tkinter et gestion des clics
└── effects/
    ├── animation.py           # animation dans le terminal
    ├── background.py           # changement de fond d'écran
    └── display_rotation.py    # rotation de l'écran
```

Le projet sépare le point d'entrée, l'interface graphique et les effets système.
Le fichier `shrek.png` utilisé par la fenêtre doit rester accessible depuis la
racine du projet.

## Commandes utiles

```sh
make clean
```

Supprime l'environnement virtuel et les fichiers Python générés.

## Co-éditeurs

- `jtardieu`
- `enadeaud`
- `tclaereb`