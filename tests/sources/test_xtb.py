from datetime import datetime
from pathlib import Path

from pytest import approx

from investd.common import Action, AssetType, Currency
from investd.sources.xtb import XTB
from investd.transaction import Transaction


def test_parse_xtb_xlsx(path_xtb_xlsx: Path) -> None:
    xtb_source = XTB()
    txs = list(xtb_source.parse_source_file(path_xtb_xlsx))
    assert len(txs) == 17

    tx: Transaction = txs[1]
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


def test_parse_xtb_csv(path_xtb_csv: Path) -> None:
    xtb_source = XTB()
    txs = list(xtb_source.parse_source_file(path_xtb_csv))
    assert len(txs) == 7

    tx: Transaction = txs[0]
    assert tx.id == "130876160"
    assert tx.symbol == "IBC5.DE"
    assert tx.timestamp == datetime(2022, 12, 9, 12, 9, 37)
    assert tx.type == AssetType.ETF
    assert tx.platform == "xtb"
    assert tx.currency == Currency.EUR
    assert tx.amount == 5 * 5.208
    assert tx.quantity == 5
    assert tx.price == 5.208
    assert tx.exchange_rate == approx(1, 10e-5)
    assert tx.amount_ref_currency == 5 * 5.208
    assert tx.action == Action.BUY


def test_parse_comment() -> None:
    assert XTB.parse_comment("OPEN BUY 1 @ 467.03") == (1, 467.03)
    assert XTB.parse_comment("OPEN BUY 10 @ 30.680") == (10, 30.68)


def test_infer_currency() -> None:
    assert XTB.infer_currency_from_symbol("V80A.DE") == Currency.EUR
    assert XTB.infer_currency_from_symbol("CDR.PL") == Currency.PLN
    assert XTB.infer_currency_from_symbol("CSPX.UK") == Currency.USD
    assert XTB.infer_currency_from_symbol("DAXEX.DE") == Currency.EUR
