import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd

from investd.sources.base import SourceBase
from investd.transaction import Transaction


class TestSource(SourceBase):

    source_name = "test_source"

    def parse_source_file(self, tx_path: Path) -> Iterable[Transaction]:
        for _, row in pd.read_csv(tx_path).iterrows():
            yield Transaction(**row)


def test_ingest_source():
    test_source = TestSource()
    txs = list(test_source.load_transactions())
    assert len(txs) == 1
    assert txs[0].id == "test-tx"
