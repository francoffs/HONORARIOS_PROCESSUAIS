from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime, date
import locale
from jinja2 import FileSystemLoader, Environment
from utilidades import leitura_dados, formatar_valor, logo
import pdfkit
import pypdf
import os
import base64

logo()

leitura_dados()

data_atual = datetime.now().date()
hora_atual = datetime.now().strftime("%H:%M:%S")
pasta_assets = Path.cwd() / 'assets'

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']
exportar = st.button('EXPORTAR RELATÓRIO')
#df_parcelas['DATA DE PAGAMENTO'] = pd.to_datetime(df_parcelas['DATA DE PAGAMENTO'])

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

df_valores_pagos['MES'] = pd.to_datetime(df_valores_pagos['DATA DE PAGAMENTO']).dt.month
df_valores_pagos['ANO'] = pd.to_datetime(df_valores_pagos['DATA DE PAGAMENTO']).dt.year
df_valores_pagos['MES/ANO'] = df_valores_pagos['MES'].astype(str) + '/' + df_valores_pagos['ANO'].astype(str)
df_valores_pagos = df_valores_pagos[['nome', 'DATA DE PAGAMENTO', 'VALOR DA PARCELA', 'MES/ANO']]

mes_ano = df_valores_pagos['MES/ANO'].unique()
mes_ano = mes_ano.tolist()
mes_ano = st.selectbox('Selecione o período para filtrar:', mes_ano)
df_valor_pagos_filtrado = df_valores_pagos[df_valores_pagos['MES/ANO'] == mes_ano]
soma_filtrada = df_valor_pagos_filtrado['VALOR DA PARCELA'].sum()
valor_formatado = f"R$ {soma_filtrada:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
st.write(f'VALOR RECEBIDO EM {mes_ano}: R$', str(soma_filtrada))
st.dataframe(df_valor_pagos_filtrado)

# EXPORTAÇÃO DE RELATÓRIOS PARA PDF


if exportar:
    pagamentos_html = df_valor_pagos_filtrado.to_html(float_format=formatar_valor)
    logotipo = Path(__file__).parents[1] / 'assets' / 'LOGO.png'
    informacao = f'VALOR RECEBIDO EM {mes_ano}: R$ {soma_filtrada:.2f}'
    infrmacao = str(informacao)
    
    with open(logotipo, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open('pagamentos_html', 'w') as arquivo:
        arquivo.write(pagamentos_html)

    arquivo_template = 'template.jinja'
    

    loader = FileSystemLoader(pasta_assets)
    environment = Environment(loader=loader)
    template = environment.get_template(arquivo_template)
    

    template_vars = {
        'stylesheet': '',
        'tipo_relatorio': 'RELATÓRIO DE VALORES RECEBIDOS',
        'valores_cliente': informacao,
        'valores_parcelas': '',
        'dia':data_atual,
        'hora':hora_atual,
        'parcelas_vencidas': pagamentos_html,
        'devedores': '',
        'logo_url' : f"data:image/png;base64,{encoded_string}",
        
    }
    arquivo_css = 'style.css'
    template_css = environment.get_template(arquivo_css)
    css_renderizado = template_css.render(logo_url=logotipo)  # Passando a variável logo_url

    with open(pasta_assets / arquivo_css) as arquivo: 
        css = arquivo.read()

    template_vars['stylesheet'] = css
    html = template.render(**template_vars)

    html = template.render(**template_vars)
    with open('pagamentos_html', 'w', encoding='utf-8') as arquivo:
         arquivo.write(html)
    with open('pagamentos_html', 'r', encoding='utf-8') as arquivo:
            st.download_button('Baixar relatório', arquivo, file_name='relatorio.html', mime='text/html')