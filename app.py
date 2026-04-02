import streamlit as st
from openai import OpenAI

# 1. Configuración visual (Tu marca siempre presente)
st.set_page_config(page_title="SÍ AL MÉRITO - Asesor IA", layout="centered")

with st.sidebar:
    st.image("logo.png", width=200) if "logo.png" else None
    st.title("SÍ AL MÉRITO")
    st.subheader("Director: César Padilla")
    st.markdown("---")
    st.info("Este es tu espacio de consultoría privada para concursos de carrera.")

# 2. Conexión segura con la IA
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except Exception as e:
    st.error("Error en la llave de conexión. Revisa los Secrets.")

# 3. Interfaz del Agente Alonso
st.header("🤖 Consultoría Estratégica con Alonso")
st.write("---")

st.markdown("### Hola, soy **Alonso**, tu asistente especializado en concursos de Carrera Administrativa.")

# Caja de chat
pregunta = st.text_input("¿En qué puedo asesorarte hoy, César?", placeholder="Ej: ¿Qué requisitos tiene la convocatoria de la DIAN?")

if pregunta:
    with st.spinner("Alonso está analizando la normativa colombiana..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o", # Usamos el modelo más moderno y estable
                messages=[
                    {"role": "system", "content": "Tu nombre es Alonso. Eres el asesor senior de la academia SÍ AL MÉRITO. Eres experto en la CNSC, leyes 909, 1952, 1437 y procesos de selección en Colombia. Respondes de forma clara, técnica y muy profesional."},
                    {"role": "user", "content": pregunta}
                ]
            )
            st.markdown("#### 📝 Respuesta de Alonso:")
            st.info(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Lo siento, hubo un error técnico: {e}")

st.markdown("---")
st.caption("SÍ AL MÉRITO - Todos los derechos reservados 2026")
