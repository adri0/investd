from datetime import datetime
from typing import Iterator

import pandas as pd

from investd.model import AssetType, Currency, Transaction

ref_currency = Currency.PLN


def recognise_file(path: str) -> bool:
    if path.endswith(".csv"):
        with open(path, "r") as f:
            line = f.readline()
            if line.startswith("Type,Completed Date,Sell Currency"):
                return True
    return False


def load_from_file(path: str) -> Iterator[Transaction]:
    df = pd.read_csv(path, parse_dates=["Completed Date"])
    df = df[df["Sell Currency"] == str(ref_currency)]
    return map(lambda i_row: _convert(i_row[1]), df.iterrows())


def _hash_record(record: pd.Series) -> str:
    elements = [
        record["Sell Currency"], 
        record["Buy Currency"],
        record["Buy Amount"],
        record["Completed Date"].date(),
        record["Completed Date"].hour,
        record["Completed Date"].minute,
        record["Completed Date"].second
    ]
    element_string = "#".join([str(el) for el in elements])
    hash_value = hash(element_string)
    return "{:X}".format(hash_value)[-9:]


def _convert(record: pd.Series) -> Transaction:
    return Transaction(
        id=_hash_record(record),
        timestamp=record["Completed Date"],
        symbol=record["Buy Currency"],
        type=AssetType.Crypto,
        platform="Revolut",
        currency=ref_currency,
        amount=abs(record["Sell Amount"]),
        quantity=record["Buy Amount"],
        price=abs(record["Sell Amount"]) / record["Buy Amount"],
        exchange_rate=abs(record["Sell Amount"]) / record["Buy Amount"],
        amount_ref_currency=abs(record["Sell Amount"]),
        action="buy"
    )


def reconciliate_exchange(*paths: str) -> None:
    """ Given a list of account statement CSVs, filters and conciliates
        internal exchanges and generate a currencies file.
    """
    df = pd.concat([pd.read_csv(path, parse_dates=["Completed Date"]) for path in paths])
    df = df[(df["Type"] == "EXCHANGE") & (df["State"] == "COMPLETED")]
    if df.shape[0] == 0:
        print("Provided files don't have completed exchanges to reconciliate.")
        return
    reconciled_columns = [
        "Type", "Completed Date", 
        "Sell Currency", "Sell Amount", "Sell Fee",
        "Buy Currency", "Buy Amount", "Buy Fee"
    ]
    df_recon = pd.DataFrame([], columns=reconciled_columns)
    for completed_date, group in df.groupby("Completed Date"):
        if len(group) < 2:
            continue
        if len(group) > 2:
            raise ValueError(
                "Reconciliation error: I don't know how to deal with more "
                f"than 2 records for the same 'Completed Date' ({completed_date})"
            )
        asset_sold = group[group["Amount"] < 0].iloc[0]
        asset_bought = group[group["Amount"] > 0].iloc[0]
        if asset_bought["Currency"] == asset_sold["Currency"]:
            raise ValueError(
                "Reconciliation error: Sold and bought "
                "assets should be of different currencies."
            )
        df_recon = df_recon.append({
            "Type": "EXCHANGE",
            "Completed Date": completed_date,
            "Sell Currency": asset_sold["Currency"],
            "Sell Amount": asset_sold["Amount"],
            "Sell Fee": asset_sold["Fee"],
            "Buy Currency": asset_bought["Currency"],
            "Buy Amount": asset_bought["Amount"],
            "Buy Fee": asset_bought["Fee"]
        }, ignore_index=True)
    if df_recon.shape[0] == 0:
        print("No records generated from reconciliation.")
    else:
        now = datetime.utcnow().isoformat(sep="-", timespec="seconds").replace(':', '')
        filename = f"reconciliation_result_{now}.csv"
        df_recon.to_csv(filename, index=False)
        print(f"{filename} generated!")
