from pathlib import Path
from typing import Generator

import pandas as pd
import pytest

from investd.common import Action, AssetType, Currency
from investd.config import INVESTD_PERSIST, INVESTD_REPORTS, INVESTD_SOURCES
from investd.quotes import QUOTES_FILENAME


@pytest.fixture
def path_resources() -> Path:
    return Path(__file__).parent / "resources"


@pytest.fixture
def setup_reports() -> Generator[None, None, None]:
    INVESTD_REPORTS.mkdir(exist_ok=True)
    yield
    for path in INVESTD_REPORTS.glob("*.html"):
        path.unlink()


@pytest.fixture
def path_revolut_csv() -> Path:
    return INVESTD_SOURCES / "revolut_stocks/revolut-stocks-statement.csv"


@pytest.fixture
def path_xtb_xlsx() -> Path:
    return INVESTD_SOURCES / "xtb/xtb-statement.xlsx"


@pytest.fixture
def path_xtb_csv() -> Path:
    return INVESTD_SOURCES / "xtb/xtb-statement.csv"


@pytest.fixture
def path_bonds_xls() -> Path:
    return INVESTD_SOURCES / "bonds/bonds-statement.xls"


@pytest.fixture
def path_bossa_csv() -> Path:
    return INVESTD_SOURCES / "bossa/bossa-statement.csv"


@pytest.fixture
def df_tx_minimal() -> pd.DataFrame:
    df_tx = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "timestamp": ["2021-12-01", "2022-01-01", "2022-01-30", "2022-02-01"],
            "symbol": ["LOL", "TLDR", "XOXO", "LOL"],
            "type": [AssetType.Stock, AssetType.Stock, AssetType.ETF, AssetType.Stock],
            "platform": ["revolut_stocks", "revolut_stocks", "xtb", "revolut_stocks"],
            "currency": [Currency.USD, Currency.USD, Currency.EUR, Currency.USD],
            "amount": [100.0, 150.0, 300.0, 60.0],
            "quantity": [2, 6, 2, 1],
            "price": [50, 25, 150, 60],
            "exchange_rate": [4.5, 4.5, 5.0, 4.6],
            "amount_ref_currency": [450, 675, 1500, 276],
            "action": [Action.BUY, Action.BUY, Action.BUY, Action.SELL],
        }
    )
    categories = ("type", "platform", "currency", "action")
    for cat in categories:
        df_tx[cat] = df_tx[cat].astype("category")
    df_tx["timestamp"] = df_tx["timestamp"].astype("datetime64[ns]")
    return df_tx


@pytest.fixture
def df_quotes_minimal() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.to_datetime(["2022-01-30"] * 5),
            "symbol": ["LOL", "TLDR", "XOXO", "USDPLN=X", "EURPLN=X"],
            "price": [55, 20, 160, 4.6, 5.0],
        }
    )


@pytest.fixture
def df_quotes() -> pd.DataFrame:
    return pd.read_csv(INVESTD_PERSIST / QUOTES_FILENAME)


@pytest.fixture
def yfinance_quotes() -> pd.DataFrame:
    df_quotes = pd.read_csv(
        INVESTD_PERSIST / "yfinance_quotes.csv", header=[0, 1], index_col=0
    )
    df_quotes.index = df_quotes.index.map(lambda dt: pd.to_datetime(dt).date())
    return df_quotes
