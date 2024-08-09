from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime

from utilidades import leitura_dados

leitura_dados()

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']

data_atual = datetime.now()

st.write('DATA/HORA DE HOJE:', data_atual)

#df_parcelas['DATA DE VENCIMENTO'] = pd.to_datetime(df_parcelas['DATA DE VENCIMENTO'])

df_recebimentos_futuros = df_parcelas.loc[df_parcelas['PAGAMENTO'] != 'PAGO']

df_clientes = df_clientes.reset_index()
df_recebimentos_futuros = df_recebimentos_futuros.rename(columns={'CODIGO': 'codigo'})
df_recebimentos_futuros = df_recebimentos_futuros.reset_index()
df_recebimentos_futuros = pd.merge(left=df_recebimentos_futuros,
                                right=df_clientes[['codigo', 'nome']],
                                on='codigo',
                                how='left'
                                )
df_clientes = df_clientes.set_index('codigo')
df_recebimentos_futuros = df_recebimentos_futuros[['nome', 'DATA DE VENCIMENTO', 'VALOR DA PARCELA']]

valores_a_receber = df_recebimentos_futuros['VALOR DA PARCELA'].sum()
valores_pendentes = df_recebimentos_futuros['VALOR DA PARCELA'].count()

st.write('Valor total a receber em data futura: R$ ', str(valores_a_receber))
st.write('Quantidade de parcelas a receber: ',str(valores_pendentes))

df_recebiveis = df_recebimentos_futuros.groupby('nome').sum('VALOR DA PARCELA')
df_recebiveis = df_recebiveis.sort_values(by='VALOR DA PARCELA', ascending=False).reset_index()

st.write('#### VALORES AGRUPADOS POR CLIENTE')
st.dataframe(df_recebiveis)
st.write('VALORES DE CADA PARCELA/CLIENTE')
st.dataframe(df_recebimentos_futuros)