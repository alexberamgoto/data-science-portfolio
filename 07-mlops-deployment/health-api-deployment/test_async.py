import asyncio
import time
# async def : Définit une fonction qui PEUT être mise en pause
async def faire_cafe():
        print("☕ Lancement du café (3s)...")
# await asyncio.sleep : "Je rends la main au système pendant 3s,
# fais autre chose en attendant"
        await asyncio.sleep(3)
        print("✅ Café prêt !")
        return "Café"
async def griller_pain():
        print("🍞 Lancement du toast (2s)...")
        await asyncio.sleep(2)
        print("✅ Toast prêt !")
async def main():
    start = time.perf_counter()
    print("🚀 Démarrage du service...")
        # asyncio.gather : Lance les deux tâches EN MÊME TEMPS et attend
        # qu'elles finissent toutes les deux
    await asyncio.gather(faire_cafe(), griller_pain())
    end = time.perf_counter()
    print(f"\n🏁 Petit déj servi en {end - start:.2f} secondes.")
if __name__ == "__main__":
# On lance la boucle d'événements (Event Loop)
      asyncio.run(main())
