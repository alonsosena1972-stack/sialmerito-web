import streamlit as st
from openai import OpenAI
from PIL import Image
import pandas as pd
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Registro Oficial", page_icon="⚖️", layout="centered")

# Archivo donde se guardará la base de datos (Usamos punto y coma para que Excel lo abra en columnas)
# Archivo donde se guardará la base de datos (Usamos punto y coma para que Excel lo abra en columnas)
  # Archivo oficial de captación de clientes
DB_FILE = "base_datos_sialmerito_v1.csv"

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
    ahora = datetime.now()
    nueva_fila = {
        "Día": ahora.strftime("%d"),
        "Mes": ahora.strftime("%m"),
        "Año": ahora.strftime("%Y"),
        "Hora": ahora.strftime("%H:%M:%S"),
        "Nombres y Apellidos": nombre,
        "Documento de Identidad": documento,
        "Número Celular": celular,
        "Nivel de Interés": nivel
    }
    df_nuevo = pd.DataFrame([nueva_fila])
    
    # Guardamos con separador punto y coma (;) para que Excel en español lo abra directo en celdas
    if not os.path.isfile(DB_FILE):
        df_nuevo.to_csv(DB_FILE, index=False, encoding='utf-8-sig', sep=';')
    else:
        df_nuevo.to_csv(DB_FILE, mode='a', header=False, index=False, encoding='utf-8-sig', sep=';')

# --- LÓGICA DE NAVEGACIÓN ---
if 'registro_completado' not in st.session_state:
    st.session_state.registro_completado = False

if not st.session_state.registro_completado:
    st.markdown("### Registro de Aspirante Certificado")
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
                st.warning("⚠️ Todos los campos son obligatorios.")
else:
    # --- INTERFAZ DE CHAT ---
    st.markdown(f"### Bienvenido, {st.session_state.nombre_usuario}")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "Eres el experto de SÍ AL MÉRITO."}]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]): st.markdown(message["content"])

    if prompt := st.chat_input("Escribe tu duda..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
            res = response.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

  # --- PANEL DEL DIRECTOR FINAL (SÍ AL MÉRITO) ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔐 Acceso Privado")
    
    # El 'key' asegura que Streamlit no se confunda
    password = st.sidebar.text_input("Clave de Administrador:", type="password", key="admin_final")

    if password == "admin123": 
        st.sidebar.success("Acceso Concedido")
        if os.path.isfile(DB_FILE):
            try:
                # Leemos la base que ya vimos que funciona bien (con punto y coma)
                df_mostrar = pd.read_csv(DB_FILE, sep=';', on_bad_lines='skip')
                st.sidebar.write(f"Registros actuales: {len(df_mostrar)}")
                
                # Preparamos la descarga con el título que te gustó
                csv_data = "BASE DE DATOS PARA SERVICIOS DE ASESORIA PERSONALIZADA - SÍ AL MÉRITO\n"
                csv_data += df_mostrar.to_csv(index=False, sep=';', encoding='utf-8-sig')
                
                st.sidebar.download_button(
                    label="📥 Descargar Excel Profesional",
                    data=csv_data,
                    file_name="Base_Datos_SiAlMerito.csv",
                    mime="text/csv",
                )
            except:
                st.sidebar.error("Error al leer los datos. Registra un nuevo usuario.")
        else:
            st.sidebar.info("Aún no hay registros en esta base de datos.")
