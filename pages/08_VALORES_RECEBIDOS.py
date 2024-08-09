from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime

from utilidades import leitura_dados

leitura_dados()

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']

df_parcelas['DATA DE PAGAMENTO'] = pd.to_datetime(df_parcelas['DATA DE PAGAMENTO'])

df_clientes = df_clientes.reset_index()
df_valores_pagos = df_parcelas[df_parcelas['PAGAMENTO'] == 'PAGO']

df_valores_pagos = df_valores_pagos.rename(columns={'CODIGO': 'codigo'})

df_clientes = df_clientes.reset_index()

df_valores_pagos = pd.merge(left=df_valores_pagos,
                                right=df_clientes[['codigo', 'nome']],
                                on='codigo',
                                how='left'
                                )
df_clientes = df_clientes.set_index('codigo')

df_valores_pagos = df_valores_pagos[['nome', 'DATA DE PAGAMENTO', 'VALOR DA PARCELA']]

df_valores_pagos['MES'] = df_valores_pagos['DATA DE PAGAMENTO'].dt.month
df_valores_pagos['ANO'] = df_valores_pagos['DATA DE PAGAMENTO'].dt.year
df_valores_pagos['MES/ANO'] = df_valores_pagos['MES'].astype(str) + '/' + df_valores_pagos['ANO'].astype(str)
df_valores_pagos = df_valores_pagos[['nome', 'DATA DE PAGAMENTO', 'VALOR DA PARCELA', 'MES/ANO']]

mes_ano = df_valores_pagos['MES/ANO'].unique()
mes_ano = mes_ano.tolist()
mes_ano = st.selectbox('Selecione o período para filtrar:', mes_ano)
df_valor_pagos_filtrado = df_valores_pagos[df_valores_pagos['MES/ANO'] == mes_ano]
soma_filtrada = df_valor_pagos_filtrado['VALOR DA PARCELA'].sum()
st.write(f'VALOR RECEBIDO NO EM {mes_ano}: R$', str(soma_filtrada))
st.dataframe(df_valor_pagos_filtrado)


