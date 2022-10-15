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
from turtle import title

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.display import Markdown

from investd.config import PERSIST_PATH, REF_CURRENCY
from investd.metrics import invested_amount_by_col, total_invested
from investd.model import Transaction

sns.set_theme()

# %% [markdown]
# # Portfolio overview

# %%
now = datetime.now()

Markdown(
    f"""
Generated date: **{now.strftime("%Y-%m-%d")}** | Reference currency: **{REF_CURRENCY.name}**
"""
)

# %%
df_tx = Transaction.from_csv(PERSIST_PATH / "tx.csv")
df_tx = df_tx[df_tx["timestamp"] <= now]

# %%
Markdown(
    f"""
### Net Worth 

{total_invested(df_tx):.2f} {REF_CURRENCY}
"""
)

# %%
pd.DataFrame(
    invested_amount_by_col(df_tx, "type").apply(lambda val: f"{val:.2f} {REF_CURRENCY}")
)

# %% [markdown]
# ### Portfolio evolution

# %%
fig, ax = plt.subplots()
fig.autofmt_xdate()
ax.set_title("Investment Evolution")

cumsum = df_tx["amount_ref_currency"].cumsum()
df_cum = pd.DataFrame({"Total value": cumsum, "Time": df_tx["timestamp"]})
sns.lineplot(x="Time", y="Total value", data=df_cum, ax=ax)

# %%
