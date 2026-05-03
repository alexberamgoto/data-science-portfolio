@echo off
REM Script de diagnostic et resolution des problemes GitHub

setlocal enabledelayedexpansion

color 0A
cls

echo.
echo ====================================================
echo   DIAGNOSTIC ET FIX - GitHub Push
echo ====================================================
echo.

REM Etape 1 : Verifier Git
echo [1/6] Verification de Git...
git --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Git n'est pas installe
    echo Installez depuis https://git-scm.com/
    pause
    exit /b 1
)
echo [OK] Git present

REM Etape 2 : Verifier le repo Git local
echo [2/6] Verification du repository local...
git status >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Pas de repository Git local
    echo Reinitialiser Git : git init
    pause
    exit /b 1
)
echo [OK] Repository Git present

REM Etape 3 : Verifier la branche
echo [3/6] Verification de la branche...
for /f "usebackq tokens=*" %%A in (`git rev-parse --abbrev-ref HEAD`) do set BRANCH=%%A
echo Branche actuelle : !BRANCH!

if not "!BRANCH!"=="main" (
    echo Renommage de !BRANCH! en main...
    git branch -M main
    if errorlevel 1 (
        color 0C
        echo [ERROR] Impossible de renommer la branche
        pause
        exit /b 1
    )
    echo [OK] Branche renommee en main
) else (
    echo [OK] Branche est main
)

echo.

REM Etape 4 : Menu des solutions
echo ====================================================
echo   CHOISISSEZ VOTRE METHODE D'AUTHENTIFICATION
echo ====================================================
echo.
echo [1] Token d'acces personnel (recommande, facile)
echo [2] SSH (plus securise, un peu plus long)
echo [3] Verifier / corriger URL existante
echo [4] Annuler
echo.
set /p CHOICE="Entrez votre choix (1-4) : "

if "%CHOICE%"=="1" goto TOKEN_METHOD
if "%CHOICE%"=="2" goto SSH_METHOD
if "%CHOICE%"=="3" goto URL_FIX
if "%CHOICE%"=="4" goto END
echo [ERROR] Choix invalide
goto RETRY_CHOICE

:TOKEN_METHOD
cls
color 0E
echo.
echo ====================================================
echo   METHODE 1 : Token d'acces personnel
echo ====================================================
echo.
echo Etapes :
echo 1. Allez sur : https://github.com/settings/tokens
echo    (ou Settings ^> Developer settings ^> Personal access tokens)
echo.
echo 2. Cliquez "Generate new token (classic)"
echo.
echo 3. Nommez-le "spark-project"
echo.
echo 4. Cochez uniquement "repo" (toutes les sous-cases)
echo.
echo 5. Cliquez "Generate token"
echo.
echo 6. COPIEZ LE TOKEN (vous ne le verrez qu'une fois!)
echo.
echo 7. Revenez ici et collez le token
echo.
pause

set /p TOKEN="Collez votre token ici : "

if "%TOKEN%"=="" (
    color 0C
    echo [ERROR] Token vide
    pause
    goto TOKEN_METHOD
)

set /p USERNAME="Entrez votre username GitHub : "
set /p REPO="Entrez le nom du repository (ou vide pour spark-bigdata-project) : "

if "%REPO%"=="" (
    set REPO=spark-bigdata-project
)

echo.
echo [4/6] Configuration du remote avec token...

REM Supprimer ancien remote
git remote remove origin >nul 2>&1

REM Ajouter nouveau remote avec token
git remote add origin https://%TOKEN%@github.com/%USERNAME%/%REPO%.git

echo [OK] Remote configure

echo.
echo [5/6] Test de connexion...

REM Test de connexion
git ls-remote origin HEAD >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Impossible de se connecter
    echo Verifiez :
    echo  - Votre token est valide
    echo  - Votre username est correct
    echo  - Le repository existe
    echo.
    pause
    goto TOKEN_METHOD
)
echo [OK] Connexion testee avec succes

goto PUSH_CODE

:SSH_METHOD
cls
color 0E
echo.
echo ====================================================
echo   METHODE 2 : SSH (plus securise)
echo ====================================================
echo.

echo [4/6] Verification de la clé SSH...

if not exist "%USERPROFILE%\.ssh\id_ed25519" (
    echo Aucune clé SSH trouvee. Generation en cours...
    
    set /p EMAIL="Entrez votre email GitHub : "
    
    ssh-keygen -t ed25519 -C "!EMAIL!" -f "%USERPROFILE%\.ssh\id_ed25519" -N ""
    
    if errorlevel 1 (
        color 0C
        echo [ERROR] Impossible de generer la clé SSH
        pause
        exit /b 1
    )
    
    echo [OK] Clé SSH generee
    echo.
    echo Clé publique (a copier sur GitHub) :
    echo.
    type "%USERPROFILE%\.ssh\id_ed25519.pub"
    echo.
    echo Etapes :
    echo 1. Allez sur https://github.com/settings/ssh/new
    echo 2. Nommez-la "Windows Laptop"
    echo 3. Collez la cle ci-dessus
    echo 4. Cliquez "Add SSH key"
    echo.
    pause
) else (
    echo [OK] Clé SSH existante trouvee
)

echo Test de connexion SSH...
ssh -T git@github.com >nul 2>&1
if errorlevel 1 (
    color 0C
    echo [ERROR] Connexion SSH echouee
    echo Assurez-vous que la clé SSH est bien ajoutee sur GitHub
    pause
    goto SSH_METHOD
)

echo [OK] Connexion SSH reussie

set /p USERNAME="Entrez votre username GitHub : "
set /p REPO="Entrez le nom du repository (ou vide pour spark-bigdata-project) : "

if "%REPO%"=="" (
    set REPO=spark-bigdata-project
)

echo.
echo [5/6] Configuration du remote SSH...

git remote remove origin >nul 2>&1
git remote add origin git@github.com:%USERNAME%/%REPO%.git

echo [OK] Remote SSH configure

goto PUSH_CODE

:URL_FIX
cls
echo.
echo [4/6] Verification du remote existant...
echo.
git remote -v

echo.
set /p FIX="Voulez-vous corriger l'URL ? (o/n) : "

if /i "%FIX%"=="o" (
    set /p NEW_URL="Entrez la nouvelle URL : "
    git remote set-url origin !NEW_URL!
    echo [OK] URL mise a jour
) else (
    echo [SKIP] URL inchangee
)

goto PUSH_CODE

:PUSH_CODE
cls
color 0A
echo.
echo ====================================================
echo   PUSH DU CODE
echo ====================================================
echo.

echo [6/6] Envoi du code vers GitHub...
echo (Cela peut prendre quelques secondes)
echo.

git push -u origin main

if errorlevel 1 (
    color 0C
    echo.
    echo [ERROR] Erreur lors du push
    echo.
    echo Causes possibles :
    echo  - Token/SSH invalide
    echo  - Repository n'existe pas sur GitHub
    echo  - Pas d'acces au repository
    echo.
    echo Consultez TROUBLESHOOT_GITHUB.md pour plus d'aide
    echo.
    pause
    exit /b 1
)

color 0B
cls
echo.
echo ====================================================
echo   SUCCES !
echo ====================================================
echo.

set /p USERNAME="Entrez votre username (pour verifier) : "
set /p REPO="Entrez le repo (ou vide pour spark-bigdata-project) : "

if "%REPO%"=="" (
    set REPO=spark-bigdata-project
)

echo.
echo Votre projet est maintenant sur GitHub :
echo.
echo    https://github.com/%USERNAME%/%REPO%
echo.
echo Clonage ulterieur :
echo    git clone https://github.com/%USERNAME%/%REPO%.git
echo.
echo Pour les autres clonages (SSH) :
echo    git clone git@github.com:%USERNAME%/%REPO%.git
echo.

pause
exit /b 0

:RETRY_CHOICE
pause
goto RETRY_CHOICE

:END
echo Annule par l'utilisateur
exit /b 0
