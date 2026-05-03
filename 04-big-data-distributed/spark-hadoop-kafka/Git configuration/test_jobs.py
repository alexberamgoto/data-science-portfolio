#!/usr/bin/env python3

import subprocess
import sys
import time

def run_job(job_name, job_path):
    """Run a Spark job and return status"""
    print(f"\n{'='*60}")
    print(f"Executing: {job_name}")
    print(f"{'='*60}")
    
    cmd = [
        "docker", "exec", "spark-master",
        "spark-submit",
        "--master", "spark://spark-master:7077",
        "--deploy-mode", "client",
        "--executor-memory", "1g",
        "--executor-cores", "1",
        "--driver-memory", "1g",
        "--num-executors", "1",
        job_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        print(f"Exit Code: {result.returncode}")
        if result.returncode == 0:
            print(f"✓ {job_name} - SUCCESS")
            return True
        else:
            print(f"✗ {job_name} - FAILED")
            print("STDERR:", result.stderr[-500:] if result.stderr else "N/A")
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ {job_name} - TIMEOUT")
        return False
    except Exception as e:
        print(f"✗ {job_name} - ERROR: {str(e)}")
        return False

def verify_results():
    """Verify if results were generated"""
    print(f"\n{'='*60}")
    print("Verifying Results in HDFS")
    print(f"{'='*60}")
    
    paths = [
        "/results/batch/engagement_utilisateur",
        "/results/batch/preferences_by_age",
        "/results/batch/sentiment_analysis"
    ]
    
    for path in paths:
        cmd = ["docker", "exec", "namenode", "hdfs", "dfs", "-test", "-d", path]
        result = subprocess.run(cmd, capture_output=True)
        status = "✓ EXISTS" if result.returncode == 0 else "✗ NOT FOUND"
        print(f"{path}: {status}")

if __name__ == "__main__":
    print("BATCH JOB EXECUTION TEST")
    print("="*60)
    
    jobs = [
        ("Batch Job 1: Engagement", "/spark_jobs/batch_engagement.py"),
        ("Batch Job 2: Preferences", "/spark_jobs/batch_preferences_age.py"),
        ("Batch Job 3: Sentiment", "/spark_jobs/batch_sentiment.py"),
    ]
    
    results = []
    for job_name, job_path in jobs:
        success = run_job(job_name, job_path)
        results.append((job_name, success))
        time.sleep(2)  # Small delay between jobs
    
    verify_results()
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for job_name, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"{job_name}: {status}")
