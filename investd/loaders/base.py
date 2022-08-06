import abc
import csv
from typing import Generator, Generic, TypeVar, get_args

import pandas as pd
from pydantic import BaseModel

from investd.model import ExchangeRate, Transaction

__Model__= TypeVar("__Model__", bound=BaseModel)


class Loader(Generic[__Model__], metaclass=abc.ABCMeta):

    original_model = __Model__

    def load_from_file(self, path: str) -> Generator[__Model__, None, None]:
        raise NotImplementedError()

    def convert_to_tx(self, source_tx: __Model__) -> Transaction:
        raise NotImplementedError()

    def convert_to_fx_rate(self, source_tx: __Model__) -> Transaction:
        raise NotImplementedError()

    def convert_file(self, path: str) -> Generator[tuple[Transaction, ExchangeRate], None, None]:
        with open(path, "r") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                yield self.original_model(**row)
