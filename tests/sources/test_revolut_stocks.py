from datetime import datetime

from pytest import approx

from investd.model import Action, AssetType, Currency
from investd.sources.revolut_stocks import RevolutStocks


def test_parse_revolut_stocks(path_revolut_csv):
    revolut_source = RevolutStocks()
    txs = revolut_source.parse_source_file(path_revolut_csv)
    txs = [tx for tx in txs]
    assert len(txs) == 4
    assert txs[0].id == ""
    assert txs[0].symbol == "AAPL"
    assert txs[0].timestamp == datetime(2022, 1, 2, 14, 9, 22)
    assert txs[0].type == AssetType.Stock
    assert txs[0].platform == "revolut_stocks"
    assert txs[0].currency == Currency.USD
    assert txs[0].amount == 100.00
    assert txs[0].quantity == 0.6420958
    assert txs[0].price == 155.74
    assert txs[0].exchange_rate == 0.2616
    assert txs[0].amount_ref_currency == approx(382.26, 0.01)
    assert txs[0].action == Action.BUY
