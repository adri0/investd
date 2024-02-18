class InvestdException(Exception):
    msg: str


class NoTransactions(InvestdException):
    msg = "No transactions! Make sure you have non-empty files in the sources folder according to each source."
