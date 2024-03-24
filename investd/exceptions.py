class InvestdError(Exception):
    msg: str


class NoTransactionsError(InvestdError):
    msg = "No transactions! Make sure you have non-empty files in the sources folder according to each source."
