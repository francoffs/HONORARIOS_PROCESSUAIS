from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import timedelta, datetime

from utilidades import leitura_dados

# Chamada da função para carregar os dados
leitura_dados()

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']

Lista_Clientes = sorted(df_clientes['nome'].unique())

Nome_selecionado = st.selectbox('Selecione o cliente:', Lista_Clientes)

Lista_Codigo_Cliente = df_clientes.index[df_clientes['nome'] == Nome_selecionado].tolist()
Codigo_selecionado = st.selectbox('Selecione o Código do Cliente:', Lista_Codigo_Cliente)

tipo_acao_cliente = df_clientes.loc[Codigo_selecionado, 'tipo_acao']
valor_honorarios_cliente = df_clientes.loc[Codigo_selecionado, 'valor_honorarios']

st.write('TIPO DE AÇÃO:', tipo_acao_cliente)
st.write('VALOR DOS HONORÁRIOS: R$', valor_honorarios_cliente)

parcelas = st.number_input('Nº DE PARCELAS DESEJADO', min_value=1, step=1, format='%d')

# Calcular o valor de cada parcela
valor_da_parcela = float(valor_honorarios_cliente) / parcelas
st.write(f'Valor de cada parcela: R$ {valor_da_parcela:.2f}')

# Solicitar a data de vencimento da primeira parcela
primeira_parcela = st.date_input("Escolha a data de vencimento da primeira parcela:")
primeira_parcela = pd.to_datetime(primeira_parcela, format="%Y-%m-%d") 

# Função para adicionar meses a uma data e ajustar para o fim do mês anterior se a data não existir
def add_months(start_date, months):
    month = start_date.month - 1 + months
    year = start_date.year + month // 12
    month = month % 12 + 1
    day = start_date.day
    while True:
        try:
            new_date = datetime(year, month, day)
            break
        except ValueError:
            day -= 1
    return new_date

datas_todas_parcelas = [add_months(primeira_parcela, i).strftime("%d/%m/%Y") for i in range(parcelas)]
ultima_parcela = add_months(primeira_parcela, parcelas - 1)
st.write(f'O parcelemento foi ajustado em {parcelas} parcelas, começando em {primeira_parcela.strftime("%d/%m/%Y")} e terminado em {ultima_parcela.strftime("%d/%m/%Y")}. Clique no botão PARCELAR para salvar esse ajuste.')

novas_parcelas = {
    'DATA DE VENCIMENTO': datas_todas_parcelas,
    'NOME': [Nome_selecionado] * parcelas,
    'NUMERO DA PARCELA': range(1, parcelas + 1),
    'VALOR DA PARCELA': [valor_da_parcela] * parcelas,
    'CODIGO': [Codigo_selecionado] * parcelas
}
df2 = pd.DataFrame(novas_parcelas)

parcelar = st.button('PARCELAR')
if parcelar:
    # Adicionando as novas parcelas ao DataFrame existente
    st.session_state['dados']['df_parcelas'] = pd.concat([st.session_state['dados']['df_parcelas'], df2], ignore_index=True)
    
    # Salvando o DataFrame atualizado no arquivo CSV
    st.session_state['dados']['df_parcelas'].to_csv('parcelas.csv', decimal=',', sep=';', index=False)
    
    st.rerun()  # Reiniciar o script para recarregar os dados

df_parcelas = st.session_state['dados']['df_parcelas']

df_parcelas=df_parcelas[df_parcelas['CODIGO']==Codigo_selecionado]


st.dataframe(df2)
st.write(df_parcelas)
#st.write(df_parcelas['VALOR DA PARCELA'], df_parcelas['CODIGO'])

editar_parcelas = st.button('EDITAR PARCELAS')

Lista_Parcelas_Cliente = df_parcelas['NUMERO DA PARCELA'][df_parcelas['CODIGO']==Codigo_selecionado].tolist()
parcela_selecionada = st.selectbox('Selecione a parcela a ser editada:', Lista_Parcelas_Cliente)

#st.text_input('PARCELA A EDITAR', parcela_selecionada)
quitação = st.selectbox('CONFIRME O PAGAMENTO', ["pago", "em aberto"])
n_valor_parcela = st.text_input('ATUALIZE O VALOR DA PARCELA')
data_pagamento = st.date_input('INFORME A DATA DE PAGAMENTO')
forma_pagamento = st.selectbox('INFORME A FORMA DE PAGAMENTO', ['Dinheiro', 'PIX', 'Cartão de Crédito', 'Cartão de Débito', 'Cheque'])
conta_recebedora = st.text_input('INFORME A CONTA QUE RECEBEU O PAGAMENTO')

index_name = df_parcelas.index.name
st.write(index_name)

salvar = st.button('SALVAR')

if salvar:
    Index_parcela = st.session_state['dados']['df_parcelas'].loc[
    (st.session_state['dados']['df_parcelas']['CODIGO'] == Codigo_selecionado) & 
    (st.session_state['dados']['df_parcelas']['NUMERO DA PARCELA'] == parcela_selecionada)
].index
    if len(Index_parcela) > 0:
        Index_parcela = Index_parcela[0]           
        st.session_state['dados']['df_parcelas'].at[Index_parcela, 'PAGAMENTO'] = quitação
        st.session_state['dados']['df_parcelas'].to_csv('parcelas.csv', decimal=',', sep=';', index=False)
    else:
        print("Índice não encontrado. Verifique os valores de 'CODIGO' e 'NUMERO DA PARCELA'.")
            