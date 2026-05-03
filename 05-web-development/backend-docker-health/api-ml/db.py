# Optionnel: exemple d'insert dans DB ML (non utilisé par défaut)
import os
import psycopg2

def get_conn():
    try:
        return psycopg2.connect(
            host=os.getenv('ML_DB_HOST','db-ml'),
            port=int(os.getenv('ML_DB_PORT','5432')),
            dbname=os.getenv('ML_DB_NAME','mldb'),
            user=os.getenv('ML_DB_USER','ml'),
            password=os.getenv('ML_DB_PASSWORD','mlpwd'),
        )
    except Exception:
        return None

def save_prediction(payload, result):
    conn = get_conn()
    if not conn:
        return
    cur = conn.cursor()
    cur.execute(
        CREATE TABLE IF NOT EXISTS ml_predictions (
          id SERIAL PRIMARY KEY,
          created_at TIMESTAMP DEFAULT NOW(),
          payload JSONB,
          result JSONB
        );
    )
    cur.execute('INSERT INTO ml_predictions(payload,result) VALUES (%s,%s)', [json.dumps(payload), json.dumps(result)])
    conn.commit()
    cur.close()
    conn.close()
