import pytest
import pandas as pd
from sqlalchemy import create_engine

@pytest.fixture
def mock_read_sql(mocker):
    # Przygotowanie danych testowych
    mock_data = {
        'raceId': [1, 2, 3],
        'surname': ['Alonso', 'Stroll', 'Alonso'],
        'position': [5, 8, None]
    }
    df_mock = pd.DataFrame(mock_data)
    return mocker.patch('pandas.read_sql', return_value=df_mock)

def test_query_results(mock_read_sql):
    # Test - uruchomienie zapytania
    engine = create_engine('mysql+mysqlconnector://root:admin@localhost:3306/f1db')
    query = """
    SELECT r.raceId, d.surname, res.position
    FROM results res
    JOIN drivers d ON res.driverId = d.driverId
    JOIN races r ON res.raceId = r.raceId
    WHERE d.surname IN ('Alonso', 'Stroll') AND r.year = 2024
    """
    df = pd.read_sql(query, engine)

    # Sprawdzamy, czy dane są poprawnie załadowane
    assert df.shape[0] == 3
    assert df['surname'].iloc[0] == 'Alonso'
    assert pd.isna(df['position'].iloc[2])


def test_fill_na():
    # Test wypełniania wartości NaN
    df = pd.DataFrame({
        'raceId': [1, 2],
        'Alonso': [5, None],
        'Stroll': [8, 10]
    })
    df.fillna({"Alonso": 21}, inplace=True)

    # Sprawdzamy, czy NaN zostały zastąpione
    assert df['Alonso'].iloc[1] == 21


def test_pivot_table():
    # Test tworzenia tabeli przekształconej (pivot)
    df = pd.DataFrame({
        'raceId': [1, 2],
        'surname': ['Alonso', 'Stroll'],
        'position': [5, 8]
    })
    df_pivot = df.pivot(index="raceId", columns="surname", values="position").reset_index()

    # Sprawdzamy, czy pivot działa poprawnie
    assert df_pivot.shape[1] == 3  # Powinna być 3 kolumny (raceId, Alonso, Stroll)
    assert df_pivot['Alonso'].iloc[0] == 5


def test_calculation_better_than_stroll():
    # Test obliczania, kto był lepszy
    df_pivot = pd.DataFrame({
        'raceId': [1, 2],
        'Alonso': [5, 8],
        'Stroll': [6, 10]
    })
    df_pivot["alonso_better_than_stroll"] = (df_pivot["Alonso"] < df_pivot["Stroll"])

    # Sprawdzamy, czy obliczenie działa poprawnie
    assert df_pivot["alonso_better_than_stroll"].sum() == 2


def test_alonso_wins():
    # Test sumowania zwycięstw Alonso
    df_pivot = pd.DataFrame({
        'raceId': [1, 2, 3],
        'Alonso': [5, 11, 7],
        'Stroll': [6, 10, 8]
    })
    df_pivot["alonso_better_than_stroll"] = (df_pivot["Alonso"] < df_pivot["Stroll"]).astype(int)

    alonso_wins = df_pivot["alonso_better_than_stroll"].sum()

    # Sprawdzamy, ile razy Alonso był lepszy
    assert alonso_wins == 2