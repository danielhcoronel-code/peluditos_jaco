import streamlit as st
import csv
from collections import Counter
import os

def mostrar_ranking():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN (SUPERIOR) ===
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Volver", key="btn_volver_arriba_ranking", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav2:
        if st.button("☰ Menú Principal", key="btn_menu_arriba_ranking", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    st.markdown("---")
    # =========================================
    
    st.markdown("<h2 style='text-align: center; color: #FFD700;'>🏆 Ranking de Héroes del Año</h2>", unsafe_allow_html=True)
    st.write("Estos son los vecinos que más mascotas han ayudado a reencontrar con sus familias. ¡Gracias por su compromiso con Jacobacci!")

    archivo = "base_rescates.csv"
    if not os.path.exists(archivo):
        st.info("Todavía no hay rescates registrados. ¡Sé el primero en ayudar!")
    else:
        rescatistas = []
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rescatistas.append(row['Rescatista'])

        if not rescatistas:
            st.info("Todavía no hay rescates registrados.")
        else:
            # Contamos las apariciones de cada nombre
            conteo = Counter(rescatistas)
            # Ordenamos de mayor a menor
            top_rescatistas = conteo.most_common()

            st.markdown("---")
            
            # Mostramos el podio
            for i, (nombre, cantidad) in enumerate(top_rescatistas):
                if i == 0: 
                    st.markdown(f"### 🥇 1er Puesto: {nombre} - **{cantidad} rescates**")
                elif i == 1:
                    st.markdown(f"### 🥈 2do Puesto: {nombre} - **{cantidad} rescates**")
                elif i == 2:
                    st.markdown(f"### 🥉 3er Puesto: {nombre} - **{cantidad} rescates**")
                else:
                    st.markdown(f"🏅 {nombre}: **{cantidad} rescates**")

            st.markdown("---")
            st.info("🎁 **Premio:** 7kg de alimento Premium. Entrega: 29 de Abril (Día del Animal).")

    # === BOTONERA DE NAVEGACIÓN (INFERIOR) ===
    st.markdown("---")
    col_nav3, col_nav4 = st.columns(2)
    with col_nav3:
        if st.button("⬅️ Volver", key="btn_volver_abajo_ranking", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav4:
        if st.button("☰ Menú Principal", key="btn_menu_abajo_ranking", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    # =========================================
