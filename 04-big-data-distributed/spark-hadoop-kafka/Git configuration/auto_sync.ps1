# =============================================================================
# Script d'Auto-Synchronisation Git vers GitHub
# Surveille les changements et pousse automatiquement toutes les 2 minutes
# =============================================================================

param(
    [int]$IntervalSeconds = 120  # 2 minutes par défaut
)

# Configuration
$ProjectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogFile = Join-Path $ProjectPath "auto_sync.log"
$ErrorLogFile = Join-Path $ProjectPath "auto_sync_error.log"

function Write-Log {
    param([string]$Message)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogMessage = "[$TimeStamp] $Message"
    Write-Host $LogMessage
    Add-Content -Path $LogFile -Value $LogMessage -Encoding UTF8
}

function Write-ErrorLog {
    param([string]$Message)
    $TimeStamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $ErrorMessage = "[$TimeStamp] ERROR: $Message"
    Write-Host $ErrorMessage -ForegroundColor Red
    Add-Content -Path $ErrorLogFile -Value $ErrorMessage -Encoding UTF8
}

function Test-GitChanges {
    Set-Location $ProjectPath
    $status = git status --porcelain
    return $null -ne $status -and $status.Length -gt 0
}

function Sync-ToGitHub {
    Set-Location $ProjectPath
    
    try {
        # Vérifier s'il y a des changements
        if (-not (Test-GitChanges)) {
            Write-Log "Aucun changement détecté"
            return $true
        }

        Write-Log "Changements détectés - Synchronisation en cours..."
        
        # Stage tous les changements
        git add -A
        if ($LASTEXITCODE -ne 0) {
            Write-ErrorLog "Erreur lors de 'git add -A'"
            return $false
        }

        # Récupérer les changements actuels
        $changes = git diff --cached --name-only
        if ($changes) {
            Write-Log "Fichiers modifiés: $(($changes | Measure-Object).Count)"
        }

        # Créer un commit avec timestamp
        $CommitMessage = "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        git commit -m $CommitMessage
        if ($LASTEXITCODE -ne 0) {
            if ($LASTEXITCODE -eq 1) {
                Write-Log "Rien à commiter (index vide)"
                return $true
            }
            Write-ErrorLog "Erreur lors du commit"
            return $false
        }

        Write-Log "Commit créé: $CommitMessage"

        # Pusher vers GitHub
        git push origin main
        if ($LASTEXITCODE -ne 0) {
            Write-ErrorLog "Erreur lors du push vers GitHub"
            return $false
        }

        Write-Log "Push réussi vers GitHub ✓"
        return $true

    }
    catch {
        Write-ErrorLog "Exception: $_"
        return $false
    }
}

# ===================================================================
# Boucle principale
# ===================================================================

Write-Log "========================================"
Write-Log "Démarrage du service d'auto-synchronisation"
Write-Log "Projet: $ProjectPath"
Write-Log "Intervalle: ${IntervalSeconds}s (toutes les 2 minutes)"
Write-Log "========================================"

$syncCount = 0
$failureCount = 0

while ($true) {
    $syncCount++
    Write-Log "--- Cycle #$syncCount ---"
    
    if (Sync-ToGitHub) {
        $failureCount = 0
    }
    else {
        $failureCount++
        Write-ErrorLog "Échec du cycle #$syncCount (Échecs cumulés: $failureCount)"
        
        if ($failureCount -ge 5) {
            Write-ErrorLog "Trop d'échecs consécutifs ($failureCount). Vérifiez la configuration SSH."
            Write-ErrorLog "Assurez-vous que votre clé SSH a été ajoutée à https://github.com/settings/keys"
            exit 1
        }
    }

    Write-Log "Prochaine vérification dans ${IntervalSeconds}s (à $(Get-Date -Date (Get-Date).AddSeconds($IntervalSeconds) -Format 'HH:mm:ss'))"
    Start-Sleep -Seconds $IntervalSeconds
}
