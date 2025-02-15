import requests
import pandas as pd

# Funkcja pobierająca wyniki Alonso
def get_alonso_results():
    url = "http://ergast.com/api/f1/drivers/alonso/results.json?limit=1000"
    response = requests.get(url)
    data = response.json()

    results = []
    for race in data["MRData"]["RaceTable"]["Races"]:
        for result in race["Results"]:
            results.append({
                "season": race["season"],
                "round": race["round"],
                "race_name": race["raceName"],
                "circuit": race["Circuit"]["circuitName"],
                "date": race["date"],
                "constructor": result["Constructor"]["name"],
                "grid": int(result["grid"]),
                "position": int(result["position"]) if result["position"].isdigit() else None,
                "status": result["status"]
            })

    return pd.DataFrame(results)

# Pobieramy dane
df_alonso = get_alonso_results()

# Podgląd danych
print(df_alonso.head())
print(df_alonso.tail())

# Zapisujemy do CSV
df_alonso.to_csv("alonso_results.csv", index=False)