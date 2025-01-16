import streamlit as st
from pathlib import Path

caminho_logo = Path(__file__).parent / 'assets'
logo = str(caminho_logo / 'LOGO.png')
st.image(logo,width=200)
st.sidebar.markdown('Escritório de Advocacia MARTINA MOHR - Direitos Reservados')

st.markdown('# REGISTROS DE HONORÁRIOS')
st.markdown('## Advogada MARTINA MOHR DA COSTA')


st.divider()

st.markdown(
    '''
    Aplicativo desenvolvido para cadastro e controle de honorários advocatícios.
    
    Acesse os menus na `barra lateral` para as funcionalidades específicas.
    '''
            )
