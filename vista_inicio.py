import streamlit as st
import os
import json
import random
import csv
import base64
import datetime # Agregado para usar el reloj en la rotación de razas

# Función auxiliar para convertir imágenes a Base64 para el carrusel
def obtener_imagen_base64(ruta_imagen):
    try:
        with open(ruta_imagen, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def mostrar_inicio():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # ==========================================
    # 1. CABECERA
    # ==========================================
    st.markdown("<h1 class='titulo-burbuja' style='text-align: center;'>PELUDITOS</h1>", unsafe_allow_html=True)
        
    # Subtítulo centrado
    st.markdown("<p style='font-weight: bold; margin-top: 5px; font-size: 16px; text-align: center;'>1ra y única red de mascoteros de Ing. Jacobacci</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # 2. CITAS INSPIRACIONALES ROTATIVAS (ARRIBA DE TODO)
    # ==========================================
    citas_dinamicas = []
    if os.path.exists("citas.json"):
        try:
            with open("citas.json", 'r', encoding='utf-8') as f:
                citas_dinamicas = json.load(f)
        except: 
            pass
    
    if citas_dinamicas:
        cita_elegida = random.choice(citas_dinamicas)
        st.markdown(f"""
        <div style='background-color: #fdf4e3; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #e8dcc4; margin-bottom: 20px;'>
        <b style='color: #5D4037;'>{cita_elegida}</b><br><span style='font-size: 11px; color: gray; margin-top: 5px; display: block;'>(Nueva cita en cada visita)</span>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # 3. VIDEO INSTITUCIONAL
    # ==========================================
    if os.path.exists("PELUDITOS.mp4"):
        st.video("PELUDITOS.mp4", autoplay=False)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # 3.5. LA RAZA DEL DÍA (Versión a prueba de fallos)
    # ==========================================
    if os.path.exists("razas.json"):
        try:
            with open("razas.json", 'r', encoding='utf-8') as f:
                catalogo_razas = json.load(f)
                
            # Solo intentamos mostrar si la lista existe y tiene al menos un animal
            if isinstance(catalogo_razas, list) and len(catalogo_razas) > 0:
                dia_del_ano = datetime.datetime.now().timetuple().tm_yday
                indice_raza = dia_del_ano % len(catalogo_razas)
                raza_hoy = catalogo_razas[indice_raza]
                
                # Validamos que los datos estén sanos (que sea un diccionario)
                if isinstance(raza_hoy, dict):
                    with st.container(border=True):
                        st.markdown("<h4 style='text-align: center; color: #8B4513;'>🐾 Raza del Día</h4>", unsafe_allow_html=True)
                        
                        col_foto_raza, col_texto_raza = st.columns([1, 2])
                        with col_foto_raza:
                            # Filtro de seguridad por si la foto no existe o quedó en blanco
                            nombre_archivo = raza_hoy.get("foto_archivo", "")
                            if not nombre_archivo: 
                                nombre_archivo = ""
                            
                            ruta_foto_raza = os.path.join("fotos_razas", str(nombre_archivo))
                            
                            if os.path.exists(ruta_foto_raza) and nombre_archivo != "":
                                st.image(ruta_foto_raza, use_container_width=True)
                            else:
                                st.info("📷 Foto en camino")
                                
                        with col_texto_raza:
                            st.markdown(f"**{raza_hoy.get('nombre', 'Raza en actualización')}**")
                            st.write(raza_hoy.get("resumen", ""))
                            if st.button("Leer más sobre esta raza...", key="btn_leer_raza", use_container_width=True):
                                st.session_state.vista = 'razas' 
                                st.rerun()
                    st.markdown("<br>", unsafe_allow_html=True)
        except Exception:
            # Si hay un error profundo, simplemente ocultamos la caja y no rompemos la app
            pass

    # ==========================================
    # 4. MOTOR DEL CARRUSEL DE FOTOS
    # ==========================================
    mascotas_portada = []
    diccionario_nombres = {}
    
    if os.path.exists("base_mascotas.csv"):
        try:
            with open("base_mascotas.csv", mode='r', encoding='utf-8-sig') as f:
                linea = f.readline()
                delimitador = ';' if ';' in linea else ','
                f.seek(0)
                reader = csv.DictReader(f, delimiter=delimitador)
                for row in reader:
                    id_interno = row.get("ID_Mascota", "").strip()
                    nombre = row.get("Nombre_Mascota", "").strip()
                    estado = row.get("Estado_Vida", "Vivo").strip()
                    if id_interno and nombre:
                        diccionario_nombres[id_interno] = {"nombre": nombre, "estado": estado}
        except Exception: 
            pass

    if os.path.exists("fotos_mascotas"):
        for f in os.listdir("fotos_mascotas"):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')) and not f.lower().startswith("sos"):
                id_archivo = os.path.splitext(f)[0].strip()
                nombre_real = diccionario_nombres.get(id_archivo, {}).get("nombre", "Un amiguito")
                estado_real = diccionario_nombres.get(id_archivo, {}).get("estado", "Vivo")
                mascotas_portada.append({
                    "ruta": os.path.join("fotos_mascotas", f), 
                    "nombre": nombre_real, 
                    "estado": estado_real
                })

    if mascotas_portada:
        mascota = random.choice(mascotas_portada)
        col_esp1, col_foto, col_esp2 = st.columns([1, 2, 1])
        with col_foto:
            img_base64 = obtener_imagen_base64(mascota["ruta"])
            html_foto = f"""
            <div style="height: 250px; background-color: #faead6; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); display: flex; align-items: center; justify-content: center; overflow: hidden; padding: 5px;">
                <img src="data:image/jpeg;base64,{img_base64}" style="max-width: 100%; max-height: 100%; object-fit: contain; border-radius: 8px;">
            </div>
            """
            st.markdown(html_foto, unsafe_allow_html=True)
            velita = " 🕯️" if "arco" in mascota["estado"].lower() else ""
            
            # --- DISEÑO EXACTO A manada.png ---
            # 1. Nombre de la mascota destacado (ROQUITO)
            st.markdown(f"<h2 style='text-align: center; color: #8B4513; margin-top: 10px; margin-bottom: 5px;'>{mascota['nombre'].upper()}{velita}</h2>", unsafe_allow_html=True)
            
            # 2. Primera frase
            st.markdown(f"<p style='text-align: center; color: #5D4037; font-size: 18px; margin-top: 0px; margin-bottom: 5px;'>Miembro de la manada</p>", unsafe_allow_html=True)
            
            # 3. Segunda frase destacada
            st.markdown(f"<p style='text-align: center; color: #5D4037; font-size: 16px; font-weight: bold; margin-top: 0px;'>DE INGENIERO JACOBACCI</p>", unsafe_allow_html=True)

    # ==========================================
    # 5. BOTONERA SUPERIOR
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("Quiénes Somos", use_container_width=True):
            st.session_state.vista = 'quienes_somos'
            st.rerun()
    with col_nav2:
        if st.button("Manual del Usuario", use_container_width=True):
            st.session_state.vista = 'faq'
            st.rerun()

    col_reg1, col_reg2, col_reg3 = st.columns(3)
    with col_reg1:
        if st.button("Registro", use_container_width=True):
            st.session_state.vista = 'formulario'
            st.rerun()
    with col_reg2:
        if st.button("Editar Registro", use_container_width=True):
            st.session_state.vista = 'modificar'
            st.rerun()
    with col_reg3:
        if st.button("🏡 Ser Hogar (H.D.T.)", use_container_width=True):
            st.session_state.vista = 'hdt'
            st.rerun()

    st.markdown("---")

    # ==========================================
    # 6. DE INTERÉS GRAL Y COMUNICADOS
    # ==========================================
    st.markdown("<h4 style='text-align: center; color: #8B4513;'>De interés Gral.</h4>", unsafe_allow_html=True)

    tips_dinamicos = []
    if os.path.exists("interes_gral.json"):
        try:
            with open("interes_gral.json", 'r', encoding='utf-8') as f:
                tips_dinamicos = json.load(f)
        except: 
            pass
    
    if tips_dinamicos:
        tip_elegido = random.choice(tips_dinamicos)
        st.info(tip_elegido)
    
    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("#### 📢 Comunicados")
        st.markdown("• **Zoonosis Municipal:** Campaña de castración gratuita (Fechas: 10-15 Oct). Vacunación antirrábica abierta.")
        st.markdown("• **Hospital Veterinario:** Guardias 24hs para urgencias. (Tel: 2944-XXXX)")
        col_leer_mas, _ = st.columns([1, 1])
        with col_leer_mas:
            if st.button("Seguir leyendo...", use_container_width=True):
                st.session_state.vista = 'avisos'
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # 7. BOTONERA INFERIOR (SALUD Y SOS)
    # ==========================================
    col_srv1, col_srv2, col_srv3 = st.columns(3)
    with col_srv1:
        if st.button("🩺 Salud y Bienestar", use_container_width=True):
            st.session_state.vista = 'bienestar'
            st.rerun()
    with col_srv2:
        if st.button("🎂 Cumples", use_container_width=True):
            st.session_state.vista = 'cumples'
            st.rerun()
    with col_srv3:
        if st.button("🌈 Arco Iris", use_container_width=True):
            st.session_state.vista = 'arcoiris'
            st.rerun()

    col_sos1, col_sos2 = st.columns(2)
    with col_sos1:
        if st.button("S.O.S. Extraviado", use_container_width=True):
            st.session_state.vista = 'sos'
            st.rerun()
    with col_sos2:
        if st.button("S.O.S. Peludito en Peligro", type="primary", use_container_width=True):
            st.session_state.vista = 'urgencias'
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)
            
    # --- ACÁ ESTÁ EL NUEVO BOTÓN OFICIAL DE URESA ---
    st.link_button("🚨 Reportar Mordedura a U.R.E.S.A. (Formulario Oficial)", "https://docs.google.com/forms/d/e/1FAIpQLScH8t9_aR3JHMVN5HmJTKzr0ut1g7-LdGMVDDvhE9LJbmIfLg/viewform?usp=sharing&ouid=118263163555837582044", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # 8. SPONSOR PREMIUM Y ACCESO ADMIN
    # ==========================================
    archivo_comercios = "comercios.json"
    if os.path.exists(archivo_comercios):
        try:
            with open(archivo_comercios, 'r', encoding='utf-8') as f:
                comercios = json.load(f)
                sponsors_premium = [c for c in comercios if "Sponsor Premium" in c.get("categoria", "")]
                if sponsors_premium:
                    sponsor = random.choice(sponsors_premium)
                    with st.container(border=True):
                        st.markdown("<p style='text-align: center; font-size: 14px; margin-bottom: 5px;'><b>SPONSOR PREMIUM</b></p>", unsafe_allow_html=True)
                        col_sp1, col_sp2 = st.columns([1, 2])
                        with col_sp1:
                            foto_publi = sponsor.get("foto_ruta", "")
                            if foto_publi and os.path.exists(foto_publi):
                                st.image(foto_publi, use_container_width=True)
                        with col_sp2:
                            st.markdown(f"<h4 style='margin-top: 10px;'>{sponsor.get('nombre', 'Comercio')}</h4>", unsafe_allow_html=True)
        except Exception: 
            pass

    st.markdown("<br><br>", unsafe_allow_html=True)

    col_v1, col_v2, col_v3 = st.columns([1, 2, 1])
    with col_v2:
        if st.button("📍 Acceso Institucional", use_container_width=True):
            st.session_state.vista = 'admin'
            st.rerun()
