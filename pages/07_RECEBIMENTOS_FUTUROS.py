from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime, date
import locale
from jinja2 import FileSystemLoader, Environment
from utilidades import leitura_dados, formatar_valor, logo
import os
import base64

logo()

leitura_dados()

data_atual = datetime.now().date()
hora_atual = datetime.now().strftime("%H:%M:%S")
pasta_assets = Path.cwd() / 'assets'

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']

data_atual = datetime.now().date()

st.write('DATA DE HOJE:', data_atual)

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

exportar = st.button('EXPORTAR RELATÓRIO')
df_recebiveis = df_recebimentos_futuros.groupby('nome').sum('VALOR DA PARCELA')
df_recebiveis = df_recebiveis.sort_values(by='VALOR DA PARCELA', ascending=False).reset_index()

st.write('#### VALORES AGRUPADOS POR CLIENTE')
st.dataframe(df_recebiveis)
st.write('VALORES DE CADA PARCELA/CLIENTE')
st.dataframe(df_recebimentos_futuros)

# EXPORTAÇÃO DE RELATÓRIOS PARA PDF


if exportar:
    recebiveis_html = df_recebiveis.to_html(float_format=formatar_valor)
    recebimentos_futuros_html = df_recebimentos_futuros.to_html(float_format=formatar_valor)
    html_recebimentos_futuros = recebiveis_html + "<br>" + recebimentos_futuros_html
    logotipo = Path(__file__).parents[1] / 'assets' / 'LOGO.png'
    
    with open(logotipo, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open('html_recebimentos_futuros', 'w') as arquivo:
        arquivo.write(html_recebimentos_futuros)

    arquivo_template = 'template.jinja'
    

    loader = FileSystemLoader(pasta_assets)
    environment = Environment(loader=loader)
    template = environment.get_template(arquivo_template)
    

    template_vars = {
        'stylesheet': '',
        'tipo_relatorio': 'RELATÓRIO DE RECEBIMENTOS FUTUROS',
        'valores_cliente': 'Valores a receber por cliente:',
        'valores_parcelas': 'Valores individualizados das parcelas',
        'dia':data_atual,
        'hora':hora_atual,
        'parcelas_vencidas': recebiveis_html,
        'devedores': recebimentos_futuros_html,
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
    with open('html_recebimentos_futuros', 'w', encoding='utf-8') as arquivo:
         arquivo.write(html)
    with open('html_recebimentos_futuros', 'r', encoding='utf-8') as arquivo:
            st.download_button('Baixar relatório', arquivo, file_name='relatorio.html', mime='text/html')     
