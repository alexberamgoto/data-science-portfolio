@echo off
REM Script d'automatisation du push sur GitHub

echo.
echo ====================================================
echo   Push automatise vers GitHub
echo ====================================================
echo.

echo [1/4] Verification de Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git n'est pas installe
    echo Installez Git depuis https://git-scm.com/
    pause
    exit /b 1
)
echo [OK] Git detecte

echo.
set /p GITHUB_USER="[2/4] Entrez votre nom d'utilisateur GitHub : "

if "%GITHUB_USER%"=="" (
    echo [ERROR] Nom d'utilisateur non fourni
    pause
    exit /b 1
)

set /p REPO_NAME="[3/4] Entrez le nom du repository (par defaut: spark-bigdata-project) : "
if "%REPO_NAME%"=="" (
    set REPO_NAME=spark-bigdata-project
)

echo.
echo ====================================================
echo   Configuration
echo ====================================================
echo Utilisateur GitHub : %GITHUB_USER%
echo Nom du repository  : %REPO_NAME%
echo.
echo IMPORTANT:
echo  1. Creez un nouveau repository VIDE sur GitHub :
echo     https://github.com/new
echo  2. NE cochez pas "Add README", ".gitignore", ou "license"
echo  3. Cliquez "Create repository"
echo.
pause

echo.
echo [4/4] Configuration du remote et push...
echo.

REM Ajouter le remote
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git

if errorlevel 1 (
    echo [WARNING] Le remote existe deja ou erreur
    echo Tentative de modification du remote existant...
    git remote set-url origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
)

REM Renommer la branche en main (si necessaire)
for /f "usebackq tokens=*" %%A in (`git rev-parse --abbrev-ref HEAD`) do set CURRENT_BRANCH=%%A

if not "%CURRENT_BRANCH%"=="main" (
    echo Renommage de la branche %CURRENT_BRANCH% en main...
    git branch -M main
)

REM Push
echo.
echo Envoi du code vers GitHub...
echo (Cela peut prendre quelques secondes...)
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo [ERROR] Erreur lors du push
    echo Verifiez :
    echo  - La connexion internet
    echo  - Votre authentification GitHub (token ou SSH)
    echo  - L'URL du repository
    echo.
    echo Pour aide : lire GITHUB_PUSH.md
    pause
    exit /b 1
)

echo.
echo ====================================================
echo   Push termine avec succes !
echo ====================================================
echo.
echo Votre projet est maintenant sur GitHub :
echo https://github.com/%GITHUB_USER%/%REPO_NAME%
echo.
echo Pour cloner ailleurs :
echo   git clone https://github.com/%GITHUB_USER%/%REPO_NAME%.git
echo.

pause
