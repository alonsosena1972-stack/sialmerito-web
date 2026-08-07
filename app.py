import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO PROFESIONAL
st.set_page_config(page_title="SÍ AL MÉRITO | Consultoría Especializada CNSC", layout="centered", page_icon="⚖️")

# Estilos CSS personalizados para una interfaz ultra profesional y limpia
st.markdown("""
    <style>
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 700;
        color: #111827;
        font-size: 2.2rem;
        margin-bottom: 0px;
        text-align: center;
    }
    .subtitle {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #4B5563;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 30px;
    }
    .card-box {
        background-color: #F9FAFB;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 2. CONEXIÓN SEGURA A OPENAI Y VARIABLES DE CONTACTO
TEL_1 = "573146715497"
TEL_2 = "573004417737"
ENLACE_GRUPO = "https://chat.whatsapp.com/HSjyh6FKsHb6mTdIkhAeaU?s=sh&p=a&ilr=4"
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
if 'usuario_concurso' not in st.session_state:
    st.session_state['usuario_concurso'] = ""
if 'contador' not in st.session_state:
    st.session_state['contador'] = 0
if 'historial' not in st.session_state:
    st.session_state['historial'] = []

# 4. PANEL DEL DIRECTOR (Barra Lateral)
with st.sidebar:
    st.markdown("### 🔐 Panel Ejecutivo")
    pass_admin = st.text_input("Contraseña Maestro:", type="password")
    
    if pass_admin == st.secrets.get("CLAVE_DIRECTOR", "CESAR2026"):
        st.success("Acceso Autorizado")
        if st.session_state['lista_registros']:
            st.write(f"Aspirantes registrados: {len(st.session_state['lista_registros'])}")
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
            st.info("Aún no hay aspirantes registrados hoy.")
    else:
        st.info("Área exclusiva para la dirección.")

# 5. ENCABEZADO PROFESIONAL
st.markdown("<h1 class='main-title'>SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Plataforma de Asesoría Inteligente para Concursos de Carrera Administrativa - CNSC</p>", unsafe_allow_html=True)

# 6. FORMULARIO DE ACCESO SIMPLIFICADO (Sin cédula, limpio y directo)
form_abierto = True if not st.session_state['usuario_nombre'] else False

if form_abierto:
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    st.markdown("#### 🎯 Inicia tu asesoría personalizada")
    st.markdown("Completa tus datos básicos para habilitar el acceso directo con **Alonso**, nuestro asesor experto en normatividad y juicios situacionales.")
    
    with st.form("registro_simplificado"):
        nombre = st.text_input("Nombres y Apellidos:")
        
        col1, col2 = st.columns(2)
        with col1:
            whatsapp = st.text_input("Número de WhatsApp (+57):")
        with col2:
            correo = st.text_input("Correo Electrónico:")
            
        concurso = st.text_input("Concurso al que aspiras (Ej: Entidades del Orden Nacional, DIAN, Territorial, etc.):")
        nivel_aspirado = st.selectbox("Nivel al que aspiras:", ["Asistencial", "Técnico", "Profesional"])
        
        submit = st.form_submit_button("ACCEDER A LA ASESORÍA EXPERTA 🚀", use_container_width=True)
        
        if submit:
            if nombre and whatsapp and correo and concurso:
                st.session_state['lista_registros'].append({
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre": nombre, "WhatsApp": whatsapp, "Email": correo, "Concurso": concurso, "Nivel": nivel_aspirado
                })
                st.session_state['usuario_nombre'] = nombre
                st.session_state['usuario_nivel'] = nivel_aspirado
                st.session_state['usuario_concurso'] = concurso
                st.rerun()
            else:
                st.warning("Socio, por favor completa todos los campos para continuar.")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("---")

# 7. AGENTE ALONSO (Cerebro Activo tras el Registro)
if st.session_state['usuario_nombre']:
    nombre_corto = st.session_state['usuario_nombre'].split()[0]
    st.success(f"🤖 **Alonso (Asesor SÍ AL MÉRITO):** ¡Hola, **{nombre_corto}**! Qué gusto saludarte. Veo que vas por el nivel **{st.session_state['usuario_nivel']}** en el concurso **{st.session_state['usuario_concurso']}**. ¿Cuál es tu primera duda sobre la CNSC o los casos situacionales?")
    
    # Mostrar historial de chat
    for chat in st.session_state['historial']:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # Entrada de chat
    prompt = st.chat_input("Escribe aquí tu duda técnica o jurídica...")

    if prompt:
        st.session_state['contador'] += 1
        st.session_state['historial'].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # CIERRE A LA TERCERA PREGUNTA CON PASO AL GRUPO Y A CÉSAR
        if st.session_state['contador'] > 3:
            with st.chat_message("assistant"):
                msg_cierre = f"He resuelto tus dudas clave y veo que te preparas con toda para el nivel **{st.session_state['usuario_nivel']}**. Para no perderte ningún aviso de la CNSC y asegurar tu plaza, únete a nuestra comunidad oficial y da el paso definitivo con nuestro director **César Padilla**."
                st.markdown(msg_cierre)
                
                texto_wa = f"Hola César, soy {st.session_state['usuario_nombre']}. Me preparo para el nivel {st.session_state['usuario_nivel']} ({st.session_state['usuario_concurso']}) y quiero asegurar mi plaza con tu asesoría."
                
                st.link_button("👥 Unirme al Grupo Oficial de WhatsApp", ENLACE_GRUPO, use_container_width=True)
                c1, c2 = st.columns(2)
                with c1: st.link_button("📲 Hablar con César (Línea 1)", f"https://wa.me/{TEL_1}?text={texto_wa}", use_container_width=True)
                with c2: st.link_button("📲 Hablar con César (Línea 2)", f"https://wa.me/{TEL_2}?text={texto_wa}", use_container_width=True)
            st.warning("Has alcanzado el límite de consultas rápidas. ¡Es momento de asegurar tu éxito directamente con la Dirección!")
        
        else:
            if client:
                with st.chat_message("assistant"):
                    with st.spinner("Alonso está analizando la normativa..."):
                        try:
                            respuesta = client.chat.completions.create(
                                model="gpt-4o",
                                messages=[
                                    {
                                        "role": "system", 
                                        "content": (
                                            "Eres Alonso, el asesor experto de 'SÍ AL MÉRITO'. Tu propósito es asesorar rigurosamente sobre "
                                            "concursos de carrera administrativa de la CNSC, la Ley 909 de 2004, juicios situacionales, "
                                            "competencias funcionales y normativas del Estado colombiano (incluyendo criterios defensivos, "
                                            "enfoque sistémico y gestión MIPG).\n\n"
                                            "REGLA ESTRICTA DE FILTRADO:\n"
                                            "1. Si el usuario te envía saludos vacíos (como 'hola', 'buenos días'), stickers, imágenes o "
                                            "cualquier mensaje ajeno a los concursos públicos, DEBES QUEDARTE COMPLETAMENTE CALLADO y no emitir respuesta.\n"
                                            "2. Mantén un tono profesional, motivador, con propiedad técnica y directo al grano."
                                        )
                                    },
                                    *st.session_state['historial']
                                ]
                            )
                            res_text = respuesta.choices[0].message.content
                            st.write(res_text)
                            st.session_state['historial'].append({"role": "assistant", "content": res_text})
                        except Exception as e:
                            st.error(f"Problema temporal de conexión: {e}")
            else:
                st.warning("API Key no configurada.")
else:
    st.info("👆 Por favor, completa el formulario superior para que Alonso pueda conocer tu perfil y atenderte de forma personalizada.")
