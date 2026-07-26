import streamlit as st

# Importamos los estilos
from estilos import aplicar_estilos

# Importamos las pantallas
from vista_inicio import mostrar_inicio
from vista_cartelera import mostrar_cartelera
from vista_formulario import mostrar_formulario
from vista_modificar import mostrar_modificar
from vista_faq import mostrar_faq
from vista_urgencias import mostrar_emitir_alerta
from vista_sos import mostrar_sos
from vista_ranking import mostrar_ranking

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mi Mascota y Yo - Jacobacci", page_icon="🐾", layout="centered")

# --- APLICAR ESTILOS ---
aplicar_estilos()

# --- NAVEGACIÓN ---
if 'vista' not in st.session_state: st.session_state.vista = 'inicio'
if 'mascota_a_editar' not in st.session_state: st.session_state.mascota_a_editar = None

def ir_a_inicio(): 
    st.session_state.vista = 'inicio'
    st.session_state.mascota_a_editar = None 

# --- ENCABEZADO FIJO ---
# Mantenemos solo el logo y el botón de navegación
col_logo, col_vacia, col_boton = st.columns([1, 2, 1])
with col_logo:
    try: st.image("logo_final.png", width=100) 
    except: st.warning("Logo no encontrado")

with col_boton:
    st.write("") 
    if st.session_state.vista == 'inicio':
        if st.button("🔗 Invitar"): st.success("¡Copiado!")
    else:
        st.button("⬅️ Volver", on_click=ir_a_inicio)

st.markdown("---")

# ==========================================
# GESTOR DE RUTAS (ROUTER)
# ==========================================
if st.session_state.vista == 'inicio':
    mostrar_inicio()
elif st.session_state.vista == 'cartelera':
    mostrar_cartelera()
elif st.session_state.vista == 'formulario':
    mostrar_formulario()
elif st.session_state.vista == 'modificar':
    mostrar_modificar()
elif st.session_state.vista == 'faq':
    mostrar_faq()
elif st.session_state.vista == 'emitir_alerta':
    mostrar_emitir_alerta()
elif st.session_state.vista == 'sos':
    mostrar_sos()
elif st.session_state.vista == 'ranking':
    mostrar_ranking()
