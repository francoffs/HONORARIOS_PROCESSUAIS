from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime, date

from utilidades import leitura_dados

leitura_dados()

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']

data_atual = datetime.now().date()


st.write('DATA/HORA DE HOJE:', data_atual)

df_parcelas['DATA DE VENCIMENTO'] = pd.to_datetime(df_parcelas['DATA DE VENCIMENTO']).dt.date

df_parcelas_vencidas = df_parcelas[(df_parcelas['DATA DE VENCIMENTO']<=data_atual) & (df_parcelas['PAGAMENTO'] != 'PAGO')]
valores_pendentes = df_parcelas_vencidas['VALOR DA PARCELA'].sum()
parcelas_pendentes = df_parcelas_vencidas['VALOR DA PARCELA'].count()

st.write('Valor total das pendências: R$ ', str(valores_pendentes))
st.write('Quantidade de parcelas pendentes: ',str(parcelas_pendentes))

st.divider()
df_clientes = df_clientes.reset_index()
df_parcelas_vencidas = df_parcelas_vencidas.rename(columns={'CODIGO': 'codigo'})
df_parcelas_vencidas = df_parcelas_vencidas.reset_index()
df_parcelas_vencidas = pd.merge(left=df_parcelas_vencidas,
                                right=df_clientes[['codigo', 'nome']],
                                on='codigo',
                                how='left'
                                )
df_clientes = df_clientes.set_index('codigo')
df_parcelas_vencidas = df_parcelas_vencidas[['nome', 'DATA DE VENCIMENTO', 'VALOR DA PARCELA']]

df_devedores = df_parcelas_vencidas.groupby('nome').sum('VALOR DA PARCELA')
df_devedores = df_devedores.sort_values(by='VALOR DA PARCELA', ascending=False).reset_index()

st.write('#### VALORES AGRUPADOS POR CLIENTE')
st.dataframe(df_devedores)
st.write('VALORES DE CADA PARCELA/CLIENTE')
st.dataframe(df_parcelas_vencidas)


#df_produtos = df_produtos.rename(columns={'nome': 'produto'})
#df_vendas = df_vendas.reset_index()
#df_vendas = pd.merge(left=df_vendas,
#                     right=df_produtos[['produto', 'preco']],
#                     on='produto',  
#                     how='left')
#df_vendas = df_vendas.set_index('data')
#df_vendas['comissao'] = df_vendas['preco'] * COMISSAO