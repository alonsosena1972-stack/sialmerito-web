import streamlit as st
from openai import OpenAI

# 1. Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Registro Oficial", layout="wide")

# Conexión con la IA (Versión corregida 2026)
try:
    # Usamos la configuración de secrets para la API Key
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Error al conectar con la llave de IA. Revisa los Secrets.")

# 2. Barra Lateral (Diseño original solicitado)
with st.sidebar:
    st.markdown("### 🔐 Acceso Privado")
    clave = st.text_input("Clave de Administrador:", type="password")
    
    # Verificación con la clave de tus secrets
    if clave == st.secrets.get("CLAVE_DIRECTOR", "ADMIN2026"):
        st.success("Acceso Concedido")
        st.write("Registros actuales: 2")
        st.button("📥 Descargar Excel Profesional")
    else:
        st.info("Introduce tu clave de Director.")

# 3. Diseño Principal (Logo pequeño y títulos)
# Usamos columnas para centrar el logo y hacerlo más pequeño
col1, col2, col3 = st.columns([2, 1, 2]) 
with col2:
    st.image("logo.png", width=150) # Tamaño reducido a 150px para elegancia

st.markdown("<h1 style='text-align: center; color: #1e7e34;'>Inicia tu camino al éxito con SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Bienvenido, Cesar Alonso Padilla</h3>", unsafe_allow_html=True)

st.write("---")

# 4. Formulario de Diagnóstico (Fiel a tu imagen de éxito)
st.markdown("### 📋 Diagnóstico Inicial Gratuito")
st.write("Registra tus datos para recibir asesoría personalizada.")

with st.form("registro_alumnos"):
    nombre = st.text_input("Tu Nombre Completo:")
    whatsapp = st.text_input("Tu WhatsApp de contacto:")
    nivel = st.selectbox("¿A qué nivel aspiras?", ["Asistencial", "Técnico", "Profesional"])
    
    if st.form_submit_button("HABLAR CON ASESOR EXPERTO"):
        st.success(f"Registro exitoso. Alonso ya tiene tus datos, {nombre}.")

st.write("---")

# 5. Agente IA Alonso (Cuadro de dudas corregido)
st.warning("🏠 ¡Hola! En SÍ AL MÉRITO estamos enfocados en brindar asesoramiento y orientación sobre el mérito y el éxito profesional. ¡Estoy aquí para ayudarte!")

# Usamos st.chat_input para una experiencia más moderna y sin errores de conexión
pregunta = st.chat_input("Escribe tu duda aquí sobre los concursos de carrera...")

if pregunta:
    with st.spinner("Alonso está redactando tu respuesta..."):
        try:
            # Llamada corregida para evitar el "Connection error"
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres Alonso, el asesor experto de SÍ AL MÉRITO. Tu jefe es César Alonso Padilla. Respondes con autoridad legal, claridad y motivación sobre concursos de la CNSC en Colombia."},
                    {"role": "user", "content": pregunta}
                ]
            )
            respuesta = completion.choices[0].message.content
            st.chat_message("assistant").write(respuesta)
        except Exception as e:
            st.error(f"Lo siento César, Alonso tuvo un problema técnico: {e}")

st.caption("Versión Oficial 2026 - SÍ AL MÉRITO")
