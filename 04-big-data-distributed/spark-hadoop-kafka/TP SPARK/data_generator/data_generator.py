import socket #socket pour la communication réseau.
import time #time pour insérer des pauses entre les envois.
import random #

def generate_data():
    host = '0.0.0.0' # ecoute sur 0.0.0.0
    port = 9998 # le port 9998 pour accepter les connexions entrantes
    
    # Liste de phrases aléatoires
    phrases = [
        "Le chat dort sur le canapé \n",
        "Il fait beau aujourd'hui \n",
        "La programmation est amusante \n",
        "Spark Streaming est puissant \n",
        "Les données sont partout \n",
        "Python est un langage génial \n",
        "Le machine learning change le monde \n",
        "Les réseaux de neurones sont fascinants \n",
        "La science des données est l'avenir \n",
        "Les algorithmes sont partout \n"
    ]

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Création d’un socket TCP.
    server_socket.bind((host, port)) # Association à l’adresse et au port définis.
    server_socket.listen(1) # Mise en écoute des connexions entrantes.

    print(f"Listening for connections on {host}:{port}...") 

    conn, addr = server_socket.accept() # Attente d’une connexion
    print(f"Connection from {addr}") # Affichage de l’adresse du client.

    try:
        while True:  # Boucle infinie pour maintenir le conteneur en vie
            # Sélectionner une phrase aléatoire
            random_phrase = random.choice(phrases)
            # Envoyer la phrase au client
            conn.send(random_phrase.encode('utf-8'))
            print(f"Sent: {random_phrase}")
            time.sleep(5)  # Attendre 1 seconde avant d'envoyer la prochaine phrase
    except KeyboardInterrupt: #Capture des erreurs et fermeture propre de la connexion en cas d’interruption.
        print("Stopping data generator.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    generate_data()
