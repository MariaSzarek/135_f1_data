from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+mysqlconnector://root:admin@localhost:3306/f1db')

query = """
SELECT r.raceId, d.surname, res.position
FROM results res
JOIN drivers d ON res.driverId = d.driverId
JOIN races r ON res.raceId = r.raceId
WHERE d.surname IN ('Alonso', 'Stroll') AND r.year > 2023
"""
df = pd.read_sql(query, engine)

# Zamiana NULL (None) na 21

df.fillna({"position":21}, inplace=True)
# Przekształcenie tabeli – każdy wyścig ma jedną linię
df_pivot = df.pivot(index="raceId", columns="surname", values="position").reset_index()

# Dodanie kolumny "alonso_better_than_ocon"
df_pivot["alonso_better_than_stroll"] = (df_pivot["Alonso"] < df_pivot["Stroll"]).astype(int)

# Ile razy Alonso był lepszy?
alonso_wins = df_pivot["alonso_better_than_stroll"].sum()

# Wyświetlenie wyników
df_pivot.to_csv('wyniki_alonso_vs_stroll.csv', index=False)
print(f"Alonso był lepszy od Ocona w {alonso_wins} wyścigach.")

