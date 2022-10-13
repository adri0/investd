from datetime import datetime

from pytest import approx

from investd.model import Action, AssetType, Currency, Transaction
from investd.sources.revolut_stocks import RevolutStocks


def test_parse_revolut_stocks(path_revolut_csv):
    revolut_source = RevolutStocks()
    txs = list(revolut_source.parse_source_file(path_revolut_csv))
    assert len(txs) == 4
    tx: Transaction = txs[0]
    assert tx.id == ""
    assert tx.symbol == "AAPL"
    assert tx.timestamp == datetime(2022, 1, 2, 14, 9, 22)
    assert tx.type == AssetType.Stock
    assert tx.platform == "revolut_stocks"
    assert tx.currency == Currency.USD
    assert tx.amount == 100.00
    assert tx.quantity == 0.6420958
    assert tx.price == 155.74
    assert tx.exchange_rate == 0.2616
    assert tx.amount_ref_currency == approx(382.26, 0.01)
    assert tx.action == Action.BUY
