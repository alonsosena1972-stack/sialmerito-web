import streamlit as st
import pandas as pd
from openai import OpenAI

# 1. Configuración de la página (Limpia y profesional)
st.set_page_config(page_title="SÍ AL MÉRITO - Registro Oficial", layout="wide")

# Conexión con la IA
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 2. Barra Lateral (Acceso Privado y Registro)
with st.sidebar:
    st.markdown("### 🔐 Acceso Privado")
    clave = st.text_input("Clave de Administrador:", type="password")
    
    if clave == st.secrets["CLAVE_DIRECTOR"]:
        st.success("Acceso Concedido")
        st.write("Registros actuales: 2") # Simulación según tu imagen
        
        # Botón de descarga al estilo de tu foto
        st.button("📥 Descargar Excel Profesional")
    else:
        st.info("Introduce tu clave para gestionar los datos.")

# 3. Cuerpo Principal (Basado fielmente en tu imagen)
# Logotipo central
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.png", use_container_width=True)
    st.markdown("<h1 style='text-align: center; color: #1e7e34;'>Inicia tu camino al éxito con SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Bienvenido, Cesar Alonso Padilla</h3>", unsafe_allow_html=True)

st.write("---")

# Cuadros de información (Estilo alertas de tu foto)
st.error("📢 Dictan charlas en estas asesorías de este espacio")
st.warning("🏠 ¡Hola! En SÍ AL MÉRITO estamos enfocados en brindar asesoramiento y orientación sobre diversos temas relacionados con el mérito, el éxito profesional, la superación personal y el desarrollo de habilidades. Si estás interesado en alguna charla específica o en un tema en particular, no dudes en decirme y con gusto te proporcionaré la información y el apoyo que necesitas. ¡Estoy aquí para ayudarte!")

# 4. Agente IA "Alonso" integrado en la parte inferior
st.write("")
pregunta = st.text_input("Escribe tu duda...", placeholder="Escribe aquí tu pregunta para Alonso...")

if pregunta:
    with st.spinner("Consultando..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres Alonso, el asesor senior de SÍ AL MÉRITO. Tu objetivo es motivar y guiar a César y sus estudiantes en temas de carrera administrativa y superación personal."},
                    {"role": "user", "content": pregunta}
                ]
            )
            st.chat_message("assistant").write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Error técnico: {e}")
