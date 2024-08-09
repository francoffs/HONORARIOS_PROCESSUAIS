from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime, date

from utilidades import leitura_dados

leitura_dados()

df_clientes = st.session_state['dados']['df_clientes']
df_parcelas = st.session_state['dados']['df_parcelas']

st.markdown('### ATUALIZAÇÃO DAS PARCELAS')
st.markdown('''
            *Nesta tela você poderá atualizar a situação de cada parcela de  seus clientes. 
            Altere as informações dos campos correspondentes e, após, clique em SALVAR.*
             ''')
st.divider()


Lista_Clientes = sorted(df_clientes['nome'].unique())

Nome_selecionado = st.selectbox('PESQUISE PELO NOME DO CLIENTE:',
                              Lista_Clientes)

Lista_Codigo_Cliente = df_clientes.index[df_clientes['nome'] == Nome_selecionado].tolist()
Codigo_selecionado = st.selectbox('Selecione o Código do Cliente:',
                                 Lista_Codigo_Cliente)
valor_honorários = df_clientes.loc[Codigo_selecionado, 'valor_honorarios']
st.write('VALOR DOS HONORÁRIOS: R$', valor_honorários)

df_parcelas_cliente = df_parcelas[df_parcelas['CODIGO'] == Codigo_selecionado]
df_parcelas_cliente = df_parcelas_cliente.drop('CODIGO', axis=1)
#df_parcelas_cliente['DATA DE PAGAMENTO'] = pd.to_datetime(df_parcelas_cliente['DATA DE PAGAMENTO'], format='%d/%m/%Y')

soma_parcelas = df_parcelas_cliente['VALOR DA PARCELA'].sum()
st.write('VALOR DA SOMA DAS PARCELAS: R$', str(soma_parcelas))

if float(soma_parcelas) > float(valor_honorários):
    st.warning('O VALOR DA SOMA DAS PARCELAS EXCEDE O VALOR DOS HONORÁRIOS CONTRATADOS. POR FAVOR, CORRIJA!!!')
elif float(soma_parcelas) < float(valor_honorários) and float(soma_parcelas) > 0:
    st.warning('O VALOR DA SOMA DAS PARCELAS É INFERIOR AO VALOR DOS HONORÁRIOS CONTRATADOS. POR FAVOR, CORRIJA!!!')
elif float(soma_parcelas) == float(valor_honorários):
    st.warning('O VALOR DA SOMA DAS PARCELAS CORRESPONDE AO VALOR DOS HONORÁRIOS CONTRATADOS. TUDO CERTO!!!!')
elif float(soma_parcelas) < float(valor_honorários) and float(soma_parcelas) == 0:
    st.warning('ESTE CLIENTE NÃO POSSUI PARCELAMENTO REGISTRADO. CASO DESEJE PARCELAR OS HONORÁRIOS, ACESSE O BOTÃO **PARCELAR** NA GUIA LATERAL.')





st.divider()

if df_parcelas_cliente.empty:
    pass
else:
    parcela_selecao = df_parcelas_cliente.index.tolist()
#st.write(parcela_selecao)
    st.dataframe(df_parcelas_cliente)

    col1, col2 = st.columns(2)
    with col1:
        parcela_selecionada = st.selectbox('Selecione o ÍNDICE da parcela a ser editada', parcela_selecao)
        valor_parcela_selecionada = df_parcelas_cliente.loc[parcela_selecionada, 'VALOR DA PARCELA']
        valor_da_parcela_editar = st.number_input('VALOR DA PARCELA A SER EDITADA:', value=float(valor_parcela_selecionada), min_value=0.0)
        

    with col2:
        quitação = st.selectbox('QUITAÇÃO:', ['PAGO', 'EM ABERTO'])
        if quitação == 'PAGO':
            data_pagamento = st.date_input('DATA DO PAGAMENTO:', format= 'DD-MM-YYYY')
            conta_depositada = st.text_input('CONTA DEPOSITADA:')
            forma_pagamento = st.selectbox('FORMA DE PAGAMENTO:', ['PIX', 'DINHEIRO', 'DEPÓSITO BANCÁRIO', 'CARTÃO DE CRÉDITO', 'CARTÃO DE DÉBITO'])
        else:
            nova_data_vencimento = st.date_input('NOVA DATA DE VENCIMENTO')
        
    
    atualizar_parcela = st.button('SALVAR ATUALIZAÇÃO')

    if atualizar_parcela:
        df_parcelas.at[(parcela_selecionada, 'PAGAMENTO')] = quitação
        if quitação == 'PAGO':
            df_parcelas.at[(parcela_selecionada, 'DATA DE PAGAMENTO')] = data_pagamento
            df_parcelas.at[(parcela_selecionada, 'FORMA DE PAGAMENTO')] = forma_pagamento
            df_parcelas.at[(parcela_selecionada, 'CONTA DEPOSITADA')] = conta_depositada
        else:
            df_parcelas.at[(parcela_selecionada, 'DATA DE VENCIMENTO')] = nova_data_vencimento
            df_parcelas.at[(parcela_selecionada, 'DATA DE PAGAMENTO')] = None
            df_parcelas.at[(parcela_selecionada, 'FORMA DE PAGAMENTO')] = None
            df_parcelas.at[(parcela_selecionada, 'CONTA DEPOSITADA')] = None
        df_parcelas.at[(parcela_selecionada, 'VALOR DA PARCELA')] = valor_da_parcela_editar
        
        df_parcelas.to_csv('parcelas.csv',decimal=',', sep=';', index=False)
        st.rerun()

    st.divider()
    st.write('Use este botão apenas para inserir uma ou mais parcelas adicionais')

    col12, col22, col32 = st.columns(3)
    proxima_parcela = df_parcelas_cliente['NUMERO DA PARCELA'].max() + 1
    
    with col12:
        n_parcela = st.number_input('Nº DA PARCELA:', proxima_parcela)
    with col22:
        n_data_vcto = st.date_input('DATA DE VENCIMENTO:')
    with col32:
        n_valor_parcela = st.number_input('VALOR DA PARCELA')

    n_pagamento = 'EM ABERTO'
    n_data_pagamento = None
    n_forma_pagamento = None
    n_conta_depositada = None
    inserir_parcela = st.button('ADICIONAR UMA NOVA PARCELA')
    max_index = df_parcelas.index.max() + 1
    
    if inserir_parcela:
        lista_adicionar = [
            Codigo_selecionado,
            n_parcela,
            n_data_vcto,
            n_valor_parcela,
            n_pagamento,
            n_data_pagamento,
            n_forma_pagamento,
            n_conta_depositada
            ]
        df_parcelas_inserida = pd.DataFrame([lista_adicionar])
        st.dataframe(df_parcelas_inserida)
        lista_colunas = df_parcelas.columns.tolist()
        df_parcelas_inserida.columns = lista_colunas
        df_parcelas = pd.concat([df_parcelas, df_parcelas_inserida], ignore_index=True)
        st.session_state['dados']['df_parcelas'] = df_parcelas
        df_parcelas.to_csv('parcelas.csv', decimal=',', sep=';', index=False)
        st.rerun()
    







