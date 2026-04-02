import streamlit as st
from openai import OpenAI
# --- CONFIGURACIÓN DE COLORES SÍ AL MÉRITO ---
st.markdown("""
    <style>
    /* Color del título principal */
    h1 {
        color: #2E8B57 !important; 
        font-weight: bold;
    }
    /* Color de los subtítulos */
    h3 {
        color: #2E8B57 !important;
    }
    /* Color del botón principal */
    .stButton>button {
        background-color: #2E8B57 !important;
        color: white !important;
        border-radius: 10px;
        border: none;
    }
    /* Color al pasar el mouse por el botón */
    .stButton>button:hover {
        background-color: #1e5d3a !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
# 1. Configuración de Marca
st.set_page_config(page_title="SÍ AL MÉRITO - Asesoría Virtual", page_icon="🏛️")

# Estilos personalizados (Verde Institucional)
st.markdown("""
    <style>
    .stApp { background-color: #f0f4f0; }
    .stButton>button { background-color: #1b5e20; color: white; width: 100%; border-radius: 20px; }
    h1, h2 { color: #1b5e20; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

if "registro_completado" not in st.session_state:
    st.session_state.registro_completado = False

# --- PANTALLA DE REGISTRO ---
if not st.session_state.registro_completado:
    st.title("🏛️ ¡Inicia tu camino al Mérito!")
    st.subheader("Regístrate para recibir asesoría personalizada")
    
    with st.form("registro_form"):
        nombre = st.text_input("Nombre Completo:")
        whatsapp = st.text_input("WhatsApp de contacto:")
        nivel = st.selectbox("Nivel de interés:", ["Selecciona...", "Asistencial", "Técnico", "Profesional"])
        submit = st.form_submit_button("HABLAR CON ASESOR EXPERTO")
        
        if submit:
            if nombre and whatsapp and nivel != "Selecciona...":
                st.session_state.nombre_usuario = nombre
                st.session_state.nivel_usuario = nivel
                st.session_state.registro_completado = True
                st.rerun()

# --- PANTALLA DEL CHAT ---
else:
    st.title("🏛️ Asesoría Virtual SÍ AL MÉRITO")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": f"Eres el asesor comercial de SÍ AL MÉRITO. El usuario es {st.session_state.nombre_usuario} de nivel {st.session_state.nivel_usuario}. Vende la asesoría de $120.000 COP y menciona los 20 años de experiencia de César Alonso Padilla."}
        ]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Escribe tu duda aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
            st.markdown(response.choices[0].message.content)
            st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
