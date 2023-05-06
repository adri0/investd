from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance
from pytest import MonkeyPatch, approx

from investd.quotes import (
    QUOTES_FILENAME,
    adjust_symbol,
    download_quotes_to_csv,
    load_quotes,
)
from investd.transaction import load_transactions

TEST_START_DATE = date(2022, 1, 1)
TEST_END_DATE = date(2023, 1, 1)  # exclusive
HOLIDAYS = [date(2022, 1, 1), date(2022, 4, 15), date(2022, 12, 26)]


def test_adjust_symbol() -> None:
    assert adjust_symbol("AAPL") == "AAPL"
    assert adjust_symbol("BETASPXP.PL") == "BETASPXP.WA"
    assert adjust_symbol("INR.FR") == "INR.PA"
    assert adjust_symbol("CSPX.UK") == "CSPX.L"


def test_download_quotes_csv(
    monkeypatch: MonkeyPatch, yfinance_quotes: pd.DataFrame, tmp_path: Path
) -> None:
    output_path = tmp_path / QUOTES_FILENAME
    assert not output_path.exists()

    yfinance_download_call_args = {}

    def mock_yfinance_download(*args, **kwargs):
        yfinance_download_call_args.update(kwargs)
        return yfinance_quotes

    monkeypatch.setattr(yfinance, "download", mock_yfinance_download)
    download_quotes_to_csv(
        output_path, start_date=TEST_START_DATE, end_date=TEST_END_DATE
    )

    df_quotes = pd.read_csv(output_path)
    assert df_quotes.shape == (_expected_rows(), 3)
    assert yfinance_download_call_args == {
        "tickers": "AAPL AMZN CDR.WA CSPX.L DAXEX.DE GOOGL TSLA V80A.DE",
        "start": TEST_START_DATE,
        "end": TEST_END_DATE,
        "group_by": "ticker",
        "interval": "1d",
    }


def test_load_quotes() -> None:
    df_quotes = load_quotes()
    assert df_quotes.shape == (_expected_rows(), 3)
    assert df_quotes[
        (df_quotes["date"] == date(2022, 12, 29)) & (df_quotes["symbol"] == "AMZN")
    ]["price"].iloc[0] == approx(84.18)


def _expected_rows() -> int:
    df_tx = load_transactions()
    symbol_count = df_tx["symbol"].unique().size
    business_days = np.busday_count(TEST_START_DATE, TEST_END_DATE, holidays=HOLIDAYS)
    return business_days * symbol_count
