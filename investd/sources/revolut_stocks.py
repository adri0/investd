import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable

from ..model import Action, AssetType, Currency, Transaction
from .base import SourceBase


class RevolutStocks(SourceBase):

    source_name = "revolut_stocks"

    def parse_source_file(self, path: Path) -> Iterable[Transaction]:
        with path.open("r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                if not row["Ticker"] or row["Type"] not in ("BUY", "SELL"):
                    continue
                yield Transaction(
                    id="",
                    timestamp=datetime.strptime(row["Date"], "%d/%m/%Y %H:%M:%S"),
                    symbol=row["Ticker"],
                    type=AssetType.Stock,
                    platform="Revolut",
                    currency=Currency(row["Currency"]),
                    amount=float(row["Total Amount"]),
                    quantity=float(row["Quantity"]),
                    exchange_rate=float(row["FX Rate"]),
                    amount_ref_currency=(
                        float(row["Total Amount"]) * float(row["FX Rate"])
                    ),
                    price=float(row["Price per share"]),
                    action=Action(row["Type"].lower()),
                )