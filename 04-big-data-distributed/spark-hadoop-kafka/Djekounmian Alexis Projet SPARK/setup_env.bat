@echo off
REM Script d'installation de l'environnement pour Windows
echo.
echo ====================================================
echo   Installation de l'environnement Python
echo ====================================================
echo.

REM Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python n'est pas installe ou n'est pas dans PATH
    echo Installez Python 3.9+ depuis python.org
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Creer l'environnement virtuel
echo [1/4] Creation de l'environnement virtuel...
if exist .venv (
    echo [WARNING] .venv existe deja, on le supprime...
    rmdir /s /q .venv
)

python -m venv .venv
if errorlevel 1 (
    echo [ERROR] Impossible de creer l'environnement virtuel
    pause
    exit /b 1
)
echo [OK] Environnement virtuel cree

echo.
echo [2/4] Activation de l'environnement virtuel...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Impossible d'activer l'environnement
    pause
    exit /b 1
)
echo [OK] Environnement virtuel active

echo.
echo [3/4] Mise a jour de pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Probleme lors de la mise a jour de pip (non critique)
)
echo [OK] pip a jour

echo.
echo [4/4] Installation des dependances...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Impossible d'installer les dependances
    echo Verifiez requirements.txt
    pause
    exit /b 1
)
echo [OK] Dependances installes

echo.
echo ====================================================
echo   Installation terminate avec succes !
echo ====================================================
echo.
echo Pour activer l'environnement a l'avenir :
echo   .venv\Scripts\activate
echo.
echo Pour verifier l'installation :
echo   python -c "import pyspark; print(pyspark.__version__)"
echo.
pause
