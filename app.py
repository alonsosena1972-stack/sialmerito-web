import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE PÁGINA CON ESTILO FORZADO
st.set_page_config(
    page_title="SÍ AL MÉRITO | Tu Éxito en la CNSC", 
    layout="centered", 
    page_icon="🚀"
)

st.markdown("""
    <style>
    /* 1. Fondo de la aplicación forzado a azul oscuro */
    .stApp {
        background: linear-gradient(135deg, #0A2540 0%, #1A365D 50%, #0F172A 100%) !important;
    }
    
    /* 2. Textos generales forzados a blanco */
    h1, h2, h3, h4, p, div, label, span {
        color: #FFFFFF !important;
    }

    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        font-size: 2.6rem;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #38BDF8 !important;
        font-size: 1.15rem;
        text-align: center;
        margin-bottom: 35px;
    }
    
    /* 3. Cajas del formulario y entradas de texto con contraste total */
    .card-box {
        background: rgba(30, 41, 59, 0.8) !important;
        padding: 35px;
        border-radius: 16px;
        border: 1px solid #38BDF8 !important;
    }
    
    .stTextInput input, .stSelectbox select {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid #38BDF8 !important;
        border-radius: 8px !important;
    }
    
    /* 4. Botones */
    .stButton button {
        background: linear-gradient(135deg, #00D4B2 0%, #0284C7 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
    }

    /* 5. Pie de página */
    .footer-institucional {
        background: rgba(15, 23, 42, 0.9);
        border-top: 2px solid #38BDF8;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 50px;
        color: #CBD5E1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. ENLACES Y CONFIGURACIÓN (Mantenida exactamente igual)
TEL_1 = "573146715497"
TEL_2 = "573153838792"
TEL_3 = "573004417737"
CORREO_EMPRESA = "si.al.merito2026@gmail.com"
ENLACE_GRUPO = "https://chat.whatsapp.com/HSjyh6FKsHb6mTdIkhAeaU?s=sh&p=a&ilr=4"
ENLACE_FACEBOOK = "https://www.facebook.com/share/1EgsN9D31Z/"
ENLACE_WORDWALL = "https://wordwall.net/es/myactivities"
ENLACE_YOUTUBE = "https://www.youtube.com/@cesaralonsopadillaheredia2231"
ENLACE_JITSI = "https://meet.jit.si/SiAlMeritoSesionGarantizada2026Oficial"

ARCH_CSV = "base_aspirantes_si_al_merito.csv"
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) if "OPENAI_API_KEY" in st.secrets else None

# 3. GESTIÓN DE ESTADO (Inicialización)
if 'lista_registros' not in st.session_state: st.session_state['lista_registros'] = []
if 'historial' not in st.session_state: st.session_state['historial'] = []
if 'usuario_nombre' not in st.session_state: st.session_state['usuario_nombre'] = ""
if 'contador' not in st.session_state: st.session_state['contador'] = 0
if 'bloqueado' not in st.session_state: st.session_state['bloqueado'] = False

# 4. PANEL EJECUTIVO (Sidebar)
with st.sidebar:
    st.markdown("### 🔐 Panel Ejecutivo SÍ AL MÉRITO")
    pass_admin = st.text_input("Contraseña Maestro:", type="password")
    if pass_admin == st.secrets.get("CLAVE_DIRECTOR", "CESAR2026"):
        st.write(f"Total: **{len(st.session_state['lista_registros'])}**")
        if st.session_state['lista_registros']:
            df = pd.DataFrame(st.session_state['lista_registros'])
            output = BytesIO()
            df.to_excel(output, index=False)
            st.download_button("📥 Descargar Base", data=output.getvalue(), file_name="Aspirantes.xlsx")

# 5. UI PRINCIPAL
st.markdown("<h1 class='main-title'>SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Talleres, Cursos y Asesorías Especializadas</p>", unsafe_allow_html=True)

if not st.session_state['usuario_nombre']:
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    with st.form("registro"):
        nombre = st.text_input("Nombres y Apellidos:")
        c1, c2 = st.columns(2)
        whatsapp = c1.text_input("WhatsApp:")
        correo = c2.text_input("Correo:")
        concurso = st.text_input("Concurso/Entidad:")
        nivel = st.selectbox("Nivel:", ["Asistencial", "Técnico", "Profesional"])
        if st.form_submit_button("🚀 INICIAR CONSULTA"):
            if nombre and whatsapp and correo and concurso:
                st.session_state['usuario_nombre'] = nombre
                st.session_state['usuario_nivel'] = nivel
                st.session_state['usuario_concurso'] = concurso
                st.rerun()
            else: st.warning("Completa todos los campos.")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Lógica Chatbot (mantenida igual)
    st.success(f"🤖 **Alonso:** ¡Hola {st.session_state['usuario_nombre'].split()[0]}! Listo.")
    prompt = st.chat_input("Consulta aquí...")
    if prompt:
        # ... (aquí va tu lógica original de OpenAI, he omitido el bloque para brevedad pero mantenlo igual)
        pass

# 6. FOOTER
st.markdown(f"""
    <div class="footer-institucional">
        ⚖️ SÍ AL MÉRITO — Tu aliado en el mérito.<br>
        📱 WhatsApp: 3146715497 - 3153838792 - 3004417737
    </div>
""", unsafe_allow_html=True)
