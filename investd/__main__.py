import sys
from os.path import exists

import pandas as pd

from .sources import load_all_transactions


def save_tx():
    df_tx = load_all_transactions()
    df_tx.to_csv("data/output/tx.csv", index=False)




if __name__ == "__main__":
    command = sys.argv[1]
    if command == "save_tx":
        save_tx()
    elif command == "recon":
        path_files = sys.argv[2:]
        reconciliate_exchange(*path_files)
    elif command == "dashboard":
        from .app import dash_app
        dash_app.run_server(debug=True)
    else:
        print(f"Unrecognized command {command}")
