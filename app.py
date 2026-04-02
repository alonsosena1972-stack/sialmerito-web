import streamlit as st
import json
import os

# Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Plataforma de Entrenamiento", layout="wide")

# --- FUNCIONES DE CARGA ---
def cargar_preguntas():
    if os.path.exists('preguntas.json'):
        with open('preguntas.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stRadio > label { font-weight: bold; color: #1e3d59; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    # Intentamos cargar logo.png o logo.jpeg
    if os.path.exists("logo.png"):
        st.image("logo.png", width=200)
    elif os.path.exists("logo.jpeg"):
        st.image("logo.jpeg", width=200)
    
    st.title("SÍ AL MÉRITO")
    st.write("Socio Estratégico: César Padilla")
    st.markdown("---")
    opcion = st.sidebar.radio(
        "Selecciona una sección:",
        ["🤖 Asistente IA", "📝 Simulacro Gratuito", "🏆 Zona Premium"]
    )
    st.markdown("---")
    st.caption("Versión 2.0 - 2026")

# --- SECCIÓN: ASISTENTE IA ---
if opcion == "🤖 Asistente IA":
    st.header("🤖 Consultoría Estratégica con IA")
    st.info("Hola César, estoy listo para asesorarte en tus proyectos legales.")
    # Espacio para tu chat anterior

# --- SECCIÓN: SIMULACRO GRATUITO ---
elif opcion == "📝 Simulacro Gratuito":
    st.header("📝 Entrenamiento de Juicio Situacional")
    st.markdown("Analiza cada caso con detenimiento. ¡Mucho éxito!")
    
    datos = cargar_preguntas()
    
    if datos:
        preguntas = datos['simulacro_gratis']
        respuestas_usuario = {}
        
        # Mostrar preguntas
        for p in preguntas:
            with st.container():
                st.subheader(f"Pregunta {p['id']}: {p['tema']}")
                st.write(p['contexto'])
                
                ops = [f"A. {p['opciones']['A']}", 
                       f"B. {p['opciones']['B']}", 
                       f"C. {p['opciones']['C']}"]
                
                respuestas_usuario[p['id']] = st.radio(
                    f"Tu elección para la pregunta {p['id']}:", 
                    ops, 
                    key=f"p_{p['id']}"
                )
                st.markdown("---")
        
        if st.button("Finalizar y Ver Calificación"):
            aciertos = 0
            for p in preguntas:
                # Obtenemos la letra seleccionada (A, B o C)
                seleccion = respuestas_usuario[p['id']][0]
                if seleccion == p['correcta']:
                    aciertos += 1
            
            puntaje = (aciertos / len(preguntas)) * 100
            st.success(f"### Tu Puntaje Final: {puntaje}/100")
            
            if puntaje >= 70:
                st.balloons()
                st.markdown("### 🏆 ¡Excelente nivel!")
            else:
                st.warning("Buen intento. Repasa los sustentos legales para mejorar.")

# --- SECCIÓN: PREMIUM ---
elif opcion == "🏆 Zona Premium":
    st.header("🚀 Entrenamiento de Alto Rendimiento (Premium)")
    st.write("Accede a simulacros de 50 preguntas con cronómetro de 3 minutos.")
    
    codigo = st.text_input("Introduce tu código de acceso:", type="password")
    if st.button("Validar Acceso"):
        if codigo == "MERITO2026":
            st.success("¡Acceso concedido, Director César! Cargando simulador profesional...")
        else:
            st.error("Código incorrecto. Solicita tu acceso en SÍ AL MÉRITO.")
