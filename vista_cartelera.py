import streamlit as st
import folium
from streamlit_folium import folium_static
import os
import random
from base_datos import obtener_datos_mascotas, obtener_alertas, CARPETA_FOTOS, actualizar_en_csv, guardar_rescate

def mostrar_cartelera():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN (SUPERIOR) ===
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Volver", key="btn_volver_arriba_cartelera", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav2:
        if st.button("☰ Menú Principal", key="btn_menu_arriba_cartelera", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    st.markdown("---")
    # =========================================
    
    st.markdown("<h2 style='text-align: center; color: #FF6B6B !important;'>🚨 Cartelera y Mapa de Búsquedas</h2>", unsafe_allow_html=True)
    
    # Definimos las 4 pestañas correctamente
    tab_perros, tab_gatos, tab_sos, tab_baja = st.tabs(["🐶 Perros Perdidos", "🐱 Gatos Perdidos", "🆘 S.O.S. Activos", "✅ ¡Apareció!"])
    
    if 'centro_mapa' not in st.session_state:
        st.session_state.centro_mapa = [-41.332, -69.545]
    if 'zoom_mapa' not in st.session_state:
        st.session_state.zoom_mapa = 15

    def mover_mapa(lat, lon):
        st.session_state.centro_mapa = [lat, lon]
        st.session_state.zoom_mapa = 18 

    diccionario_mascotas = obtener_datos_mascotas()
    
    alertas_guardadas = obtener_alertas()
    ubicaciones_reales = {}
    alertas_sos = []
    
    for alerta in alertas_guardadas:
        try:
            lat = float(alerta.get('Latitud', 0))
            lon = float(alerta.get('Longitud', 0))
            if lat != 0 and lon != 0:
                ubicaciones_reales[alerta['ID_Mascota']] = (lat, lon)
        except ValueError:
            continue
        
        # Filtramos las que son emergencias comunitarias
        if alerta.get('Tipo_Alerta') == 'SOS_Emergencia':
            alertas_sos.append(alerta)

    # --- PESTAÑA PERROS ---
    with tab_perros:
        col_lista_p, col_mapa_p = st.columns([1, 1.5])
        mapa_perros = folium.Map(location=st.session_state.centro_mapa, zoom_start=st.session_state.zoom_mapa)
        
        with col_lista_p:
            with st.container(height=500):
                st.markdown("### 📋 Listado")
                hay_perros = False
                for id_mascota, mascota in diccionario_mascotas.items():
                    if mascota['Especie'] == 'Perro' and mascota.get('PIN') != '':
                        hay_perros = True
                        with st.container(border=True):
                            ruta_foto = os.path.join(CARPETA_FOTOS, f"{id_mascota}.jpg")
                            if os.path.exists(ruta_foto):
                                st.image(ruta_foto, use_container_width=True)
                            else:
                                st.markdown("*(Sin foto)*")
                            st.markdown(f"🐾 **{mascota['Nombre_Mascota']}** - {mascota['Raza']}")
                            st.error(f"**PIN del caso: {mascota['PIN']}**")
                            
                            if id_mascota in ubicaciones_reales:
                                lat_avistaje, lon_avistaje = ubicaciones_reales[id_mascota]
                            else:
                                random.seed(id_mascota)
                                lat_avistaje = -41.332 + random.uniform(-0.005, 0.005)
                                lon_avistaje = -69.545 + random.uniform(-0.005, 0.005)
                                random.seed() 
                            
                            st.button("📍 Ubicar en el mapa", key=f"btn_{id_mascota}", on_click=mover_mapa, args=(lat_avistaje, lon_avistaje))
                            
                            texto_popup = f"<b>{mascota['Nombre_Mascota']}</b><br>PIN: {mascota['PIN']}"
                            folium.Marker([lat_avistaje, lon_avistaje], popup=folium.Popup(texto_popup, max_width=200), tooltip="Perdido acá", icon=folium.Icon(color="red", icon="info-sign")).add_to(mapa_perros)
                
                if not hay_perros: st.info("¡No hay perritos extraviados!")

        with col_mapa_p:
            folium_static(mapa_perros, width=700, height=500)

    # --- PESTAÑA GATOS ---
    with tab_gatos:
        col_lista_g, col_mapa_g = st.columns([1, 1.5])
        mapa_gatos = folium.Map(location=st.session_state.centro_mapa, zoom_start=st.session_state.zoom_mapa)
        with col_lista_g:
            with st.container(height=500):
                st.markdown("### 📋 Listado")
                hay_gatos = False
                for id_mascota, mascota in diccionario_mascotas.items():
                    if mascota['Especie'] == 'Gato' and mascota.get('PIN') != '':
                        hay_gatos = True
                        with st.container(border=True):
                            ruta_foto = os.path.join(CARPETA_FOTOS, f"{id_mascota}.jpg")
                            if os.path.exists(ruta_foto): st.image(ruta_foto, use_container_width=True)
                            else: st.markdown("*(Sin foto)*")
                            st.markdown(f"🐾 **{mascota['Nombre_Mascota']}** - {mascota['Raza']}")
                            st.error(f"**PIN del caso: {mascota['PIN']}**")
                            
                            if id_mascota in ubicaciones_reales:
                                lat_avistaje, lon_avistaje = ubicaciones_reales[id_mascota]
                            else:
                                random.seed(id_mascota)
                                lat_avistaje = -41.332 + random.uniform(-0.005, 0.005)
                                lon_avistaje = -69.545 + random.uniform(-0.005, 0.005)
                                random.seed() 
                            st.button("📍 Ubicar en el mapa", key=f"btn_gato_{id_mascota}", on_click=mover_mapa, args=(lat_avistaje, lon_avistaje))
                            folium.Marker([lat_avistaje, lon_avistaje], tooltip="Perdido acá", icon=folium.Icon(color="blue", icon="info-sign")).add_to(mapa_gatos)
                if not hay_gatos: st.info("¡No hay michis extraviados!")
        with col_mapa_g:
            folium_static(mapa_gatos, width=700, height=500)

    # --- PESTAÑA S.O.S. ACTIVOS ---
    with tab_sos:
        col_lista_sos, col_mapa_sos = st.columns([1, 1.5])
        mapa_sos = folium.Map(location=st.session_state.centro_mapa, zoom_start=st.session_state.zoom_mapa)
        with col_lista_sos:
            with st.container(height=500):
                st.markdown("### 📋 Urgencias Comunitarias")
                if len(alertas_sos) > 0:
                    for alerta in alertas_sos:
                        id_sos = alerta['ID_Mascota']
                        with st.container(border=True):
                            
                            # >>> ACÁ VOLVIMOS A AGREGAR LA FOTO <<<
                            ruta_foto_sos = os.path.join(CARPETA_FOTOS, f"{id_sos}.jpg")
                            if os.path.exists(ruta_foto_sos):
                                st.image(ruta_foto_sos, use_container_width=True)
                            
                            st.error("🚨 **ALERTA S.O.S.**")
                            st.write(alerta.get('Detalles_Extra', 'Sin detalles.'))
                            if id_sos in ubicaciones_reales:
                                lat_sos, lon_sos = ubicaciones_reales[id_sos]
                                st.button("📍 Ver en el mapa", key=f"btn_sos_{id_sos}", on_click=mover_mapa, args=(lat_sos, lon_sos))
                                folium.Marker([lat_sos, lon_sos], tooltip="¡Urgencia acá!", icon=folium.Icon(color="orange", icon="warning-sign")).add_to(mapa_sos)
                else: st.info("¡No hay emergencias activas!")
        with col_mapa_sos:
            folium_static(mapa_sos, width=700, height=500)

    # --- PESTAÑA APARECIÓ MI MASCOTA (CON PREMIO AL RESCATISTA) ---
    with tab_baja:
        st.markdown("### 🎉 ¡Desactivar la búsqueda!")
        st.write("Si tu mascota volvió, registrá quién la encontró para que sume puntos al Premio del Día del Animal.")
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                num_baja = st.text_input("Número de mascota", placeholder="Ej: 45921")
                nombre_rescatista = st.text_input("¿Quién encontró a la mascota?", placeholder="Nombre del héroe/a")
            with col2:
                pin_baja = st.text_input("PIN de la Alerta", placeholder="Ej: 1272")
                
            if st.button("🎊 ¡Registrar rescate y cerrar alerta!", type="primary", use_container_width=True):
                if num_baja and pin_baja and nombre_rescatista:
                    id_limpio = f"ID-{''.join(filter(str.isdigit, num_baja))}"
                    if id_limpio in diccionario_mascotas:
                        mascota_baja = diccionario_mascotas[id_limpio]
                        if mascota_baja.get('PIN') == pin_baja.strip():
                            guardar_rescate(id_limpio, mascota_baja['Nombre_Mascota'], nombre_rescatista)
                            mascota_baja['PIN'] = ''
                            mascota_baja['Sena_Control'] = ''
                            actualizar_en_csv(mascota_baja)
                            st.success(f"¡Excelente! Rescate registrado. {nombre_rescatista} suma puntos.")
                            st.balloons()
                        else: st.error("PIN incorrecto.")
                    else: st.error("Mascota no encontrada.")
                else: st.warning("Completá todos los datos para cerrar la alerta.")

    # === BOTONERA DE NAVEGACIÓN (INFERIOR) ===
    st.markdown("---")
    col_nav3, col_nav4 = st.columns(2)
    with col_nav3:
        if st.button("⬅️ Volver", key="btn_volver_abajo_cartelera", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav4:
        if st.button("☰ Menú Principal", key="btn_menu_abajo_cartelera", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    # =========================================
