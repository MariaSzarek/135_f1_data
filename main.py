import mysql.connector
import pandas as pd

password = input("Podaj haslo do db: ")
# Połączenie z MySQL
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password=password,
    database="f1db"
)

# Pobieramy dane z bazy
query = """
SELECT r.raceId, d.surname, res.position
FROM results res
JOIN drivers d ON res.driverId = d.driverId
JOIN races r ON res.raceId = r.raceId
WHERE d.surname IN ('Alonso', 'Stroll') AND r.year > 2023
"""
df = pd.read_sql(query, conn)

# Zamiana NULL (None) na 21
df["position"].fillna(21, inplace=True)

# Przekształcenie tabeli – każdy wyścig ma jedną linię
df_pivot = df.pivot(index="raceId", columns="surname", values="position").reset_index()

# Dodanie kolumny "alonso_better_than_ocon"
df_pivot["alonso_better_than_stroll"] = (df_pivot["Alonso"] < df_pivot["Stroll"]).astype(int)

# Ile razy Alonso był lepszy?
alonso_wins = df_pivot["alonso_better_than_stroll"].sum()

# Wyświetlenie wyników
print(df_pivot)
print(f"Alonso był lepszy od Ocona w {alonso_wins} wyścigach.")

# Zamknięcie połączenia
conn.close()