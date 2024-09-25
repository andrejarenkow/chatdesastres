# Importação de bibliotecas
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai import Agent

# Leitura do dataframe
data = pd.read_excel("https://docs.google.com/spreadsheets/d/1mnF0CnGhJD41i7L-FZ1_K1gEhfpIgVmQO_6AEEVFNyM/pub?output=xlsx")

# filtrando somente Carimbo de data/hora depoius de 2024-09-09
data = data[data['Carimbo de data/hora'] > '2024-09-09']

data
