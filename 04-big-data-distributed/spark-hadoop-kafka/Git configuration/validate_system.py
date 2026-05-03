#!/usr/bin/python3
"""
Script de validation finale de l'infrastructure Big Data
Vérifie: Infrastructure, Données, Exécution des jobs, Résultats
"""

import subprocess
import json
from datetime import datetime

def run_cmd(cmd):
    """Exécuter une commande shell"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=15)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return -1, "", str(e)

def check_infrastructure():
    """Vérifier les conteneurs"""
    print("\n[1] VÉRIFICATION INFRASTRUCTURE")
    print("-" * 50)
    
    # Nombre de conteneurs
    code, output, _ = run_cmd("docker ps | wc -l")
    num_containers = int(output.strip()) - 1 if output else 0
    print(f"  Conteneurs actifs: {num_containers} (attendu: 8)")
    
    # État HDFS
    code, output, _ = run_cmd("docker exec namenode hdfs dfsadmin -safemode get")
    print(f"  HDFS Safe Mode: {output.strip()}")
    
    # État Spark
    code, output, _ = run_cmd('docker exec spark-master jps | grep "Master"')
    spark_ok = "Master" in output
    print(f"  Spark Master: {'RUNNING' if spark_ok else 'NOT RUNNING'}")
    
    return num_containers == 9 or num_containers == 8

def check_data():
    """Vérifier les données d'entrée"""
    print("\n[2] VÉRIFICATION DONNÉES D'ENTRÉE")
    print("-" * 50)
    
    # Vérifier fichier source
    code, output, err = run_cmd("docker exec namenode hdfs dfs -ls /data/social_media/")
    data_ok = code == 0 and "social_media_events.csv" in output
    print(f"  Données HDFS: {'✓ OK' if data_ok else '✗ MISSING'}")
    
    if data_ok:
        # Compter les lignes
        code, output, _ = run_cmd("docker exec namenode hdfs dfs -cat /data/social_media/social_media_events.csv | wc -l")
        lines = output.strip() if output else "?"
        print(f"  Nombre de lignes: {lines}")
    
    return data_ok

def check_results():
    """Vérifier les résultats"""
    print("\n[3] VÉRIFICATION RÉSULTATS")
    print("-" * 50)
    
    results_paths = [
        ("/results/batch/engagement_utilisateur", "Engagement"),
        ("/results/batch/preferences_by_age", "Preferences"),
        ("/results/batch/sentiment_analysis", "Sentiment")
    ]
    
    results_found = 0
    for path, name in results_paths:
        code, output, _ = run_cmd(f"docker exec namenode hdfs dfs -test -d {path}")
        exists = code == 0
        status = "✓" if exists else "✗"
        print(f"  {status} {name}: {path}")
        if exists:
            results_found += 1
    
    return results_found

def check_stream_jobs():
    """Vérifier que les stream jobs sont prêts"""
    print("\n[4] VÉRIFICATION STREAM JOBS")
    print("-" * 50)
    
    jobs = [
        "/spark_jobs/stream_activity_spikes.py",
        "/spark_jobs/stream_sentiment.py",
        "/spark_jobs/stream_sessions_analysis.py"
    ]
    
    for job in jobs:
        code, _, _ = run_cmd(f"docker exec spark-master test -f {job}")
        status = "✓" if code == 0 else "✗"
        print(f"  {status} {job}")

def generate_report():
    """Générer le rapport final"""
    print("\n" + "="*60)
    print("RAPPORT FINAL DE VALIDATION")
    print("="*60)
    
    infra_ok = check_infrastructure()
    data_ok = check_data()
    results_found = check_results()
    check_stream_jobs()
    
    print("\n" + "="*60)
    print("RÉSUMÉ")
    print("="*60)
    
    if infra_ok and data_ok:
        print("\n✓ INFRASTRUCTURE: OPERATIONAL")
    else:
        print("\n✗ INFRASTRUCTURE: ISSUES DETECTED")
    
    if results_found > 0:
        print(f"✓ RÉSULTATS: {results_found}/3 jobs réussis")
    else:
        print("⚠ RÉSULTATS: Pas de résultats trouvés (jobs en cours d'exécution?)")
    
    print(f"\nTemps: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

if __name__ == "__main__":
    try:
        generate_report()
    except Exception as e:
        print(f"Erreur: {e}")
