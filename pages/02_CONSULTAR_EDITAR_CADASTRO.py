from pathlib import Path
import streamlit as st
import pandas as pd

from utilidades import leitura_dados

leitura_dados()

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']

st.markdown('### CONSULTA DE CLIENTES')
st.markdown('''
            *Nesta tela você poderá consultar e alterar os dados de seus clientes. 
            Por favor, confirme os dados antes de salvar.*
             ''')
st.divider()


Lista_Clientes = sorted(df_clientes['nome'].unique())

Nome_selecionado = st.selectbox('PESQUISE PELO NOME DO CLIENTE:',
                              Lista_Clientes)

Lista_Codigo_Cliente = df_clientes.index[df_clientes['nome'] == Nome_selecionado].tolist()
Codigo_seleciondo = st.selectbox('Selecione o Código do Cliente:',
                                 Lista_Codigo_Cliente)

st.divider()
contato_cliente = df_clientes.loc[Codigo_seleciondo, 'contato']
cpf_cliente = df_clientes.loc[Codigo_seleciondo, 'cpf']
senha_gov_cliente = df_clientes.loc[Codigo_seleciondo, 'senha_egov']
tipo_acao_cliente = df_clientes.loc[Codigo_seleciondo, 'tipo_acao']
valor_honorarios_cliente = str(df_clientes.loc[Codigo_seleciondo, 'valor_honorarios'])
resumo_caso_cliente = df_clientes.loc[Codigo_seleciondo, 'resumo_caso']
data_cadastro_cliente = df_clientes.loc[Codigo_seleciondo, 'data_cadastro']

#Lista_Codigo_Cliente = Lista_Codigo_Cliente.strip('][').replace("'", '').split(', ')

#st.write(Lista_Codigo_Cliente)


#st.write('CLIENTE:', Nome_selecionado)
#st.write('CONTATO:', contato_cliente)
#st.write('CPF:', cpf_cliente)
#st.write('SENHA .GOV:', senha_gov_cliente)
#st.write('TIPO DE AÇÃO:', tipo_acao_cliente)
#st.write('VALOR DOS HONORÁRIOS:', valor_honorarios_cliente)
#st.write('RESUMO DO CASO:', resumo_caso_cliente)
#st.write('DATA DO CADASTRO:', data_cadastro_cliente)


nome = st.text_input('NOME:',
                     Nome_selecionado)
contato = st.text_input('CONTATO:',
                     contato_cliente)
cpf = st.text_input('CPF:',
                     cpf_cliente)
senha = st.text_input('SENHA .GOV:',
                     senha_gov_cliente)
tipo_acao = st.text_input('TIPO DE AÇÃO:',
                     tipo_acao_cliente)
honorarios = st.text_input('VALOR DOS HONORÁRIO:',
                     valor_honorarios_cliente)
resumo = st.text_area('RESUMO DO CASO:',
                     resumo_caso_cliente)
data_cadastro = st.write('DATA DE CADASTRO:',
                     data_cadastro_cliente)
    
atualizar_cadastro = st.button('ATUALIZAR')

if atualizar_cadastro:
    df_clientes.at[(Codigo_seleciondo, 'nome')] = nome
    df_clientes.at[(Codigo_seleciondo, 'contato')] = contato
    df_clientes.at[(Codigo_seleciondo, 'cpf')] = cpf
    df_clientes.at[(Codigo_seleciondo, 'senha_egov')] = senha
    df_clientes.at[(Codigo_seleciondo, 'tipo_acao')] = tipo_acao
    df_clientes.at[(Codigo_seleciondo, 'valor_honorarios')] = honorarios
    df_clientes.at[(Codigo_seleciondo, 'resumo_caso')] = resumo
    df_clientes.at[(Codigo_seleciondo, 'data_cadastro')] = data_cadastro_cliente
    df_clientes.to_csv('clientes.csv',decimal=',', sep=';')

#st.dataframe(df_clientes)
#st.dataframe(df_parcelas)

