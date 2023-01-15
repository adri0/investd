from datetime import date
from pathlib import Path

import pandas as pd
import yfinance
from pytest import MonkeyPatch, approx

from investd.quotes import (
    QUOTES_FILENAME,
    adjust_symbol,
    download_quotes_to_csv,
    load_quotes,
)


def test_adjust_symbol() -> None:
    assert adjust_symbol("AAPL") == "AAPL"
    assert adjust_symbol("BETASPXP.PL") == "BETASPXP.WA"
    assert adjust_symbol("INR.FR") == "INR.PA"
    assert adjust_symbol("CSPX.UK") == "CSPX.L"


def test_download_quotes_csv(
    monkeypatch: MonkeyPatch, df_quotes: pd.DataFrame, tmp_path: Path
) -> None:
    output_path = tmp_path / QUOTES_FILENAME
    assert not output_path.exists()

    yfinance_download_call_args = {}

    def mock_yfinance_download(*args, **kwargs):
        yfinance_download_call_args.update(kwargs)
        return df_quotes

    monkeypatch.setattr(yfinance, "download", mock_yfinance_download)
    download_quotes_to_csv(output_path, end_date=date(2022, 12, 30))

    df_quotes = pd.read_csv(output_path)
    assert df_quotes.shape == (259, 50)
    assert yfinance_download_call_args == {
        "tickers": "AAPL TSLA CDR.WA AMZN GOOGL DAXEX.DE V80A.DE CSPX.L",
        "start": date(2022, 1, 2),
        "end": date(2022, 12, 30),
        "group_by": "ticker",
    }


def test_load_quotes() -> None:
    df_quotes = load_quotes()
    assert df_quotes.shape == (257, 48)
    assert df_quotes.loc[date(2022, 12, 29), ("AMZN", "Close")][0] == approx(84.18)
