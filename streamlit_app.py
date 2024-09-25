# Importação de bibliotecas
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai import Agent

# Configurações da página
st.set_page_config(
    page_title="ChatDesastres RS",
    page_icon="⛈️",
    #layout="wide",
    #initial_sidebar_state='collapsed'
) 

# Leitura do dataframe
data = pd.read_excel(st.secrets['link_planilha'])

# filtrando somente Carimbo de data/hora depoius de 2024-09-09
data = data[data['Carimbo de data/hora'] > '2024-09-09']

# Instantiate a LLM
llm = OpenAI(
    api_token=st.secrets['OPENAI_API_KEY'],
    temperature=0,
)

agente = Agent(data, config={"llm": llm})

prompt = st.chat_input('Fale com o chat')
#resposta = agente.chat('faça um gráfico de linha do tempo com as respostas')
