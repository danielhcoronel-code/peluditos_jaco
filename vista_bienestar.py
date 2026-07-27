import streamlit as st
import json
import os

def mostrar_bienestar():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN (SUPERIOR) ===
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Volver", key="btn_volver_arriba_bienestar", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav2:
        if st.button("☰ Menú Principal", key="btn_menu_arriba_bienestar", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    st.markdown("---")
    # =========================================
    
    st.markdown("<h2 style='text-align: center; color: #2e7d32;'>🩺 Consultorio Frecuente</h2>", unsafe_allow_html=True)
    
    # Nota de rigor profesional y seguridad (innegociable)
    st.warning("⚠️ **Atención:** Esta sección es una guía de primeros auxilios y conocimientos generales. Toda información aquí expuesta es provista por el equipo de Zoonosis y no reemplaza el criterio médico individual. Ante cualquier síntoma severo, intoxicación o alteración repentina en el comportamiento de su mascota, la revisión final debe hacerla siempre un médico veterinario.")
    st.markdown("---")

    archivo_salud = "salud.json"
    
    if os.path.exists(archivo_salud):
        with open(archivo_salud, 'r', encoding='utf-8') as f:
            try:
                preguntas = json.load(f)
                if len(preguntas) == 0:
                    st.info("Aún no hay consultas cargadas. Zoonosis está preparando el material.")
                else:
                    # Usamos st.expander para que se vea como un diccionario ordenado
                    for item in preguntas:
                        with st.expander(f"❓ {item['pregunta']}"):
                            st.write(item['respuesta'])
            except:
                st.error("Hubo un error cargando los datos de salud.")
    else:
        st.info("Aún no hay consultas frecuentes cargadas. Zoonosis está preparando el material.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN (INFERIOR) ===
    st.markdown("---")
    col_nav3, col_nav4 = st.columns(2)
    with col_nav3:
        if st.button("⬅️ Volver", key="btn_volver_abajo_bienestar", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav4:
        if st.button("☰ Menú Principal", key="btn_menu_abajo_bienestar", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    # =========================================
