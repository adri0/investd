import csv
from datetime import datetime
from typing import Generator

import pandas as pd
from pydantic import BaseModel, Field

from investd.loaders.base import Loader
from investd.model import AssetType, Currency, ExchangeRate, Transaction


class RevolutStockTx(BaseModel):
    date: datetime = Field(alias="Date")
    ticker: str = Field(alias="Ticker")
    type: str = Field(alias="Type")
    quantity: float = Field(alias="Quantity")
    price_per_share: float = Field(alias="Price per share")
    total_amount: float = Field(alias="Total Amount")
    currency: str = Field(alias="Currency")
    fx_rate: float = Field(alias="FX Rate")


class RevolutStocksLoader(Loader[RevolutStockTx]):

    def convert_to_tx(self, revolut_tx: RevolutStockTx) -> Transaction:
        return Transaction(
            timestamp=revolut_tx.date,
            symbol=revolut_tx.ticker,
            type=AssetType.Stock,
            platform="Revolut",
            currency=revolut_tx.currency,
            amount=revolut_tx.total_amount,
            quantity=revolut_tx.quantity,
            price=revolut_tx.price_per_share,
            action=revolut_tx.type
        )

    def convert_to_fx_rate(self, revolut_tx: RevolutStockTx) -> ExchangeRate:
        return ExchangeRate(
            timestamp=revolut_tx.date,
            currency_from=Currency.PLN,
            currency_to=revolut_tx.currency
        )
        
    def convert_file(self, path: str) -> Generator[tuple[Transaction, ExchangeRate], None, None]:
        with open(path, "r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                rev_tx = RevolutStockTx(**row)
                tx = self.convert_to_tx(rev_tx)
                fx_rate  = self.convert_to_fx_rate(rev_tx)
                yield (tx, fx_rate)
