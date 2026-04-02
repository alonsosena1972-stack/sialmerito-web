import streamlit as st
from openai import OpenAI
from PIL import Image
import pandas as pd
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Registro Oficial", page_icon="⚖️", layout="centered")

# Archivo donde se guardará la base de datos
DB_FILE = "usuarios_si_al_merito.csv"

# --- CONFIGURACIÓN DE COLORES Y ESTILOS ---
st.markdown("""
    <style>
    h1 { color: #2E8B57 !important; text-align: center; font-weight: bold; }
    h3 { color: #2E8B57 !important; text-align: center; }
    .stButton>button {
        background-color: #2E8B57 !important;
        color: white !important;
        border-radius: 12px;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARGAR LOGO ---
try:
    image = Image.open('logo.png')
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, use_column_width=True)
except:
    pass

st.markdown("# Inicia tu camino al éxito con SÍ AL MÉRITO")

# --- FUNCIONES DE BASE DE DATOS ---
def guardar_datos(nombre, documento, celular, nivel):
    nueva_fila = {
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nombre": nombre,
        "Documento": documento,
        "WhatsApp": celular,
        "Nivel": nivel
    }
    df_nuevo = pd.DataFrame([nueva_fila])
    
    if not os.path.isfile(DB_FILE):
        df_nuevo.to_csv(DB_FILE, index=False, encoding='utf-8')
    else:
        df_nuevo.to_csv(DB_FILE, mode='a', header=False, index=False, encoding='utf-8')

# --- LÓGICA DE NAVEGACIÓN ---
if 'registro_completado' not in st.session_state:
    st.session_state.registro_completado = False

if not st.session_state.registro_completado:
    st.markdown("### Registro de Aspirante Certificado")
    st.info("Por favor, ingresa tus datos reales para recibir orientación precisa sobre los concursos de méritos.")
    
    with st.form("registro_profesional"):
        nombre = st.text_input("Nombres y Apellidos Completos:")
        documento = st.text_input("Documento de Identidad (C.C):")
        celular = st.text_input("Número de Celular / WhatsApp:")
        nivel = st.selectbox("Nivel de Interés:", ["Asistencial", "Técnico", "Profesional"])
        
        btn_registro = st.form_submit_button("REGISTRARME Y EMPEZAR CONSULTA")
        
        if btn_registro:
            if nombre and documento and celular:
                guardar_datos(nombre, documento, celular, nivel)
                st.session_state.nombre_usuario = nombre
                st.session_state.nivel_usuario = nivel
                st.session_state.registro_completado = True
                st.rerun()
            else:
                st.warning("⚠️ Todos los campos son obligatorios para validar tu identidad.")

else:
    # --- INTERFAZ DE CHAT ---
    st.markdown(f"### Bienvenido, {st.session_state.nombre_usuario}")
    st.write(f"Asesoría activa para Nivel: **{st.session_state.nivel_usuario}**")

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": f"Eres el consultor experto de SÍ AL MÉRITO. Atiendes a {st.session_state.nombre_usuario}. Tu especialidad son los concursos de la CNSC y la Procuraduría. Ofrece asesoría personalizada por $120.000 COP."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Escribe tu duda legal o técnica..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages
            )
            full_res = response.choices[0].message.content
            st.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})

    # --- ZONA DEL DIRECTOR (Solo César) ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Panel del Director")
    if st.sidebar.checkbox("Ver Base de Datos"):
        if os.path.isfile(DB_FILE):
            df_mostrar = pd.read_csv(DB_FILE)
            st.sidebar.write(f"Total registros: {len(df_mostrar)}")
            
            # Botón para descargar el Excel
            csv = df_mostrar.to_csv(index=False).encode('utf-8')
            st.sidebar.download_button(
                label="📥 Descargar Base de Datos",
                data=csv,
                file_name=f"Base_Datos_SiAlMerito_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
            )
        else:
            st.sidebar.write("Aún no hay registros.")
