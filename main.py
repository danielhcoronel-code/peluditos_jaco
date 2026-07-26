import streamlit as st
import random
import os
import base64
import streamlit.components.v1 as components

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILOS GLOBALES
# ==========================================
st.set_page_config(page_title="Peluditos | Ing. Jacobacci", page_icon="🐾", layout="centered", initial_sidebar_state="collapsed")

def aplicar_estilos_globales():
    st.markdown("""
    <style>
        /* Tipografía redondita y amigable */
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&display=swap');
        
        /* Fondo crema clarito para toda la aplicación */
        .stApp { background-color: #FFF9F2; }
        
        /* Aplicamos la fuente a todos los textos */
        h1, h2, h3, h4, p, label, li, span { 
            font-family: 'Nunito', sans-serif !important; 
            color: #5D4037 !important; 
        }
        
        /* --- AUMENTO DE TAMAÑO DE FUENTES --- */
        p, li, label, div[data-testid="stMarkdownContainer"] {
            font-size: 18px !important;
            line-height: 1.6 !important;
        }
        h1 { font-size: 34px !important; }
        h2 { font-size: 28px !important; }
        h3 { font-size: 24px !important; }
        
        /* --- OCULTAR PUBLICIDAD Y 3 PUNTITOS (Sólo rincón derecho) --- */
        div[data-testid="stToolbar"] {
            visibility: hidden !important; 
        }

        /* --- BOTONES PRINCIPALES (Pantalla Central) --- */
        section[data-testid="stMain"] div.stButton > button:first-child {
            background-color: #FFB347 !important; 
            color: white !important; 
            border-radius: 20px !important; 
            border: none !important; 
            font-weight: 600 !important; 
            font-size: 18px !important; /* Botón más legible */
            width: 100%;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        section[data-testid="stMain"] div.stButton > button:first-child:hover { 
            background-color: #FF9800 !important; 
            transform: translateY(-2px); 
        }
        
        /* Botones de Urgencia en principal (S.O.S) */
        section[data-testid="stMain"] div.stButton > button[kind="primary"] { 
            background-color: #FF6B6B !important; 
            color: white !important;
        }
        section[data-testid="stMain"] div.stButton > button[kind="primary"]:hover { 
            background-color: #FF4757 !important; 
        }

        /* --- BOTONES DEL MENÚ LATERAL --- */
        section[data-testid="stSidebar"] div.stButton > button {
            background-color: transparent !important;
            color: #5D4037 !important;
            border-radius: 10px !important;
            box-shadow: none !important;
            padding: 8px 15px !important;
            border: none !important;
            display: flex !important;
            justify-content: flex-start !important;
        }
        
        section[data-testid="stSidebar"] div.stButton > button:hover {
            background-color: #f2e8dc !important; 
        }
        
        section[data-testid="stSidebar"] div.stButton > button p {
            font-size: 18px !important; /* Menú más legible */
            font-weight: 600 !important;
            text-align: left !important;
            margin: 0 !important;
            width: 100% !important;
        }
    </style>
    """, unsafe_allow_html=True)

aplicar_estilos_globales()

# ==========================================
# 2. FUNCIÓN DE SONIDO DE BIENVENIDA
# ==========================================
def jugar_sonido_bienvenida():
    if 'sonido_jugado' not in st.session_state:
        st.session_state.sonido_jugado = False

    if not st.session_state.sonido_jugado and st.session_state.vista == 'inicio':
        sonidos = ["ladrido.mp3", "maullido.mp3"]
        sonido_elegido = random.choice(sonidos)
        
        if os.path.exists(sonido_elegido):
            with open(sonido_elegido, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                
            reproductor_oculto = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
            st.markdown(reproductor_oculto, unsafe_allow_html=True)
            st.session_state.sonido_jugado = True

# ==========================================
# 3. IMPORTACIÓN DE VISTAS
# ==========================================
from vista_tutor import mostrar_tutor
from vista_inicio import mostrar_inicio
from vista_avisos import mostrar_avisos
from vista_comercios import mostrar_comercios
from vista_formulario import mostrar_formulario
from vista_modificar import mostrar_modificar
from vista_bienestar import mostrar_bienestar
from vista_sos import mostrar_sos
from vista_cartelera import mostrar_cartelera
from vista_admin import mostrar_admin
from vista_manual import mostrar_manual 
from vista_quienes_somos import mostrar_quienes_somos
from vista_cumples import mostrar_cumples
from vista_ranking import mostrar_ranking
from vista_arcoiris import mostrar_arcoiris
from vista_urgencias import mostrar_emitir_alerta
from vista_hdt import mostrar_hdt
from vista_razas import mostrar_razas
from vista_consultas import mostrar_consultas

# ==========================================
# 4. MEMORIA Y CONTROL DE IDENTIDAD
# ==========================================
if 'vista' not in st.session_state:
    st.session_state.vista = 'inicio'

if 'tutor_registrado' not in st.session_state:
    st.session_state.tutor_registrado = False

# ==========================================
# 4.5 BARRA LATERAL (MENÚ ESTÁNDAR OFICIAL)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; margin-bottom: 15px; padding-top: 10px;">
        <div style="font-size: 40px; margin-right: 15px;">🧑‍🌾🐾</div>
        <div>
            <h4 style="margin: 0; color: #5D4037; font-size: 20px;">Vecino de Jaco</h4>
            <p style="margin: 0; font-size: 14px; color: #888;">Red Peluditos</p>
        </div>
    </div>
    <hr style="margin-top: 0px; margin-bottom: 15px;">
    """, unsafe_allow_html=True)
    
    if st.button("🏠 Inicio", use_container_width=True):
        st.session_state.vista = 'inicio'
        st.rerun()
    if st.button("📖 Manual del Usuario", use_container_width=True):
        st.session_state.vista = 'faq'
        st.rerun()
    if st.button("🩺 Consultorio Médico", use_container_width=True):
        st.session_state.vista = 'consultas'
        st.rerun()
    if st.button("🐾 Registrar Mascota", use_container_width=True):
        st.session_state.vista = 'formulario'
        st.rerun()
    if st.button("🆘 S.O.S Alertas", use_container_width=True):
        st.session_state.vista = 'urgencias'
        st.rerun()
    if st.button("🏡 Hogar de Tránsito", use_container_width=True):
        st.session_state.vista = 'hdt'
        st.rerun()
    if st.button("🗓️ Información del día", use_container_width=True):
        st.session_state.vista = 'avisos'
        st.rerun()
    if st.button("🏪 Comercios Amigos", use_container_width=True):
        st.session_state.vista = 'comercios'
        st.rerun()
    if st.button("✏️ Modificar Ficha", use_container_width=True):
        st.session_state.vista = 'modificar'
        st.rerun()
    if st.button("⚙️ Configuración", use_container_width=True):
        st.session_state.vista = 'admin'
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #8B4513;'>📢 ¡Hagamos ruido!</h3>", unsafe_allow_html=True)
    st.write("Ayudanos a tejer esta red vecinal. Mientras más seamos, más peluditos salvamos.")
    
    texto_viral = "¡Hola! Descubrí una app espectacular para los que amamos a nuestras mascotas. Tiene todo lo que necesitás y, además, nos hace parte de una red de contención vecinal que hace mucha falta. Sumate desde este link: https://peluditosjaco.streamlit.app"
    texto_formateado = texto_viral.replace(" ", "%20")
    link_whatsapp = f"https://api.whatsapp.com/send?text={texto_formateado}"
    
    boton_wa = f"""
    <a href="{link_whatsapp}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #25D366; color: white; padding: 12px; border-radius: 20px; text-align: center; font-weight: bold; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-family: 'Nunito', sans-serif;">
            <span style="font-size: 18px;">💬</span> Compartir en WhatsApp
        </div>
    </a>
    """
    st.markdown(boton_wa, unsafe_allow_html=True)

# ==========================================
# 5. EL DIRECTOR DE TRÁNSITO (EFECTO ASCENSOR Y VIDEO)
# ==========================================
components.html(
    """
    <script>
        setTimeout(function() {
            var doc = window.parent.document;
            
            // 1. Efecto ascensor al cargar
            var contenedores = doc.querySelectorAll('.main, .stApp, section[data-testid="stMain"], main, div[data-testid="stVerticalBlock"]');
            contenedores.forEach(function(c) {
                c.scrollTo({top: 0, behavior: 'instant'});
                c.scrollTop = 0;
            });
            window.parent.scrollTo(0, 0);
            var banderita = doc.getElementById('tope-pagina');
            if (banderita) banderita.scrollIntoView({behavior: 'instant', block: 'start'});

            // 2. Arranque automático de los videos
            var videos = doc.querySelectorAll('video');
            videos.forEach(function(vid) {
                vid.muted = true;
                var playPromise = vid.play();
                if (playPromise !== undefined) {
                    playPromise.catch(function(e){});
                }
            });
        }, 250);
    </script>
    """,
    height=0
)

if st.session_state.vista == 'inicio':
    mostrar_inicio()
    jugar_sonido_bienvenida()   
elif st.session_state.vista == 'formulario':
    if not st.session_state.tutor_registrado:
        st.warning("👋 ¡Qué bueno que quieras sumar a tu compañero! Primero necesitamos crear tu perfil de Tutor.")
        mostrar_tutor()
    else:
        mostrar_formulario()
elif st.session_state.vista == 'avisos':
    mostrar_avisos()
elif st.session_state.vista == 'comercios':
    mostrar_comercios()
elif st.session_state.vista == 'modificar':
    mostrar_modificar()
elif st.session_state.vista == 'bienestar':
    mostrar_bienestar()
elif st.session_state.vista == 'sos':
    mostrar_sos()
elif st.session_state.vista == 'cartelera':
    mostrar_cartelera()
elif st.session_state.vista == 'admin':
    mostrar_admin()
elif st.session_state.vista == 'faq':
    mostrar_manual()
elif st.session_state.vista == 'quienes_somos':
    mostrar_quienes_somos()
elif st.session_state.vista == 'cumples':
    mostrar_cumples()
elif st.session_state.vista == 'ranking':
    mostrar_ranking()
elif st.session_state.vista == 'arcoiris':
    mostrar_arcoiris()
elif st.session_state.vista == 'urgencias':
    mostrar_emitir_alerta()
elif st.session_state.vista == 'hdt':
    mostrar_hdt()
elif st.session_state.vista == 'razas':
    mostrar_razas()
elif st.session_state.vista == 'consultas':
    mostrar_consultas()
    
# ==========================================
# 6. SECCIÓN SOLIDARIA PERMANENTE
# ==========================================
st.markdown("---")
st.info("🐾 **Solidaridad en Jaco:** Con tu aporte voluntario colaborás directamente con Patitas Felices y ayudás a mantener esta plataforma gratuita para los vecinos.")
if st.button("💛 Convertirme en Padrino", use_container_width=True, key="btn_solidario"):
    st.success("¡Gracias de corazón! Próximamente habilitaremos el link seguro de Mercado Pago.")
