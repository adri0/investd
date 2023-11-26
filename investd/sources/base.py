import abc
import logging
from pathlib import Path
from typing import Generator, Iterable

from investd import config
from investd.transaction import Transaction

log = logging.getLogger(__name__)


class SourceBase(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def source_name(self) -> str:
        pass

    @abc.abstractmethod
    def parse_source_file(self, tx_path: Path) -> Iterable[Transaction]:
        pass

    def load_transactions(self) -> Generator[Transaction, None, None]:
        for path in (config.INVESTD_SOURCES / self.source_name).glob("*"):
            log.info(f"Loading {path}")
            for tx in self.parse_source_file(path):
                yield tx
