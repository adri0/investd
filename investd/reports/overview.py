# %%
import os
from datetime import date, datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import Markdown, display

from investd import views
from investd.config import INVESTD_REF_CURRENCY
from investd.quotes import load_quotes
from investd.transaction import load_transactions

sns.set_theme()
pd.options.display.float_format = "{:,.2f}".format
# %% [markdown]
# # Portfolio overview

# %%
now = datetime.now()

report_date_env_var = os.getenv("REPORT_DATE")
report_date = (
    date.fromisoformat(report_date_env_var) if report_date_env_var else date.today()
)

pd.DataFrame(
    {
        "Reporting date": [report_date],
        "Reference currency": [INVESTD_REF_CURRENCY],
        "Created date": [now.strftime("%Y-%m-%d")],
    },
    index=[""],
)


# %%
df_tx = load_transactions()
df_tx = df_tx[df_tx["timestamp"] <= pd.Timestamp(report_date)]

# %%

df_quotes = load_quotes()
df_portfolio = views.portfolio_value(df_tx, df_quotes, at_date=report_date)

# %%

ref_amount_cols = [
    col for col in df_portfolio.columns if str(INVESTD_REF_CURRENCY) in col
]
row_total = df_portfolio.loc[:, ref_amount_cols].sum(axis=0)
row_total = pd.DataFrame(row_total, columns=["Total"]).transpose()
df_p_total = pd.concat([df_portfolio, row_total])


def highlight_total_row(row: pd.Series) -> list[str]:
    if row.name == "Total":
        return [("font-weight: bold" if not np.isnan(val) else "") for val in row]
    return [""] * len(row)


df_p_total.style.apply(highlight_total_row, axis=1).format(na_rep="", precision=2)

# %% [markdown]
# ### Invested amount by asset type

# %%
df = views.invested_ref_amount_by_col(df_tx, "type")

display(df)
fig = df.plot.pie(y=str(INVESTD_REF_CURRENCY))
fig.get_legend().remove()

# %% [markdown]
# ### Invested amount by currency

# %%
df = views.amounts_by_currency(df_tx)

display(df)
fig = df.plot.pie(y=str(INVESTD_REF_CURRENCY))
fig.get_legend().remove()

# %% [markdown]
# ### Invested amount over time

# %%
df = views.amount_over_time(df_tx, period="Y")
display(df)

# %%
df = views.amount_over_time(df_tx, period="M").iloc[-12:]
display(df)

# %%
fig, ax = plt.subplots()
fig.autofmt_xdate()

cumsum = df_tx["amount_ref_currency"].cumsum()
df_cum = pd.DataFrame({INVESTD_REF_CURRENCY: cumsum, "Date": df_tx["timestamp"]})

fig = sns.lineplot(x="Date", y=INVESTD_REF_CURRENCY, data=df_cum, ax=ax)
