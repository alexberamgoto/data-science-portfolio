# Étape 1 : Image de base
FROM ubuntu:20.04

# Étape 2 : Installer Nginx
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Étape 3 : Définir une variable d'environnement
ENV APP_HOME=/var/www/html

# Étape 4 : Copier la page index.html dans le répertoire web
COPY index.html $APP_HOME/index.html

# Étape 5 : Définir un volume pour les fichiers web
VOLUME ["/usr/share/nginx/html"]

# Étape 6 : Exposer le port HTTP
EXPOSE 80

# Étape 7 : Définir l'ENTRYPOINT (ici le serveur nginx)
ENTRYPOINT ["nginx"]

# Étape 8 : Définir la commande par défaut
CMD ["-g", "daemon off;"]
