import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO

# 1. Configuración de la página
st.set_page_config(page_title="SÍ AL MÉRITO - Plataforma Oficial", layout="wide")

# 2. Inicialización de la IA con manejo seguro de errores
def inicializar_alonso():
    try:
        return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    except:
        return None

client = inicializar_alonso()

# 3. Base de datos temporal para el Excel
if 'registros' not in st.session_state:
    st.session_state['registros'] = []

# 4. Barra Lateral (Acceso Privado y Descarga de Excel)
with st.sidebar:
    st.markdown("### 🔐 Acceso Privado")
    clave = st.text_input("Clave de Administrador:", type="password")
    
    if clave == st.secrets.get("CLAVE_DIRECTOR", "ADMIN2026"):
        st.success("Acceso Concedido")
        
        if st.session_state['registros']:
            df = pd.DataFrame(st.session_state['registros'])
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Alumnos_Registrados')
            
            st.download_button(
                label="📥 Descargar Excel de Registros",
                data=output.getvalue(),
                file_name="Registros_SiAlMerito.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Aún no hay nuevos registros para descargar.")
    else:
        st.info("Introduce tu clave para ver el panel de control.")

# 5. Encabezado Principal
col1, col2, col3 = st.columns([2, 1, 2]) 
with col2:
    st.image("logo.png", width=150)

st.markdown("<h1 style='text-align: center; color: #1e7e34;'>Inicia tu camino al éxito con SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Bienvenido, Cesar Alonso Padilla</h3>", unsafe_allow_html=True)

st.write("---")

# 6. SECCIÓN RECUPERADA: Formulario de Registro
st.markdown("### 📋 Diagnóstico Inicial Gratuito")
st.write("Por favor, regístrate para recibir asesoría personalizada.")

with st.form("formulario_registro"):
    nombre = st.text_input("Nombre Completo:")
    whatsapp = st.text_input("WhatsApp de contacto (ej: +57):")
    nivel = st.selectbox("¿A qué nivel aspiras?", ["Asistencial", "Técnico", "Profesional"])
    
    boton_registro = st.form_submit_button("REGISTRAR MIS DATOS")
    
    if boton_registro:
        if nombre and whatsapp:
            st.session_state['registros'].append({"Nombre": nombre, "WhatsApp": whatsapp, "Nivel": nivel})
            st.success(f"¡Excelente {nombre}! Tus datos han sido guardados. Ahora puedes consultar a Alonso abajo.")
        else:
            st.error("Por favor completa tu nombre y WhatsApp para continuar.")

st.write("---")

# 7. Consultoría con el Agente Alonso
st.warning("🏠 ¡Hola! Soy Alonso. Estoy aquí para guiarte en el mérito y el éxito profesional.")

duda = st.text_input("Escribe tu duda legal o de carrera aquí:", key="input_alonso")

if duda:
    if client:
        with st.spinner("Alonso está redactando tu respuesta técnica..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Eres Alonso, el asesor experto de SÍ AL MÉRITO. Tu jefe es César Alonso Padilla. Respondes con rigor legal y motivación sobre la CNSC en Colombia."},
                        {"role": "user", "content": duda}
                    ]
                )
                st.info(response.choices[0].message.content)
            except:
                st.error("Hubo un problema de conexión con Alonso. Intenta enviar tu duda nuevamente.")
    else:
        st.error("Error: La llave de la IA no está configurada correctamente.")

st.caption("Versión Oficial 2026 - SÍ AL MÉRITO")
