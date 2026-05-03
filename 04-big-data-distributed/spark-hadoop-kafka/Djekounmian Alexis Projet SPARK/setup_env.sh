#!/bin/bash
# Script d'installation de l'environnement pour Linux/Mac

echo ""
echo "===================================================="
echo "   Installation de l'environnement Python"
echo "===================================================="
echo ""

# Verifier Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 n'est pas installe"
    echo "Installez Python 3.9+ depuis python.org"
    exit 1
fi

python3 --version
echo "[OK] Python detecte"
echo ""

# Creer l'environnement virtuel
echo "[1/4] Creation de l'environnement virtuel..."
if [ -d ".venv" ]; then
    echo "[WARNING] .venv existe deja, on le supprime..."
    rm -rf .venv
fi

python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "[ERROR] Impossible de creer l'environnement virtuel"
    exit 1
fi
echo "[OK] Environnement virtuel cree"

echo ""
echo "[2/4] Activation de l'environnement virtuel..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Impossible d'activer l'environnement"
    exit 1
fi
echo "[OK] Environnement virtuel active"

echo ""
echo "[3/4] Mise a jour de pip..."
python -m pip install --upgrade pip setuptools wheel > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "[WARNING] Probleme lors de la mise a jour de pip (non critique)"
fi
echo "[OK] pip a jour"

echo ""
echo "[4/4] Installation des dependances..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Impossible d'installer les dependances"
    echo "Verifiez requirements.txt"
    exit 1
fi
echo "[OK] Dependances installes"

echo ""
echo "===================================================="
echo "   Installation terminer avec succes !"
echo "===================================================="
echo ""
echo "Pour activer l'environnement a l'avenir :"
echo "   source .venv/bin/activate"
echo ""
echo "Pour verifier l'installation :"
echo "   python -c \"import pyspark; print(pyspark.__version__)\""
echo ""
