#!/usr/bin/env python3
import sys

def main():
    for line in sys.stdin:
        # Nettoyage de la ligne
        line = line.strip()
        if not line:
            continue

        # Ignorer une éventuelle ligne d'en-tête
        if line.startswith("utilisateur,produit,montant"):
            continue

        parts = line.split(",")
        if len(parts) != 3:
            # Ligne mal formée
            continue

        utilisateur, produit, montant_str = parts

        # On émet : clé = produit, valeur = montant (texte)
        # Séparateur tabulation obligatoire pour le reducer
        print(f"{produit}\t{montant_str}")

if __name__ == "__main__":
    main()
