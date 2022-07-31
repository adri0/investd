import pandas as pd

from . import xtb, revolut_stocks, revolut_currencies


def load_transactions_from_file(path: str) -> pd.DataFrame:
    for loader in (xtb, revolut_stocks, revolut_currencies):
        try:
            if loader.recognise_file(path):
                break
        except Exception as e:
            print("Loader failed upon recognising file: ", loader)
            print(e)
    else:
        raise ValueError(f"No loaders found for file {path}")

    return loader.load_from_file(path)