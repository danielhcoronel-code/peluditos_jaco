import streamlit as st
import os
import json

# --- SVG DE UNA SOLA HUELLA PARA EVITAR CONFUSIÓN VISUAL ---
def get_paw_svg(color):
    # Dibuja matemáticamente una única huella perfecta en lugar de usar el emoji doble
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="18" height="18" style="margin-right: 3px; vertical-align: middle;">
        <path fill="{color}" d="M226.5 92.9c14.3 7.3 28.9 21.3 32.8 45.2c3.1 19.4-1.6 39.8-36 67.3c-23.6 18.7-48.1 11.8-59 2.4C153.3 198.2 145 182.4 150.1 160.5c6.8-29.4 43.5-75.3 76.4-67.6zM61.5 257.9c-26.6-14.9-50-2.7-58.4 26.3c-7.5 26.1 4.3 56.5 26.1 68c22.6 12 50 2.7 58.4-26.3c7.6-26.1-4.3-56.5-26.1-68zm389 26.3c-8.4-29-31.8-41.2-58.4-26.3c-21.8 11.5-33.6 41.9-26.1 68c8.4 29 31.8 41.2 58.4 26.3c21.8-11.5 33.6-41.9 26.1-68zm-8-204.4c-28.7-5.9-63 35.6-70.1 66.5c-4.7 20.3 3.1 36.3 14 45.7c11 9.4 35.6 16.6 59.2-2.1c34.1-27.2 39.1-47.3 36-66.5c-4.1-25-18.4-38.3-39.1-43.6zM256 258.3c-41.5 0-74.8 28.7-88.5 68.3c-11.6 33.5-2 69.7 13.9 92.5c23.6 33.9 73 50.9 100.8 50.9c27.8 0 77.2-17 100.8-50.9c15.9-22.8 25.5-59 13.9-92.5c-13.7-39.6-47-68.3-88.5-68.3z"/>
    </svg>
    """

def dibujar_huellas(puntuacion):
    try:
        puntos = int(puntuacion)
    except:
        puntos = 3
    html = ""
    for i in range(puntos):
        html += get_paw_svg("#4CAF50") # Huella verde encendida
    for i in range(5 - puntos):
        html += get_paw_svg("#E0E0E0") # Huella gris apagada
    return html

def mostrar_razas():
    # El ancla para que el ascensor llegue arriba
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    col_volver, _ = st.columns([1, 2])
    with col_volver:
        if st.button("⬅️ Volver al Inicio", use_container_width=True):
            st.session_state.vista = 'inicio'
            st.rerun()

    st.markdown("<h2 style='text-align: center; color: #5D4037;'>📚 Enciclopedia Canina y Felina</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    if os.path.exists("razas.json"):
        try:
            with open("razas.json", 'r', encoding='utf-8') as f:
                catalogo = json.load(f)
                
            for raza in catalogo:
                with st.container(border=True):
                    # Título de la raza
                    st.markdown(f"<h2 style='color: #4CAF50; margin-bottom: 5px; margin-top: 5px;'>{raza.get('nombre', '')}</h2>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 15px; font-style: italic; color: #7f8c8d; margin-bottom: 20px;'>{raza.get('resumen', '')}</p>", unsafe_allow_html=True)
                    
                    # Estructura a dos columnas (Foto izquierda, Ficha derecha)
                    col_img, col_datos = st.columns([1.3, 1])
                    with col_img:
                        nombre_archivo = raza.get("foto_archivo", "")
                        ruta_foto = os.path.join("fotos_razas", nombre_archivo)
                        
                        if nombre_archivo != "" and os.path.isfile(ruta_foto):
                            st.image(ruta_foto, use_container_width=True)
                        else:
                            st.info("📷 Foto en camino")
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.write(raza.get('descripcion', ''))
                    
                    with col_datos:
                        # Cuadro de Apariencia
                        st.markdown("""
                        <div style='background-color: #f9f9f9; padding: 10px 15px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 10px;'>
                            <h4 style='color: #2c3e50; margin: 0; font-size: 16px;'>Apariencia</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Badges (Etiquetas de colores)
                        st.markdown(f"""
                        <div style='margin-bottom: 25px; margin-top: 5px;'>
                            <span style='background-color: #4CAF50; color: white; padding: 5px 12px; border-radius: 15px; font-size: 13px; font-weight: bold; margin-right: 5px; display: inline-block; margin-bottom: 8px;'>Tamaño: {raza.get('tamano', 'No definido')}</span>
                            <span style='background-color: #4CAF50; color: white; padding: 5px 12px; border-radius: 15px; font-size: 13px; font-weight: bold; margin-right: 5px; display: inline-block; margin-bottom: 8px;'>Pelo: {raza.get('pelo', 'No definido')}</span>
                            <span style='background-color: #4CAF50; color: white; padding: 5px 12px; border-radius: 15px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 8px;'>Origen: {raza.get('origen', 'Desconocido')}</span>
                        </div>
                        """, unsafe_allow_html=True)

                        # Cuadro de Características
                        st.markdown("""
                        <div style='background-color: #f9f9f9; padding: 10px 15px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 15px;'>
                            <h4 style='color: #2c3e50; margin: 0; font-size: 16px;'>Características</h4>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Dibujamos las puntuaciones con las nuevas huellas vectoriales
                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 14px; color: #5D4037;">Convivencia con niños</span>
                            <span style="display: flex;">{dibujar_huellas(raza.get('ninos', 3))}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 14px; color: #5D4037;">Nivel de energía</span>
                            <span style="display: flex;">{dibujar_huellas(raza.get('energia', 3))}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 14px; color: #5D4037;">Salud / Rusticidad</span>
                            <span style="display: flex;">{dibujar_huellas(raza.get('salud', 3))}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 14px; color: #5D4037;">Inteligencia / Apego</span>
                            <span style="display: flex;">{dibujar_huellas(raza.get('inteligencia', 3))}</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
        except Exception as e:
            st.error(f"Ocurrió un error al cargar el catálogo de razas. Falla técnica: {e}")
    else:
        st.warning("El catálogo de razas se está construyendo. ¡Pronto habrá novedades!")
