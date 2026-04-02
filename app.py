import streamlit as st
from openai import OpenAI
from PIL import Image

# Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Asesoría Virtual", page_icon="⚖️", layout="centered")

# --- CONFIGURACIÓN DE COLORES Y ESTILOS "SÍ AL MÉRITO" ---
st.markdown("""
    <style>
    /* Fondo de la página */
    .main {
        background-color: #fcfcfc;
    }
    /* Color VERDE para el título principal (H1) */
    h1 {
        color: #2E8B57 !important; /* Verde esmeralda profesional */
        font-weight: bold;
        text-align: center;
        margin-top: -20px;
    }
    /* Color VERDE para subtítulos (H3) */
    h3 {
        color: #2E8B57 !important;
        text-align: center;
    }
    /* Estilo del botón principal (VERDE) */
    .stButton>button {
        background-color: #2E8B57 !important;
        color: white !important;
        border-radius: 12px;
        border: none;
        width: 100%;
        font-weight: bold;
        font-size: 18px;
        padding: 10px;
    }
    /* Efecto al pasar el mouse por el botón */
    .stButton>button:hover {
        background-color: #1e5d3a !important;
        color: white !important;
    }
    /* Ocultar menú de Streamlit para más profesionalismo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- MOSTRAR EL LOGO Y EL TÍTULO ---
# Intentamos cargar el logo (asegúrate de haber subido 'logo.png')
try:
    image = Image.open('logo.png')
    # Creamos columnas para centrar el logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, use_column_width=True)
except FileNotFoundError:
    # Si no encuentra el logo, no muestra nada (o un mensaje de error discreto)
    pass

# El TÍTULO EN VERDE que me pediste
st.markdown("# Inicia tu camino al éxito con SÍ AL MÉRITO")

# --- INICIALIZAR ESTADOS ---
if 'registro_completado' not in st.session_state:
    st.session_state.registro_completado = False
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- PANTALLA 1: REGISTRO (Si no se ha completado) ---
if not st.session_state.registro_completado:
    st.markdown("### Diagnóstico Inicial Gratuito")
    st.write("Registra tus datos para recibir asesoría personalizada sobre carrera administrativa en Colombia.")
    
    with st.form("registro_form"):
        nombre = st.text_input("Tu Nombre Completo:")
        whatsapp = st.text_input("Tu WhatsApp de contacto (con indicativo, ej: +57):")
        nivel = st.selectbox("¿A qué nivel aspiras?", ["Selecciona...", "Asistencial", "Técnico", "Profesional"])
        
        submit = st.form_submit_button("HABLAR CON ASESOR EXPERTO")
        
        if submit:
            if not nombre or not whatsapp or nivel == "Selecciona...":
                st.error("Por favor, completa todos los campos para continuar.")
            else:
                st.session_state.nombre_usuario = nombre
                st.session_state.nivel_usuario = nivel
                st.session_state.registro_completado = True
                st.rerun()

# --- PANTALLA 2: EL CHAT CON LA IA ---
else:
    # Título secundario
    st.markdown(f"### Asesor Virtual para Nivel {st.session_state.nivel_usuario}")
    
    # Configurar cliente OpenAI (usa el Secret 'OPENAI_API_KEY')
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    # Instrucciones del Sistema (Perfil de SÍ AL MÉRITO)
    # ¡Importante! Aquí usamos 'gpt-3.5-turbo' para el saldo
    if "system" not in [m["role"] for m in st.session_state.messages]:
        prompt_sistema = f"""
        Eres el consultor experto de SÍ AL MÉRITO. El usuario es {st.session_state.nombre_usuario}, aspira al nivel {st.session_state.nivel_usuario}. 
        Tu tono es profesional, alentador y conocedor de la Ley 909 de 2004 y los procesos de la CNSC. 
        Menciona que la asesoría personalizada completa tiene un costo de $120.000 COP cuando sea pertinente.
        Responde siempre en español de Colombia.
        """
        st.session_state.messages.append({"role": "system", "content": prompt_sistema})

    # Mostrar historial de mensajes
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Capturar nueva pregunta
    if prompt := st.chat_input("Escribe tu duda aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Llamada a la IA (con el modelo correcto y saldo prepago)
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo", # Modelo rápido y económico
                    messages=st.session_state.messages
                )
                full_response = response.choices[0].message.content
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                # Manejo de error de saldo (RateLimitError)
                st.error("Lo siento, hubo un problema técnico. Asegúrate de que la cuenta de OpenAI tenga saldo disponible.")
                # st.write(f"Detalle del error: {e}") # Descomentar para depurar
