from pathlib import Path
import streamlit as st
import pandas as pd

from utilidades import leitura_dados, logo

logo()

leitura_dados()

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']

st.write('EXCLUSÃO DE PARCELAS')

Lista_Clientes = sorted(df_clientes['nome'].unique())

Nome_selecionado = st.selectbox('PESQUISE PELO NOME DO CLIENTE:',
                              Lista_Clientes)

Lista_Codigo_Cliente = df_clientes.index[df_clientes['nome'] == Nome_selecionado].tolist()
Codigo_selecionado = st.selectbox('Selecione o Código do Cliente:',
                                 Lista_Codigo_Cliente)


df_parcelas_cliente = df_parcelas[df_parcelas['CODIGO'] == Codigo_selecionado]
                              
df_parcelas_cliente = df_parcelas_cliente.drop('CODIGO', axis=1)
st.dataframe(df_parcelas_cliente)
st.divider()

parcela_selecao = df_parcelas_cliente.index.tolist()

parcela_selecionada_exc = st.selectbox('Selecione o ÍNDICE da parcela a ser EXCLUÍDA', parcela_selecao)
excluir_parcela = st.button('EXCLUIR PARCELA')

if excluir_parcela:
    df_parcelas = df_parcelas.drop(parcela_selecionada_exc)
    st.session_state['dados']['df_parcelas'] = df_parcelas
    df_parcelas.to_csv('parcelas.csv',decimal=',', sep=';', index=False)
    st.dataframe(df_parcelas_cliente)
    st.rerun()