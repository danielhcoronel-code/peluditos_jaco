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
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;800&display=swap');
        .stApp { background-color: #FFF9F2; }
        h1, h2, h3, h4, p, label, li, span { font-family: 'Nunito', sans-serif !important; color: #5D4037 !important; }
        p, li, label, div[data-testid="stMarkdownContainer"] { font-size: 18px !important; line-height: 1.6 !important; }
        h1 { font-size: 34px !important; }
        h2 { font-size: 28px !important; }
        h3 { font-size: 24px !important; }
        header[data-testid="stHeader"] { display: none !important; height: 0px !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        [data-testid="stSidebar"] { display: none !important; }
        .stAppDeployButton { display: none !important; }
        [data-testid="stToolbar"] { display: none !important; }
        footer { display: none !important; }
        .block-container { padding-top: 1.5rem !important; }
        .stButton > button { border-radius: 12px !important; font-weight: 800 !important; font-size: 18px !important; transition: all 0.3s ease; border: 2px solid rgba(0,0,0,0.05) !important; box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important; background-color: transparent !important; color: #5D4037 !important; justify-content: flex-start !important; }
        .stButton > button:hover { transform: translateY(-2px); background-color: #f2e8dc !important; }
        .stButton > button[kind="primary"] { background-color: #FF6B6B !important; color: white !important; justify-content: center !important; }
        .stButton > button[kind="primary"]:hover { background-color: #FF4757 !important; }
    </style>
    """, unsafe_allow_html=True)

aplicar_estilos_globales()

# ==========================================
# 1.5 PANTALLA DE PRE-INICIO (BIENVENIDA Y ACCESOS)
# ==========================================
if 'pre_inicio_visto' not in st.session_state:
    st.session_state.pre_inicio_visto = False

if not st.session_state.pre_inicio_visto:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_dummy1, col_centro, col_dummy2 = st.columns([1, 5, 1])
    with col_centro:
        with st.container(border=True):
            st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🐾 Peluditos en Red</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; color: #5D4037;'>Ingeniero Jacobacci para toda la Región</h3>", unsafe_allow_html=True)
            st.markdown("""
            <p style='text-align: center; font-size: 18px; color: #5D4037; line-height: 1.6; margin-top: 20px;'>
                La primera aplicación de <b>Ingeniero Jacobacci</b> para toda la región, pensada y construida para el registro, cuidado y protección de nuestras mascotas.
            </p>
            <p style='text-align: center; font-size: 16px; color: #888; margin-bottom: 25px;'>
                ¿Es tu primera vez acá? Conocé nuestra historia o ingresá directamente al sistema.
            </p>
            """, unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🚀 Continuar a Inicio", type="primary", use_container_width=True):
                    st.session_state.pre_inicio_visto = True
                    st.session_state.vista = 'inicio'
                    st.rerun()
            with col_btn2:
                if st.button("👥 Quiénes Somos", use_container_width=True):
                    st.session_state.pre_inicio_visto = True
                    st.session_state.vista = 'quienes_somos'
                    st.rerun()
    st.stop()

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
                b64 = base64.b64encode(f.read()).decode()
            reproductor_oculto = f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
            st.markdown(reproductor_oculto, unsafe_allow_html=True)
            st.session_state.sonido_jugado = True

# ==========================================
# 2.5 FUNCIÓN FLOTANTE: CÓMO INSTALAR LA APP
# ==========================================
@st.dialog("📲 Instalar Peluditos en tu Celular")
def mostrar_guia_instalacion():
    st.markdown("<p style='text-align: center; font-size: 16px; color: #5D4037;'>¡Tené la app siempre a mano para cualquier urgencia! Seguí estos 3 pasos según tu celular:</p>", unsafe_allow_html=True)
    tab_android, tab_apple = st.tabs(["🤖 Si tenés Android", "🍎 Si tenés iPhone"])
    with tab_android:
        st.markdown("<ol style='color: #5D4037; font-size: 16px; line-height: 1.8;'><li>Abrí esta página en <b>Google Chrome</b>.</li><li>Tocá los <b>tres puntitos (⋮)</b> arriba a la derecha.</li><li>Elegí la opción <b>'Agregar a la pantalla principal'</b> o <b>'Instalar aplicación'</b>.</li></ol>", unsafe_allow_html=True)
    with tab_apple:
        st.markdown("<ol style='color: #5D4037; font-size: 16px; line-height: 1.8;'><li>Abrí esta página en <b>Safari</b>.</li><li>Tocá el ícono de <b>Compartir</b> (el cuadradito con la flecha hacia arriba 📤).</li><li>Elegí <b>'Agregar a Inicio'</b>.</li></ol>", unsafe_allow_html=True)

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
# 4. NAVEGACIÓN
# ==========================================
if 'vista' not in st.session_state: st.session_state.vista = 'inicio'
if 'vista_anterior' not in st.session_state: st.session_state.vista_anterior = 'inicio'
if 'tutor_registrado' not in st.session_state: st.session_state.tutor_registrado = False

def navegar_a(nueva_vista):
    st.session_state.vista_anterior = st.session_state.vista
    st.session_state.vista = nueva_vista
    st.rerun()

def mostrar_menu_principal():
    st.markdown("<h2 style='text-align: center;'>Menú Principal</h2>", unsafe_allow_html=True)
    if st.button("🏠 Portada de Inicio", width="stretch"): navegar_a('inicio')
    if st.button("📲 Instalar App en el Celular", width="stretch"): mostrar_guia_instalacion()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👥 Quiénes Somos", width="stretch"): navegar_a('quienes_somos')
    with col2:
        if st.button("📖 Manual de Uso", width="stretch"): navegar_a('faq')
    st.markdown("---")
    if st.button("⬅️ Volver a donde estaba", width="stretch"): navegar_a(st.session_state.vista_anterior)

# ==========================================
# 5. EL DIRECTOR DE TRÁNSITO (AUDIO PERMITIDO)
# ==========================================
components.html(
    """
    <script>
        setTimeout(function() {
            var doc = window.parent.document;
            var videos = doc.querySelectorAll('video');
            videos.forEach(function(vid) {
                // ELIMINAMOS vid.muted = true para permitir sonido
                var playPromise = vid.play();
                if (playPromise !== undefined) {
                    playPromise.catch(function(e){});
                }
            });
        }, 250);
    </script>
    """, height=0
)

# === RUTEO PRINCIPAL ===
if st.session_state.vista == 'menu':
    mostrar_menu_principal()
elif st.session_state.vista == 'inicio':
    mostrar_inicio()
    jugar_sonido_bienvenida()   
elif st.session_state.vista == 'formulario':
    if not st.session_state.tutor_registrado: mostrar_tutor()
    else: mostrar_formulario()
elif st.session_state.vista == 'avisos': mostrar_avisos()
elif st.session_state.vista == 'comercios': mostrar_comercios()
elif st.session_state.vista == 'modificar': mostrar_modificar()
elif st.session_state.vista == 'bienestar': mostrar_bienestar()
elif st.session_state.vista == 'sos': mostrar_sos()
elif st.session_state.vista == 'cartelera': mostrar_cartelera()
elif st.session_state.vista == 'faq': mostrar_manual()
elif st.session_state.vista == 'quienes_somos': mostrar_quienes_somos()
elif st.session_state.vista == 'cumples': mostrar_cumples()
elif st.session_state.vista == 'ranking': mostrar_ranking()
elif st.session_state.vista == 'arcoiris': mostrar_arcoiris()
elif st.session_state.vista == 'urgencias': mostrar_emitir_alerta()
elif st.session_state.vista == 'hdt': mostrar_hdt()
elif st.session_state.vista == 'razas': mostrar_razas()
elif st.session_state.vista == 'consultas': mostrar_consultas()
