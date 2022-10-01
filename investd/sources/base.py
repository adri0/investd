import abc
from pathlib import Path
from typing import Generator, Iterable

from ..model import Transaction


class SourceBase(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def source_name(self) -> str:
        pass

    @abc.abstractmethod
    def parse_source_file(self, tx_path: Path) -> Iterable[Transaction]:
        pass

    def load_transactions(self) -> Generator[Transaction, None, None]:
        for path in Path("data/source/" + self.source_name).glob("*"):
            for tx in self.parse_source_file(path):
                yield tx
