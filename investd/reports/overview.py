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

from investd import views
from investd.config import PERSIST_PATH, REF_CURRENCY
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
Markdown(
    f"""
{views.total_invested_ref_currency(df_tx):.2f} {REF_CURRENCY}
"""
)

# %% [markdown]
# ### Invested amount by asset type

# %%
df = views.invested_ref_amount_by_col(df_tx, "type")

display(df)
fig = df.plot.pie(y=str(REF_CURRENCY))
fig.get_legend().remove()

# %% [markdown]
# ### Invested amount by currency

# %%
df = views.amounts_by_currency(df_tx)

display(df)
fig = df.plot.pie(y=str(REF_CURRENCY))
fig.get_legend().remove()

# %% [markdown]
# ### Invested amount evolution

# %%
fig, ax = plt.subplots()
fig.autofmt_xdate()

cumsum = df_tx["amount_ref_currency"].cumsum()
df_cum = pd.DataFrame({REF_CURRENCY: cumsum, "Date": df_tx["timestamp"]})

fig = sns.lineplot(x="Date", y=REF_CURRENCY, data=df_cum, ax=ax)

# %%
