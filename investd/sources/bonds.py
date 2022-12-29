from pathlib import Path
from typing import Iterator

import pandas as pd

from ..model import Action, AssetType, Currency, Transaction
from .base import SourceBase

BOND_VALUE = 100

COL_DATE = "DATA DYSPOZYCJI"
COL_CODE = "KOD OBLIGACJI"
COL_STATUS = "STATUS"
COL_TYPE = "RODZAJ DYSPOZYCJI"
COL_COUNT = "LICZBA OBLIGACJI"
COL_AMOUNT = "KWOTA OPERACJI"

STATUS_COMPLETED = "zrealizowana"
TYPE_BUY = "zakup papierów"
TYPE_PREMATURE_SELL = "przedterminowy wykup"
TYPE_SELL = "wykup papierów"
TYPE_TAX = "podatek"
TYPE_SELL_INTEREST = "wykup - odsetki"
TYPE_PREMATURE_SELL_INTEREST = "odsetki"
TYPE_PREMATURE_SELL_FEE = "opłata za przedterminowy wykup"


class Bonds(SourceBase):
    source_name = "bonds"

    def parse_source_file(self, path: Path) -> Iterator[Transaction]:
        df = pd.read_excel(
            path,
            usecols=[COL_DATE, COL_TYPE, COL_CODE, COL_COUNT, COL_AMOUNT, COL_STATUS],
            parse_dates=[COL_DATE],
        )
        df = df[df[COL_STATUS] == STATUS_COMPLETED]

        # correct the number and amount sell operations
        for i in df.index[df[COL_TYPE] == TYPE_SELL].tolist():
            df.at[i, COL_AMOUNT] = df.at[i, COL_COUNT] * BOND_VALUE
            df.at[i, COL_AMOUNT] += df.at[i - 2, COL_AMOUNT] + df.at[i - 3, COL_AMOUNT]
            assert (df.at[i - 2, COL_TYPE] == TYPE_TAX) and (
                df.at[i - 2, COL_CODE] == df.at[i, COL_CODE]
            )
            assert (df.at[i - 3, COL_TYPE] == TYPE_SELL_INTEREST) and (
                df.at[i - 3, COL_CODE] == df.at[i, COL_CODE]
            )

        # correct the number and amount of premature sell operations
        for i in df.index[df[COL_TYPE] == TYPE_PREMATURE_SELL].tolist():
            df.at[i, COL_COUNT] = df.at[i, COL_AMOUNT] // BOND_VALUE
            df.at[i, COL_AMOUNT] += df.loc[i + 1 : i + 3][COL_AMOUNT].sum()
            assert (df.at[i + 1, COL_TYPE] == TYPE_PREMATURE_SELL_INTEREST) and (
                df.at[i + 1, COL_CODE] == df.at[i, COL_CODE]
            )
            assert (df.at[i + 2, COL_TYPE] == TYPE_PREMATURE_SELL_FEE) and (
                df.at[i + 2, COL_CODE] == df.at[i, COL_CODE]
            )

        df = df[df[COL_TYPE].isin({TYPE_BUY, TYPE_SELL, TYPE_PREMATURE_SELL})]
        return map(lambda i_row: self._convert(i_row[1]), df.iterrows())

    def _convert(self, record: pd.Series) -> Transaction:
        quantity = record[COL_COUNT]
        amount = record[COL_AMOUNT]
        price = amount / quantity

        if record[COL_TYPE] == TYPE_BUY:
            action = "BUY"
        elif record[COL_TYPE] in {TYPE_SELL, TYPE_PREMATURE_SELL}:
            action = "SELL"
        else:
            raise Exception(
                f"Value: {record[COL_TYPE]} for column {COL_TYPE} not supported"
            )

        return Transaction(
            id="",
            timestamp=record[COL_DATE].to_pydatetime(),
            symbol=record[COL_CODE],
            type=AssetType.Bond,
            platform=self.source_name,
            currency=Currency.PLN,
            amount=amount,
            quantity=quantity,
            price=price,
            exchange_rate=1,
            amount_ref_currency=amount,
            action=Action(action),
        )
