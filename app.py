import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO

# 1. Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Plataforma Oficial", layout="wide")

# 2. Inicialización de la IA
def inicializar_alonso():
    try:
        return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    except:
        return None

client = inicializar_alonso()

# 3. Datos para el Excel
datos_alumnos = pd.DataFrame([
    {"Nombre": "Cesar Alonso Padilla", "WhatsApp": "3146715497", "Nivel": "Profesional"}
])

# 4. Barra Lateral (Acceso y Descarga)
with st.sidebar:
    st.markdown("### 🔐 Acceso Privado")
    clave = st.text_input("Clave de Administrador:", type="password")
    
    if clave == st.secrets.get("CLAVE_DIRECTOR", "ADMIN2026"):
        st.success("Acceso Concedido")
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            datos_alumnos.to_excel(writer, index=False, sheet_name='Registros')
        
        st.download_button(
            label="📥 Descargar Excel Profesional",
            data=output.getvalue(),
            file_name="Registros_SiAlMerito.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Introduce tu clave de Director.")

# 5. Diseño Principal (Logo pequeño y títulos)
col1, col2, col3 = st.columns([2, 1, 2]) 
with col2:
    st.image("logo.png", width=150)

st.markdown("<h1 style='text-align: center; color: #1e7e34;'>Inicia tu camino al éxito con SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Bienvenido, Cesar Alonso Padilla</h3>", unsafe_allow_html=True)

st.write("---")

# 6. Agente IA Alonso
st.warning("🏠 ¡Hola! Soy Alonso. Estoy aquí para guiarte en el mérito y el éxito profesional.")

duda = st.text_input("Escribe aquí tu duda para Alonso:", key="input_alonso")

if duda:
    if client:
        with st.spinner("Alonso está analizando..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Eres Alonso, el asesor experto de SÍ AL MÉRITO. Tu jefe es César Alonso Padilla. Respondes con rigor legal sobre la CNSC en Colombia."},
                        {"role": "user", "content": duda}
                    ]
                )
                st.info(response.choices[0].message.content)
            except:
                st.error("Error de conexión. Intenta de nuevo en un momento.")
    else:
        st.error("Configura la llave de OpenAI en los Secrets.")

st.caption("Versión Oficial 2026 - SÍ AL MÉRITO")
