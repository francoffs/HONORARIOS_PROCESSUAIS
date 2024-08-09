from pathlib import Path
import streamlit as st
import pandas as pd
import re
from datetime import date, datetime
from utilidades import leitura_dados

leitura_dados()

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']


st.markdown('### CADASTRO DE CLIENTES')
st.markdown('''
            *Nesta tela você poderá apenas cadastrar novos clientes. 
            Por favor, digite os campos correspondentes e confirme os dados antes de salvar.*
             ''')
st.divider()

nome = st.text_input('NOME')
contato = st.text_input('TELEFONE')
cpf = st.text_input('CPF (formato: XXX.XXX.XXX-XX)')
senha_egov = st.text_input('SENHA E-GOV')
tipo_de_acao = st.text_input('TIPO DE AÇÃO')
honorarios_total = st.number_input('VALOR DOS HONORÁRIOS CONTRATADOS')
resumo_caso = st.text_area('RESUMO DO CASO')
data_registro =  st.date_input('DATA DE REGISTRO')


def formatar_cpf(cpf):
    # Remove todos os caracteres que não sejam dígitos
    cpf = ''.join(filter(str.isdigit, cpf))
    # Formata o CPF no padrão XXX.XXX.XXX-XX
    cpf_formatado = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
    return cpf_formatado

if cpf:
    if len(cpf) == 11 and cpf.isdigit():
        cpf_formatado = formatar_cpf(cpf)
        st.success(f"CPF formatado: {cpf_formatado}")
    else:
        st.error("CPF inválido. Certifique-se de digitar 11 dígitos.")



adicionar_cliente = st.button('Adicionar Cliente')
if adicionar_cliente:
    lista_adicionar = [
                       nome,
                       contato,
                       cpf,
                       senha_egov,
                       tipo_de_acao,
                       honorarios_total,
                       resumo_caso,
                       data_registro
                       ]
    if df_clientes.empty:
        index_adicionar = 1
    else:
        index_adicionar = df_clientes.index.max() + 1
    df_clientes.loc[index_adicionar] = lista_adicionar
    #caminho_datasets = st.session_state['caminho_datasets']
    df_clientes.to_csv('clientes.csv', decimal=',', sep=';')


#st.dataframe(df_clientes)
#st.dataframe(df_parcelas)
