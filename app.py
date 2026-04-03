import streamlit as st
import openai

# --- 1. CONFIGURACIÓN Y DATOS DEL DIRECTOR ---
st.set_page_config(page_title="SÍ AL MÉRITO - Consultoría IA", page_icon="⚖️")
TEL_1 = "573146715497"
TEL_2 = "573004417737"

# --- 2. INICIALIZACIÓN DE MEMORIA ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "contador" not in st.session_state:
    st.session_state.contador = 0

# --- 3. TU FORMULARIO ACTUAL (Mantenemos tu estructura de éxito) ---
if "usuario_registrado" not in st.session_state:
    st.image("logo.png", width=150) # Asegúrate que el archivo se llame logo.png
    st.title("Inicia tu camino al Éxito con SÍ AL MÉRITO")
    
    with st.expander("📝 REGISTRO DE ASPIRANTE (Completa para iniciar)", expanded=True):
        with st.form("registro_form"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombres y Apellidos Completos:")
                cedula = st.text_input("Número de Documento (C.C.):")
            with col2:
                celular = st.text_input("Celular / WhatsApp (+57):")
                correo = st.text_input("Correo Electrónico:")
            
            nivel = st.selectbox("¿A qué nivel aspiras en el concurso?", ["Asistencial", "Técnico", "Profesional"])
            
            if st.form_submit_button("¡INICIAR MI CAMINO AL ÉXITO! 🚀"):
                if nombre and cedula and celular and correo:
                    st.session_state.usuario_nombre = nombre
                    st.session_state.usuario_nivel = nivel
                    st.session_state.usuario_registrado = True
                    st.rerun()
                else:
                    st.error("Socio, por favor completa todos los campos para continuar.")
    st.stop()

# --- 4. PANEL DE CONSULTORÍA ---
st.success(f"🤝 Hola, {st.session_state.usuario_nombre}. Ya tengo tus datos registrados. ¿Qué duda legal o de carrera tienes hoy?")

# Mostrar historial
for m in st.session_state.mensajes:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# --- 5. LÓGICA DE CIERRE ESTRATÉGICO ---
if prompt := st.chat_input("Escribe aquí tu duda sobre la CNSC, leyes o procesos..."):
    st.session_state.contador += 1
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # BLOQUEO DE VENTAS (A la 5ta pregunta)
    if st.session_state.contador > 5:
        with st.chat_message("assistant"):
            st.markdown(f"""
            **He resuelto varias de tus dudas y veo que te tomas muy en serio tu preparación para el nivel {st.session_state.usuario_nivel}.** Para profundizar en este tema y asegurar tu plaza en esta convocatoria, te invito a hablar directamente con nuestro director **César Padilla**.
            """)
            
            msg = f"Hola César, soy {st.session_state.usuario_nombre}. Consulté a la IA sobre el nivel {st.session_state.usuario_nivel} y quiero asegurar mi plaza."
            
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("📲 Hablar con César (Línea 1)", f"https://wa.me/{TEL_1}?text={msg}")
            with c2:
                st.link_button("📲 Hablar con César (Línea 2)", f"https://wa.me/{TEL_2}?text={msg}")
        st.stop()

    # RESPUESTA DE LA IA
    else:
        with st.chat_message("assistant"):
            # Aquí va el motor de OpenAI
            # RECUERDA: La API KEY debe estar en los "Secrets" de tu plataforma
            client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Eres el experto de SÍ AL MÉRITO en leyes colombianas y CNSC. Responde de forma técnica pero humana."},
                    *st.session_state.mensajes
                ]
            )
            res_text = response.choices[0].message.content
            st.markdown(res_text)
            st.session_state.mensajes.append({"role": "assistant", "content": res_text})
