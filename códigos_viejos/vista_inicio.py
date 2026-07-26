import streamlit as st
import os
import json
import random
import csv
import base64

# Función auxiliar para convertir imágenes a Base64 para el carrusel
def obtener_imagen_base64(ruta_imagen):
    try:
        with open(ruta_imagen, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def mostrar_inicio():
    # ==========================================
    # 1. CABECERA Y TEXTOS (Solo la nueva imagen)
    # ==========================================
    
    # Inyectamos tu imagen directamente en el centro, ocupando el ancho disponible
    if os.path.exists("image_494b2d-3.jpg"):
        st.image("image_494b2d-3.jpg", use_container_width=True)
    else:
        # Plan B por si alguna vez se mueve el archivo de la imagen
        st.markdown("<h1 class='titulo-burbuja' style='text-align: center;'>PELUDITOS</h1>", unsafe_allow_html=True)
        
    # Subtítulo centrado
    st.markdown("<p style='font-weight: bold; margin-top: 5px; font-size: 16px; text-align: center;'>1ra y única red de mascoteros de Ing. Jacobacci</p>", unsafe_allow_html=True)

    # Un pequeño espacio para que no se pegue con el carrusel
    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================
    # 2. MOTOR DEL CARRUSEL DE FOTOS
    # ==========================================
    mascotas_portada = []
    diccionario_nombres = {}
    
    # Leemos la base de datos para cruzar nombres y estados (vivo/arco iris)
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

    # Buscamos las fotos disponibles
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

    # Si hay fotos, mostramos una al azar
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
            st.markdown(f"<p style='text-align: center; color: #8B4513; margin-top: 15px; font-size: 16px;'>Miembro de la manada:</p>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #8B4513; margin-top: -15px;'>{mascota['nombre'].upper()}{velita}</h3>", unsafe_allow_html=True)

    # Frase inspiradora de Gandhi
    st.markdown("""
    <div style='background-color: #faead6; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 15px; margin-top: 15px;'>
    <i>"La grandeza de una nación y su progreso moral pueden juzgarse por la forma en que se trata a sus animales."</i><br>
    <b>— Mahatma Gandhi</b>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # 3. BOTONERA SUPERIOR
    # ==========================================
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
    # 4. SERVICIOS Y AVISOS
    # ==========================================
    st.markdown("<h3 style='text-align: center; color: #8B4513;'>SERVICIOS</h3>", unsafe_allow_html=True)

    # Citas rotativas desde frases.json
    citas_dinamicas = []
    if os.path.exists("frases.json"):
        try:
            with open("frases.json", 'r', encoding='utf-8') as f:
                citas_dinamicas = json.load(f)
        except: 
            pass
    
    if citas_dinamicas:
        cita_elegida = random.choice(citas_dinamicas)
        st.markdown(f"""
        <div style='background-color: #fdf4e3; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #e8dcc4;'>
        <b>{cita_elegida}</b><br><span style='font-size: 11px; color: gray;'>(Próxima cita en 1 min.)</span>
        </div>
        <br>
        """, unsafe_allow_html=True)

    # Avisos Oficiales ZOO y Hospital
    with st.container(border=True):
        st.markdown("#### 📢 AVISOS OFICIALES ZOO-MUN y HOSPITAL")
        st.markdown("• **Zoonosis Municipal:** Campaña de castración gratuita (Fechas: 10-15 Oct). Vacunación antirrábica abierta.")
        st.markdown("• **Hospital Veterinario:** Guardias 24hs para urgencias. (Tel: 2944-XXXX)")
        col_leer_mas, _ = st.columns([1, 1])
        with col_leer_mas:
            if st.button("Seguir leyendo...", use_container_width=True):
                st.session_state.vista = 'avisos'
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Fila de Botones: Salud, Cumples, Arco Iris
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

    # Fila de Botones: S.O.S
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

    # Mitos y Verdades
    with st.container(border=True):
        st.markdown("#### 🤔 MITOS Y VERDADES")
        st.markdown("**Mito:** Los perros se curan lamiéndose.")
        st.markdown("**Verdad:** La saliva puede infectar las heridas y retrasar la cicatrización.")

    # Sponsor Premium (Se levanta de comercios.json)
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

    # Acceso Institucional (Botón Admin)
    col_v1, col_v2, col_v3 = st.columns([1, 2, 1])
    with col_v2:
        if st.button("📍 Acceso Institucional", use_container_width=True):
            st.session_state.vista = 'admin'
            st.rerun()
