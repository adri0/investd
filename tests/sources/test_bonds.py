from datetime import datetime
from pathlib import Path

from pytest import approx

from investd.common import Action, AssetType, Currency
from investd.sources.bonds import Bonds
from investd.transaction import Transaction


def test_parse_bonds(path_bonds_xls: Path) -> None:
    bonds_source = Bonds()
    txs = list(bonds_source.parse_source_file(path_bonds_xls))
    assert len(txs) == 5

    txs = sorted(txs, key=lambda t: t.timestamp)

    tx: Transaction = txs[0]
    assert tx.id == ""
    assert tx.symbol == "OTS1020"
    assert tx.timestamp == datetime(2020, 7, 13, 0, 0, 0)
    assert tx.type == AssetType.Bond
    assert tx.platform == "bonds"
    assert tx.currency == Currency.PLN
    assert tx.amount == 1000
    assert tx.quantity == 10
    assert tx.price == 100
    assert tx.exchange_rate == 1
    assert tx.amount_ref_currency == 1000
    assert tx.action == Action.BUY

    tx2: Transaction = txs[1]
    assert tx2.symbol == "OTS1020"
    assert tx2.timestamp == datetime(2020, 10, 13, 0, 0, 0)
    assert tx2.amount == 1001.05
    assert tx2.quantity == 10
    assert tx2.price == approx(1001.05 / 10, 10e-5)
    assert tx2.exchange_rate == 1
    assert tx2.amount_ref_currency == 1001.05
    assert tx2.action == Action.SELL
