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
import pandas as pd
import seaborn as sns

sns.set_theme()

# %%
df = pd.read_csv("../../sample_data/persist/tx.csv")

# %% [markdown]
# ## Portfolio evolution

# %%
figure = sns.lineplot(x="timestamp", y="amount_ref_currency", data=df)

# %%
pd.DataFrame(
    [df["amount_ref_currency"].sum()],
    index=["Total Amount (PLN)"]
)

# %%
df_by_currency = df.groupby("currency")[["amount", "amount_ref_currency"]].sum()
df_by_currency.columns = ["Amount", "Amount Ref Currency"]
df_by_currency
