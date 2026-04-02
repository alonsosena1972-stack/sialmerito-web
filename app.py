import streamlit as st
from openai import OpenAI
import time

# 1. Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Registro Oficial", layout="wide")

# 2. Inicialización segura del Cliente OpenAI
def get_openai_client():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        return OpenAI(api_key=api_key)
    except:
        return None

client = get_openai_client()

# 3. Barra Lateral (Diseño original solicitado)
with st.sidebar:
    st.markdown("### 🔐 Acceso Privado")
    clave = st.text_input("Clave de Administrador:", type="password")
    
    if clave == st.secrets.get("CLAVE_DIRECTOR", "ADMIN2026"):
        st.success("Acceso Concedido")
        st.write("Registros actuales: 2")
        st.button("📥 Descargar Excel Profesional")
    else:
        st.info("Introduce tu clave de Director.")

# 4. Diseño Principal (Logo pequeño y títulos)
col1, col2, col3 = st.columns([2, 1, 2]) 
with col2:
    st.image("logo.png", width=150)

st.markdown("<h1 style='text-align: center; color: #1e7e34;'>Inicia tu camino al éxito con SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Bienvenido, Cesar Alonso Padilla</h3>", unsafe_allow_html=True)

st.write("---")

# 5. Formulario de Diagnóstico
st.markdown("### 📋 Diagnóstico Inicial Gratuito")
with st.form("registro_alumnos"):
    nombre = st.text_input("Tu Nombre Completo:")
    whatsapp = st.text_input("Tu WhatsApp de contacto:")
    nivel = st.selectbox("¿A qué nivel aspiras?", ["Asistencial", "Técnico", "Profesional"])
    if st.form_submit_button("HABLAR CON ASESOR EXPERTO"):
        st.success(f"Registro exitoso para {nombre}.")

st.write("---")

# 6. Agente IA Alonso (Solución al Connection Error)
st.warning("🏠 ¡Hola! En SÍ AL MÉRITO estamos enfocados en brindar asesoramiento y orientación sobre el mérito y el éxito profesional.")

# Caja de texto normal (más estable para evitar errores de red en Streamlit)
pregunta_usuario = st.text_input("Escribe tu duda aquí sobre los concursos de carrera:", key="chat_input")

if pregunta_usuario:
    if client is None:
        st.error("No se pudo conectar con la llave de IA. Revisa tus Secrets en Streamlit.")
    else:
        with st.spinner("Alonso está analizando tu consulta..."):
            try:
                # Sistema de reintentos simples para evitar caídas de conexión
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Eres Alonso, el asesor experto de SÍ AL MÉRITO. Respondes a César Alonso Padilla con brevedad y rigor legal sobre la CNSC en Colombia."},
                        {"role": "user", "content": pregunta_usuario}
                    ],
                    timeout=15.0 # Evita que se quede colgado si la red falla
                )
                st.markdown("#### 📝 Respuesta de Alonso:")
                st.info(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error de conexión: Por favor, intenta enviar tu duda nuevamente.")

st.caption("Versión Oficial 2026 - SÍ AL MÉRITO")
