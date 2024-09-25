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

# Verifica se a chave 'mensagens' existe no st.session_state
if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []  # Inicializa 'mensagens' como uma lista vazia

mensagens = st.session_state['mensagens']  # Acessa a lista de mensagens

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

prompt = st.chat_input('Pergunte algo sobre as respostas do formulário do Vigidesastres')
#resposta = agente.chat('faça um gráfico de linha do tempo com as respostas')
if prompt:
    nova_mensagem = {'role':'user', 'content':prompt}
    chat = st.chat_message(nova_mensagem['role'])
    chat.markdown(nova_mensagem['content'])
    mensagens.append(nova_mensagem)
