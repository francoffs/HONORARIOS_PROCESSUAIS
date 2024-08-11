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
    html_conteudo = parcelas_vencidas_html + "<br>" + devedores_html

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
    }
    arquivo_css = 'style.css'
    with open(pasta_assets / arquivo_css) as arquivo: 
        css = arquivo.read()

    template_vars['stylesheet'] = css
    html = template.render(**template_vars)


    pasta_output = Path('output')
    pasta_output.mkdir(exist_ok=True, parents=True)

    nome_relatorio = f'Relatório de parcelas vencidas.pdf'
    caminho_relatorio = pasta_output / nome_relatorio

    caminho_exec = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
    pdfkit_config = pdfkit.configuration(wkhtmltopdf=caminho_exec)
    pdfkit.from_string(html, output_path=str(caminho_relatorio), configuration=pdfkit_config)

    arquivo_layout = 'layout_relatorio.pdf'
    caminho_layout = pasta_assets / arquivo_layout

    layout_pdf = pypdf.PdfReader(caminho_layout).pages[0]
    pdf = pypdf.PdfWriter(clone_from=caminho_relatorio)
    pdf.pages[0].merge_page(layout_pdf, over=True)
    pdf.write(caminho_relatorio)
    os.startfile(caminho_relatorio)



