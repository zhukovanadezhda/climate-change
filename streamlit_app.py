import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

from scripts import toolbox as tb

data = "data/co2_surface-insitu_ccgg_text/co2_brw_surface-insitu_1_ccgg_MonthlyData.txt"
df = pd.read_csv(data, comment="#", sep=" ", header=0)
df.drop(columns="qcflag", inplace=True)
df = tb.convert_to_datetime(df)
df = tb.drop_missing_values(df)
df = tb.correct_season(df)

fig = make_subplots(rows=1, cols=2)
fig = px.line(df, x='datetime', y='value', labels={'datetime': 'Time', 'value': 'CO2 Concentration'},
              title='CO2 Concentration Over Time')
fig.update_traces(mode='lines+markers', hovertemplate='%{y:.2f} ppm<br>%{x}', line=dict(width=2)


st.title('My Streamlit App')
st.plotly_chart(fig)


# st.sidebar.header("Let's look for the info you need")
# req = st.sidebar.text_area("Write your request below:")
# search_button = st.sidebar.button("Search")

# if search_button:
#     try:
#         req_text = fc.call_wiki(req.strip())
#         st.title(f"{req}")
#         st.write(req_text)
#     except:
#         st.title(f"{req}")
#         st.header("Sorry!")
#         st.write(f"I don't have any information about {req}")
# else:
#     st.title(f"Ooops...")
#     st.header("Sorry!")
#     st.write("You have to provide a request!")
    
    

#col1, col2 = st.columns(2)
#col1.header("")
#col1.expander("")
