import time
def faire_cafe():
      print("☕ Lancement du café (3s)...")
      time.sleep(3) # Le processeur est BLOQUÉ ici, il dort
      print("✅ Café prêt !")
      return "Café"
def griller_pain():
    print("🍞 Lancement du toast (2s)...")
    time.sleep(2) # Le processeur est BLOQUÉ ici
    print("✅ Toast prêt !")
    return "Toast"
def main():
    start = time.perf_counter()
# Exécution séquentielle
    resultat_1 = faire_cafe()
    resultat_2 = griller_pain()
    end = time.perf_counter()
    print(f"\n🏁 Petit déj servi en {end - start:.2f} secondes.")

if __name__ == "__main__":
    main()