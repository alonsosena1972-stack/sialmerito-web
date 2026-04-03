import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA (Pestaña del navegador)
st.set_page_config(page_title="SÍ AL MÉRITO - Oficial", layout="wide", page_icon="⚖️")

# 2. CONEXIÓN SEGURA A OPENAI Y VARIABLES DE CONTACTO
TEL_1 = "573146715497"
TEL_2 = "573004417737"
client = None

try:
    if "OPENAI_API_KEY" in st.secrets:
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    else:
        st.error("Error: No se encontró la llave API en los Secrets de Streamlit.")
except Exception as e:
    st.error(f"Error de conexión inicial: {e}")

# 3. MEMORIA DE LA SESIÓN
if 'lista_registros' not in st.session_state:
    st.session_state['lista_registros'] = []
if 'usuario_nombre' not in st.session_state:
    st.session_state['usuario_nombre'] = ""
if 'usuario_nivel' not in st.session_state:
    st.session_state['usuario_nivel'] = ""
if 'contador' not in st.session_state:
    st.session_state['contador'] = 0
if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# 4. PANEL DEL DIRECTOR (Barra Lateral - RECUPERADO)
with st.sidebar:
    st.image("logo.png", width=150) 
    st.markdown("### 🔐 Panel de Control")
    pass_admin = st.text_input("Contraseña Maestro:", type="password")
    
    if pass_admin == st.secrets.get("CLAVE_DIRECTOR", "CESAR2026"):
        st.success("Acceso Autorizado")
        if st.session_state['lista_registros']:
            st.write(f"Registros actuales: {len(st.session_state['lista_registros'])}")
            df = pd.DataFrame(st.session_state['lista_registros'])
            
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

# 5. ENCABEZADO PRINCIPAL (Tu Marca Original)
st.markdown("<h1 style='text-align: center; color: #1e7e34; font-family: sans-serif;'>Inicia tu camino al Éxito con SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.3em; color: #555;'>Asesoría Especializada en Concursos de Carrera Administrativa - CNSC</p>", unsafe_allow_html=True)

# 6. FORMULARIO DE REGISTRO (Mantiene tus 5 datos originales)
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
                st.session_state['lista_registros'].append({
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre": nombre, "Documento": cedula, "WhatsApp": whatsapp, "Email": correo, "Nivel": nivel_aspirado
                })
                st.session_state['usuario_nombre'] = nombre
                st.session_state['usuario_nivel'] = nivel_aspirado
                st.balloons()
                st.rerun()
            else:
                st.error("Socio, llena todos los campos para tu asesoría personalizada.")

st.write("---")

# 7. AGENTE ALONSO (Chat Inteligente con Cierre Estratégico)
if st.session_state['usuario_nombre']:
    nombre_corto = st.session_state['usuario_nombre'].split()[0]
    st.success(f"🏠 **Alonso:** ¡Hola, **{nombre_corto}**! Bienvenido/a a **SÍ AL MÉRITO**. Ya tengo tus datos registrados. ¿Qué duda legal o de carrera tienes hoy?")
    
    # Mostrar historial de chat
    for chat in st.session_state['historial']:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Entrada de chat
    prompt = st.chat_input("Escribe aquí tu duda sobre la CNSC, leyes o procesos...")

    if prompt:
        st.session_state['contador'] += 1
        st.session_state['historial'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # BLOQUEO ESTRATÉGICO A LA 6ta PREGUNTA (Cierre de ventas)
        if st.session_state['contador'] > 5:
            with st.chat_message("assistant"):
                msg_cierre = f"He resuelto varias de tus dudas y veo que te tomas muy en serio tu preparación para el nivel **{st.session_state['usuario_nivel']}**. Para asegurar tu plaza, te invito a hablar directamente con nuestro director **César Padilla**."
                st.markdown(msg_cierre)
                
                texto_wa = f"Hola César, soy {st.session_state['usuario_nombre']}. Hablé con Alonso sobre el nivel {st.session_state['usuario_nivel']} y quiero asegurar mi plaza."
                
                c1, c2 = st.columns(2)
                with c1: st.link_button("📲 Hablar con César (Línea 1)", f"https://wa.me/{TEL_1}?text={texto_wa}")
                with c2: st.link_button("📲 Hablar con César (Línea 2)", f"https://wa.me/{TEL_2}?text={texto_wa}")
            st.warning("Has alcanzado el límite de consultas gratuitas. ¡Es momento de asegurar tu éxito con el Director!")
        
        else:
            if client:
                with st.chat_message("assistant"):
                    with st.spinner("Alonso está consultando la normativa..."):
                        try:
                            respuesta = client.chat.completions.create(
                                model="gpt-4o",
                                messages=[
                                    {"role": "system", "content": "Eres Alonso, el asesor experto de 'SÍ AL MÉRITO'. Eres profesional, motivador y te basas en leyes como la 909 de 2004 y 1960 de 2019. Siempre despídete deseando éxito en el mérito."},
                                    *st.session_state['historial']
                                ]
                            )
                            res_text = respuesta.choices[0].message.content
                            st.write(res_text)
                            st.session_state['historial'].append({"role": "assistant", "content": res_text})
                        except Exception as e:
                            st.error(f"Problema de conexión: {e}")
            else:
                st.warning("API Key no configurada.")
else:
    st.info("🏠 **Alonso:** ¡Hola! Soy Alonso. Por favor, **regístrate arriba** para poder saludarte por tu nombre y asesorarte.")
