import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="SÍ AL MÉRITO | Consultoría Especializada", layout="centered", page_icon="⚖️")

# 2. ESTILOS CSS: AZUL VIVO, LETRAS BLANCAS Y CONTENEDORES CLAROS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0A2540 0%, #1A365D 100%); color: #FFFFFF; }
    .main-title { font-family: 'Inter', sans-serif; font-weight: 800; color: #FFFFFF; font-size: 2.5rem; text-align: center; }
    .subtitle { color: #38BDF8; text-align: center; margin-bottom: 25px; }
    
    /* Recuadros de formularios y chat */
    .stTextInput input, .stSelectbox select, .stTextArea textarea { 
        background-color: #1E3A8A !important; 
        color: #FFFFFF !important; 
        border: 2px solid #38BDF8 !important; 
        border-radius: 10px !important; 
    }
    .stChatInput textarea { background-color: #1E3A8A !important; color: #FFFFFF !important; }
    
    /* Botones */
    .stButton button { background: #00D4B2 !important; color: #000000 !important; font-weight: bold; border-radius: 8px; }
    
    .footer-institucional { background: #0F172A; border-top: 2px solid #38BDF8; padding: 20px; border-radius: 10px; text-align: center; margin-top: 40px; color: #FFFFFF; }
    </style>
""", unsafe_allow_html=True)

# 3. CONFIGURACIÓN Y RECURSOS
TEL_1, TEL_2, TEL_3 = "573146715497", "573153838792", "573004417737"
CORREO_EMPRESA = "si.al.merito2026@gmail.com"
ENLACE_JITSI = "https://meet.jit.si/SiAlMeritoSesionGarantizada2026Oficial"
ENLACE_WORDWALL = "https://wordwall.net/es/myactivities"
ENLACE_YOUTUBE = "https://www.youtube.com/@cesaralonsopadillaheredia2231"
ENLACE_FACEBOOK = "https://www.facebook.com/share/1EgsN9D31Z/"
ARCH_CSV = "base_aspirantes_si_al_merito.csv"

# 4. MEMORIA
if 'lista_registros' not in st.session_state: st.session_state['lista_registros'] = []
if os.path.exists(ARCH_CSV): st.session_state['lista_registros'] = pd.read_csv(ARCH_CSV).to_dict('records')

# 5. BARRA LATERAL (Panel de control con descarga de datos)
with st.sidebar:
    st.title("🔐 Panel Director")
    pass_admin = st.text_input("Contraseña:", type="password")
    if pass_admin == st.secrets.get("CLAVE_DIRECTOR", "CESAR2026"):
        st.success("Acceso Autorizado")
        if st.session_state['lista_registros']:
            df = pd.DataFrame(st.session_state['lista_registros'])
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer: df.to_excel(writer, index=False)
            st.download_button("📥 DESCARGAR EXCEL", output.getvalue(), "Aspirantes_SiAlMerito.xlsx", "application/vnd.ms-excel", use_container_width=True)
            st.write(f"Total registrados: {len(df)}")
    else: st.info("Solo acceso administrativo.")

# 6. INTERFAZ
st.markdown("<h1 class='main-title'>SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Tu éxito en los Concursos de Carrera Administrativa</p>", unsafe_allow_html=True)

if not st.session_state.get('usuario_nombre'):
    with st.form("registro"):
        nombre = st.text_input("Nombre y Apellido")
        col1, col2 = st.columns(2)
        whatsapp = col1.text_input("Celular (+57)")
        correo = col2.text_input("Correo")
        concurso = st.text_input("Concurso al que aspiras")
        nivel = st.selectbox("Nivel", ["Asistencial", "Técnico", "Profesional"])
        if st.form_submit_button("INGRESAR A LA ASESORÍA"):
            if nombre and whatsapp and correo:
                st.session_state.update({'usuario_nombre': nombre, 'usuario_nivel': nivel, 'usuario_concurso': concurso})
                pd.DataFrame(st.session_state['lista_registros'] + [{'Nombre': nombre, 'WhatsApp': whatsapp, 'Email': correo, 'Concurso': concurso, 'Nivel': nivel}]).to_csv(ARCH_CSV, index=False)
                st.rerun()
else:
    st.success(f"Hola {st.session_state['usuario_nombre']}, Alonso está listo para asesorarte.")
    if 'historial' not in st.session_state: st.session_state['historial'] = []
    for msg in st.session_state['historial']:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    prompt = st.chat_input("Escribe tu duda...")
    if prompt:
        st.session_state['historial'].append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": (
                    f"Eres Alonso de 'SÍ AL MÉRITO'. Tu asesoría es de alto nivel: utilizas la Taxonomía de Bloom para evaluar el conocimiento "
                    f"y diseñas simulacros de alta exigencia basados en una comprensión lectora crítica. "
                    f"Recuerda siempre: Capacitaciones Jitsi ({ENLACE_JITSI}) Jueves/Viernes. "
                    f"Asesoría Personalizada $120.000 incluye PDFs, videos OPEC y simulacros de 50 preguntas. "
                    f"Wordwall: {ENLACE_WORDWALL}. Facebook: {ENLACE_FACEBOOK}. "
                    f"Mantén tono profesional y académico."
                )}, *st.session_state['historial']]
            ).choices[0].message.content
            st.markdown(response)
            st.session_state['historial'].append({"role": "assistant", "content": response})

# 7. FOOTER
st.markdown(f"""
    <div class="footer-institucional">
        <p><b>SÍ AL MÉRITO — Talleres, Cursos y Asesorías Especializadas</b></p>
        <p>Somos un equipo encargado de visibilizar los Concursos de Carrera Administrativa.</p>
        <p>WhatsApp: 3146715497 - 3153838792 - 3004417737 | Correo: {CORREO_EMPRESA}</p>
    </div>
""", unsafe_allow_html=True)
