import streamlit as st
from openai import OpenAI
import pandas as pd
from io import BytesIO
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO DINÁMICO
st.set_page_config(
    page_title="SÍ AL MÉRITO | Tu Éxito en la CNSC", 
    layout="centered", 
    page_icon="🚀"
)

# Estilos CSS modernos: Azul influyente (#0A2540, #00D4B2)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0A2540 0%, #1A365D 50%, #0F172A 100%);
        color: #F8FAFC;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #FFFFFF;
        font-size: 2.6rem;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    .subtitle {
        font-family: 'Inter', sans-serif;
        color: #38BDF8;
        font-size: 1.15rem;
        text-align: center;
        margin-bottom: 35px;
        font-weight: 500;
    }
    .card-box {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(12px);
        padding: 35px;
        border-radius: 16px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .stTextInput input, .stSelectbox select {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background: linear-gradient(135deg, #00D4B2 0%, #0284C7 100%);
        color: white;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# 2. ENLACES OFICIALES Y RECURSOS DE SÍ AL MÉRITO
TEL_1 = "573146715497"
TEL_2 = "573004417737"
ENLACE_GRUPO = "https://chat.whatsapp.com/HSjyh6FKsHb6mTdIkhAeaU?s=sh&p=a&ilr=4"
WEB_URL = "https://sialmerito-web-bdo27kw6gkkzbg8psnzqx.streamlit.app"
ENLACE_FACEBOOK = "https://www.facebook.com/share/1EgsN9D31Z/"
ENLACE_WORDWALL = "https://wordwall.net/es/myactivities"

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
if 'bloqueado' not in st.session_state:
    st.session_state['bloqueado'] = False

# 4. PANEL DEL DIRECTOR (Barra Lateral Ejecutiva)
with st.sidebar:
    st.markdown("### 🔐 Panel Ejecutivo SÍ AL MÉRITO")
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

# 5. ENCABEZADO VIVO Y PROFESIONAL
st.markdown("<h1 class='main-title'>SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Estrategia e Inteligencia Artificial para Conquistar tu Empleo Público en la CNSC</p>", unsafe_allow_html=True)

# 6. FORMULARIO DE ACCESO FLUIDO
form_abierto = True if not st.session_state['usuario_nombre'] else False

if form_abierto:
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Activa tu Asesoría Experta con Alonso")
    st.markdown("Ingresa tus datos para conectar de inmediato con nuestro consultor inteligente especializado en normatividad y juicios situacionales.")
    
    with st.form("registro_vibrante"):
        nombre = st.text_input("Nombres y Apellidos:")
        
        col1, col2 = st.columns(2)
        with col1:
            whatsapp = st.text_input("Número de WhatsApp (+57):")
        with col2:
            correo = st.text_input("Correo Electrónico:")
            
        concurso = st.text_input("Concurso o Entidad a la que aspiras (Ej: DIAN, Territorial, etc.):")
        nivel_aspirado = st.selectbox("Nivel al que aspiras:", ["Asistencial", "Técnico", "Profesional"])
        
        submit = st.form_submit_button("🚀 INICIAR CONSULTA CON ALONSO", use_container_width=True)
        
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

# 7. AGENTE ALONSO (Cerebro Completo: Pack $120k, Wordwall, Facebook, Anti-Trolls y Enlaces)
if st.session_state['usuario_nombre']:
    nombre_corto = st.session_state['usuario_nombre'].split()[0]
    
    if st.session_state['bloqueado']:
        st.error("🚫 Lo sentimos, debido a lenguaje inapropiado o intentos de sabotaje, tu acceso al chat ha sido suspendido permanentemente. Comunícate directamente con la dirección si consideras que es un error.")
    else:
        st.success(f"🤖 **Alonso (Asesor SÍ AL MÉRITO):** ¡Hola, **{nombre_corto}**! Preparándonos para el nivel **{st.session_state['usuario_nivel']}** en **{st.session_state['usuario_concurso']}**. ¿Cuál es tu consulta hoy?")
        
        # Mostrar historial de chat
        for chat in st.session_state['historial']:
            with st.chat_message(chat["role"]):
                st.markdown(chat["content"])

        # Entrada de chat
        prompt = st.chat_input("Escribe tu consulta sobre la CNSC, OPEC, simulacros o redes...")

        if prompt:
            # FILTRO ANTI-TROLLS / SABOTAJE LOCAL RÁPIDO
            palabras_nefastas = ["puta", "mierda", "idiota", "estupido", "imbecil", "sexo", "porno", "hack", "burlas"]
            if any(p in prompt.lower() for p in palabras_nefastas):
                st.session_state['bloqueado'] = True
                st.rerun()

            st.session_state['contador'] += 1
            st.session_state['historial'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # CIERRE A LA CUARTA PREGUNTA CON DETALLE DE TODOS LOS CANALES Y SERVICIOS
            if st.session_state['contador'] > 4:
                with st.chat_message("assistant"):
                    msg_cierre = (
                        f"¡Excelente recorrido, **{nombre_corto}**! Has completado tus 4 consultas de rigor para el nivel **{st.session_state['usuario_nivel']}**.\n\n"
                        f"🎯 **Da el salto definitivo al éxito con la Asesoría Personalizada de César Padilla ($120.000 COP):**\n"
                        f"- Materiales en PDF, normas y leyes completas.\n"
                        f"- Enlaces de videos exclusivos con expertos temáticos por OPEC.\n"
                        f"- Simulacro avanzado de 50 preguntas ajustado a los ejes temáticos de tu OPEC.\n\n"
                        f"🔗 **Explora más recursos y comunidad oficial:**\n"
                        f"- Simulacros Gratuitos y VIP en Wordwall: [Acceder a Wordwall]({ENLACE_WORDWALL})\n"
                        f"- Síguenos en nuestra página de Facebook: [Visitar Facebook]({ENLACE_FACEBOOK})"
                    )
                    st.markdown(msg_cierre)
                    
                    texto_wa = f"Hola César, soy {st.session_state['usuario_nombre']}. Terminé mis consultas con Alonso para el nivel {st.session_state['usuario_nivel']} ({st.session_state['usuario_concurso']}) y quiero asegurar mi plaza con tu asesoría."
                    
                    st.link_button("👥 Unirme al Grupo Oficial de WhatsApp", ENLACE_GRUPO, use_container_width=True)
                    st.link_button("📘 Visitar Nuestra Página de Facebook", ENLACE_FACEBOOK, use_container_width=True)
                    st.link_button("🎯 Ir a Simulacros Wordwall (VIP y Gratis)", ENLACE_WORDWALL, use_container_width=True)
                    
                    c1, c2 = st.columns(2)
                    with c1: st.link_button("📲 Hablar con César (Línea 1)", f"https://wa.me/{TEL_1}?text={texto_wa}", use_container_width=True)
                    with c2: st.link_button("📲 Hablar con César (Línea 2)", f"https://wa.me/{TEL_2}?text={texto_wa}", use_container_width=True)
                st.warning("Has alcanzado el límite de 4 consultas rápidas. ¡Es momento de asegurar tu plaza con la Dirección!")
            
            else:
                if client:
                    with st.chat_message("assistant"):
                        with st.spinner("Alonso está consultando la normativa y enlaces..."):
                            try:
                                respuesta = client.chat.completions.create(
                                    model="gpt-4o",
                                    messages=[
                                        {
                                            "role": "system", 
                                            "content": (
                                                f"Eres Alonso, el asesor experto de 'SÍ AL MÉRITO' dirigido por César Padilla. Tu propósito es asesorar rigurosamente sobre "
                                                f"concursos de la CNSC, Ley 909, OPEC, juicios situacionales y normatividad.\n\n"
                                                f"REGLAS CRÍTICAS DE COMPORTAMIENTO:\n"
                                                f"1. FILTRO DE SALUDOS/TROLLEO: Si te escriben saludos vacíos ('hola'), responde cordialmente invitandole a hacer su consulta técnica. Si detectas insultos, lenguaje obsceno o intentos de sabotaje, incluye la palabra clave [BLOQUEAR_USUARIO].\n"
                                                f"2. NUNCA DIGAS 've a la página de la CNSC' de forma genérica: Proporciona siempre el enlace oficial de la CNSC (https://www.cnsc.gov.co) o SIMO.\n"
                                                f"3. PROMOCIÓN DE RECURSOS: Cuando pregunten por simulacros, recuérdales que tenemos versiones gratuitas y simulacros VIP por $20.000 COP en nuestra plataforma Wordwall ({ENLACE_WORDWALL}). Cuando pregunten por información, notas o contenidos recientes, recuérdales que pueden visitar nuestra página de Facebook ({ENLACE_FACEBOOK}). Y menciona que la Asesoría Personalizada de César Padilla cuesta $120.000 COP e incluye PDFs normativos, videos de YouTube por OPEC y simulacros de 50 preguntas.\n"
                                                f"4. Mantén tono profesional, experto, persuasivo y directo."
                                            )
                                        },
                                        *st.session_state['historial']
                                    ]
                                )
                                res_text = respuesta.choices[0].message.content
                                
                                # VALIDAR SI EL MODELO DETECTÓ SABOTAJE EXPLÍCITO
                                if "[BLOQUEAR_USUARIO]" in res_text:
                                    st.session_state['bloqueado'] = True
                                    st.rerun()
                                else:
                                    st.write(res_text)
                                    st.session_state['historial'].append({"role": "assistant", "content": res_text})
                            except Exception as e:
                                st.error(f"Problema temporal de conexión: {e}")
                else:
                    st.warning("API Key no configurada.")
else:
    st.info("👆 Por favor, completa el formulario superior para que Alonso conozca tu perfil y comience tu asesoría.")
