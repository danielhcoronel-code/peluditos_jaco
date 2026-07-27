import streamlit as st
import os
import json
from datetime import datetime

ARCHIVO_CONSULTAS = "consultas.json"

def cargar_consultas():
    if os.path.exists(ARCHIVO_CONSULTAS):
        with open(ARCHIVO_CONSULTAS, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def mostrar_consultas():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN (SUPERIOR) ===
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Volver", key="btn_volver_arriba_consultas", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav2:
        if st.button("☰ Menú Principal", key="btn_menu_arriba_consultas", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    st.markdown("---")
    # =========================================

    # Título principal
    st.markdown("<h2 style='text-align: center;'>🩺 Consultorio Médico</h2>", unsafe_allow_html=True)
    
    # Creamos dos columnas: una para la foto y otra para el texto general
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Cargamos la imagen de los doctores
        try:
            st.image("doctores-2.png", use_container_width=True)
        except:
            st.info("🖼️ Falta la imagen doctores-2.png en la carpeta")
            
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("Elegí a quién querés consultarle hoy para sacarte las dudas. Recordá que esta es una guía de primeros auxilios y conocimientos generales de la manada. **Ante síntomas severos o dudas urgentes, la revisión final siempre debe hacerla un médico veterinario.**")

    st.markdown("---")

    # Creamos las dos pestañas
    tab_roco, tab_aquita = st.tabs(["🐶 El rincón de Roco", "🐱 Los consejos de Aquí-ta"])
    
    consultas = cargar_consultas()
    consultas_perros = [c for c in consultas if c.get("categoria", "Perros") == "Perros"]
    consultas_gatos = [c for c in consultas if c.get("categoria") == "Gatos"]

    # ==========================================
    # PESTAÑA DE ROCO
    # ==========================================
    with tab_roco:
        st.markdown("<h3 style='color: #8B4513;'>🐶 Roco te orienta</h3>", unsafe_allow_html=True)
        st.write("¡Guau! Llevo más de 15 años siendo el rey absoluto de mi casa, rodeado de mimos, siestas cómodas y excelente atención. Nunca me faltó nada, así que conozco de primera mano la importancia de una buena cucha, una dieta sana y el calor de una familia. Preguntame lo que necesites sobre nuestros cuidados.")
        
        st.markdown("**Tus dudas perrunas:**")
        
        if not consultas_perros:
            st.info("Todavía no subimos respuestas de Roco. ¡Volvé pronto!")
        else:
            for c in consultas_perros:
                with st.expander(f"🐾 {c['pregunta']}"):
                    st.write(c['respuesta'])

    # ==========================================
    # PESTAÑA DE AQUÍ-TA
    # ==========================================
    with tab_aquita:
        st.markdown("<h3 style='color: #5D4037;'>🐱 Aquí-ta te aconseja</h3>", unsafe_allow_html=True)
        st.write("¡Miau! Los felinos somos un mundo aparte. Elegantes, independientes pero muy mimosos cuando queremos. Acá te dejo los mejores consejos para que nos entiendas mejor.")
        
        st.markdown("**Tus dudas felinas:**")
        
        if not consultas_gatos:
            st.info("Todavía no subimos respuestas de Aquí-ta. ¡Volvé pronto!")
        else:
            for c in consultas_gatos:
                with st.expander(f"🐾 {c['pregunta']}"):
                    st.write(c['respuesta'])

    # ==========================================
    # BUZÓN DE NUEVAS CONSULTAS (CAPTURA DE PREGUNTAS)
    # ==========================================
    st.markdown("---")
    st.markdown("<h4 style='text-align: center; color: #5D4037;'>¿No encontraste lo que buscabas?</h4>", unsafe_allow_html=True)
    st.write("Dejale tu pregunta a Roco o a Aquí-ta. El equipo veterinario la revisará y pronto aparecerá en la lista de respuestas.")
    
    with st.form("form_nuevas_consultas", clear_on_submit=True):
        nueva_pregunta = st.text_area("Escribí tu consulta acá:")
        enviado = st.form_submit_button("Enviar consulta a la Manada")
        
        if enviado:
            if nueva_pregunta.strip() == "":
                st.warning("Por favor, escribí una pregunta antes de enviar.")
            else:
                # Se crea y guarda en un archivo de texto dentro de tu carpeta
                with open("nuevas_consultas.txt", "a", encoding="utf-8") as f:
                    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{fecha_hora}] {nueva_pregunta}\n")
                st.success("¡Tu consulta fue enviada con éxito! Próximamente la sumaremos al consultorio.")

    # === BOTONERA DE NAVEGACIÓN (INFERIOR) ===
    st.markdown("---")
    col_nav3, col_nav4 = st.columns(2)
    with col_nav3:
        if st.button("⬅️ Volver", key="btn_volver_abajo_consultas", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav4:
        if st.button("☰ Menú Principal", key="btn_menu_abajo_consultas", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    # =========================================
