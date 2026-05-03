#!/usr/bin/env python3
import sys

def main():
    current_product = None
    current_sum = 0.0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            product, amount_str = line.split("\t", 1)
            amount = float(amount_str)
        except ValueError:
            # Ligne mal formée ou montant non numérique
            continue

        if current_product is None:
            # Première clé rencontrée
            current_product = product
            current_sum = amount
            continue

        if product == current_product:
            # Même produit : on cumule
            current_sum += amount
        else:
            # Changement de produit : on affiche le total précédent
            print(f"{current_product}\t{current_sum}")
            current_product = product
            current_sum = amount

    # Dernier produit
    if current_product is not None:
        print(f"{current_product}\t{current_sum}")

if __name__ == "__main__":
    main()
