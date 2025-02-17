from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('mysql+mysqlconnector://root:admin@localhost:3306/f1db')
year = 2021

query = f"""
SELECT r.raceId, d.surname, res.position
FROM results res
JOIN drivers d ON res.driverId = d.driverId
JOIN races r ON res.raceId = r.raceId
WHERE d.surname IN ('Alonso', 'Stroll') AND r.year = {year}
"""

def read_data(query, engine):
    return pd.read_sql(query, engine)

def na_to_21(df):
    df = pd.read_sql(query, engine)
    return df.fillna({"position":21}, inplace=True)


def pivot_data(df):

    df_pivot = df.pivot(index="raceId", columns="surname", values="position").reset_index()
    df_pivot["alonso_better_than_stroll"] = (df_pivot["Alonso"] < df_pivot["Stroll"])
    alonso_wins = df_pivot["alonso_better_than_stroll"].sum()
    df_pivot.to_csv('wyniki_alonso_vs_stroll.csv', index=True)
    return f"Alonso był lepszy od Ocona w {alonso_wins} wyścigach w {year} roku"

df = read_data(query, engine)
na_to_21(df)
print(pivot_data(df))

