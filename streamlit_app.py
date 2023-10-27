import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from scripts import toolbox as tb
st.set_page_config(page_title="Climate Change Dashboard",
                   layout="wide")

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

tb.add_timeseries_to_app(df_list, observ_names)
st.markdown("<p style='font-size: small; font-style: italic;'>Data Source: National Oceanic and Atmospheric Administration (NOAA)</p>", unsafe_allow_html=True)
