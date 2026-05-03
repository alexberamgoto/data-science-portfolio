import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1) Chargement du dataset
# =========================

# Modification  du chemin vers le fichier
FILE_PATH = "2019-Oct.csv"

df = pd.read_csv(FILE_PATH)

print("=== Aperçu dataset ===")
print(df.head())
print("\n=== Shape ===")
print(df.shape)

# =========================
# 2) Nettoyage MINIMAL autorisé (sans modifier les valeurs)
#    => on ne supprime rien, on prépare juste des colonnes de lecture
# =========================

# Conversion date (sans toucher aux données brutes)
if "event_time" in df.columns:
    df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")
    df["event_date"] = df["event_time"].dt.date
    df["event_hour"] = df["event_time"].dt.hour
    df["event_dayofweek"] = df["event_time"].dt.day_name()

# =========================
# 3) Compréhension structurelle
# =========================

print("\n=== Types de colonnes ===")
print(df.dtypes)

print("\n=== Valeurs manquantes (top 15) ===")
missing = df.isna().mean().sort_values(ascending=False) * 100
print(missing.head(15))

print("\n=== Colonnes ===")
print(df.columns.tolist())

# =========================
# 4) Analyse univariée
# =========================

# Répartition event_type
if "event_type" in df.columns:
    print("\n=== Répartition des event_type ===")
    event_counts = df["event_type"].value_counts()
    event_percent = df["event_type"].value_counts(normalize=True) * 100
    print(pd.DataFrame({"count": event_counts, "%": event_percent.round(2)}))

    # Plot
    event_counts.plot(kind="bar")
    plt.title("Répartition des types d'événements")
    plt.xlabel("event_type")
    plt.ylabel("Nombre d'événements")
    plt.tight_layout()
    plt.show()

# Analyse prix
if "price" in df.columns:
    print("\n=== Statistiques prix ===")
    price_desc = df["price"].describe()
    print(price_desc)

    # Distribution prix (log utile)
    df["price"].dropna().plot(kind="hist", bins=50)
    plt.title("Distribution des prix")
    plt.xlabel("price")
    plt.ylabel("count")
    plt.tight_layout()
    plt.show()

# =========================
# 5) Analyse multivariée
# =========================

# Events par heure
if "event_hour" in df.columns:
    events_by_hour = df.groupby("event_hour").size()
    print("\n=== Événements par heure ===")
    print(events_by_hour)

    events_by_hour.plot(kind="line")
    plt.title("Nombre d'événements par heure")
    plt.xlabel("Heure")
    plt.ylabel("Nombre d'événements")
    plt.tight_layout()
    plt.show()

# Events par jour
if "event_date" in df.columns:
    events_by_day = df.groupby("event_date").size()
    print("\n=== Événements par jour ===")
    print(events_by_day.head())

    events_by_day.plot(kind="line")
    plt.title("Nombre d'événements par jour")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'événements")
    plt.tight_layout()
    plt.show()

# =========================
# 6) Tunnel d'achat (conversion)
# =========================

# On travaille au niveau session si dispo
if "user_session" in df.columns and "event_type" in df.columns:
    sessions = df.groupby("user_session")["event_type"].apply(list)

    total_sessions = sessions.shape[0]
    sessions_with_view = sessions.apply(lambda x: "view" in x).sum()
    sessions_with_cart = sessions.apply(lambda x: "cart" in x).sum()
    sessions_with_purchase = sessions.apply(lambda x: "purchase" in x).sum()

    print("\n=== Tunnel par session ===")
    print(f"Sessions totales : {total_sessions}")
    print(f"Sessions avec view : {sessions_with_view} ({sessions_with_view/total_sessions*100:.2f}%)")
    print(f"Sessions avec cart : {sessions_with_cart} ({sessions_with_cart/total_sessions*100:.2f}%)")
    print(f"Sessions avec purchase : {sessions_with_purchase} ({sessions_with_purchase/total_sessions*100:.2f}%)")

    # Conversion simple
    conversion = sessions_with_purchase / total_sessions * 100
    print(f"\n>>> Conversion globale (purchase/session) : {conversion:.3f}%")

# =========================
# 7) Top produits et concentration
# =========================

if "product_id" in df.columns and "event_type" in df.columns:
    # Top produits vus
    top_view = df[df["event_type"] == "view"]["product_id"].value_counts().head(10)
    print("\n=== Top 10 produits les plus vus ===")
    print(top_view)

    top_view.plot(kind="bar")
    plt.title("Top 10 produits les plus vus")
    plt.xlabel("product_id")
    plt.ylabel("Nombre de views")
    plt.tight_layout()
    plt.show()

    # Top produits achetés
    top_purchase = df[df["event_type"] == "purchase"]["product_id"].value_counts().head(10)
    print("\n=== Top 10 produits les plus achetés ===")
    print(top_purchase)

    top_purchase.plot(kind="bar")
    plt.title("Top 10 produits les plus achetés")
    plt.xlabel("product_id")
    plt.ylabel("Nombre de purchases")
    plt.tight_layout()
    plt.show()

# Concentration des achats
if "product_id" in df.columns and "event_type" in df.columns:
    purchases = df[df["event_type"] == "purchase"]["product_id"].value_counts()
    if len(purchases) > 0:
        total_purchases = purchases.sum()
        top_10_share = purchases.head(10).sum() / total_purchases * 100
        top_1_share = purchases.head(1).sum() / total_purchases * 100

        print("\n=== Concentration des achats ===")
        print(f"Part des 1 produit top : {top_1_share:.2f}%")
        print(f"Part des 10 produits top : {top_10_share:.2f}%")

# =========================
# 8) 5 CONSTATS MESURÉS (automatiques)
# =========================

constats = []

# Constat 1
if "event_type" in df.columns:
    event_percent = df["event_type"].value_counts(normalize=True) * 100
    constats.append(
        f"Répartition des événements : " +
        ", ".join([f"{k}={v:.2f}%" for k, v in event_percent.items()])
    )

# Constat 2 : conversion session
if "user_session" in df.columns and "event_type" in df.columns:
    conversion = sessions_with_purchase / total_sessions * 100
    constats.append(f"Taux de conversion global (purchase/session) = {conversion:.4f}%")

# Constat 3 : prix
if "price" in df.columns:
    constats.append(
        f"Prix : moyenne={df['price'].mean():.2f}, médiane={df['price'].median():.2f}, max={df['price'].max():.2f}"
    )

# Constat 4 : concentration achats
if "product_id" in df.columns and "event_type" in df.columns and len(purchases) > 0:
    constats.append(f"Les 10 produits les plus achetés représentent {top_10_share:.2f}% des achats.")

# Constat 5 : activité temporelle
if "event_hour" in df.columns:
    peak_hour = df["event_hour"].value_counts().idxmax()
    constats.append(f"Le pic d’activité (tous événements) se situe vers {peak_hour}h.")

print("\n============================")
print("✅ 5 CONSTATS MESURÉS")
print("============================")
for i, c in enumerate(constats[:5], 1):
    print(f"{i}. {c}")

# =========================
# 9) 3 HYPOTHÈSES MÉTIERS (proposées)
# =========================

hypotheses = [
    "Le taux de conversion faible peut indiquer une friction au checkout ou des prix jugés élevés.",
    "Certains produits très consultés mais peu achetés pourraient souffrir d’un problème d’attractivité (prix, description, concurrence).",
    "Les pics d’activité horaires/journaliers pourraient correspondre à des campagnes marketing ou à des habitudes de consommation (soir/week-end)."
]

print("\n============================")
print("💡 3 HYPOTHÈSES MÉTIERS")
print("============================")
for i, h in enumerate(hypotheses, 1):
    print(f"{i}. {h}")

# =========================
# 10) 3 RISQUES IDENTIFIÉS
# =========================

risques = []

# Risque 1 : valeurs manquantes
if missing.iloc[0] > 0:
    risques.append(f"Présence de valeurs manquantes (ex : {missing.index[0]} = {missing.iloc[0]:.2f}%).")

# Risque 2 : tracking incohérent
if "user_session" in df.columns and "event_type" in df.columns:
    sessions_with_purchase_no_view = sessions.apply(lambda x: ("purchase" in x) and ("view" not in x)).sum()
    if sessions_with_purchase_no_view > 0:
        risques.append(f"{sessions_with_purchase_no_view} sessions ont un achat sans view (possible tracking incomplet).")

# Risque 3 : dépendance aux top produits
if "product_id" in df.columns and "event_type" in df.columns and len(purchases) > 0:
    risques.append(f"Forte dépendance aux produits top : top 10 = {top_10_share:.2f}% des achats.")

# compléter si moins de 3
while len(risques) < 3:
    risques.append("Risque potentiel : biais de représentativité (dataset limité à un mois, octobre 2019).")

print("\n============================")
print("⚠️ 3 RISQUES IDENTIFIÉS")
print("============================")
for i, r in enumerate(risques[:3], 1):
    print(f"{i}. {r}")
