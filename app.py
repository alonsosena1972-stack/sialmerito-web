import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA (Pestaña del navegador)
st.set_page_config(page_title="SÍ AL MÉRITO - Oficial", layout="wide", page_icon="⚖️")

# 2. CONEXIÓN SEGURA A OPENAI
client = None
try:
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    else:
        st.error("Error: No se encontró la llave API en los Secrets de Streamlit.")
except Exception as e:
    st.error(f"Error de conexión inicial: {e}")

# 3. MEMORIA DE LA SESIÓN (Para registros y nombre de usuario)
if 'lista_registros' not in st.session_state:
    st.session_state['lista_registros'] = []
if 'usuario_nombre' not in st.session_state:
    st.session_state['usuario_nombre'] = ""

# 4. PANEL DEL DIRECTOR (Barra Lateral)
with st.sidebar:
    st.image("logo.png", width=150) # Asegúrate de tener logo.png en GitHub
    st.markdown("### 🔐 Panel de Control")
    pass_admin = st.text_input("Contraseña Maestro:", type="password")
    
    # Usamos la clave que configuramos en los Secrets
    if pass_admin == st.secrets.get("CLAVE_DIRECTOR", "CESAR2026"):
        st.success("Acceso Autorizado")
        if st.session_state['lista_registros']:
            st.write(f"Registros actuales: {len(st.session_state['lista_registros'])}")
            df = pd.DataFrame(st.session_state['lista_registros'])
            
            # Generador de Excel en memoria
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
            st.info("Aún no hay aspirantes registrados.")
    else:
        st.info("Ingrese la clave para gestionar datos.")

# 5. ENCABEZADO PRINCIPAL (Tu Marca Personal)
st.markdown("<h1 style='text-align: center; color: #1e7e34; font-family: sans-serif;'>Inicia tu camino al Éxito con SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.3em; color: #555;'>Asesoría Especializada en Concursos de Carrera Administrativa - CNSC</p>", unsafe_allow_html=True)

# 6. FORMULARIO DE REGISTRO PERSONALIZADO (5 DATOS)
# El formulario se cierra solo una vez que el usuario se registra (expanded=False)
form_abierto = True if not st.session_state['usuario_nombre'] else False

with st.expander("📝 REGISTRO DE ASPIRANTE (Completa para iniciar)", expanded=form_abierto):
    with st.form("registro_detallado"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombres y Apellidos Completos:")
            cedula = st.text_input("Número de Documento (C.C.):")
        with col2:
            whatsapp = st.text_input("Celular / WhatsApp (+57):")
            correo = st.text_input("Correo Electrónico:")
            
        nivel_aspirado = st.selectbox("¿A qué nivel aspiras en el concurso?", ["Asistencial", "Técnico", "Profesional"])
        
        submit = st.form_submit_button("¡INICIAR MI CAMINO AL ÉXITO! 🚀")
        
        if submit:
            if nombre and cedula and whatsapp and correo:
                # Guardamos en la lista de registros
                st.session_state['lista_registros'].append({
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre": nombre,
                    "Documento": cedula,
                    "WhatsApp": whatsapp,
                    "Email": correo,
                    "Nivel": nivel_aspirado
                })
                # Guardamos el nombre para el saludo de Alonso
                st.session_state['usuario_nombre'] = nombre
                st.balloons()
                st.rerun() # Reinicia para aplicar el saludo y cerrar el expander
            else:
                st.error("Por favor, llena todos los campos para poder brindarte una asesoría personalizada.")

st.write("---")

# 7. AGENTE ALONSO (Chat Inteligente)
if st.session_state['usuario_nombre']:
    nombre_corto = st.session_state['usuario_nombre'].split()[0] # Toma el primer nombre
    st.success(f"🏠 **Alonso:** ¡Hola, **{nombre_corto}**! Bienvenido/a a **SÍ AL MÉRITO**. Ya tengo tus datos registrados. ¿Qué duda legal o de carrera tienes hoy?")
else:
    st.info("🏠 **Alonso:** ¡Hola! Soy Alonso. Por favor, **regístrate arriba** con tus datos para poder darte una asesoría personalizada y saludarte por tu nombre.")

# Entrada de chat
prompt = st.chat_input("Escribe aquí tu duda sobre la CNSC, leyes o procesos...")

if prompt:
    if client:
        # Mostramos la pregunta del usuario
        with st.chat_message("user"):
            st.write(prompt)
        
        # Respuesta de Alonso
        with st.chat_message("assistant"):
            with st.spinner("Alonso está consultando la normativa..."):
                try:
                    respuesta = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "Eres Alonso, el asesor experto de la empresa 'SÍ AL MÉRITO'. Tu objetivo es ayudar a aspirantes a ganar concursos de la CNSC en Colombia. Eres profesional, motivador y te basas siempre en leyes como la 909 de 2004, 1960 de 2019 y acuerdos de convocatoria. Siempre despídete deseando éxito en el mérito."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    st.write(respuesta.choices[0].message.content)
                except Exception as e:
                    st.error(f"Lo siento, tuve un pequeño problema de conexión. Error: {e}")
    else:
        st.warning("Alonso no puede responder porque la API Key no está configurada correctamente en los Secrets.")
