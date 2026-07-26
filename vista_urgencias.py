import streamlit as st
import folium
from streamlit_folium import st_folium
import urllib.parse
import os

def mostrar_emitir_alerta():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # Título de la Emergencia
    st.markdown("<h2 style='text-align: center; color: #FF4C4C;'>🚨 S.O.S. PELUDITO EN PELIGRO</h2>", unsafe_allow_html=True)

    # ==========================================
    # GUÍA RÁPIDA (Versión Pro)
    # ==========================================
    st.markdown("""
    <div style='background-color: #ffe6e6; padding: 15px; border-radius: 8px; border: 2px solid #ff4c4c; margin-bottom: 20px;'>
    <h4 style='color: #cc0000; margin-top: 0;'>🛑 CÓMO ACTUAR EN ESTA EMERGENCIA:</h4>
    <ol style='color: #555; margin-bottom: 0;'>
        <li><b>Seguridad primero:</b> Asegurate de que no corrés riesgo al ayudar.</li>
        <li><b>Ubicación:</b> Tocá el mapa para marcar el punto exacto.</li>
        <li><b>Evidencia (Clave):</b> Si podés, sacá una foto. Ayuda a los socorristas a saber qué equipo llevar (camilla, medicamentos, etc.).</li>
        <li><b>Dispará la alarma:</b> Completá tus datos y enviá el aviso a la guardia 24hs.</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

    # Botón de escape rápido al Inicio
    if st.button("⬅️ Volver al Inicio", use_container_width=True):
        st.session_state.alerta_generada = False
        st.session_state.vista = 'inicio'
        st.rerun()

    # Si la alerta ya se generó, mostramos el botón de WhatsApp
    if st.session_state.get("alerta_generada", False):
        st.success("✅ ¡Situación registrada! Hacé clic abajo para enviar el aviso a la guardia.")
        st.markdown(f"""
        <a href="{st.session_state.link_wa}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-size: 18px; font-weight: bold; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                💬 ENVIAR AVISO AL WHATSAPP DE LA GUARDIA
            </div>
        </a>
        """, unsafe_allow_html=True)
        return

    # ==========================================
    # 1. MAPA DE UBICACIÓN
    # ==========================================
    st.markdown("### 📍 1. ¿Dónde estás ahora?")
    st.write("Hacé **clic en el mapa** para marcar el lugar exacto.")
    
    mapa_urgencia = folium.Map(location=[-41.332, -69.545], zoom_start=15)
    mapa_datos = st_folium(mapa_urgencia, height=300, width=700, key="mapa_sos_peligro")

    lat_click = ""
    lon_click = ""
    if mapa_datos and mapa_datos.get("last_clicked"):
        lat_click = mapa_datos["last_clicked"]["lat"]
        lon_click = mapa_datos["last_clicked"]["lng"]
        st.success("✅ ¡Ubicación capturada!")
    else:
        st.info("👆 Tocar el mapa es obligatorio.")

    st.markdown("---")

    # ==========================================
    # 2. FORMULARIO
    # ==========================================
    with st.form("form_urgencia_peligro"):
        st.markdown("### 📝 2. Detalles y Evidencia")
        descripcion = st.text_area("¿Qué pasó? (Ej: Perrito atropellado, gato atrapado, etc.)")
        
        # Campo para foto
        foto_emergencia = st.file_uploader("📸 Subí una foto si podés (esto ayuda a que la guardia sepa qué llevar)", type=['jpg', 'jpeg', 'png'])

        st.markdown("### 👤 3. Tus Datos (Vecino Solidario)")
        st.info("🔒 Datos obligatorios y confidenciales.")
        
        nombre_vecino = st.text_input("Tu Nombre Completo")
        col_v1, col_v2 = st.columns(2)
        with col_v1: dni_vecino = st.text_input("Tu DNI (Solo números)")
        with col_v2: celular_vecino = st.text_input("Tu Celular (Ej: 2944123456)")

        submit = st.form_submit_button("🚨 PREPARAR ALERTA S.O.S", type="primary")

        if submit:
            if not lat_click:
                st.error("🛑 Falta la ubicación: Hacé clic en el mapa.")
            elif not descripcion or not nombre_vecino or not celular_vecino:
                st.error("🛑 Faltan datos obligatorios.")
            else:
                # Tu número corregido listo para la API de WhatsApp
                telefono_guardia = "5492944318910" 
                link_maps = f"https://www.google.com/maps?q={lat_click},{lon_click}"
                
                mensaje = f"🚨 *ALERTA S.O.S. PELUDITO EN PELIGRO* 🚨\n\n"
                mensaje += f"📝 *Situación:* {descripcion}\n"
                mensaje += f"📍 *Ubicación Exacta:* {link_maps}\n\n"
                mensaje += f"👤 *Reportado por:* {nombre_vecino} (DNI: {dni_vecino})\n"
                mensaje += f"📱 *Celular:* {celular_vecino}"
                
                if foto_emergencia:
                    mensaje += "\n\n⚠️ *Nota:* El vecino adjuntó una foto de la emergencia."

                st.session_state.link_wa = f"https://api.whatsapp.com/send?phone={telefono_guardia}&text={urllib.parse.quote(mensaje)}"
                st.session_state.alerta_generada = True
                st.rerun()
