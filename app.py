import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO CSS PARA MODO FIJO
st.set_page_config(
    page_title="SÍ AL MÉRITO | Tu Éxito en la CNSC", 
    layout="centered", 
    page_icon="🚀"
)

st.markdown("""
    <style>
    /* Forzar diseño profesional coherente en modo claro y oscuro */
    .stApp {
        background: linear-gradient(135deg, #0A2540 0%, #1A365D 50%, #0F172A 100%) !important;
        color: #F8FAFC !important;
    }
    
    /* Textos principales */
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #FFFFFF !important;
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
    
    /* Contenedor del formulario */
    .card-box {
        background: rgba(30, 41, 59, 0.95) !important;
        padding: 35px;
        border-radius: 16px;
        border: 1px solid #3B82F6 !important;
    }
    
    /* Ajuste de cajas de texto (Solución para visibilidad clara) */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 8px !important;
    }
    label {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
    }
    
    /* Botones */
    .stButton button {
        background: linear-gradient(135deg, #00D4B2 0%, #0284C7 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
    }
    
    .footer-institucional {
        background: rgba(15, 23, 42, 0.9);
        border-top: 2px solid #38BDF8;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 50px;
        color: #CBD5E1;
    }
    </style>
""", unsafe_allow_html=True)

# 2. ENLACES OFICIALES
TEL_1 = "573146715497"
TEL_3 = "573004417737"
CORREO_EMPRESA = "si.al.merito2026@gmail.com"
ENLACE_GRUPO = "https://chat.whatsapp.com/HSjyh6FKsHb6mTdIkhAeaU?s=sh&p=a&ilr=4"
ENLACE_FACEBOOK = "https://www.facebook.com/share/1EgsN9D31Z/"
ENLACE_WORDWALL = "https://wordwall.net/es/myactivities"
ENLACE_YOUTUBE = "https://www.youtube.com/@cesaralonsopadillaheredia2231"
ENLACE_JITSI = "https://meet.jit.si/SiAlMeritoSesionGarantizada2026Oficial"

ARCH_CSV = "base_aspirantes_si_al_merito.csv"

# Inicialización OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) if "OPENAI_API_KEY" in st.secrets else None

# 3. GESTIÓN DE ESTADOS
for key in ['usuario_nombre', 'usuario_nivel', 'usuario_concurso', 'contador', 'historial', 'bloqueado', 'lista_registros']:
    if key not in st.session_state:
        st.session_state[key] = [] if key == 'lista_registros' or key == 'historial' else ("" if key != 'contador' and key != 'bloqueado' else (0 if key == 'contador' else False))

if os.path.exists(ARCH_CSV):
    try:
        st.session_state['lista_registros'] = pd.read_csv(ARCH_CSV).to_dict('records')
    except: pass

# 4. PANEL EJECUTIVO
with st.sidebar:
    st.markdown("### 🔐 Panel Ejecutivo SÍ AL MÉRITO")
    pass_admin = st.text_input("Contraseña Maestro:", type="password")
    if pass_admin == st.secrets.get("CLAVE_DIRECTOR", "CESAR2026"):
        st.success("Acceso Autorizado")
        df = pd.DataFrame(st.session_state['lista_registros'])
        if not df.empty:
            st.write(f"Aspirantes: **{len(df)}**")
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer: df.to_excel(writer, index=False)
            st.download_button("📥 Descargar Base Completa", data=output.getvalue(), file_name="Aspirantes_SiAlMerito.xlsx")
        else: st.info("Sin registros.")

# 5. UI PRINCIPAL
st.markdown("<h1 class='main-title'>SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Tu éxito en la CNSC comienza aquí</p>", unsafe_allow_html=True)

if not st.session_state['usuario_nombre']:
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Activa tu Asesoría Experta con Alonso")
    with st.form("registro"):
        nombre = st.text_input("Nombres y Apellidos:")
        c1, c2 = st.columns(2)
        whatsapp = c1.text_input("WhatsApp (+57):")
        correo = c2.text_input("Correo:")
        concurso = st.text_input("Concurso o Entidad:")
        nivel = st.selectbox("Nivel:", ["Asistencial", "Técnico", "Profesional"])
        if st.form_submit_button("🚀 INICIAR CONSULTA"):
            if nombre and whatsapp and correo and concurso:
                st.session_state['lista_registros'].append({"Nombre": nombre, "WhatsApp": whatsapp, "Email": correo, "Concurso": concurso, "Nivel": nivel})
                pd.DataFrame(st.session_state['lista_registros']).to_csv(ARCH_CSV, index=False)
                st.session_state['usuario_nombre'] = nombre
                st.session_state['usuario_nivel'] = nivel
                st.session_state['usuario_concurso'] = concurso
                st.rerun()
            else: st.warning("Completa todos los campos.")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Lógica Chatbot (simplificada para legibilidad)
    st.success(f"🤖 **Alonso:** ¡Hola {st.session_state['usuario_nombre'].split()[0]}! Listo para nivel {st.session_state['usuario_nivel']}.")
    prompt = st.chat_input("Consulta aquí...")
    if prompt:
        st.session_state['historial'].append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            st.write("Procesando consulta técnica...") # Aquí iría la llamada a OpenAI
            # ... (código de respuesta igual al que tenías)

# 6. FOOTER
st.markdown(f"""
    <div class="footer-institucional">
        ⚖️ SÍ AL MÉRITO — Tu aliado en el mérito. <br>
        📱 WhatsApp: 3146715497 - 3153838792 - 3004417737
    </div>
""", unsafe_allow_html=True)
