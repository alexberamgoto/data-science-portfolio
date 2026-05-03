# E-Commerce Events — Data Engineering Pipeline

Pipeline d'ingestion et d'analyse exploratoire d'un dataset volumineux (~5 Go) d'événements e-commerce (vues, ajouts panier, achats) sur un mois.

## Objectif
- Ingestion d'un large CSV avec contraintes mémoire
- EDA : distribution des `event_type`, prix, top catégories/marques
- Analyse temporelle (heure, jour de la semaine)

## Scripts
| Fichier | Rôle |
|---------|------|
| `00_DOWNLOAD_DATA.py` | Script d'amorçage du dataset (Kaggle) |
| `e-commerce.py` | Chargement, nettoyage léger, analyses uni- et multivariées |

## Dataset
**eCommerce events history in cosmetics shop** (Kaggle) — 2019-Oct.csv, ~42 M lignes.
Le CSV n'est **pas inclus dans le repo** (trop lourd). À télécharger via :
```bash
python "00_DOWNLOAD_DATA (1).py"
```

## Stack
Python 3.11 · pandas · numpy · matplotlib
