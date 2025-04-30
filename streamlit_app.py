import streamlit as st
import pandas as pd
from langchain.agents import Agent
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.llms import Groq
from langchain_openai import ChatOpenAI
import os

# Configurações da página
st.set_page_config(
    page_title="ChatDesastres RS",
    page_icon="⛈️",
)

# Título
st.header('Chat Desastres RS - memória curta', divider=True)

# Verifica se a chave 'mensagens' existe no st.session_state
if 'mensagens' not in st.session_state:
    st.session_state.mensagens = []

mensagens = st.session_state['mensagens']

# Nomes das colunas
nomes_colunas = [
    'Data e hora da resposta',
    'Coordenadoria Regional de Saúde (CRS)',
    'Município',
    'Respondente',
    'Área técnica',
    'E-mail',
    'Finalidade do preenchimento',
    'Tipologia do desastre',
    'Data de ocorrência do evento',
    'Interrupção do fornecimento de energia elétrica',
    'Interrupção do abastecimento de água',
    'Fontes de abastecimento alternativas água',
    'Estabelecimento de saúde afetado',
    'Descrição estabelecimentos de saúde afetados',
    'Interrupção dos serviços de saúde',
    'Perda de medicamentos',
    'Perda de imunobiológicos',
    'Descrição dos insumos, medicamentos e imunobiológicos que foram perdidos',
    'Abrigos públicos utilizados',
    'Trabalhadores/voluntários tem acesso aos EPIs necessários para atuar nessa emergência? ',
    'Óbitos',
    'Possiblidade de abrigos',
    'O município possui Plano de Contigência ou Ação, no âmbito da saúde, para desastres?',
    'Perda de insumos',
    'Quais são esses abrigos? Descreva o local e sua capacidade de ocupação. Se possível informe o número de pessoas abrigadas (Ex: Ginásio municipal...)'
]

# Carregando os dados
consumer_complaint_data = pd.read_csv(
    'https://docs.google.com/spreadsheets/d/1mnF0CnGhJD41i7L-FZ1_K1gEhfpIgVmQO_6AEEVFNyM/pub?output=csv',
    parse_dates=['Data e hora da resposta'],
    dayfirst=True,
    names=nomes_colunas,
    header=0
)
df = consumer_complaint_data[consumer_complaint_data['Data e hora da resposta'] >= '2024-09-23']

# Salvar como CSV
df.to_csv('consumer_complaint_data.csv', index=False, sep=';')

# Configurar o modelo Groq
groq_api_key = st.secrets["GROQ_API_KEY"]
llm = Groq(
    model_name="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=2000,
    api_key=groq_api_key
)

# Criar o agente do dataframe
csv_agent = create_pandas_dataframe_agent(
    llm,
    df,
    agent_type="tool-calling",
    allow_dangerous_code=True,
    verbose=True,
    include_df_in_prompt=True,
    number_of_head_rows=10,
    prefix='Este é um dataframe chamado df a partir de um Google Forms, onde as respostas são relacionadas aos municípios que passam por situação de desastre'
)

# Interface de chat
prompt_usuario = st.chat_input('Pergunte algo sobre as respostas do formulário do Vigidesastres')

if prompt_usuario:
    nova_mensagem = {'role': 'user', 'content': prompt_usuario}
    chat = st.chat_message(nova_mensagem['role'])
    chat.write(nova_mensagem['content'])
    mensagens.append(nova_mensagem)

    # Gerar resposta do modelo da tabela
    chat = st.chat_message('assistant')
    placeholder = chat.empty()

    resposta = csv_agent.invoke({'input': prompt_usuario})['output']
    placeholder.write(resposta)
    nova_resposta = {'role': 'assistant', 'content': resposta}
    mensagens.append(nova_resposta)

    st.session_state['mensagens'] = mensagens
