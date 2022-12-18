from datetime import datetime

from investd.model import Action, AssetType, Currency, Transaction
from investd.sources.bossa import Bossa


def test_parse_bossa(path_bossa_csv):
    bossa_source = Bossa()
    txs = list(bossa_source.parse_source_file(path_bossa_csv))
    assert len(txs) == 2

    txs = sorted(txs, key=lambda t: t.timestamp)

    tx: Transaction = txs[0]
    assert tx.id == ""
    assert tx.symbol == "Vanguard LifeStrategy 80% Equity UCITS ETF"
    assert tx.timestamp == datetime(2022, 3, 23, 0, 0, 0)
    assert tx.type == AssetType.Stock
    assert tx.platform == "bossa"
    assert tx.currency == Currency.PLN
    assert tx.amount == 4306.29
    assert tx.quantity == 31
    assert tx.price == 138.9126
    assert tx.exchange_rate == 1
    assert tx.amount_ref_currency == 4306.29
    assert tx.action == Action.BUY
