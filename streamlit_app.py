import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from scripts import toolbox as tb


def plot_timeseries(df_list, observ_names):
    fig = go.Figure()

    for i, df in enumerate(df_list):
        fig.add_trace(go.Scatter(x=df["datetime"], y=df["value"], mode='lines+markers', 
                                 name=f"CO2 mole fraction - {observ_names[i]}", visible=i == 0))

    for i, df in enumerate(df_list):
        fig.add_trace(go.Scatter(x=df["datetime"], y=df["corrected_value"], mode='lines', 
                                 name=f"Average seasonal cycle correction - {observ_names[i]}", 
                                 line=dict(color="black", width=1), visible=i == 0))

    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="CO2 mole fraction (ppm)")
    fig.update_layout(
        title=f"CO2 Concentration Over Time",
        showlegend=True,
        updatemenus=[
            {
                'buttons': [
                    {'method': 'restyle',
                     'label': f'{observ_names[i]}',
                     'args': [{'visible': [(j == i) for j in range(len(df_list))]}],
                    } for i in range(len(df_list))
                ],
                'direction': 'down',
                'showactive': True,
                'x': 0.1,
                'xanchor': 'left',
                'y': 1.1,
                'yanchor': 'top',
            }
        ],
        width=1000,
        height=400
    )

    fig.show()

data_lables = {"brw": "Barrow Observatory, Alaska", 
               "mlo": "Mauna Loa, Hawaii",
               "smo": "American Samoa, USA"}

data_sources = [f"data/co2_surface-insitu_ccgg_text/co2_{lable}_surface-insitu_1_ccgg_MonthlyData.txt" 
        for lable in data_lables.keys()]

df_list =[]
observ_names = []

for data in data_sources:
    df = pd.read_csv(data, comment="#", sep=" ", header=0)
    df.drop(columns="qcflag", inplace=True)
    df = tb.convert_to_datetime(df)
    df = tb.drop_missing_values(df)
    df = tb.correct_season(df)
    df_list.append(df)
    observ_names.append(data_lables[data.split("_")[4]])  

plot_timeseries(df_list, observ_names)
