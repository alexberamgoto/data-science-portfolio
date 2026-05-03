import sys

def main():
    current_key = None
    current_sum = 0

    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue
        try:
            key, val = line.split("\t", 1)
            val = int(val)
        except ValueError:
            # Ligne mal formée : on l’ignore
            continue

        if current_key is None:
            # Première clé rencontrée
            current_key = key
            current_sum = val
            continue

        if key == current_key:
            # Même clé : on cumule
            current_sum += val
        else:
            # Nouvelle clé : on affiche le total précédent
            print(f"{current_key}\t{current_sum}")
            current_key = key
            current_sum = val

    # Dernière clé à afficher
    if current_key is not None:
        print(f"{current_key}\t{current_sum}")

if __name__ == "__main__":
    main()
