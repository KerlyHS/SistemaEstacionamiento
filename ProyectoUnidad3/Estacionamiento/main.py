import time
import sys
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from components.dashboard import render as render_dashboard
from Api_rest.api import obtener_estado_estacionamiento

st.set_page_config(
    page_title="Dashboard - Estacionamiento",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu{visibility:hidden}
footer{visibility:hidden}
header{visibility:hidden}
.stApp{background:#F5F6F8}
.block-container{max-width:100%!important;padding:0!important;max-width:100%!important}
</style>
""", unsafe_allow_html=True)

placeholder = st.empty()

while True:
    conectado, plazas = obtener_estado_estacionamiento()

    plaza1 = None
    plaza2 = None
    libres = 0
    ocupadas = 0

    if plazas:
        ocupadas = sum(1 for p in plazas if p.get("estado") == "ocupado")
        libres = sum(1 for p in plazas if p.get("estado") != "ocupado")
        if len(plazas) > 0:
            plaza1 = "OCUPADA" if plazas[0].get("estado") == "ocupado" else "LIBRE"
        if len(plazas) > 1:
            plaza2 = "OCUPADA" if plazas[1].get("estado") == "ocupado" else "LIBRE"

    hora = time.strftime("%H:%M:%S")

    with placeholder.container():
        render_dashboard(
            plaza1=plaza1,
            plaza2=plaza2,
            libres=libres,
            ocupadas=ocupadas,
            conectado=conectado,
            hora=hora,
        )

    time.sleep(2)
