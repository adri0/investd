import sys
from os.path import exists

import pandas as pd

from .loaders import load_transactions_from_file
from .loaders.revolut_currencies import reconciliate_exchange


def build_transactions_table(*paths):
    """ Build a transactions tables from a list of files that can be 
        extracted using existing loaders.
    """
    txs = []
    for path in path_files:
        if not exists(path):
            raise ValueError(f"File does not exist: {path}")
        txs += load_transactions_from_file(path)
    df_tx = pd.DataFrame(txs)
    df_tx.sort_values("timestamp", inplace=True)
    df_tx.set_index("id", inplace=True)
    df_tx.to_csv("all_transactions.csv")


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "transactions":
        path_files = sys.argv[2:]
        build_transactions_table(path_files)
    elif command == "recon":
        path_files = sys.argv[2:]
        reconciliate_exchange(*path_files)
    elif command == "dashboard":
        from .app import dash_app
        dash_app.run_server(debug=True)
    else:
        print(f"Unrecognized command {command}")
