class InvestdError(Exception):
    msg: str
    pass


class NoTransactions(InvestdError):
    msg = "No transactions! Make sure you non-empty files in the sources folder according to each source."
