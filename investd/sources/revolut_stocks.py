import csv
from pathlib import Path
from typing import Iterable

import dateutil.parser

from investd.common import Action, AssetType, Currency
from investd.sources.base import SourceBase
from investd.transaction import Transaction


class RevolutStocks(SourceBase):
    source_name = "revolut_stocks"

    def parse_source_file(self, path: Path) -> Iterable[Transaction]:
        with path.open("r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                row_type, *_ = row["Type"].split()
                if not row["Ticker"] or row_type not in ("BUY", "SELL"):
                    continue
                amount = float(row["Total Amount"].replace("$", "").replace(",", ""))
                price = float(row["Price per share"].replace("$", "").replace(",", ""))
                yield Transaction(
                    id="",
                    timestamp=dateutil.parser.isoparse(row["Date"]),
                    symbol=row["Ticker"],
                    type=AssetType.Stock,
                    platform=self.source_name,
                    currency=Currency(row["Currency"]),
                    amount=amount,
                    quantity=float(row["Quantity"]),
                    exchange_rate=float(row["FX Rate"]),
                    amount_ref_currency=(amount / float(row["FX Rate"])),
                    price=price,
                    action=Action(row_type.upper()),
                )
