# Python OOP — Application MVC

Application Python organisée selon le pattern **Modèle-Vue-Contrôleur**, à partir d'une étude de cas notes/logs.

## Architecture MVC

```
┌──────────┐      ┌──────────────┐      ┌──────────┐
│  vue.py  │ ←──→ │ controleur.py│ ←──→ │ modele.py│
└──────────┘      └──────────────┘      └──────────┘
                       │
                  application.py (point d'entrée)
```

| Module | Responsabilité |
|--------|----------------|
| `modele.py` | Données, logique métier, accès CSV |
| `vue.py`    | Interface (Tkinter) |
| `controleur.py` | Orchestration entre modèle et vue |
| `application.py` | Bootstrap |

## Sous-dossiers
- `APPLICATION/` — version applicative finale
- `ENTRAINEMENT/` — exercices d'entraînement progressifs

## Lancer
```bash
python application.py
```

## Stack
Python 3.11 · Tkinter · pandas (programmation orientée objet)
