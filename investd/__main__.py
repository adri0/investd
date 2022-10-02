import logging
import sys

from .source import load_txs_from_source

log = logging.getLogger("investd")


def save_tx():
    df_tx = load_txs_from_source()
    output = "data/transactions/tx.csv"
    log.info(f"Writing {output}")
    df_tx.to_csv(output, index=False)


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "load_from_source":
        save_tx()
    else:
        print(f"Unrecognized command {command}")
    log.info("Finish.")
