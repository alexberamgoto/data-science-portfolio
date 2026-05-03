import time
def download_data(server_name, delay):
    print(f"⬇️ Début du téléchargement sur {server_name}...")
    time.sleep(delay)
    print(f"✅ {server_name} terminé !")
def main():
    start = time.perf_counter()
    download_data("Serveur A", 2)
    download_data("Serveur B", 3)
    download_data("Serveur C", 1)
    end = time.perf_counter()
    print(f"Temps total : {end - start:.2f} s")
if __name__ == "__main__":
   main()