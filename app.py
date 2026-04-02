import streamlit as st
from openai import OpenAI

# 1. Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Registro Oficial", layout="wide")

# Conexión con la IA
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("Configura la llave de OpenAI en los Secrets.")

# 2. Barra Lateral (Estilo original)
with st.sidebar:
    st.markdown("### 🔐 Acceso Privado")
    clave = st.text_input("Clave de Administrador:", type="password")
    
    if clave == st.secrets.get("CLAVE_DIRECTOR", "ADMIN2026"):
        st.success("Acceso Concedido")
        st.write("Registros actuales: 2")
        st.button("📥 Descargar Excel Profesional")
    else:
        st.info("Introduce tu clave de Director.")

# 3. Diseño Principal (Fiel a tu imagen de éxito)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", use_container_width=True)
    st.markdown("<h1 style='text-align: center; color: #1e7e34;'>Inicia tu camino al éxito con SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Bienvenido, Cesar Alonso Padilla</h3>", unsafe_allow_html=True)

st.write("---")

# 4. Formulario de Diagnóstico Inicial (Lo que tenías funcionando)
st.markdown("### 📋 Diagnóstico Inicial Gratuito")
st.write("Registra tus datos para recibir asesoría personalizada sobre carrera administrativa en Colombia.")

with st.form("registro_form"):
    nombre = st.text_input("Tu Nombre Completo:", value="Cesar Alonso Padilla")
    whatsapp = st.text_input("Tu WhatsApp de contacto (con indicativo, ej: +57):", value="3146715497")
    nivel = st.selectbox("¿A qué nivel aspiras?", ["Asistencial", "Técnico", "Profesional"], index=2)
    
    submit = st.form_submit_button("HABLAR CON ASESOR EXPERTO")
    
    if submit:
        st.success(f"¡Gracias {nombre}! Alonso procesará tu perfil para el nivel {nivel}.")

st.write("---")

# 5. Agente IA Alonso (Caja de dudas inferior)
st.info("🏠 ¡Hola! En SÍ AL MÉRITO estamos enfocados en brindar asesoramiento y orientación sobre el mérito y el éxito profesional. ¡Estoy aquí para ayudarte!")

pregunta = st.text_input("Escribe tu duda aquí abajo:", placeholder="Ej: ¿Cómo me inscribo en el proceso de la Procuraduría?")

if pregunta:
    with st.spinner("Alonso está redactando tu respuesta..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres Alonso, el asesor experto de SÍ AL MÉRITO. Respondes a César Alonso Padilla con brevedad, tecnicismo legal y motivación."},
                    {"role": "user", "content": pregunta}
                ]
            )
            st.markdown("#### 📝 Respuesta de Alonso:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error de conexión con Alonso: {e}")

st.caption("Versión Oficial 2026 - SÍ AL MÉRITO")
