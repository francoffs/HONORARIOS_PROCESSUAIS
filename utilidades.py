from pathlib import Path
import streamlit as st
import pandas as pd
import re
from datetime import date, datetime



def leitura_dados():
    if not 'dados' in st.session_state:
        df_clientes = pd.read_csv('clientes.csv', sep=';', decimal=',', index_col=0, parse_dates=True)
        df_parcelas = pd.read_csv('parcelas.csv', sep=';', decimal=',', parse_dates=True)
        dados = {'df_clientes': df_clientes,
                'df_parcelas': df_parcelas}
        st.session_state['dados'] = dados
   
#def converte_datas(): 


'''def leitura_dados():
    if not 'dados' in st.session_state:
        df_clientes = pd.read_excel('clientes.csv', sep=';', decimal=',', index_col=0, parse_dates=True)
        dados = {'df_clientes': df_clientes}
        st.session_state['dados'] = dados'''



