import dash
from dash import dcc, html, dash_table as dt

import plotly.express as px
import pandas as pd

from .components import get_state


dash_app = dash.Dash(__name__)

df_tx = pd.read_csv("all_transactions.csv", index_col="id")

df_state = get_state(df_tx)

fig = px.scatter(df_tx, x="timestamp", y="amount_ref_currency")

dash_app.layout = html.Div(children=[
    html.H1(children="Investd - Dashboard"),

    dcc.Graph(
        id="Amount invested over time",
        figure=fig
    ),

    dt.DataTable(
        id='invested', data=df_tx.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_tx.columns],
    )

])
