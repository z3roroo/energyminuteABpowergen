import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import plotly.express as px
import streamlit as st

url = 'http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet'
data = requests.get(url).text

soup = BeautifulSoup(data, 'html.parser')

termMapper = {'GAS': {'Type': 'Gas', 'df': None},
              'HYDRO': {'Type': 'Hydro', 'df': None},
              'STORAGE': {'Type': 'Storage', 'df': None},
              'SOLAR': {'Type': 'Solar', 'df': None},
              'WIND': {'Type': 'Wind', 'df': None},
              'BIOMASS': {'Type': 'Biomass/Other', 'df': None},
              'DUAL': {'Type': 'Dual', 'df': None},
              'COAL': {'Type': 'Coal', 'df': None}}

def getData(soup, searchTerm):
    summary = soup.select_one(
        'table:has(b:-soup-contains(' + searchTerm + ')):not(:has(table))'
    )
    summary.tr.extract()
    return pd.read_html(str(summary))[0]

for t in termMapper:
    termMapper[t]['df'] = getData(soup, t).copy()
    if t == 'GAS':
        termMapper[t]['df'].columns = termMapper[t]['df'].iloc[1]
    else:
        termMapper[t]['df'].columns = termMapper[t]['df'].iloc[0]
    termMapper[t]['df'] = termMapper[t]['df'][termMapper[t]['df']['ASSET'] != 'ASSET']
    termMapper[t]['df']['Geog'] = 'Alberta'
    termMapper[t]['df']['Type'] = termMapper[t]['Type']
    termMapper[t]['df']['SubType'] = np.where(termMapper[t]['df']['DCR'].str.isnumeric(), 
                                              np.nan, termMapper[t]['df']['ASSET'])
    termMapper[t]['df']['SubType'] = termMapper[t]['df']['SubType'].ffill(axis=0)
    termMapper[t]['df'] = termMapper[t]['df'][termMapper[t]['df']['MC'].str.isnumeric()]
    termMapper[t]['df'][['MC', 'TNG', 'DCR']] = termMapper[t]['df'][['MC', 'TNG', 'DCR']].apply(pd.to_numeric)

dfConsol = pd.concat([termMapper[j]['df'] for j in termMapper], ignore_index=True)
dfConsol['SubType'].fillna(dfConsol['Type'], inplace=True)

fig = px.sunburst(dfConsol, path=['Type', 'SubType', 'ASSET'], values='TNG', 
                  color_discrete_sequence=px.colors.qualitative.Vivid,
                  title='Total Current Generation: ' + str(sum(dfConsol['TNG'])) + 'MW')
fig.update_traces(hovertemplate = '<b>%{label}</b><br>Current Generation: %{value} MW',
                  insidetextorientation='radial')
fig.update_layout(width=800, height=800)
st.markdown('### ENERGYminute Current Alberta Electricity Generation')
st.markdown('#### By type, subtype (where available) and individual generation facility')
st.markdown('*Click on a power type to zoom to that level.  Clicking on the center of the ' +
            'suburst will take you up one level.*')
st.plotly_chart(fig, use_container_width=True)
st.markdown('All data from the Alberta Energy System Operator [(AESO)](http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet)')
st.markdown('Inspiration for the chart from [Voltex](https://voltex.ca/dashboard/aeso/supply)')
st.markdown('Python code for aggregation and charting at [this link](https://github.com/jawook/energyminuteABpowergen)')