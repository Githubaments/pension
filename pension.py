import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import math
import sys
import os
import requests
#import SessionState


years = st.sidebar.slider('Investment timeline', min_value=1, value=50, max_value=100, format="%i ", key=0) +1
returns = st.sidebar.slider('Investment Returns', min_value=0.00, value=5.00, max_value=100.00, format="%f %%", key=1) / 100
initial = int(st.sidebar.text_input('Initial Amount', value=0, max_chars=20, key=None, type='default'))
inflow = int(st.sidebar.text_input('Montly Savings', value='0', max_chars=20, key=None, type='default'))
inflow_growth = st.sidebar.slider('Annual Savings Increase', min_value=0.00, value=0.00, max_value=100.00, format="%f %%", key=1)
fees = st.sidebar.slider('Investment Fees', min_value=0.00, value=1.00, max_value=100.00, format="%f %%", key=1) / 100

df = pd.DataFrame(index=(np.arange(1, years)))
df['Inflow'] = (inflow * 12) * df.index

returns2 = (returns - (fees)*(1 + returns))
gross_rate = ((1 + (returns / 1)) ** (1/12)) -1
net_rate =  ((1 + (returns2 / 1)) ** (1/12)) -1


df['Compound']  = (initial * (1 + gross_rate) ** (df.index * 12)) + inflow * ( ( ( 1 + gross_rate) **(df.index * 12) - 1) / gross_rate)
df['Compound Net fees']  = (initial * (1 + net_rate) ** (df.index * 12)) + inflow * ( ( ( 1 + net_rate) **(df.index * 12) - 1) / net_rate)
#df['Gains'] = df['Compound'] - df['Inflow']

df = df.astype(int)


fig = px.line(df)
fig.add_trace(go.Scatter(x=df.index , y=df['Compound Net fees'] ,
                         mode = 'lines',
                         fill='tonexty'))
st.plotly_chart(fig)


st.table(df)
