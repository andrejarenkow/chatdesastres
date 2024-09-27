# Importação de bibliotecas
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from pandasai import Agent
from pandasai.responses.streamlit_response import StreamlitResponse
from pandasai.llm import BambooLLM
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI

# Configurações da página
st.set_page_config(
    page_title="ChatDesastres RS",
    page_icon="⛈️",
    #layout="wide",
    #initial_sidebar_state='collapsed'
) 

# título
st.header('Chat Desastres RS', divider=True)

    # Verifica se a chave 'mensagens' existe no st.session_state
if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []  # Inicializa 'mensagens' como uma lista vazia

mensagens = st.session_state['mensagens']  # Acessa a lista de mensagens

consumer_complaint_data = pd.read_csv('https://docs.google.com/spreadsheets/d/1mnF0CnGhJD41i7L-FZ1_K1gEhfpIgVmQO_6AEEVFNyM/pub?output=csv', parse_dates= ['Carimbo de data/hora'], dayfirst =  True)
consumer_complaint_data_setembro = consumer_complaint_data[consumer_complaint_data['Carimbo de data/hora']>='2024-09-23']

# Save dataset as CSV
consumer_complaint_data_setembro.to_csv('consumer_complaint_data.csv', index=False, sep=';')

# Nomes das colunas
nomes_colunas =         [
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
       'Quais são esses abrigos? Descreva o local e sua capacidade de ocupação. Se possível informe o número de pessoas abrigadas (Ex: Ginásio municipal ...)']


csv_agent = create_csv_agent(
    ChatOpenAI(temperature=0, model="gpt-4o-mini-2024-07-18", api_key=st.secrets["OPENAI_API_KEY"]),
    path='consumer_complaint_data.csv',
    pandas_kwargs={'sep': ';', 'parse_dates': ['Data e hora da resposta'], 'dayfirst': True, 'names':nomes_colunas, 'header':0},
    allow_dangerous_code=True,
    verbose=True,
    include_df_in_prompt  = 10,
    agent_type = AgentType.OPENAI_FUNCTIONS,
    prefix='Este é um dataframe chamado df a partir de um Google Forms, onde as respostas são relacionadas aos municípios que passam por situação de desastre'
)


prompt_usuario = st.chat_input('Pergunte algo sobre as respostas do formulário do Vigidesastres')

resposta = csv_agent.invoke({'input': 'quais municípios tiveram problema com abastecimento de água?'})
print(resposta['output'])

#resposta = agente.chat('faça um gráfico de linha do tempo com as respostas')
if prompt_usuario:
    nova_mensagem = {'role':'user', 'content':prompt_usuario}
    chat = st.chat_message(nova_mensagem['role'])
    chat.markdown(nova_mensagem['content'])
    mensagens.append(nova_mensagem)

    # Gerar resposta do modelo da tabela
    chat = st.chat_message('assistant')
    placeholder = chat.empty()
    resposta_completa = ''

    placeholder.markdown('| ')
    respostas = csv_agent.invoke({'input': prompt_usuario})['output']
    #placeholder.write(resposta_completa)

    for resposta in respostas:
        resposta_completa += str(resposta)
        placeholder.markdown(resposta_completa)  # Atualiza o placeholder com o conteúdo parcial
      
      # Cria a nova mensagem apenas se houver conteúdo na resposta completa
      if resposta_completa:
          nova_mensagem = {'role': 'assistant', 'content': resposta_completa}
          mensagens.append(nova_mensagem)

      st.session_state['mensagens'] = mensagens
     



    
    
