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

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']

data_atual = datetime.now().date()
hora_atual = datetime.now().strftime("%H:%M:%S")
pasta_assets = Path.cwd() / 'assets'





st.write('DATA DE HOJE:', data_atual)

df_parcelas['DATA DE VENCIMENTO'] = pd.to_datetime(df_parcelas['DATA DE VENCIMENTO']).dt.date

df_parcelas_vencidas = df_parcelas[(df_parcelas['DATA DE VENCIMENTO']<=data_atual) & (df_parcelas['PAGAMENTO'] != 'PAGO')]
valores_pendentes = df_parcelas_vencidas['VALOR DA PARCELA'].sum()
parcelas_pendentes = df_parcelas_vencidas['VALOR DA PARCELA'].count()

st.write('Valor total das pendências: R$ ', str(valores_pendentes))
st.write('Quantidade de parcelas pendentes: ',str(parcelas_pendentes))
exportar = st.button('EXPORTAR RELATÓRIO')
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

# EXPORTAÇÃO DE RELATÓRIOS PARA PDF


if exportar:
    parcelas_vencidas_html = df_parcelas_vencidas.to_html(float_format=formatar_valor)
    devedores_html = df_devedores.to_html(float_format=formatar_valor)
    html_parcelas_vencidas = parcelas_vencidas_html + "<br>" + devedores_html
    logotipo = Path(__file__).parents[1] / 'assets' / 'LOGO.png'
    
    with open(logotipo, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    with open('html_parcelas_vencidas', 'w') as arquivo:
        arquivo.write(html_parcelas_vencidas)

    arquivo_template = 'template.jinja'
    

    loader = FileSystemLoader(pasta_assets)
    environment = Environment(loader=loader)
    template = environment.get_template(arquivo_template)
    

    template_vars = {
        'stylesheet': '',
        'tipo_relatorio': 'RELATÓRIO DE PARCELAS VENCIDAS',
        'valores_cliente': 'Total de parcelas vencidas por cliente:',
        'valores_parcelas': 'Valores de cada parcela vencida:',
        'dia':data_atual,
        'hora':hora_atual,
        'parcelas_vencidas': parcelas_vencidas_html,
        'devedores': devedores_html,
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
    with open('html_parcelas_vencidas', 'w', encoding='utf-8') as arquivo:
         arquivo.write(html)
    
    with open('html_parcelas_vencidas', 'r', encoding='utf-8') as arquivo:
            st.download_button('Baixar relatório', arquivo, file_name='relatorio.html', mime='text/html')
