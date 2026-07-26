import streamlit as st
import json
import os

def mostrar_avisos():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #8B4513;'>📢 Avisos a la Comunidad</h2>", unsafe_allow_html=True)
    
    # --- NUEVA INTRODUCCIÓN AMIGABLE (UX) ---
    st.markdown("""
    <div style='background-color: #faead6; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 20px;'>
    👋 <b>¡Hola! Esta es la cartelera oficial de Jacobacci.</b><br>
    Acá vas a encontrar las fechas de vacunación de Zoonosis, campañas del Hospital, perritos en adopción y comunicados importantes de Patitas Felices. Revisá esta sección seguido para no perderte de nada.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    archivo_anuncios = "anuncios.json"
    if os.path.exists(archivo_anuncios):
        with open(archivo_anuncios, 'r', encoding='utf-8') as f:
            try:
                anuncios = json.load(f)
                if len(anuncios) == 0:
                    st.info("No hay avisos activos en este momento.")
                else:
                    # Recorremos y mostramos a lo grande
                    for a in anuncios:
                        emisor = a.get("emisor", "")
                        texto_corto = a.get("texto_corto", a.get("texto", ""))
                        texto_largo = a.get("texto_largo", "")
                        foto_ruta = a.get("foto_ruta", "")

                        st.markdown(f"#### 📌 {emisor}")
                        st.markdown(f"<p style='font-size: 18px; font-weight: bold; color: #5D4037;'>{texto_corto}</p>", unsafe_allow_html=True)
                        
                        if foto_ruta and os.path.exists(foto_ruta):
                            st.image(foto_ruta, use_container_width=True)
                            
                        if texto_largo:
                            st.write(texto_largo)
                            
                        st.markdown("---")
            except:
                st.error("Hubo un error leyendo los comunicados. Por favor, avisale al administrador del sistema.")
    else:
        st.info("No hay avisos activos en este momento.")
