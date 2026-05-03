# Pizza Metz — Collection Bruno (tests d'API REST)

Collection de tests API REST écrits avec [**Bruno**](https://www.usebruno.com/) — alternative open-source à Postman, fichiers `.bru` versionnables en git.

## Couverture
14 requêtes documentant l'API Pizza Metz :
- Listing & filtrage (catégorie tradition, base crème, top 5, tri par prix)
- Recherche par nom (`Diavola`)
- Sélection partielle d'attributs (`id, name, price`)
- Statistiques (prix moyen)
- Affichage d'image
- Authentification (création utilisateur, login)

## Lancer
```bash
# Ouvrir le dossier dans Bruno
bru run --env <env-name>
```

> Démontre la maîtrise du **test d'API REST**, du contrôle qualité et de la documentation par l'exemple.
