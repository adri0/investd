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
from IPython.display import Markdown

from investd.config import REF_CURRENCY
from investd.model import Transaction
from investd.portfolio import net_worth_by_asset_type, total_net_worth

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
df_tx = Transaction.from_csv("../../sample_data/persist/tx.csv")
df_tx = df_tx[df_tx["timestamp"] <= now]

# %%
Markdown(
    f"""
### Net Worth 

{total_net_worth(df_tx):.2f} {REF_CURRENCY}
"""
)

# %%
pd.DataFrame(
    net_worth_by_asset_type(df_tx).apply(lambda val: f"{val:.2f} {REF_CURRENCY}")
)

# %% [markdown]
# ### Portfolio evolution

# %%
fig, ax = plt.subplots()
fig.autofmt_xdate()

cumsum = df_tx["amount_ref_currency"].cumsum()
df_cum = pd.DataFrame({"Total value": cumsum, "Time": df_tx["timestamp"]})

fig = sns.lineplot(x="Time", y="Total value", data=df_cum, ax=ax)
