from typing import Iterator

import pandas as pd

from ..model import Transaction, AssetType, Currency


def recognise_file(path: str) -> bool:
    if path.endswith(".csv"):
        with open(path, "r") as f:
            line = f.readline()
            if line.startswith("Date,Ticker"):
                return True
    return False


def load_from_file(path: str) -> Iterator[Transaction]:
    df = pd.read_csv(path, parse_dates=["Date"], dayfirst=True)
    df = df[~pd.isna(df["Ticker"]) & (df["Type"]=="buy")]
    return map(lambda i_row: _convert(i_row[1]), df.iterrows())


def _hash_record(record: pd.Series) -> str:
    elements = [
        record["Ticker"], 
        record["Date"].date(),
        record["Date"].hour,
        record["Date"].minute,
        record["Quantity"]
    ]
    element_string = "#".join([str(el) for el in elements])
    hash_value = hash(element_string)
    return "{:X}".format(hash_value)[-9:]


def _convert(record: pd.Series) -> Transaction:
    return Transaction(
        id=_hash_record(record),
        timestamp=record["Date"],
        symbol=record["Ticker"],
        type=AssetType.Stock,
        platform="Revolut",
        currency=Currency[record["Currency"]],
        amount=record["Total Amount"],
        quantity=record["Quantity"],
        price=record["Price per share"],
        exchange_rate=1 / record["FX Rate"],
        amount_ref_currency=record["Total Amount"] / record["FX Rate"],
        action=record["Type"].lower()
    )

