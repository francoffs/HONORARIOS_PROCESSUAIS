from pathlib import Path
import streamlit as st
import pandas as pd
import re
from datetime import date, datetime
from jinja2 import FileSystemLoader, Environment
import locale

data_atual = datetime.now().date()
hora_atual = datetime.now().strftime("%H:%M:%S")

def leitura_dados():
    if not 'dados' in st.session_state:
        df_clientes = pd.read_csv('clientes.csv', sep=';', decimal=',', index_col=0, parse_dates=True)
        df_parcelas = pd.read_csv('parcelas.csv', sep=';', decimal=',', parse_dates=True)
        dados = {'df_clientes': df_clientes,
                'df_parcelas': df_parcelas}
        st.session_state['dados'] = dados
   
#def converte_datas(): 


def formatar_valor(valor):
    # Converte o valor para string, com duas casas decimais, separadas por vírgula
    valor_formatado = f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    # Adiciona o símbolo de moeda R$ no início
    return f"R$ {valor_formatado}"

def logo():
    caminho_logo = Path(__file__).parent / 'assets'
    logo = str(caminho_logo / 'LOGO.png')
    st.image(logo,width=200)