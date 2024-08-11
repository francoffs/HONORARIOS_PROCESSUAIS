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
    html_conteudo = recebiveis_html + "<br>" + recebimentos_futuros_html

    arquivo_template = 'template.jinja'

    loader = FileSystemLoader(pasta_assets)
    environment = Environment(loader=loader)
    template = environment.get_template(arquivo_template)

    template_vars = {
        'stylesheet': '',
        'tipo_relatorio': 'RELATÓRIO DE RECEBIMENTOS FUTUROS',
        'valores_cliente': 'Valores a receber por cliente:',
        'valores_parcelas': 'Valores por parcela a receber:',
        'dia':data_atual,
        'hora':hora_atual,
        'parcelas_vencidas': recebiveis_html,
        'devedores': recebimentos_futuros_html,
    }
    arquivo_css = 'style.css'
    with open(pasta_assets / arquivo_css) as arquivo: 
        css = arquivo.read()

    template_vars['stylesheet'] = css
    html = template.render(**template_vars)


    pasta_output = Path('output')
    pasta_output.mkdir(exist_ok=True, parents=True)

    nome_relatorio = f'Relatório de recebimentos futuros.pdf'
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
