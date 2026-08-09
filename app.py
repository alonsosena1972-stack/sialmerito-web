import streamlit as str_app
from openai import OpenAI
import pandas as pd
from io import BytesIO
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO DINÁMICO
str_app.set_page_config(
    page_title="SÍ AL MÉRITO | Tu Éxito en la CNSC", 
    layout="centered", 
    page_icon="🚀"
)

# Estilos CSS con franja superior verde, sidebar azul cielo y diseño pro
str_app.markdown("""
    <style>
    .stApp {
        background: #0D1117 !important;
        color: #F0F6FC !important;
    }
    
    header[data-testid="stHeader"] {
        background-color: #238636 !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        background-color: #0D1117 !important;
    }
    
    /* Bloque superior en verde */
    div.block-container > div:first-child {
        background-color: #238636 !important;
        padding: 30px !important;
        border-radius: 12px !important;
        margin-bottom: 25px !important;
        border-bottom: 2px solid #161B22 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1E3A8A !important;
        border-right: 2px solid #38BDF8 !important;
    }
    
    [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #FFFFFF !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #F0F6FC !important;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #FFFFFF !important;
        font-size: 2.6rem;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    .subtitle {
        font-family: 'Inter', sans-serif;
        color: #E2E8F0 !important;
        font-size: 1.15rem;
        text-align: center;
        margin-bottom: 0px;
        font-weight: 500;
    }
    
    .card-box {
        background: #161B22 !important;
        backdrop-filter: blur(12px);
        padding: 35px;
        border-radius: 14px;
        border: 2px solid #38BDF8 !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.2);
    }
    
    .stChatMessage {
        background-color: #161B22 !important;
        border: 1px solid #00D4B2 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }

    /* Franja inferior del chat input de color verde */
    [data-testid="stChatInput"] {
        background-color: #238636 !important;
        padding: 10px !important;
        border-radius: 12px !important;
        border: 2px solid #00D4B2 !important;
    }
    [data-testid="stChatInput"] textarea {
        background-color: #0D1117 !important;
        color: #FFFFFF !important;
    }

    .footer-institucional {
        background: #161B22 !important;
        border-top: 3px solid #00D4B2;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 50px;
        font-family: 'Inter', sans-serif;
        box-shadow: 0 -5px 20px rgba(0, 212, 178, 0.15);
    }
    .footer-title {
        color: #00D4B2 !important;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 8px;
    }
    .footer-text {
        color: #C9D1D9 !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .footer-contacto {
        color: #00D4B2 !important;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 10px;
    }
    
    .texto-verde {
        color: #00D4B2 !important;
        font-weight: 700;
    }
    .texto-correo {
        color: #38BDF8 !important;
        text-decoration: underline;
    }
    .texto-whatsapp {
        color: #00D4B2 !important;
        font-weight: 700;
    }
    
    [data-testid="stSidebar"] label p {
        color: #38BDF8 !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] .stAlert {
        background-color: rgba(0, 212, 178, 0.15) !important;
        border: 1px solid #00D4B2 !important;
        color: #00D4B2 !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] .stAlert p {
        color: #00D4B2 !important;
        font-weight: 600 !important;
    }

    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #0D1117 !important;
        color: #FFFFFF !important;
        border: 1px solid #38BDF8 !important;
        border-radius: 6px !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #00D4B2 0%, #0284C7 100%) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.6rem 1.2rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(0, 212, 178, 0.3);
    }
    .stButton button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# 2. ENLACES OFICIALES Y RECURSOS
TEL_1 = "573146715497"
TEL_2 = "573153838792"
TEL_3 = "573004417737"
CORREO_EMPRESA = "si.al.merito2026@gmail.com"
ENLACE_GRUPO = "https://chat.whatsapp.com/HSjyh6FKsHb6mTdIkhAeaU?s=sh&p=a&ilr=4"
ENLACE_PROCURADURIA = "https://meritoconstruyendoexcelencia.com.co/#/"
ENLACE_CONTRALORIA = "https://concursocgr2024-2026.com.co/#/convocatorias/avisos-informativos"
ENLACE_JITSI = "https://meet.jit.si/SiAlMeritoSesionGarantizada2026Oficial"
ENLACE_FACEBOOK = "https://www.facebook.com/share/1EgsN9D31Z/"
ENLACE_WORDWALL = "https://wordwall.net/es/myactivities"
ENLACE_YOUTUBE = "https://www.youtube.com/@cesaralonsopadillaheredia2231"

ARCH_CSV = "base_aspirantes_si_al_merito.csv"
client = None

try:
    if "OPENAI_API_KEY" in str_app.secrets:
        client = OpenAI(api_key=str_app.secrets["OPENAI_API_KEY"])
except:
    pass

# 3. GESTIÓN DE MEMORIA
if 'usuario_nombre' not in str_app.session_state:
    str_app.session_state['usuario_nombre'] = ""
if 'lista_registros' not in str_app.session_state:
    str_app.session_state['lista_registros'] = []
if 'contador' not in str_app.session_state:
    str_app.session_state['contador'] = 0
if 'historial' not in str_app.session_state:
    str_app.session_state['historial'] = []
if 'bloqueado' not in str_app.session_state:
    str_app.session_state['bloqueado'] = False

# 4. PANEL DEL DIRECTOR
with str_app.sidebar:
    str_app.markdown("### 🔐 Panel Ejecutivo", unsafe_allow_html=True)
    pass_admin = str_app.text_input("Contraseña Maestro:", type="password")
    if pass_admin == str_app.secrets.get("CLAVE_DIRECTOR", "CESAR2026"):
        str_app.success("Acceso Autorizado")
        if str_app.session_state['lista_registros']:
            df = pd.DataFrame(str_app.session_state['lista_registros'])
            str_app.write(f"Total Aspirantes: **{len(df)}**")
            for idx, row in df.tail(5).iterrows():
                str_app.caption(f"📌 **{row.get('Nombre')}**")
    else:
        str_app.info("Área exclusiva para la dirección.")

# 5. ENCABEZADO
str_app.markdown("<h1 class='main-title'>SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
str_app.markdown("<p class='subtitle'>Talleres, Cursos y Asesorías Especializadas para Conquistar tu Empleo Público</p>", unsafe_allow_html=True)

# 6. FORMULARIO DE ACCESO
if not str_app.session_state['usuario_nombre']:
    str_app.markdown("<div class='card-box'>", unsafe_allow_html=True)
    str_app.markdown("### 🎯 Activa tu Asesoría Experta con AlonsoBot")
    with str_app.form("registro"):
        nombre = str_app.text_input("Nombres y Apellidos:")
        c1, c2 = str_app.columns(2)
        with c1: whatsapp = str_app.text_input("WhatsApp:")
        with c2: correo = str_app.text_input("Correo:")
        concurso = str_app.text_input("Concurso o Entidad:")
        nivel = str_app.selectbox("Nivel:", ["Asistencial", "Técnico", "Profesional"])
        if str_app.form_submit_button("🚀 INICIAR CONSULTA CON ALONSOBOT"):
            if nombre and whatsapp and correo and concurso:
                str_app.session_state['usuario_nombre'] = nombre
                str_app.session_state['usuario_nivel'] = nivel
                str_app.session_state['usuario_concurso'] = concurso
                str_app.rerun()
    str_app.markdown("</div>", unsafe_allow_html=True)

# 7. CHAT ALONSOBOT
if str_app.session_state['usuario_nombre']:
    nombre_corto = str_app.session_state['usuario_nombre'].split()[0]
    str_app.success(f"🤖 **Soy Alonsobot tu Asesor especializado de <span class='texto-verde'>SÍ AL MÉRITO</span>.** ¡Hola, **{nombre_corto}**! ¿Cuál es tu consulta?")
    
    for chat in str_app.session_state['historial']:
        with str_app.chat_message(chat["role"]):
            str_app.markdown(chat["content"])

    prompt = str_app.chat_input("Escribe tu consulta sobre la CNSC, OPEC, simulacros o capacitaciones...")

    if prompt:
        str_app.session_state['contador'] += 1
        str_app.session_state['historial'].append({"role": "user", "content": prompt})
        with str_app.chat_message("user"): str_app.write(prompt)

        if str_app.session_state['contador'] > 4:
            with str_app.chat_message("assistant"):
                str_app.markdown("¡Has completado tus consultas! Te invitamos a nuestros servicios profesionales: Actualización SIMO ($50k), Diagnóstico de Hoja de Vida, convenios SABERNET para antecedentes y Asesoría Personalizada de César Padilla ($120k).")
                str_app.link_button("📲 Hablar con César", f"https://wa.me/{TEL_1}")
        else:
            with str_app.chat_message("assistant"):
                respuesta = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{
                        "role": "system", 
                        "content": f"""Eres Alonsobot, asesor especializado de 'SÍ AL MÉRITO' dirigido por César Padilla. Equipo ganador de concursos (Unidad de Víctimas, MinTrabajo).
                        BASE LEGAL: Ley 909, Ley 1755, Ley 815.
                        ENLACES: Procuraduría: {ENLACE_PROCURADURIA}, Contraloría: {ENLACE_CONTRALORIA}.
                        SERVICIOS: Actualización SIMO ($50k), Diagnóstico de HV, Convenios SABERNET (ETDH/Lab/Académicos para antecedentes), Asesoría Personalizada ($120k).
                        SALUDO DE BIENVENIDA: "Bienvenido al chatbot de SI AL MÉRITO. Hoy hablaremos sobre los concursos regulados por la CNSC, Procuraduría General de la Nación, Fiscalía y Contralorías, y cómo realizar un proceso de inscripción exitoso en la plataforma SIMO. ¿Sabías que en SI AL MÉRITO ofrecemos un diagnóstico preliminar de tu hoja de vida para determinar si aplicas a una OPEC específica? Además, contamos con convenios interinstitucionales con SABERNET que te brindan ofertas especiales para realizar tus ETDH, laborales y académicos en diversas áreas temáticas. Participa en nuestros simulacros en línea para maximizar tus oportunidades. ¿Te gustaría saber más sobre alguno de estos servicios?"
                        Mantén tono profesional y persuasivo."""
                    }, *str_app.session_state['historial']]
                )
                res = respuesta.choices[0].message.content
                str_app.write(res)
                str_app.session_state['historial'].append({"role": "assistant", "content": res})

# 8. PIE DE PÁGINA
str_app.markdown(f"""
    <div class="footer-institucional">
        <div class="footer-title">⚖️ <span class='texto-verde'>SÍ AL MÉRITO</span> — Talleres, Cursos y Asesorías Especializadas</div>
        <div class="footer-text">Somos un equipo profesional ganador de concursos (Unidad de Víctimas, MinTrabajo). 24/7 para que logres tu empleo por mérito.</div>
        <div class="footer-contacto">📱 WhatsApp: 3146715497 - 3153838792 | ✉️ {CORREO_EMPRESA}</div>
    </div>
""", unsafe_allow_html=True)
