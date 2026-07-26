import streamlit as st
import json
import os

def ir_a_inicio(): st.session_state.vista = 'inicio'

def mostrar_bienestar():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #2e7d32;'>🩺 Consultorio Frecuente</h2>", unsafe_allow_html=True)
    
    # Nota de rigor profesional y seguridad (innegociable)
    st.warning("⚠️ **Atención:** Esta sección es una guía de primeros auxilios y conocimientos generales. Toda información aquí expuesta es provista por el equipo de Zoonosis y no reemplaza el criterio médico individual. Ante cualquier síntoma severo, intoxicación o alteración repentina en el comportamiento de su mascota, la revisión final debe hacerla siempre un médico veterinario.")
    
    st.button("⬅️ Volver al Inicio", on_click=ir_a_inicio, use_container_width=True)
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
    st.button("⬅️ Volver", on_click=ir_a_inicio, use_container_width=True, key="btn_volver_salud_abajo")
