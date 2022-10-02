import sys

from .source import load_txs_from_source


def save_tx():
    df_tx = load_txs_from_source()
    df_tx.to_csv("data/transactions/tx.csv", index=False)


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "load_from_source":
        save_tx()
    else:
        print(f"Unrecognized command {command}")
