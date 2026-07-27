import streamlit as st
import json
import os
from datetime import datetime

def mostrar_comercios():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN (SUPERIOR) ===
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Volver", key="btn_volver_arriba_comercios", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav2:
        if st.button("☰ Menú Principal", key="btn_menu_arriba_comercios", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    st.markdown("---")
    # =========================================
    
    st.markdown("<h2 style='text-align: center; color: #e65100;'>🏪 Comercios Amigos</h2>", unsafe_allow_html=True)
    
    # --- NUEVA INTRODUCCIÓN AMIGABLE (UX) ---
    st.markdown("""
    <div style='background-color: #fff3e0; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 20px; border: 1px solid #ffe0b2;'>
    👋 <b>¡Apoyemos a quienes nos apoyan!</b><br>
    Acá vas a encontrar a todos los comercios locales que le dan una pata a <b>Patitas Felices</b>. Comprando en estos locales o aprovechando sus beneficios, ayudás a sostener esta red solidaria.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    archivo_comercios = "comercios.json"
    if os.path.exists(archivo_comercios):
        with open(archivo_comercios, 'r', encoding='utf-8') as f:
            try:
                comercios = json.load(f)
                
                # --- LÓGICA DE VENCIMIENTO AUTOMÁTICO ---
                comercios_activos = []
                hoy = datetime.now().date()
                
                for c in comercios:
                    vencimiento_str = c.get("vencimiento", "")
                    if vencimiento_str:
                        try:
                            # Convertimos el texto "YYYY-MM-DD" a una fecha real
                            vencimiento_date = datetime.strptime(vencimiento_str, "%Y-%m-%d").date()
                            if vencimiento_date >= hoy:
                                comercios_activos.append(c)
                        except ValueError:
                            # Si tipeaste mal la fecha en el JSON, lo mostramos igual por las dudas para no ocultar un sponsor vigente
                            comercios_activos.append(c)
                    else:
                        # Si no tiene fecha de vencimiento anotada, es permanente
                        comercios_activos.append(c)

                if len(comercios_activos) == 0:
                    st.info("Aún no hay comercios adheridos (o sus promociones caducaron). ¡Pronto sumaremos más beneficios!")
                else:
                    # Dibujamos solo los comercios que pasaron el filtro de fecha
                    for c in comercios_activos:
                        st.markdown(f"### 🛍️ {c.get('nombre', 'Comercio Amigo')}")
                        
                        # Si es Premium, lo resaltamos un poquito
                        categoria = c.get('categoria', '')
                        if "Premium" in categoria:
                            st.markdown(f"⭐ <span style='color:#e65100; font-weight:bold;'>{categoria}</span>", unsafe_allow_html=True)
                        
                        st.success(f"🎁 **Beneficio / Aporte:** {c.get('beneficio', '')}")
                        
                        if c.get('direccion'):
                            st.write(f"📍 **Dirección/Contacto:** {c['direccion']}")
                        
                        foto_ruta = c.get("foto_ruta", "")
                        if foto_ruta and os.path.exists(foto_ruta):
                            st.image(foto_ruta, width=300) # Tamaño controlado
                            
                        st.markdown("---")
            except:
                st.error("Hubo un error cargando los comercios. Por favor, avisale al administrador del sistema.")
    else:
        st.info("Aún no hay comercios adheridos. ¡Pronto sumaremos beneficios!")

    # === BOTONERA DE NAVEGACIÓN (INFERIOR) ===
    col_nav3, col_nav4 = st.columns(2)
    with col_nav3:
        if st.button("⬅️ Volver", key="btn_volver_abajo_comercios", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav4:
        if st.button("☰ Menú Principal", key="btn_menu_abajo_comercios", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    # =========================================
