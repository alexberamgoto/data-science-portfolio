"""
═══════════════════════════════════════════════════════════════
KAFKA PRODUCER : Simulateur de stream en temps réel
═══════════════════════════════════════════════════════════════
Ce script lit le fichier CSV ligne par ligne et envoie chaque
événement dans un topic Kafka, simulant ainsi un flux temps réel.

Il envoie les données au format JSON dans le topic "social_media_events".
Un délai configurable entre chaque batch simule le rythme réel.
═══════════════════════════════════════════════════════════════
"""

import csv
import json
import time
import sys
from kafka import KafkaProducer

# ─── Configuration ───
KAFKA_BROKER = "kafka:9092"
TOPIC = "social_media_events"
CSV_PATH = "/data/social_media_events.csv"
BATCH_SIZE = 100          # Nombre de messages par batch
DELAY_BETWEEN_BATCHES = 1 # Secondes entre chaque batch

def create_producer():
    """Crée un producteur Kafka avec retry."""
    for attempt in range(10):
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )
            print(f"✅ Connecté à Kafka ({KAFKA_BROKER})")
            return producer
        except Exception as e:
            print(f"⏳ Tentative {attempt+1}/10 - Kafka pas encore prêt : {e}")
            time.sleep(5)
    print("❌ Impossible de se connecter à Kafka")
    sys.exit(1)

def main():
    print("=" * 60)
    print("  KAFKA PRODUCER : Simulation de stream")
    print("=" * 60)

    producer = create_producer()
    total_sent = 0

    with open(CSV_PATH, 'r') as f:
        reader = csv.DictReader(f)
        batch = []

        for row in reader:
            # Convertir les types
            event = {
                "user_id": int(row["user_id"]),
                "timestamp": row["timestamp"],
                "platform": row["platform"],
                "action": row["action"],
                "session_id": int(row["session_id"]),
                "device": row["device"],
                "country": row["country"],
                "age_group": row["age_group"],
                "lifestyle": row["lifestyle"],
                "topic": row["topic"],
                "duration_sec": int(row["duration_sec"]),
                "sentiment": int(row["sentiment"])
            }

            # Envoyer dans Kafka (clé = user_id pour partitionnement)
            producer.send(
                TOPIC,
                key=str(event["user_id"]),
                value=event
            )

            total_sent += 1
            batch.append(event)

            # Log et pause par batch
            if total_sent % BATCH_SIZE == 0:
                producer.flush()
                print(f"📤 {total_sent} événements envoyés... "
                      f"(dernier: {event['timestamp']} - {event['platform']} - {event['action']})")
                time.sleep(DELAY_BETWEEN_BATCHES)

    producer.flush()
    producer.close()
    print(f"\n✅ Terminé ! {total_sent} événements envoyés au total.")

if __name__ == "__main__":
    main()
