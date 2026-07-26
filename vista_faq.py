import streamlit as st

def mostrar_faq():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center;'>Preguntas Frecuentes</h2>", unsafe_allow_html=True)
    st.info("Respuestas a dudas comunes.")
