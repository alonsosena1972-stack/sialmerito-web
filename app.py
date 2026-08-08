import streamlit as str_app
from openai import OpenAI
import pandas as pd
from io import BytesIO
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO DINÁMICO (ESTILO GITHUB DARK & CONTRASTE TOTAL)
str_app.set_page_config(
    page_title="SÍ AL MÉRITO | Tu Éxito en la CNSC", 
    layout="centered", 
    page_icon="🚀"
)

# Estilos CSS optimizados al estilo de entorno de desarrollo profesional (GitHub Dark)
str_app.markdown("""
    <style>
    .stApp {
        background: #0D1117 !important;
        color: #F0F6FC !important;
    }
    
    /* Textos generales claros y legibles */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #F0F6FC !important;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: #238636 !important; /* Verde estilo GitHub para SÍ AL MÉRITO */
        font-size: 2.6rem;
        text-align: center;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }
    .subtitle {
        font-family: 'Inter', sans-serif;
        color: #58A6FF !important;
        font-size: 1.15rem;
        text-align: center;
        margin-bottom: 35px;
        font-weight: 500;
    }
    .card-box {
        background: #161B22 !important;
        backdrop-filter: blur(12px);
        padding: 35px;
        border-radius: 12px;
        border: 1px solid #30363D !important;
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.6);
    }
    .footer-institucional {
        background: #161B22 !important;
        border-top: 2px solid #238636;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-top: 50px;
        font-family: 'Inter', sans-serif;
    }
    .footer-title {
        color: #238636 !important; /* Verde */
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 8px;
    }
    .footer-text {
        color: #8B949E !important;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .footer-contacto {
        color: #238636 !important; /* WhatsApp en Verde */
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 10px;
    }
    
    /* Clases personalizadas para colorear textos específicos */
    .texto-verde {
        color: #238636 !important;
        font-weight: 700;
    }
    .texto-correo {
        color: #58A6FF !important; /* Correo en Azul */
        text-decoration: underline;
    }
    .texto-whatsapp {
        color: #238636 !important; /* WhatsApp en Verde */
        font-weight: 700;
    }
    
    /* Estilo específico para el texto "Contraseña Maestro:" en la barra lateral (Azul Cielo) */
    [data-testid="stSidebar"] label p {
        color: #58A6FF !important;
        font-weight: 600 !important;
    }

    /* Estilo para la cajita de aviso del panel (Área exclusiva para la dirección en Verde) */
    [data-testid="stSidebar"] .stAlert {
        background-color: rgba(35, 134, 54, 0.15) !important;
        border: 1px solid #238636 !important;
        color: #238636 !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] .stAlert p {
        color: #238636 !important;
        font-weight: 600 !important;
    }

    /* Cajas de texto y selectores estilo editor limpio */
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #0D1117 !important;
        color: #F0F6FC !important;
        border: 1px solid #30363D !important;
        border-radius: 6px !important;
    }
    
    .stButton button {
        background: #238636 !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 0.6rem 1.2rem;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background: #2ea043 !important;
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# 2. ENLACES OFICIALES Y RECURSOS DE SÍ AL MÉRITO
TEL_1 = "573146715497"
TEL_2 = "573153838792"
TEL_3 = "573004417737"
CORREO_EMPRESA = "si.al.merito2026@gmail.com"
ENLACE_GRUPO = "https://chat.whatsapp.com/HSjyh6FKsHb6mTdIkhAeaU?s=sh&p=a&ilr=4"
WEB_URL = "https://sialmerito-web-bdo27kw6gkkzbg8psnzqx.streamlit.app"
ENLACE_FACEBOOK = "https://www.facebook.com/share/1EgsN9D31Z/"
ENLACE_WORDWALL = "https://wordwall.net/es/myactivities"
ENLACE_YOUTUBE = "https://www.youtube.com/@cesaralonsopadillaheredia2231"
ENLACE_JITSI = "https://meet.jit.si/SiAlMeritoSesionGarantizada2026Oficial"

ARCH_CSV = "base_aspirantes_si_al_merito.csv"
client = None

try:
    if "OPENAI_API_KEY" in str_app.secrets:
        client = OpenAI(api_key=str_app.secrets["OPENAI_API_KEY"])
    else:
        str_app.error("Error: No se encontró la llave API en los Secrets de Streamlit.")
except Exception as e:
    str_app.error(f"Error de conexión inicial: {e}")

# 3. GESTIÓN DE MEMORIA Y PERSISTENCIA (CSV)
if 'usuario_nombre' not in str_app.session_state:
    str_app.session_state['usuario_nombre'] = ""
if 'usuario_nivel' not in str_app.session_state:
    str_app.session_state['usuario_nivel'] = ""
if 'usuario_concurso' not in str_app.session_state:
    str_app.session_state['usuario_concurso'] = ""
if 'contador' not in str_app.session_state:
    str_app.session_state['contador'] = 0
if 'historial' not in str_app.session_state:
    str_app.session_state['historial'] = []
if 'bloqueado' not in str_app.session_state:
    str_app.session_state['bloqueado'] = False

if os.path.exists(ARCH_CSV):
    try:
        df_persisted = pd.read_csv(ARCH_CSV)
        str_app.session_state['lista_registros'] = df_persisted.to_dict('records')
    except:
        str_app.session_state['lista_registros'] = []
else:
    if 'lista_registros' not in str_app.session_state:
        str_app.session_state['lista_registros'] = []

# 4. PANEL DEL DIRECTOR (Barra Lateral Ejecutiva)
with str_app.sidebar:
    str_app.markdown("### 🔐 Panel Ejecutivo <span class='texto-verde'>SÍ AL MÉRITO</span>", unsafe_allow_html=True)
    pass_admin = str_app.text_input("Contraseña Maestro:", type="password")
    
    if pass_admin == str_app.secrets.get("CLAVE_DIRECTOR", "CESAR2026"):
        str_app.success("Acceso Autorizado")
        registros = str_app.session_state['lista_registros']
        if registros:
            str_app.write(f"Total Aspirantes Registrados: **{len(registros)}**")
            df = pd.DataFrame(registros)
            
            str_app.markdown("---")
            str_app.markdown("#### 👥 Últimos Aspirantes:")
            for idx, row in df.tail(5).iterrows():
                str_app.caption(f"📌 **{row.get('Nombre', 'N/A')}**\n📧 <span class='texto-correo'>{row.get('Email', 'N/A')}</span>\n📱 <span class='texto-whatsapp'>{row.get('WhatsApp', 'N/A')}</span>\n🎯 Nivel: {row.get('Nivel', 'N/A')}", unsafe_allow_html=True)
            
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Aspirantes')
            
            str_app.download_button(
                label="📥 Descargar Base Completa (Excel)",
                data=output.getvalue(),
                file_name=f"Aspirantes_SiAlMerito_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            str_app.info("Aún no hay aspirantes registrados.")
    else:
        str_app.info("Área exclusiva para la dirección.")

# 5. ENCABEZADO VIVO Y PROFESIONAL
str_app.markdown("<h1 class='main-title'>SÍ AL MÉRITO</h1>", unsafe_allow_html=True)
str_app.markdown("<p class='subtitle'>Talleres, Cursos y Asesorías Especializadas para Conquistar tu Empleo Público</p>", unsafe_allow_html=True)

# 6. FORMULARIO DE ACCESO FLUIDO
form_abierto = True if not str_app.session_state['usuario_nombre'] else False

if form_abierto:
    str_app.markdown("<div class='card-box'>", unsafe_allow_html=True)
    str_app.markdown("### 🎯 Activa tu Asesoría Experta con Alonso")
    str_app.markdown(f"Ingresa tus datos para conectar de inmediato. Empresa autorizada • Correo: <span class='texto-correo'>{CORREO_EMPRESA}</span>", unsafe_allow_html=True)
    
    with str_app.form("registro_vibrante"):
        nombre = str_app.text_input("Nombres y Apellidos:")
        
        col1, col2 = str_app.columns(2)
        with col1:
            whatsapp = str_app.text_input("Número de <span class='texto-whatsapp'>WhatsApp</span> (+57):", help="Número de contacto")
        with col2:
            correo = str_app.text_input("Correo Electrónico:")
            
        concurso = str_app.text_input("Concurso o Entidad a la que aspiras (Ej: DIAN, Territorial, etc.):")
        nivel_aspirado = str_app.selectbox("Nivel al que aspiras:", ["Asistencial", "Técnico", "Profesional"])
        
        submit = str_app.form_submit_button("🚀 INICIAR CONSULTA CON ALONSO", use_container_width=True)
        
        if submit:
            if nombre and whatsapp and correo and concurso:
                nuevo_registro = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre": nombre, 
                    "WhatsApp": whatsapp, 
                    "Email": correo, 
                    "Concurso": concurso, 
                    "Nivel": nivel_aspirado
                }
                
                str_app.session_state['lista_registros'].append(nuevo_registro)
                df_temp = pd.DataFrame(str_app.session_state['lista_registros'])
                df_temp.to_csv(ARCH_CSV, index=False)
                
                str_app.session_state['usuario_nombre'] = nombre
                str_app.session_state['usuario_nivel'] = nivel_aspirado
                str_app.session_state['usuario_concurso'] = concurso
                str_app.rerun()
            else:
                str_app.warning("Socio, por favor completa todos los campos para continuar.")
    str_app.markdown("</div>", unsafe_allow_html=True)

str_app.write("---")

# 7. AGENTE ALONSO (Cerebro Completo: Jueves/Viernes Jitsi, YouTube, Pack $120k, Wordwall, Facebook, Anti-Trolls)
if str_app.session_state['usuario_nombre']:
    nombre_corto = str_app.session_state['usuario_nombre'].split()[0]
    
    if str_app.session_state['bloqueado']:
        str_app.error("🚫 Lo sentimos, debido a lenguaje inapropiado o intentos de sabotaje, tu acceso al chat ha sido suspendido permanentemente. Comunícate directamente con la dirección si consideras que es un error.")
    else:
        str_app.success(f"🤖 **Alonso (Asesor <span class='texto-verde'>SÍ AL MÉRITO</span>):** ¡Hola, **{nombre_corto}**! Preparándonos para el nivel **{str_app.session_state['usuario_nivel']}** en **{str_app.session_state['usuario_concurso']}**. ¿Cuál es tu consulta hoy?")
        
        for chat in str_app.session_state['historial']:
            with str_app.chat_message(chat["role"]):
                str_app.markdown(chat["content"])

        prompt = str_app.chat_input("Escribe tu consulta sobre la CNSC, OPEC, simulacros o capacitaciones...")

        if prompt:
            palabras_nefastas = ["puta", "mierda", "idiota", "estupido", "imbecil", "sexo", "porno", "hack", "burlas"]
            if any(p in prompt.lower() for p in palabras_nefastas):
                str_app.session_state['bloqueado'] = True
                str_app.rerun()

            str_app.session_state['contador'] += 1
            str_app.session_state['historial'].append({"role": "user", "content": prompt})
            with str_app.chat_message("user"):
                str_app.write(prompt)

            if str_app.session_state['contador'] > 4:
                with str_app.chat_message("assistant"):
                    msg_cierre = (
                        f"¡Excelente recorrido, **{nombre_corto}**! Has completado tus 4 consultas clave para el nivel **{str_app.session_state['usuario_nivel']}**.\n\n"
                        f"🎓 **Te invitamos a nuestras Capacitaciones Gratuitas (Jueves y Viernes):**\n"
                        f"Conéctate a nuestras charlas en vivo sobre temas transversales, funcionales, competencias comportamentales y simulacros en vivo:\n"
                        f"🔗 [Entrar a la Sala Jitsi - Sesión Garantizada 2026]({ENLACE_JITSI})\n\n"
                        f"🎯 **Asesoría Personalizada de César Padilla ($120.000 COP):**\n"
                        f"- Materiales en PDF, normas y leyes completas.\n"
                        f"- Videos exclusivos con expertos temáticos por OPEC.\n"
                        f"- Simulacro avanzado de 50 preguntas ajustado a los ejes de tu OPEC.\n\n"
                        f"🔗 **Ecosistema SÍ AL MÉRITO:**\n"
                        f"- Simulacros Gratuitos y VIP en Wordwall: [Ver Simulacros]({ENLACE_WORDWALL})\n"
                        f"- Canal de YouTube (Videos de concursos): [Ver Canal]({ENLACE_YOUTUBE})\n"
                        f"- Página de Facebook: [Visitar Facebook]({ENLACE_FACEBOOK})"
                    )
                    str_app.markdown(msg_cierre)
                    
                    texto_wa = f"Hola César, soy {str_app.session_state['usuario_nombre']}. Terminé mis consultas con Alonso para el nivel {str_app.session_state['usuario_nivel']} ({str_app.session_state['usuario_concurso']}) y quiero asegurar mi plaza con tu asesoría."
                    
                    str_app.link_button("🎙️ Unirme a la Capacitación Gratuita (Jueves y Viernes por Jitsi)", ENLACE_JITSI, use_container_width=True)
                    str_app.link_button("👥 Unirme al Grupo Oficial de WhatsApp", ENLACE_GRUPO, use_container_width=True)
                    str_app.link_button("📺 Visitar Canal de YouTube", ENLACE_YOUTUBE, use_container_width=True)
                    str_app.link_button("📘 Visitar Nuestra Página de Facebook", ENLACE_FACEBOOK, use_container_width=True)
                    str_app.link_button("🎯 Ir a Simulacros Wordwall (VIP y Gratis)", ENLACE_WORDWALL, use_container_width=True)
                    
                    c1, c2 = str_app.columns(2)
                    with c1: str_app.link_button("📲 Hablar con César (Línea 1)", f"https://wa.me/{TEL_1}?text={texto_wa}", use_container_width=True)
                    with c2: str_app.link_button("📲 Hablar con César (Línea 3)", f"https://wa.me/{TEL_3}?text={texto_wa}", use_container_width=True)
                str_app.warning("Has alcanzado el límite de 4 consultas rápidas. ¡Es momento de asegurar tu plaza con la Dirección!")
            
            else:
                if client:
                    with str_app.chat_message("assistant"):
                        with str_app.spinner("Alonso está consultando la normativa y enlaces..."):
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
                                                f"1. FILTRO DE SALUDOS/TROLLEO: Si te escriben saludos vacíos ('hola'), responde cordialmente invitandole a hacer su consulta técnica. Si detectas insultos o lenguaje obsceno, incluye la palabra clave [BLOQUEAR_USUARIO].\n"
                                                f"2. NUNCA DIGAS 've a la página de la CNSC' de forma genérica: Proporciona siempre el enlace oficial de la CNSC (https://www.cnsc.gov.co) o SIMO.\n"
                                                f"3. PROMOCIÓN DE CAPACITACIONES Y RECURSOS: Recuerda activamente que realizamos **capacitaciones gratuitas los jueves y viernes** sobre temas transversales, funcionales, competencias comportamentales y simulacros en vivo a través de nuestro enlace de Jitsi Meet ({ENLACE_JITSI}). Promociona también nuestro canal de YouTube ({ENLACE_YOUTUBE}), los simulacros en Wordwall (gratuitos y VIP por $20.000 COP en {ENLACE_WORDWALL}), la página de Facebook ({ENLACE_FACEBOOK}) y la Asesoría Personalizada de César Padilla por $120.000 COP, especificando nuestro correo de contacto ({CORREO_EMPRESA}).\n"
                                                f"4. Mantén tono profesional, experto, persuasivo y directo."
                                            )
                                        },
                                        *str_app.session_state['historial']
                                    ]
                                )
                                res_text = respuesta.choices[0].message.content
                                
                                if "[BLOQUEAR_USUARIO]" in res_text:
                                    str_app.session_state['bloqueado'] = True
                                    str_app.rerun()
                                else:
                                    str_app.write(res_text)
                                    str_app.session_state['historial'].append({"role": "assistant", "content": res_text})
                            except Exception as e:
                                str_app.error(f"Problema temporal de conexión: {e}")
                else:
                    str_app.warning("API Key no configurada.")
else:
    str_app.info("👆 Por favor, completa el formulario superior para que Alonso conozca tu perfil y comience tu asesoría.")

# 8. PIE DE PÁGINA INSTITUCIONAL (Fijo y con toda la identidad corporativa)
str_app.markdown(f"""
    <div class="footer-institucional">
        <div class="footer-title">⚖️ <span class='texto-verde'>SÍ AL MÉRITO</span> — Talleres, Cursos y Asesorías Especializadas</div>
        <div class="footer-text">
            Somos un equipo de trabajo encargado de visibilizar los Concursos de Carrera Administrativa en Colombia, para todos los interesados, Bachilleres, Técnicos, Tecnólogos y Profesionales. Estamos 24/7 para que te conviertas en un servidor público por mérito.
        </div>
        <div class="footer-contacto">
            📱 <span class='texto-whatsapp'>WhatsApp</span>: 3146715497 - 3153838792 - 3004417737 &nbsp;|&nbsp; ✉️ Correo: <span class='texto-correo'>{CORREO_EMPRESA}</span>
        </div>
    </div>
""", unsafe_allow_html=True)
