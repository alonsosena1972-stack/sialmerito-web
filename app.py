import streamlit as st
import json
import os
import openai

# 1. Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Plataforma de Entrenamiento", layout="wide")

# 2. Conexión con los "Misterios" (Secrets)
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    CLAVE_ADMIN = st.secrets["CLAVE_DIRECTOR"]
except:
    st.error("⚠️ Error: No se configuraron correctamente los Secrets en Streamlit.")

# 3. Funciones de Base de Datos (JSON)
def cargar_datos():
    if os.path.exists('preguntas.json'):
        with open('preguntas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"simulacro_gratis": [], "premium": []}

def guardar_datos(datos):
    with open('preguntas.json', 'w', encoding='utf-8') as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

# 4. Estilos y Barra Lateral
st.markdown("""<style>.main { background-color: #f5f7f9; }</style>""", unsafe_allow_html=True)

with st.sidebar:
    if os.path.exists("logo.png"): st.image("logo.png", width=200)
    elif os.path.exists("logo.jpeg"): st.image("logo.jpeg", width=200)
    
    st.title("SÍ AL MÉRITO")
    st.subheader("Socio Estratégico: César Padilla")
    st.markdown("---")
    
    opcion = st.radio(
        "Selecciona una sección:",
        ["🤖 Asistente IA", "📝 Simulacro Gratuito", "🏆 Zona Premium", "🔑 Panel Director"]
    )
    st.markdown("---")
    st.caption("Versión 2.0 - 2026")

# --- LÓGICA DE SECCIONES ---

if opcion == "🤖 Asistente IA":
    st.header("🤖 Consultoría Estratégica con IA")
    st.info("Hola, soy **Alonso**, tu asistente especializado en concursos de Carrera Administrativa.")
    
    pregunta = st.text_input("¿En qué puedo asesorarte hoy, César?")
    if pregunta:
        with st.spinner("Alonso está analizando la normativa..."):
            try:
                res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Tu nombre es Alonso. Eres un experto en la CNSC y derecho administrativo colombiano. Respondes de forma técnica y profesional."},
                        {"role": "user", "content": pregunta}
                    ]
                )
                st.markdown("### 📝 Respuesta de Alonso:")
                st.write(res.choices[0].message.content)
            except Exception as e:
                st.error(f"Error de conexión: {e}")

elif opcion == "📝 Simulacro Gratuito":
    st.header("📝 Entrenamiento de Juicio Situacional (Gratis)")
    st.write("Demuestra tus conocimientos básicos.")
    datos = cargar_datos()
    if not datos["simulacro_gratis"]:
        st.warning("Aún no hay preguntas cargadas por el Director.")

elif opcion == "🏆 Zona Premium":
    st.header("🚀 Entrenamiento de Alto Rendimiento")
    st.write("Área exclusiva para estudiantes de SÍ AL MÉRITO.")
    acceso = st.text_input("Código de Acceso Premium:", type="password")
    if acceso == "MERITO2026":
        st.success("Acceso concedido. Cargando simuladores de alta complejidad...")
    elif acceso != "":
        st.error("Código no válido.")

elif opcion == "🔑 Panel Director":
    st.header("🔑 Consola de Mando - SÍ AL MÉRITO")
    password = st.text_input("Clave de Director:", type="password")
    
    if password == CLAVE_ADMIN:
        st.success("Bienvenido, Director César.")
        nuevo_tema = st.text_input("Tema para generar nuevo examen (ej: Ley 1437):")
        if st.button("🚀 Generar y Publicar en Premium"):
            with st.spinner("La IA está redactando casos de juicio situacional..."):
                # Aquí se simula la generación y guardado
                st.success(f"¡Examen sobre '{nuevo_tema}' publicado con éxito en la Zona Premium!")
    elif password != "":
        st.error("Acceso denegado.")
