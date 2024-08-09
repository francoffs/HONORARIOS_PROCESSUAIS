from pathlib import Path
import streamlit as st
import pandas as pd

from datetime import datetime


from utilidades import leitura_dados

leitura_dados()

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']

# Definilçaão dos índices das tabelas. Somente para acompanhar. 
# Apagar ao final

cliente_indez = df_clientes.index.name
st.write(cliente_indez)
parcelas_indez = df_parcelas.index.name
st.write(parcelas_indez)

# Seleção de clientes
Lista_Clientes = sorted(df_clientes['nome'].unique())
Nome_selecionado = st.selectbox('Selecione o cliente:', Lista_Clientes)

Lista_Codigo_Cliente = df_clientes.index[df_clientes['nome'] == Nome_selecionado].tolist()
Codigo_selecionado = st.selectbox('Selecione o Código do Cliente:',
                                 Lista_Codigo_Cliente)



tipo_acao_cliente = df_clientes.loc[Codigo_selecionado, 'tipo_acao']
valor_honorarios_cliente = df_clientes.loc[Codigo_selecionado, 'valor_honorarios']
st.write('VALOR DOS HONORÁRIOS CONTRATADOS: R$:', float(valor_honorarios_cliente))

st.divider()

col1, col2 = st.columns(2)
col1.text_input('TIPO DE AÇÃO:', tipo_acao_cliente)
valor_a_ser_parcelado = col2.number_input('VALOR A SER PARCELADO:')

parcelas = st.number_input('Nº DE PARCELAS DESEJADO', min_value=1, step=1, format='%d')
valor_da_parcela = valor_a_ser_parcelado / parcelas
#st.write(f'Valor de cada parcela: R$ {valor_da_parcela:.2f}')

primeira_parcela = st.date_input("Escolha a data de vencimento da primeira parcela:")

#primeira_parcela = primeira_parcela.date()
# Função para adicionar meses a uma data e ajustar para o fim do mês anterior se a data não existir
def add_months(start_date, months):
    month = start_date.month - 1 + months
    year = start_date.year + month // 12
    month = month % 12 + 1
    day = start_date.day
    while True:
        try:
            new_date = datetime(year, month, day).date()
            break
        except ValueError:
            day -= 1
    return new_date

datas_todas_parcelas = [add_months(primeira_parcela, i) for i in range(parcelas)]
ultima_parcela = add_months(primeira_parcela, parcelas - 1)
st.write(f'##### O parcelemento foi ajustado em {parcelas} parcelas, no valor de R$ {valor_da_parcela:.2f} cada parcela, começando em {primeira_parcela.strftime("%d/%m/%Y")} e terminado em {ultima_parcela.strftime("%d/%m/%Y")}. Clique no botão PARCELAR para salvar esse ajuste.')


#st.write(type(datas_todas_parcelas[0]))
quitacao_inicial = 'EM ABERTO'
data_pgto_inicial = ''
forma_pagamento_inicial = ''
conta_depositada_inicial = ''
adicionar_parcelas = st.button('Adicionar Parcelas')

if adicionar_parcelas:
    lista_adicionar = []
    for i in range(parcelas):
        sublista =[
            Codigo_selecionado,
            i + 1,
            datas_todas_parcelas[i],
            valor_da_parcela,
            quitacao_inicial,
            data_pgto_inicial,
            forma_pagamento_inicial,
            conta_depositada_inicial
            ]
        lista_adicionar.append(sublista)
    df_novas_parcelas = pd.DataFrame(lista_adicionar)
    lista_colunas = df_parcelas.columns.tolist()
    #st.write(lista_colunas)    
    df_novas_parcelas.columns = lista_colunas
    st.dataframe(df_novas_parcelas)
    st.dataframe(df_novas_parcelas)
            #st.write(sublista)
    df_parcelas = pd.concat([df_parcelas, df_novas_parcelas], axis=0, ignore_index=True)
    st.session_state['dados']['df_parcelas'] = df_parcelas
    df_parcelas.to_csv('parcelas.csv', decimal=',', sep=';', index=False)
        
        
#st.dataframe(df_parcelas)
#df_parcelas.to_csv('parcelas.csv', decimal=',', sep=';')        




#st.write(i_adicionar)
"""st.write(df_clientes)
st.write(df_parcelas)
"""
