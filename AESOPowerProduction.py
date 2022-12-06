import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
import plotly.express as px
import streamlit as st
st. set_page_config(layout="wide")

url = 'http://ets.aeso.ca/ets_web/ip/Market/Reports/CSDReportServlet'
data = requests.get(url).text

soup = BeautifulSoup(data, 'html.parser')

def getGas(soup):
    summary = soup.select_one(
        "table:has(b:-soup-contains(GAS)):not(:has(table))"
    )
    summary.tr.extract()
    return pd.read_html(str(summary))[0] 

dfGas = getGas(soup).copy()
dfGas.columns = dfGas.iloc[1]
dfGas = dfGas[dfGas['ASSET'] != 'ASSET']
dfGas['Type'] = 'Gas'
dfGas['SubType'] = np.where(dfGas['DCR'].str.isnumeric(), np.nan, dfGas['ASSET'])
dfGas['SubType'] = dfGas['SubType'].ffill(axis=0)
dfGas = dfGas[dfGas['MC'].str.isnumeric()]
dfGas[['MC', 'TNG', 'DCR']] = dfGas[['MC', 'TNG', 'DCR']].apply(pd.to_numeric)

def getHydro(soup):
    summary = soup.select_one(
        "table:has(b:-soup-contains(HYDRO)):not(:has(table))"
    )
    summary.tr.extract()
    return pd.read_html(str(summary))[0]

dfHydro = getHydro(soup).copy()
dfHydro.columns = dfHydro.iloc[0]
dfHydro = dfHydro[dfHydro['ASSET'] != 'ASSET']
dfHydro['Type'] = 'Hydro'
dfHydro['SubType'] = np.where(dfHydro['DCR'].str.isnumeric(), np.nan, dfHydro['ASSET'])
dfHydro['SubType'] = dfHydro['SubType'].ffill(axis=0)
dfHydro = dfHydro[dfHydro['MC'].str.isnumeric()]
dfHydro[['MC', 'TNG', 'DCR']] = dfHydro[['MC', 'TNG', 'DCR']].apply(pd.to_numeric)

def getStorage(soup):
    summary = soup.select_one(
        "table:has(b:-soup-contains(STORAGE)):not(:has(table))"
    )
    summary.tr.extract()
    return pd.read_html(str(summary))[0]

dfStorage = getStorage(soup).copy()
dfStorage.columns = dfStorage.iloc[0]
dfStorage = dfStorage[dfStorage['ASSET'] != 'ASSET']
dfStorage['Type'] = 'Storage'
dfStorage['SubType'] = np.where(dfStorage['DCR'].str.isnumeric(), np.nan, dfStorage['ASSET'])
dfStorage['SubType'] = dfStorage['SubType'].ffill(axis=0)
dfStorage = dfStorage[dfStorage['MC'].str.isnumeric()]
dfStorage[['MC', 'TNG', 'DCR']] = dfStorage[['MC', 'TNG', 'DCR']].apply(pd.to_numeric)

def getSolar(soup):
    summary = soup.select_one(
        "table:has(b:-soup-contains(SOLAR)):not(:has(table))"
    )
    summary.tr.extract()
    return pd.read_html(str(summary))[0]

dfSolar = getSolar(soup).copy()
dfSolar.columns = dfSolar.iloc[0]
dfSolar = dfSolar[dfSolar['ASSET'] != 'ASSET']
dfSolar['Type'] = 'Solar'
dfSolar['SubType'] = np.where(dfSolar['DCR'].str.isnumeric(), np.nan, dfSolar['ASSET'])
dfSolar['SubType'] = dfSolar['SubType'].ffill(axis=0)
dfSolar = dfSolar[dfSolar['MC'].str.isnumeric()]
dfSolar[['MC', 'TNG', 'DCR']] = dfSolar[['MC', 'TNG', 'DCR']].apply(pd.to_numeric)

def getWind(soup):
    summary = soup.select_one(
        "table:has(b:-soup-contains(WIND)):not(:has(table))"
    )
    summary.tr.extract()
    return pd.read_html(str(summary))[0]

dfWind = getWind(soup).copy()
dfWind.columns = dfWind.iloc[0]
dfWind = dfWind[dfWind['ASSET'] != 'ASSET']
dfWind['Type'] = 'Wind'
dfWind['SubType'] = np.where(dfWind['DCR'].str.isnumeric(), np.nan, dfWind['ASSET'])
dfWind['SubType'] = dfWind['SubType'].ffill(axis=0)
dfWind = dfWind[dfWind['MC'].str.isnumeric()]
dfWind[['MC', 'TNG', 'DCR']] = dfWind[['MC', 'TNG', 'DCR']].apply(pd.to_numeric)


def getBiomass(soup):
    summary = soup.select_one(
        "table:has(b:-soup-contains(BIOMASS)):not(:has(table))"
    )
    summary.tr.extract()
    return pd.read_html(str(summary))[0]

dfBiomass = getBiomass(soup).copy()
dfBiomass.columns = dfBiomass.iloc[0]
dfBiomass = dfBiomass[dfBiomass['ASSET'] != 'ASSET']
dfBiomass['Type'] = 'Biomass and Other'
dfBiomass['SubType'] = np.where(dfBiomass['DCR'].str.isnumeric(), np.nan, dfBiomass['ASSET'])
dfBiomass['SubType'] = dfBiomass['SubType'].ffill(axis=0)
dfBiomass = dfBiomass[dfBiomass['MC'].str.isnumeric()]
dfBiomass[['MC', 'TNG', 'DCR']] = dfBiomass[['MC', 'TNG', 'DCR']].apply(pd.to_numeric)

def getDual(soup):
    summary = soup.select_one(
        "table:has(b:-soup-contains(DUAL)):not(:has(table))"
    )
    summary.tr.extract()
    return pd.read_html(str(summary))[0]

dfDual = getDual(soup).copy()
dfDual.columns = dfDual.iloc[0]
dfDual = dfDual[dfDual['ASSET'] != 'ASSET']
dfDual['Type'] = 'Dual'
dfDual['SubType'] = np.where(dfDual['DCR'].str.isnumeric(), np.nan, dfDual['ASSET'])
dfDual['SubType'] = dfDual['SubType'].ffill(axis=0)
dfDual = dfDual[dfDual['MC'].str.isnumeric()]
dfDual[['MC', 'TNG', 'DCR']] = dfDual[['MC', 'TNG', 'DCR']].apply(pd.to_numeric)

def getCoal(soup):
    summary = soup.select_one(
        "table:has(b:-soup-contains(COAL)):not(:has(table))"
    )
    summary.tr.extract()
    return pd.read_html(str(summary))[0]

dfCoal = getCoal(soup).copy()
dfCoal.columns = dfCoal.iloc[0]
dfCoal = dfCoal[dfCoal['ASSET'] != 'ASSET']
dfCoal['Type'] = 'Coal'
dfCoal['SubType'] = np.where(dfCoal['DCR'].str.isnumeric(), np.nan, dfCoal['ASSET'])
dfCoal['SubType'] = dfCoal['SubType'].ffill(axis=0)
dfCoal = dfCoal[dfCoal['MC'].str.isnumeric()]
dfCoal[['MC', 'TNG', 'DCR']] = dfCoal[['MC', 'TNG', 'DCR']].apply(pd.to_numeric)

dfConsol = pd.concat([dfGas, dfHydro, dfStorage, dfSolar, dfWind, dfBiomass, dfDual, dfCoal], ignore_index=True)
dfConsol['SubType'].fillna(dfConsol['Type'], inplace=True)

fig = px.sunburst(dfConsol, path=['Type', 'SubType', 'ASSET'], values='TNG', 
                  color_discrete_sequence=px.colors.qualitative.Vivid)
fig.update_traces(hovertemplate = '<b>%{label}</b><br>Current Generation: %{value} MW',
                  insidetextorientation='radial')
st.plotly_chart(fig, use_container_width=True)