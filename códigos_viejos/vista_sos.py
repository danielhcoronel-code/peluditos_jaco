import streamlit as st
import random
import folium
from streamlit_folium import st_folium
import urllib.parse
import os
import datetime
# ---> Acá conectamos con tu ruta de fotos oficial <---
from base_datos import guardar_alerta_csv, CARPETA_FOTOS

def mostrar_sos():
    st.markdown("<h2 style='text-align: center; color: #D32F2F;'>🚨 S.O.S. Animalito en Peligro</h2>", unsafe_allow_html=True)
    st.warning("Usá esta sección SOLO para emergencias con animalitos sin dueño aparente (atropellados, cajas con cachorros, peligro inminente).")

    # --- PASO 1: MAPA ---
    st.markdown("### 📍 ¿Dónde es la emergencia?")
    st.write("Hacé clic en el mapa para marcar el lugar exacto:")
    
    mapa_sos = folium.Map(location=[-41.332, -69.545], zoom_start=15)
    mapa_datos = st_folium(mapa_sos, height=300, width=700, key="mapa_emergencia_sos")
    
    lat_click = ""
    lon_click = ""
    if mapa_datos and mapa_datos.get("last_clicked"):
        lat_click = mapa_datos["last_clicked"]["lat"]
        lon_click = mapa_datos["last_clicked"]["lng"]
        st.success("✅ Ubicación marcada.")
    else:
        st.info("👆 Tocá el mapa para fijar la ubicación.")

    # --- PASO 2: FORMULARIO ---
    with st.form("form_sos"):
        st.markdown("### 📸 Detalles de la situación")
        foto_sos = st.file_uploader("Subir foto del animalito (ayuda muchísimo a los rescatistas)", type=['png', 'jpg', 'jpeg'])
        detalles = st.text_area("Describí qué pasó", placeholder="Ej: Hay una caja con 4 gatitos abandonados al lado del contenedor de basura.")
        
        st.markdown("---")
        st.markdown("### 🛑 Identificación Obligatoria (Filtro Anti-Bromas)")
        st.write("Para evitar falsas alarmas, el sistema exige tu identificación real. **Tus datos NO serán públicos en el mapa**.")
        
        col_id1, col_id2 = st.columns(2)
        with col_id1:
            nombre_den = st.text_input("Nombre y Apellido")
            dni_den = st.text_input("DNI (Sin puntos)")
        with col_id2:
            celular_den = st.text_input("Tu Celular")

        if st.form_submit_button("📢 Publicar Alerta S.O.S.", type="primary"):
            if not lat_click or not lon_click:
                st.error("⚠️ Por favor, marcá la ubicación en el mapa haciendo clic.")
            elif not detalles:
                st.error("⚠️ Por favor, escribí un breve detalle de la situación.")
            elif not nombre_den or not dni_den or not celular_den:
                st.error("⚠️ Faltan datos. Tu identificación (Nombre, DNI y Celular) es estrictamente obligatoria.")
            else:
                id_sos = f"SOS-{random.randint(1000, 9999)}"
                
                # --- AQUÍ LA MAGIA: Guardamos usando la ruta oficial de tu sistema ---
                if foto_sos:
                    os.makedirs(CARPETA_FOTOS, exist_ok=True) 
                    ruta_guardado = os.path.join(CARPETA_FOTOS, f"{id_sos}.jpg")
                    with open(ruta_guardado, "wb") as f:
                        f.write(foto_sos.getbuffer())

                # 1. Guardamos la alerta en el CSV
                nueva_alerta = {
                    'ID_Mascota': id_sos,
                    'Tipo_Alerta': 'SOS_Emergencia',
                    'Detalles_Extra': detalles,
                    'Latitud': str(lat_click), 
                    'Longitud': str(lon_click)
                }
                guardar_alerta_csv(nueva_alerta)
                
                # 2. Guardamos los datos del denunciante en privado
                fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                registro_privado = f"[{fecha_hora}] ALERTA: {id_sos} | DENUNCIANTE: {nombre_den} | DNI: {dni_den} | CEL: {celular_den} | REPORTE: {detalles}\n"
                
                with open("auditoria_sos_privado.txt", "a", encoding="utf-8") as f:
                    f.write(registro_privado)
                
                st.session_state.sos_publicado = detalles
                st.success("¡Ubicación, foto y alerta guardadas en la plataforma!")

    # --- PASO 3: AVISO POR WHATSAPP ---
    if st.session_state.get('sos_publicado'):
        st.markdown("---")
        st.markdown("<h3 style='color: #25D366;'>📲 Paso Final: Dar aviso a los rescatistas</h3>", unsafe_allow_html=True)
        
        num_zoonosis = "5492944000001" 
        num_patitas = "5492944000002" 
        
        mensaje = urllib.parse.quote(f"¡Hola! Reporté una emergencia en la plataforma: {st.session_state.sos_publicado}. Por favor revisen el mapa.")
        
        col_z, col_p = st.columns(2)
        with col_z:
            st.markdown(f'<a href="https://wa.me/{num_zoonosis}?text={mensaje}" target="_blank" style="text-decoration: none;"><button style="width:100%; background-color:#25D366; color:white; font-weight:bold; border:none; padding:10px; border-radius:5px; cursor:pointer;">💬 Avisar a Zoonosis</button></a>', unsafe_allow_html=True)
        with col_p:
            st.markdown(f'<a href="https://wa.me/{num_patitas}?text={mensaje}" target="_blank" style="text-decoration: none;"><button style="width:100%; background-color:#25D366; color:white; font-weight:bold; border:none; padding:10px; border-radius:5px; cursor:pointer;">💬 Avisar a Patitas Felices</button></a>', unsafe_allow_html=True)
