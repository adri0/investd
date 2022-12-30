from datetime import date
from pathlib import Path

import pandas as pd
import yfinance
from pytest import approx

from investd.config import PERSIST_PATH
from investd.quotes import adjust_symbol, generate_quotes_csv, load_quotes


def test_adjust_symbol():
    assert adjust_symbol("AAPL") == "AAPL"
    assert adjust_symbol("BETASPXP.PL") == "BETASPXP.WA"
    assert adjust_symbol("INR.FR") == "INR.PA"
    assert adjust_symbol("CSPX.UK") == "CSPX.L"


def test_generate_quotes_csv(monkeypatch, df_quotes: pd.DataFrame):
    assert not Path(PERSIST_PATH / "quotes.csv").exists()

    def mock_download(*args, **kwargs):
        return df_quotes

    monkeypatch.setattr(yfinance, "download", mock_download)
    generate_quotes_csv(end_date=date(2022, 12, 30))

    df_quotes = pd.read_csv(PERSIST_PATH / "quotes.csv")
    assert df_quotes.shape == (259, 50)


def test_load_quotes():
    df_quotes = load_quotes()
    assert df_quotes.shape == (257, 48)
    assert df_quotes.loc[date(2022, 12, 29), ("AMZN", "Close")][0] == approx(84.18)
