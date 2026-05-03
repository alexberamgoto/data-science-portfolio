#!/bin/bash
# Script d'automatisation du push sur GitHub pour Linux/Mac

echo ""
echo "===================================================="
echo "   Push automatise vers GitHub"
echo "===================================================="
echo ""

echo "[1/4] Verification de Git..."
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git n'est pas installe"
    echo "Installez Git avec : brew install git (Mac) ou apt install git (Linux)"
    exit 1
fi
git --version
echo "[OK] Git detecte"

echo ""
read -p "[2/4] Entrez votre nom d'utilisateur GitHub : " GITHUB_USER

if [ -z "$GITHUB_USER" ]; then
    echo "[ERROR] Nom d'utilisateur non fourni"
    exit 1
fi

read -p "[3/4] Entrez le nom du repository (par defaut: spark-bigdata-project) : " REPO_NAME
REPO_NAME=${REPO_NAME:-spark-bigdata-project}

echo ""
echo "===================================================="
echo "   Configuration"
echo "===================================================="
echo "Utilisateur GitHub : $GITHUB_USER"
echo "Nom du repository  : $REPO_NAME"
echo ""
echo "IMPORTANT:"
echo "  1. Creez un nouveau repository VIDE sur GitHub :"
echo "     https://github.com/new"
echo "  2. NE cochez pas \"Add README\", \".gitignore\", ou \"license\""
echo "  3. Cliquez \"Create repository\""
echo ""
read -p "Appuyez sur ENTER quand c'est fait..."

echo ""
echo "[4/4] Configuration du remote et push..."
echo ""

# Ajouter le remote
git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git 2>/dev/null

if [ $? -ne 0 ]; then
    echo "[WARNING] Le remote existe deja, modification..."
    git remote set-url origin https://github.com/$GITHUB_USER/$REPO_NAME.git
fi

# Renommer la branche en main
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Renommage de la branche $CURRENT_BRANCH en main..."
    git branch -M main
fi

# Push
echo ""
echo "Envoi du code vers GitHub..."
echo "(Cela peut prendre quelques secondes...)"
echo ""

git push -u origin main

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Erreur lors du push"
    echo "Verifiez :"
    echo "  - La connexion internet"
    echo "  - Votre authentification GitHub (token ou SSH)"
    echo "  - L'URL du repository"
    echo ""
    echo "Pour aide : lire GITHUB_PUSH.md"
    exit 1
fi

echo ""
echo "===================================================="
echo "   Push termine avec succes !"
echo "===================================================="
echo ""
echo "Votre projet est maintenant sur GitHub :"
echo "https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "Pour cloner ailleurs :"
echo "   git clone https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo ""
