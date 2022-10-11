from datetime import datetime

from pytest import approx

from investd.model import Action, AssetType, Currency, Transaction
from investd.sources.xtb import XTB


def test_parse_xtb(path_xtb_xlsx):
    xtb_source = XTB()
    txs = list(xtb_source.parse_source_file(path_xtb_xlsx))
    tx: Transaction = txs[1]
    assert len(txs) == 14
    assert tx.id == "202210996"
    assert tx.symbol == "V80A.DE"
    assert tx.timestamp == datetime(2022, 5, 2, 14, 30, 0)
    assert tx.type == AssetType.ETF
    assert tx.platform == "xtb"
    assert tx.currency == Currency.EUR
    assert tx.amount == 5 * 29.765
    assert tx.quantity == 5
    assert tx.price == 29.765
    assert tx.exchange_rate == approx(688.84 / (5 * 29.765), 10e-5)
    assert tx.amount_ref_currency == 688.84
    assert tx.action == Action.BUY


def test_parse_comment():
    assert XTB.parse_comment("OPEN BUY 1 @ 467.03") == ("BUY", 1, 467.03)
    assert XTB.parse_comment("OPEN BUY 10 @ 30.680") == ("BUY", 10, 30.68)


def test_infer_currency():
    assert XTB.infer_currency_from_symbol("V80A.DE") == Currency.EUR
    assert XTB.infer_currency_from_symbol("CDR.PL") == Currency.PLN
    assert XTB.infer_currency_from_symbol("CSPX.UK") == Currency.USD
    assert XTB.infer_currency_from_symbol("DAXEX.DE") == Currency.EUR
