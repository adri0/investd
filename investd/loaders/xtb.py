import re
from typing import  Iterator

import pandas as pd
from openpyxl import load_workbook

from ..model import Transaction, Currency, AssetType 


def recognise_file(path: str) -> bool:
    if path.endswith(".xlsx"):
        workbook = load_workbook(path)
        for worksheet in workbook.worksheets:
            if worksheet.title == "CASH OPERATION HISTORY":
                return True
    return False


def load_from_file(path: str) -> Iterator[Transaction]:
    df = pd.read_excel(
        path, 
        sheet_name="CASH OPERATION HISTORY",        
        skiprows=10, 
        usecols=["ID", "Type", "Time", "Comment", "Symbol", "Amount"],
        parse_dates=["Time"]
    )
    df = df[~pd.isna(df["Symbol"])]
    return map(lambda i_row: _convert(i_row[1]), df.iterrows())


def parse_comment(comment: str) -> tuple[str, float, float]:
    for match in re.finditer(r"(?P<action>BUY|SELL) (?P<quantity>[\d\.]+) @ (?P<price>[\d\.]+)", comment):
        return match["action"], float(match["quantity"]), float(match["price"])
    raise ValueError(f"No matches found for comment pattern in Comment: {comment}")


currency_by_symbol = {
    "INR.FR": Currency.EUR,
    "BETASPXP.PL": Currency.PLN,
    "V80A.DE": Currency.EUR,
    "ETFBWTECH.PL": Currency.PLN,
    "CSPX.UK": Currency.USD,
    "VHYD.UK": Currency.USD
}


def _convert(record: pd.Series) -> Transaction:
    action, quantity, price = parse_comment(record["Comment"])
    return Transaction(
        id=record["ID"],
        timestamp=record["Time"],
        symbol=record["Symbol"],
        type=AssetType.ETF,
        platform="XTB",
        currency=currency_by_symbol[record["Symbol"]],
        amount=price * quantity,
        quantity=quantity,
        price=price,
        exchange_rate=abs(record["Amount"]) / price / quantity,
        amount_ref_currency=abs(record["Amount"]),
        action=action.lower()
    )
