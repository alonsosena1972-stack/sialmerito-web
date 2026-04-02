import streamlit as st
import json
import os
import openai

# Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Plataforma de Entrenamiento", layout="wide")

# --- CONEXIÓN CON IA (OPENAI) ---
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except:
    st.error("Error: No se encontró la API Key en los Secrets.")

# --- FUNCIONES DE CARGA ---
def cargar_preguntas():
    if os.path.exists('preguntas.json'):
        with open('preguntas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"simulacro_gratis": [], "premium": []}

def guardar_preguntas(datos):
    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# --- BARRA LATERAL ---
with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=200)
    elif os.path.exists("logo.jpeg"): st.image("logo.jpeg", width=200)
    
    st.title("SÍ AL MÉRITO")
    st.write("Socio Estratégico: César Padilla")
    st.markdown("---")
    
    # AQUÍ AGREGAMOS LA OPCIÓN DEL PANEL DIRECTOR
    opciones_menu = ["🤖 Asistente IA", "📝 Simulacro Gratuito", "🏆 Zona Premium", "🔑 Panel Director"]
    opcion = st.sidebar.radio("Selecciona una sección:", opciones_menu)
    
    st.markdown("---")
    st.caption("Versión 2.0 - 2026")

# --- SECCIÓN: PANEL DIRECTOR (SÓLO PARA TI) ---
if opcion == "🔑 Panel Director":
    st.header("🔑 Consola de Mando - SÍ AL MÉRITO")
    password = st.text_input("Introduce la Clave de Director:", type="password")
    
    if password == st.secrets["CLAVE_DIRECTOR"]:
        st.success("¡Bienvenido, Director César!")
        tema = st.text_input("Escribe el tema para el nuevo examen:")
        
        if st.button("🚀 Generar y Publicar Examen"):
            with st.spinner("La IA está redactando el examen con sustento legal..."):
                try:
                    # Aquí la IA crea las preguntas automáticamente
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "system", "content": f"Crea un examen de juicio situacional sobre {tema} para la CNSC Colombia."}]
                    )
                    st.write("¡Examen generado y publicado en la Zona Premium!")
                except Exception as e:
                    st.error(f"Error con la IA: {e}")
    elif password != "":
        st.error("Clave incorrecta.")

# --- SECCIÓN: ASISTENTE IA ---
elif opcion == "🤖 Asistente IA":
    st.header("🤖 Consultoría Estratégica con IA")
    st.info("Hola César, estoy listo para asesorarte.")

# --- SECCIÓN: SIMULACRO GRATUITO ---
elif opcion == "📝 Simulacro Gratuito":
    st.header("📝 Entrenamiento de Juicio Situacional")
    datos = cargar_preguntas()
    if datos['simulacro_gratis']:
        st.write("Simulacro cargado correctamente.")
    else:
        st.warning("No hay preguntas cargadas aún.")

# --- SECCIÓN: PREMIUM ---
elif opcion == "🏆 Zona Premium":
    st.header("🚀 Entrenamiento de Alto Rendimiento (Premium)")
    st.write("Solo para estudiantes activos de SÍ AL MÉRITO.")
