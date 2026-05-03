#!/bin/bash
# ===================================================================
# Script d'arret et nettoyage du projet
# ===================================================================

echo "===================================================="
echo "   Arret et nettoyage du projet Big Data"
echo "====================================================="
echo ""

case "${1:-stop}" in
    stop)
        echo "[STOP] Arret des conteneurs (sans supprimer les volumes)..."
        docker compose down
        echo "[OK] Conteneurs arretes"
        echo ""
        echo "[SAVE] Les donnees HDFS et les resultats sont conserves."
        echo "   Pour supprimer tout, executez : $0 clean"
        ;;
    clean)
        echo "[DELETE] Suppression complete (conteneurs + volumes)..."
        docker compose down -v
        echo "[OK] Tous les conteneurs et volumes supprimes"
        ;;
    restart)
        echo "[RELOAD] Redemarrage des conteneurs..."
        docker compose restart
        echo "[OK] Conteneurs redemarres"
        ;;
    *)
        echo "Usage: $0 {stop|clean|restart}"
        echo ""
        echo "  stop    - Arrete les conteneurs (volumes preserves)"
        echo "  clean   - Arrete ET supprime tout (complet)"
        echo "  restart - Redémarre les conteneurs"
        exit 1
        ;;
esac
echo ""
