import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable

from ..common import Action, AssetType, Currency
from ..transaction import Transaction
from .base import SourceBase

COL_AMOUNT = "wartość"
COL_CURRENCY = "waluta"
COL_DATE = "data"
COL_PAPER = "papier"
COL_PRICE = "cena"
COL_QUANTITY = "ilość"


class Bossa(SourceBase):
    source_name = "bossa"

    def parse_source_file(self, path: Path) -> Iterable[Transaction]:
        with path.open("r", encoding="windows-1250") as csvfile:
            csv_reader = csv.DictReader(csvfile, delimiter=";")
            for row in csv_reader:
                amount = float(row[COL_AMOUNT].replace(",", "."))
                price = float(row[COL_PRICE].replace(",", "."))
                yield Transaction(
                    id="",
                    timestamp=datetime.strptime(row[COL_DATE], "%Y-%m-%d"),
                    symbol=row[COL_PAPER],
                    type=AssetType.Stock,
                    platform=self.source_name,
                    currency=Currency(row[COL_CURRENCY]),
                    amount=amount,
                    quantity=float(row[COL_QUANTITY]),
                    exchange_rate=1,
                    amount_ref_currency=amount,
                    price=price,
                    action=Action("BUY" if row["-"] == "K" else "SELL"),
                )
