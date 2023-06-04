# %%
from datetime import date, datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from IPython.display import Markdown, display

from investd import views
from investd.config import INVESTD_REF_CURRENCY
from investd.quotes import load_quotes
from investd.transaction import load_transactions

sns.set_theme()

# %% [markdown]
# # Portfolio overview

# %%
now = datetime.now()
Markdown(
    f"""
Generated at: **{now.strftime("%Y-%m-%d")}** | Reference currency: **{INVESTD_REF_CURRENCY}**
"""
)

# %%
df_tx = load_transactions()
df_tx = df_tx[df_tx["timestamp"] <= now]

# %% [markdown]
# ### Invested amount

# %%
Markdown(
    f"""
{views.total_invested_ref_currency(df_tx):.2f} {INVESTD_REF_CURRENCY}
"""
)

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

# %%

df_quotes = load_quotes()
df_portfolio = views.portfolio_value(
    df_tx, df_quotes, at_date=date(2022, 12, 30)
).round(2)

display(df_portfolio)

print("Total amount PLN:", df_portfolio[f"Amount at date {INVESTD_REF_CURRENCY}"].sum())
