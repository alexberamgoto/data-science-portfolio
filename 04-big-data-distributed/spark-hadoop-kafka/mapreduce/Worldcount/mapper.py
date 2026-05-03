#!/usr/bin/env python3
import sys

def main():
    for line in sys.stdin:
        line = line.rstrip("\n")  # lire une ligne
        for word in line.split():  # Découpage de la ligne par espaces / blancs
            emit(word, 1)          # Émet (mot, 1)

def emit(key, value):  # Émet des paires (clé, valeur)
    print(f"{key}\t{value}")

if __name__ == "__main__":
    main()
