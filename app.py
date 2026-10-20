import streamlit as st

from core.auth import exigir_login
from core.data import usa_credencial
from core.ui import ICONE, estilo

st.set_page_config(page_title="Plataforma Logística | Grupo CVF",
                   page_icon=str(ICONE) if ICONE.exists() else "🚢", layout="wide")
estilo()
exigir_login()

paginas = {
    "Acompanhamento": [
        st.Page("paginas/navios.py", title="Atracação de navios", icon=":material/anchor:", default=True),
        st.Page("paginas/booking.py", title="Aguardando booking", icon=":material/schedule:"),
    ],
    "Indicadores": [
        st.Page("paginas/indicadores.py", title="Dashboard de agentes", icon=":material/bar_chart:"),
        st.Page("paginas/frete.py", title="Consulta de frete", icon=":material/request_quote:"),
    ],
    "Ferramentas": [
        st.Page("paginas/calculadora.py", title="Calculadora logística", icon=":material/calculate:"),
    ],
}
nav = st.navigation(paginas)

with st.sidebar:
    st.divider()
    if st.button("↻ Atualizar dados", width="stretch", help="Os dados são relidos da planilha a cada 10 min."):
        st.cache_data.clear()
        st.rerun()
    if not usa_credencial():
        st.caption("Fonte: arquivos locais em data/ (modo desenvolvimento)")

nav.run()
