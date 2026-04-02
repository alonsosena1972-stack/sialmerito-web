import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO

# 1. Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Oficial", layout="wide")

# 2. Conexión Directa a OpenAI
client = None
try:
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    else:
        st.error("Falta la clave OPENAI_API_KEY en Secrets.")
except Exception as e:
    st.error(f"Error al conectar con la llave: {e}")

# 3. Almacenamiento de registros
if 'lista_registros' not in st.session_state:
    st.session_state['lista_registros'] = []

# 4. Barra Lateral
with st.sidebar:
    st.markdown("### 🔐 Panel Director")
    pass_admin = st.text_input("Contraseña:", type="password")
    
    if pass_admin == st.secrets.get("CLAVE_DIRECTOR", "ADMIN2026"):
        st.success("Acceso Maestro")
        if st.session_state['lista_registros']:
            df = pd.DataFrame(st.session_state['lista_registros'])
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            st.download_button("📥 Descargar Excel", data=output.getvalue(), file_name="registros.xlsx")
    else:
        st.info("Ingresa clave para descargar datos.")

# 5. Interfaz Visual
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.image("logo.png", width=120)

st.markdown("<h2 style='text-align: center; color: #1e7e34;'>SÍ AL MÉRITO: Tu Carrera Administrativa</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Bienvenido, Cesar Alonso Padilla</p>", unsafe_allow_html=True)

# 6. Registro de Aspirante
with st.expander("📝 REGISTRO DE ASPIRANTE", expanded=True):
    with st.form("reg_form"):
        nom = st.text_input("Nombre Completo:")
        wa = st.text_input("WhatsApp (+57):")
        niv = st.selectbox("Nivel:", ["Asistencial", "Técnico", "Profesional"])
        if st.form_submit_button("GUARDAR REGISTRO"):
            if nom and wa:
                st.session_state['lista_registros'].append({"Nombre": nom, "WhatsApp": wa, "Nivel": niv})
                st.success(f"¡Listo {nom}! Ya puedes consultar a Alonso.")

st.write("---")

# 7. AGENTE ALONSO
st.info("🏠 **Alonso:** Hola, soy tu asesor. ¿En qué puedo ayudarte?")

pregunta = st.chat_input("Escribe tu duda aquí...")

if pregunta:
    if client:
        with st.chat_message("user"):
            st.write(pregunta)
        
        with st.chat_message("assistant"):
            with st.spinner("Alonso está pensando..."):
                try:
                    chat_completion = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Eres Alonso, asesor de SÍ AL MÉRITO. Respondes con rigor legal sobre la CNSC en Colombia."},
                            {"role": "user", "content": pregunta}
                        ]
                    )
                    st.write(chat_completion.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error técnico real: {e}")
    else:
        st.error("La IA no está configurada en los Secrets.")
