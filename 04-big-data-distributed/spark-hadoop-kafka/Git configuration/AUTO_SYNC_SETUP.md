# Configuration Auto-Sync GitHub - Guide d'Installation

## Étape 1: Ajouter votre clé SSH à GitHub ✓

Votre clé SSH a été générée. Suivez ces étapes pour l'ajouter à GitHub:

1. **Visitez**: https://github.com/settings/keys
2. **Cliquez**: "New SSH key"
3. **Titre**: "Alexis Laptop - Auto-Sync"
4. **Type**: "Authentication Key"
5. **Copiez la clé ci-dessous et collez-la dans GitHub**:

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDG28CAJQQIYTUQ3kwtDGfnOSZFxYNVKeD8B5dFXxGg
9W5RtDhs8Z/++Ymt3XEOExNiHqgqKw5jQi+ovVrbRyz46DMPUr8ciYc70SLc09l13LjjA6soOpy7n9d9fekZrBQNo7eqIM7wrcv7PYMJBPkqY7DNLsbx5fqFG6O+OwwY38v4eI42obdRMjK2wTEoGTtwhmygvFz/th6IaP3vxtcupCQH+GR6Zz9TerRHBRrT1GM1bX6HPuvr1OhthPpNezD+e2XjhmfjIrKhFOmvi/0p+POSti9YSiBF/FrWiQd69Me5ZjXA/iD2h3+ZRJL97YlYlKfaUD8Roh3jRu9HyVPb3xoTDXWnf53NUB0DdO1F0s+D85aTcPLecnARJqsTsKiS4pVYxZX6sWaXySoo9/xhZJ/6DrxzO2JjHGzUGpSPkG/fZxE64GZAgwoW2ZpF7/om5G9V7xkcgdvdb/T+aaXLNEwPYHIqF2xIuVnIw47COgXf+wF92gin4EemBjkgIMguqU72zXcUEt0nFBtTe1nQlIw7598iurIU75LYL0OBMZ8A9B+D4ihmER2j7JblGh3a6325mFrlPR5xQcNUfZ2br9LULzrGzfu8HyRlXzw81psQ/OcfO1sACJD9ZojM/C9UKipPqtHn6eepf8qeKxhgvQBJm4mifqPH1F5yygMRAQ== etudiant@HS-IDM-F-CFC-07
```

6. **Cliquez**: "Add SSH key"
7. **Autorisez** GitHub si vous y êtes invité

---

## Étape 2: Tester la connexion SSH

Ouvrez un terminal PowerShell et exécutez:

```powershell
ssh -T git@github.com
```

Vous devriez voir:
```
Hi alexberamgoto! You've successfully authenticated, but GitHub does not provide shell access.
```

Si vous voyez une erreur "Permission denied", vérifiez que votre clé a été ajoutée à GitHub.

---

## Étape 3: Démarrer la synchronisation automatique

### Option A: VS Code (Recommandé)

1. **Redémarrez VS Code**
2. **La tâche devrait démarrer automatiquement** (vérifiez le panneau "Terminal")
3. **Consultez les logs**: 
   - Ouvrez VS Code
   - Raccourci: `Ctrl+Shift+P`
   - Cherchez: "Tasks: Run Task"
   - Sélectionnez: "Voir logs Auto-Sync"

### Option B: PowerShell (Manuel)

Ouvrez PowerShell et exécutez:

```powershell
cd "c:\Users\Etudiant\Desktop\ressources Data Scientist\TD systeme distribuée\Djekounmian Alexis Projet SPARK"
.\auto_sync.ps1 -IntervalSeconds 120
```

---

## Configuration disponible

- **Fichier script**: `auto_sync.ps1`
- **Fichier tâches VS Code**: `.vscode/tasks.json`
- **Fichier config VS Code**: `.vscode/settings.json`
- **Logs**: `auto_sync.log` (créé automatiquement)
- **Erreurs**: `auto_sync_error.log` (créé automatiquement)

---

## Commandes VS Code

Ouvrez la palette de commandes (`Ctrl+Shift+P`) et cherchez:

| Commande | Résultat |
|----------|----------|
| `Tasks: Run Task` → `Auto-Sync GitHub (2 min)` | Démarre la synchronisation |
| `Tasks: Run Task` → `Arrêter Auto-Sync` | Arrête la synchronisation |
| `Tasks: Run Task` → `Voir logs Auto-Sync` | Affiche les 50 dernières lignes de logs |

---

## Comportement attendu

À chaque cycle (toutes les 2 minutes):

1. ✓ Vérification des changements
2. ✓ `git add -A` (ajouter tous les fichiers modifiés)
3. ✓ `git commit` (créer un commit timestampé)
4. ✓ `git push origin main` (envoyer vers GitHub)
5. ✓ Logs écrits dans `auto_sync.log`

**Exemple de log**:
```
[2026-03-23 14:30:15] --- Cycle #1 ---
[2026-03-23 14:30:15] Changements détectés - Synchronisation en cours...
[2026-03-23 14:30:17] Commit créé: Auto-sync: 2026-03-23 14:30:17
[2026-03-23 14:30:19] Push réussi vers GitHub ✓
```

---

## Dépannage

### Erreur: "Permission denied (publickey)"

**Solution**: Votre clé SSH n'est pas configurée. Recommencez l'étape 1 et vérifiez que la clé est bien ajoutée à GitHub.

### Erreur: "Could not read from remote repository"

**Solution**: Vérifiez que votre connexion Internet fonctionne et que votre clé SSH est valide.

### Le script ne démarre pas automatiquement

**Solution**: 
1. Redémarrez VS Code complètement
2. Ou exécutez manuellement: `Ctrl+Shift+P` → `Tasks: Run Task` → `Auto-Sync GitHub (2 min)`

### Je veux arrêter la synchronisation

**Solution**: 
- Dans VS Code: `Ctrl+Shift+P` → `Tasks: Run Task` → `Arrêter Auto-Sync`
- Ou fermez le terminal PowerShell (raccourci: `Ctrl+Maj+Accent grave`)

---

## Sécurité

- ✓ Votre clé SSH est stockée localement: `~/.ssh/id_rsa`
- ✓ Aucun mot de passe stocké
- ✓ Seule la clé publique est chez GitHub
- ✓ Les logs ne contiennent que les commandes, pas les données sensibles

---

## Prochaines étapes

1. ✓ Testez la connexion SSH: `ssh -T git@github.com`
2. ✓ Redémarrez VS Code
3. ✓ Regardez les logs pour confirmer le démarrage automatique
4. ✓ Modifiez un fichier pour tester

**Bon développement! 🚀**
