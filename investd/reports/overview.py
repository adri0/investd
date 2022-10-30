# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.display import Markdown, display

from investd.config import PERSIST_PATH, REF_CURRENCY
from investd.metrics import invested_ref_amount_by_col, total_invested_ref_currency
from investd.model import Transaction

sns.set_theme()

# %% [markdown]
# # Portfolio overview

# %%
now = datetime.now()
Markdown(
f"""
Generated at: **{now.strftime("%Y-%m-%d")}** | Reference currency: **{REF_CURRENCY}**
"""
)

# %%
df_tx = Transaction.from_csv(PERSIST_PATH / "tx.csv")
df_tx = df_tx[df_tx["timestamp"] <= now]

# %% [markdown]
# ### Invested amount

# %%
Markdown(f"""
{total_invested_ref_currency(df_tx):.2f} {REF_CURRENCY}
""")

# %% [markdown]
# ### Invested amount by asset type

# %%
df = pd.DataFrame(invested_ref_amount_by_col(df_tx, "type"))

df.columns = [REF_CURRENCY]
df.index.set_names("", inplace=True)
df = df.applymap(round, ndigits=2)

display(df)

# %% [markdown]
# ### Invested amount by currency

# %%
df = pd.DataFrame(invested_ref_amount_by_col(df_tx, "currency"))

df.columns = [REF_CURRENCY]
df.index.set_names("", inplace=True)
df = df.applymap(round, ndigits=2)

display(df)

# %% [markdown]
# ### Invested amount evolution

# %%
fig, ax = plt.subplots()
fig.autofmt_xdate()
ax.set_title("Investment Evolution")

cumsum = df_tx["amount_ref_currency"].cumsum()
df_cum = pd.DataFrame({"Total value": cumsum, "Time": df_tx["timestamp"]})

rep = sns.lineplot(x="Time", y="Total value", data=df_cum, ax=ax)

# %%
