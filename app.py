import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO DINÁMICO (AZUL INFLUYENTE & VIVO)
st.set_page_config(
    page_title="SÍ AL MÉRITO | Tu Éxito en la CNSC", 
    layout="centered", 
    page_icon="🚀"
)

# Estilos CSS modernos: Azul influyente (#0A2540, #00D4B2, #635BFF), vibrante, juvenil y altamente profesional
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0A2540 0%, #1A365D 50%, #0F172A 100%);
        color: #F8FAFC;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #FFFFFF;
        font-size: 2.6rem;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    .subtitle {
        font-family: 'Inter', sans-serif;
        color: #38BDF8;
        font-size: 1.15rem;
        text-align: center;
        margin-bottom: 35px;
        font-weight: 500;
    }
    .card-box {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        padding: 35px;
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .stTextInput input, .stSelectbox select {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #00D4B2 0%, #0284C7 100%);
        color: white;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# 2. CONEXIÓN SEGURA A OPENAI Y VARIABLES DE CONTACTO
TEL_1 = "573146715497"
TEL_2 = "573004417737"
ENLACE_GRUPO = "https://chat.whatsapp.com/HSjyh6FKsHb6mTdIkhAeaU?s=sh&p=a&ilr=4"
WEB_URL = "https://sialmerito-web-bdo27kw6gkkzbg8psnzqx.streamlit.app"
client = None

try:
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    else:
        st.error("Error: No se encontró la llave API en los Secrets de Streamlit.")
except Exception as e:
    st.error(f"Error de conexión inicial: {e}")

# 3. MEMORIA DE LA SESIÓN
if 'lista_registros' not in st.session_state:
    st.session_state['lista_registros'] = []
if 'usuario_nombre' not in st.session_state:
    st.session_state['usuario_nombre'] = ""
if 'usuario_nivel' not in st.session_state:
    st.session_state['usuario_nivel'] = ""
if 'usuario_concurso' not in st.session_state:
    st.session_state['usuario_concurso'] = ""
if 'contador' not in st.session_state:
    st.session_state['contador'] = 0
if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# 4. PANEL DEL DIRECTOR (Barra Lateral Ejecutiva)
with st.sidebar:
    st.markdown("### 🔐 Panel Ejecutivo SÍ AL MÉRITO")
    pass_admin = st.text_input("Contraseña Maestro:", type="password")
    
    if pass_admin == st.secrets.get("CLAVE_DIRECTOR", "CESAR2026"):
        st.success("Acceso Autorizado")
        if st.session_state['lista_registros']:
            st.write(f"Aspirantes registrados: {len(st.session_state['lista_registros'])}")
            df = pd.DataFrame(st.session_state['lista_registros'])
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Aspirantes')
            
            st.download_button(
                label="📥 Descargar Base de Datos (Excel)",
                data=output.getvalue(),
                file_name=f"Aspirantes_SiAlMerito_{datetime.now().strftime('%d_%m')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Aún no hay aspirantes registrados hoy.")
    else:
        st.info("Área exclusiva para la dirección.")

# 5. ENCABEZADO VIVO Y PROFESIONAL
st.markdown("<h1 class='main-title'>SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Estrategia e Inteligencia Artificial para Conquistar tu Empleo Público en la CNSC</p>", unsafe_allow_html=True)

# 6. FORMULARIO DE ACCESO FLUIDO
form_abierto = True if not st.session_state['usuario_nombre'] else False

if form_abierto:
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Activa tu Asesoría Experta con Alonso")
    st.markdown("Ingresa tus datos para conectar de inmediato con nuestro consultor inteligente especializado en normatividad y juicios situacionales.")
    
    with st.form("registro_vibrante"):
        nombre = st.text_input("Nombres y Apellidos:")
        
        col1, col2 = st.columns(2)
        with col1:
            whatsapp = st.text_input("Número de WhatsApp (+57):")
        with col2:
            correo = st.text_input("Correo Electrónico:")
            
        concurso = st.text_input("Concurso o Entidad a la que aspiras (Ej: DIAN, Territorial, etc.):")
        nivel_aspirado = st.selectbox("Nivel al que aspiras:", ["Asistencial", "Técnico", "Profesional"])
        
        submit = st.form_submit_button("🚀 INICIAR CONSULTA CON ALONSO", use_container_width=True)
        
        if submit:
            if nombre and whatsapp and correo and concurso:
                st.session_state['lista_registros'].append({
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre": nombre, "WhatsApp": whatsapp, "Email": correo, "Concurso": concurso, "Nivel": nivel_aspirado
                })
                st.session_state['usuario_nombre'] = nombre
                st.session_state['usuario_nivel'] = nivel_aspirado
                st.session_state['usuario_concurso'] = concurso
                st.rerun()
            else:
                st.warning("Socio, por favor completa todos los campos para continuar.")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")

# 7. AGENTE ALONSO (Cerebro Activo - Filtro de 4 Preguntas + Enlaces Directos)
if st.session_state['usuario_nombre']:
    nombre_corto = st.session_state['usuario_nombre'].split()[0]
    st.success(f"🤖 **Alonso (Asesor SÍ AL MÉRITO):** ¡Hola, **{nombre_corto}**! Qué gusto saludarte. Preparándonos con toda para el nivel **{st.session_state['usuario_nivel']}** en **{st.session_state['usuario_concurso']}**. ¿Cuál es tu primera duda técnica o jurídica sobre la CNSC?")
    
    # Mostrar historial de chat
    for chat in st.session_state['historial']:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Entrada de chat
    prompt = st.chat_input("Escribe tu consulta sobre la CNSC, Ley 909 o casos situacionales...")

    if prompt:
        st.session_state['contador'] += 1
        st.session_state['historial'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # CIERRE A LA CUARTA PREGUNTA (4 PREGUNTAS LÍMITE) CON FACILITACIÓN DE ENLACES
        if st.session_state['contador'] > 4:
            with st.chat_message("assistant"):
                msg_cierre = (
                    f"He respondido tus 4 consultas clave de preparación para el nivel **{st.session_state['usuario_nivel']}**. "
                    f"Para dar el siguiente paso y asegurar tu plaza con acompañamiento experto, te comparto el acceso directo a nuestra comunidad y a la plataforma:\n\n"
                    f"🔗 **Enlace de la Plataforma:** {WEB_URL}"
                )
                st.markdown(msg_cierre)
                
                texto_wa = f"Hola César, soy {st.session_state['usuario_nombre']}. Completé mis consultas con Alonso para el nivel {st.session_state['usuario_nivel']} ({st.session_state['usuario_concurso']}) y quiero asegurar mi plaza."
                
                st.link_button("👥 Unirme al Grupo Oficial de WhatsApp", ENLACE_GRUPO, use_container_width=True)
                c1, c2 = st.columns(2)
                with c1: st.link_button("📲 Hablar con César (Línea 1)", f"https://wa.me/{TEL_1}?text={texto_wa}", use_container_width=True)
                with c2: st.link_button("📲 Hablar con César (Línea 2)", f"https://wa.me/{TEL_2}?text={texto_wa}", use_container_width=True)
            st.warning("Has alcanzado el límite de 4 consultas rápidas. ¡Es momento de asegurar tu éxito directamente con la Dirección!")
        
        else:
            if client:
                with st.chat_message("assistant"):
                    with st.spinner("Alonso está procesando la normatividad..."):
                        try:
                            respuesta = client.chat.completions.create(
                                model="gpt-4o",
                                messages=[
                                    {
                                        "role": "system", 
                                        "content": (
                                            "Eres Alonso, el asesor experto de 'SÍ AL MÉRITO'. Tu propósito es asesorar rigurosamente sobre "
                                            "concursos de carrera administrativa de la CNSC, la Ley 909 de 2004, juicios situacionales, "
                                            "competencias funcionales y normativas del Estado colombiano (incluyendo criterios defensivos, "
                                            "enfoque sistémico y gestión MIPG).\n\n"
                                            "REGLA ESTRICTA DE FILTRADO:\n"
                                            "1. Si el usuario te envía saludos vacíos (como 'hola'), stickers, imágenes o "
                                            "cualquier mensaje ajeno a los concursos públicos, DEBES QUEDARTE COMPLETAMENTE CALLADO y no emitir respuesta.\n"
                                            "2. Mantén un tono profesional, motivador, con propiedad técnica y directo al grano."
                                        )
                                    },
                                    *st.session_state['historial']
                                ]
                            )
                            res_text = respuesta.choices[0].message.content
                            st.write(res_text)
                            st.session_state['historial'].append({"role": "assistant", "content": res_text})
                        except Exception as e:
                            st.error(f"Problema temporal de conexión: {e}")
            else:
                st.warning("API Key no configurada.")
else:
    st.info("👆 Por favor, completa el formulario superior para que Alonso conozca tu perfil y comience tu asesoría.")
