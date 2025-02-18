import pytest
import pandas as pd
from unittest.mock import patch
from main import pivot_data, na_to_21, read_data


mock_data = {
    'raceId': [1, 1, 2, 2, 3, 3],
    'surname': ['Alonso', 'Stroll', 'Alonso', 'Stroll', 'Alonso', 'Stroll'],
    'position': [5, 8, None, 10, 6, None]
}

mock_df = pd.DataFrame(mock_data)

@pytest.fixture
def mock_read_sql(mocker):
    mocker.patch('pandas.read_sql', return_value=mock_df)


def test_na_to_21(mock_read_sql):
    df = pd.read_sql('SELECT * FROM table', None)
    na_to_21(df)

    assert df['position'].iloc[2] == 21
    assert df['position'].iloc[5] == 21


def test_pivot_data(mock_read_sql):

    df = pd.read_sql('SELECT * FROM table', None)
    result = pivot_data(df)

    assert result == "Alonso był lepszy od Ocona w 2 wyścigach w 2021 roku"