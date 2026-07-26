import streamlit as st
import qrcode
import io
import urllib.parse
import csv
import os
import folium
from streamlit_folium import st_folium
import random
import base64
import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Mi Mascota y Yo - Jacobacci", page_icon="🐾", layout="centered")

# --- LÓGICA DE BASES DE DATOS LOCALES ---
ARCHIVO_CSV = "base_mascotas.csv"
ARCHIVO_ALERTAS = "base_alertas.csv" 
CARPETA_FOTOS = "fotos_mascotas" 

os.makedirs(CARPETA_FOTOS, exist_ok=True)

def guardar_en_csv(datos_mascota):
    archivo_existe = os.path.isfile(ARCHIVO_CSV)
    with open(ARCHIVO_CSV, mode='a', newline='', encoding='utf-8') as archivo:
        nombres_columnas = ['ID_Mascota', 'Nombre_Mascota', 'Especie', 'Raza', 'Edad', 'Sexo', 'Castrado', 'Peso_Kg', 'Vacuna_Antirrabica', 'Condicion_Medica', 'Nombre_Contacto', 'Celular', 'Domicilio']
        escritor = csv.DictWriter(archivo, fieldnames=nombres_columnas)
        if not archivo_existe: escritor.writeheader()
        escritor.writerow(datos_mascota)

def actualizar_en_csv(datos_actualizados):
    mascotas = []
    if os.path.isfile(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            mascotas = list(lector)
            
    nombres_columnas = ['ID_Mascota', 'Nombre_Mascota', 'Especie', 'Raza', 'Edad', 'Sexo', 'Castrado', 'Peso_Kg', 'Vacuna_Antirrabica', 'Condicion_Medica', 'Nombre_Contacto', 'Celular', 'Domicilio']
    
    for i, mascota in enumerate(mascotas):
        if mascota['ID_Mascota'] == datos_actualizados['ID_Mascota']:
            mascotas[i] = datos_actualizados
            break
            
    with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=nombres_columnas)
        escritor.writeheader()
        escritor.writerows(mascotas)

def guardar_alerta_csv(datos_alerta):
    archivo_existe = os.path.isfile(ARCHIVO_ALERTAS)
    with open(ARCHIVO_ALERTAS, mode='a', newline='', encoding='utf-8') as archivo:
        nombres_columnas = ['ID_Mascota', 'Detalles_Extra', 'Latitud', 'Longitud']
        escritor = csv.DictWriter(archivo, fieldnames=nombres_columnas)
        if not archivo_existe: escritor.writeheader()
        escritor.writerow(datos_alerta)

def obtener_datos_mascotas():
    mascotas = {}
    if os.path.isfile(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                mascotas[fila['ID_Mascota']] = fila
    return mascotas

def obtener_alertas():
    alertas = []
    if os.path.isfile(ARCHIVO_ALERTAS):
        with open(ARCHIVO_ALERTAS, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                alertas.append(fila)
    return alertas

def codificar_foto_base64(ruta_imagen):
    if os.path.isfile(ruta_imagen):
        with open(ruta_imagen, "rb") as archivo_img:
            return base64.b64encode(archivo_img.read()).decode()
    return None

# --- ESTILOS SIMPLES Y SEGUROS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap');
    
    .stApp { background-color: #FDFBF7; }
    h1, h2, h3, h4, p, label, span { font-family: 'Fredoka', sans-serif !important; color: #2C3E50 !important; }
    
    div.stButton > button {
        background-color: #2E86C1 !important; color: white !important; 
        border-radius: 8px !important; border: none !important; font-weight: 600 !important; width: 100%;
    }
    div.stButton > button:hover { background-color: #1A5276 !important; }
    button[kind="primary"] { background-color: #E74C3C !important; }
    button[kind="primary"]:hover { background-color: #C0392B !important; }
    
    .caja-info { background-color: #EAF2F8; padding: 20px; border-radius: 10px; border-left: 5px solid #2E86C1; margin-bottom: 20px; }
    .faq-box { background-color: #FFFFFF; padding: 15px; border-radius: 8px; border: 1px solid #BDC3C7; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
if 'vista' not in st.session_state: st.session_state.vista = 'inicio'
if 'mascota_a_editar' not in st.session_state: st.session_state.mascota_a_editar = None

def ir_a_formulario(): st.session_state.vista = 'formulario'
def ir_a_inicio(): 
    st.session_state.vista = 'inicio'
    st.session_state.mascota_a_editar = None 
def ir_a_faq(): st.session_state.vista = 'faq'
def ir_a_cartelera(): st.session_state.vista = 'cartelera'
def ir_a_modificar(): st.session_state.vista = 'modificar' 

# --- ENCABEZADO FIJO ---
col_logo, col_titulos, col_boton = st.columns([1, 3, 1])
with col_logo:
    try: st.image("logo_final.png", width=120) 
    except: st.warning("Falta imagen")

with col_titulos:
    st.markdown("<h1 style='text-align: center;'>MI MASCOTA Y YO</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; margin-top: -15px;'>Jacobacci</h3>", unsafe_allow_html=True)

with col_boton:
    st.write("") 
    if st.session_state.vista == 'inicio':
        if st.button("🔗 Invitar"): st.success("¡Copiado!")
    else:
        st.button("⬅️ Volver", on_click=ir_a_inicio)

st.markdown("---")

# ==========================================
# PANTALLA 1: INICIO
# ==========================================
if st.session_state.vista == 'inicio':
    st.markdown("""
    <div class='caja-info'>
        <p style='text-align: center;'><strong>🐾 ¿Qué es esta plataforma?</strong><br>
        Somos la red comunitaria para cuidar a nuestros animales. Obtené tu código QR para emergencias.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.button("❓ Preguntas Frecuentes", on_click=ir_a_faq)
    st.markdown("---")
    st.markdown("<h3 style='text-align: center; color: #E74C3C !important;'>🚨 Mascotas Perdidas</h3>", unsafe_allow_html=True)
    st.button("🔍 Ver Cartelera de Perdidos", type="primary", use_container_width=True, on_click=ir_a_cartelera)
    st.markdown("<br>", unsafe_allow_html=True)

    col_registro, col_comunidad = st.columns(2, gap="large")
    with col_registro:
        st.markdown("<h3 style='text-align: center;'>Registrá a tu amigo</h3>", unsafe_allow_html=True)
        st.button("📝 Crear Ficha", on_click=ir_a_formulario, use_container_width=True)
        st.button("✏️ Modificar Ficha", on_click=ir_a_modificar, use_container_width=True) 

    with col_comunidad:
        st.markdown("<h3 style='text-align: center;'>Patitas Felices</h3>", unsafe_allow_html=True)
        st.button("❤️ Apadrinar / Adopciones")

    st.markdown("---")
    sugerencia = st.text_area("Te leemos:", placeholder="Ej: Veterinaria de guardia...", label_visibility="collapsed")
    if st.button("Enviar sugerencia"): st.success("¡Gracias! Tu idea nos ayuda a mejorar.")

# ==========================================
# PANTALLA 2: MAPA DE PERDIDOS
# ==========================================
elif st.session_state.vista == 'cartelera':
    st.markdown("<h2 style='text-align: center; color: #E74C3C !important;'>Cartelera de Urgencias</h2>", unsafe_allow_html=True)
    st.info("👆 **Instrucción:** Navegá por el mapa y hacé clic exactamente en la calle donde viste a tu mascota por última vez para reportarla.")
    
    latitud_jacobacci = -41.332
    longitud_jacobacci = -69.545
    mapa_emergencias = folium.Map(location=[latitud_jacobacci, longitud_jacobacci], zoom_start=15)
    
    diccionario_mascotas = obtener_datos_mascotas()
    lista_alertas = obtener_alertas()
    
    for alerta in lista_alertas:
        id_perdido = alerta['ID_Mascota']
        if id_perdido in diccionario_mascotas:
            datos_perro = diccionario_mascotas[id_perdido]
            ruta_foto = os.path.join(CARPETA_FOTOS, f"{id_perdido}.jpg")
            foto_b64 = codificar_foto_base64(ruta_foto)
            
            # ACA ESTÁ LA MAGIA DEL REDIMENSIONAMIENTO AUTOMÁTICO (max-height: 130px)
            html_foto = f'<div style="text-align: center;"><img src="data:image/jpeg;base64,{foto_b64}" style="max-height: 130px; max-width: 100%; object-fit: cover; border-radius: 8px; margin-bottom: 5px; border: 1px solid #ccc;"></div>' if foto_b64 else ''
            
            tarjeta_html = f"""
            <div style="font-family: sans-serif; min-width: 200px; max-width: 250px;">
                {html_foto}
                <h4 style="color: #E74C3C; margin-bottom: 5px; margin-top: 0; font-size: 16px;">🚨 {datos_perro['Nombre_Mascota']}</h4>
                <p style="margin: 0; font-size: 13px;"><b>Raza:</b> {datos_perro['Raza']}</p>
                <p style="margin: 0; font-size: 13px;"><b>Detalle:</b> {alerta['Detalles_Extra']}</p>
                <hr style="margin: 8px 0;">
                <div style="background-color: #EAF2F8; padding: 6px; text-align: center; border-radius: 5px; border: 1px solid #BDC3C7; line-height: 1.2;">
                    <span style="font-size: 11px; color: #2C3E50;"><b>🔒 Dueño Protegido</b><br>El sistema resguarda los datos. Si lo encontrás, avisá a Patitas Felices para triangular el contacto.</span>
                </div>
            </div>
            """
            
            folium.Marker(
                [float(alerta['Latitud']), float(alerta['Longitud'])],
                popup=folium.Popup(tarjeta_html, max_width=280),
                tooltip=f"¡Buscamos a {datos_perro['Nombre_Mascota']}!",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(mapa_emergencias)

    mapa_datos = st_folium(mapa_emergencias, width=700, height=450)
    
    if mapa_datos and mapa_datos.get("last_clicked"):
        lat_clic = mapa_datos["last_clicked"]["lat"]
        lng_clic = mapa_datos["last_clicked"]["lng"]
        with st.form("form_reporte_perdido"):
            st.markdown("### 🚨 Reportar Extravío (Dueño)")
            id_ingresado = st.text_input("ID de la Mascota", placeholder="Ej: ID-45921")
            detalles_perdido = st.text_area("Información de último momento")
            if st.form_submit_button("Publicar Alerta de Extravío"):
                if id_ingresado:
                    guardar_alerta_csv({'ID_Mascota': id_ingresado.strip(), 'Detalles_Extra': detalles_perdido, 'Latitud': lat_clic, 'Longitud': lng_clic})
                    st.success("¡Alerta registrada! Actualizá la página para verla en el mapa.")

# ==========================================
# PANTALLA 3: FORMULARIO Y GENERADOR DE QR
# ==========================================
elif st.session_state.vista == 'formulario':
    st.markdown("<h2 style='text-align: center;'>Formulario de Registro</h2>", unsafe_allow_html=True)
    with st.form("registro_mascota"):
        st.markdown("### 🐶 Perfil Público")
        col1, col2 = st.columns(2)
        with col1: 
            nombre = st.text_input("Nombre", placeholder="Ej. Rocco")
            especie = st.selectbox("Especie", ["Perro", "Gato", "Otro"])
        with col2: 
            st.info("📸 **Subir foto de la mascota**")
            foto = st.file_uploader("Debe ser clara y de frente", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
            raza = st.text_input("Raza", placeholder="Mestizo")

        st.markdown("---")
        st.markdown("### 📋 Ficha Clínica")
        col3, col4 = st.columns(2)
        with col3: 
            edad = st.number_input("Edad (años)", 0, 30, 14)
            sexo = st.radio("Sexo", ["Macho", "Hembra"], horizontal=True)
            castrado = st.radio("¿Está castrado/a?", ["Sí", "No"], horizontal=True) 
        with col4: 
            peso = st.number_input("Peso (kg)", 0.0, 50.0, 16.0)
            fecha_antirrabica = st.date_input("Última Antirrábica")
            
        condicion = st.text_area("Condición Médica (Opcional)")

        st.markdown("---")
        st.markdown("### 📞 Contacto de Emergencia")
        st.warning("🔒 Tus datos personales son confidenciales. Solo se usarán en el código QR y de forma interna.")
        nombre_contacto = st.text_input("Tu nombre"); celular = st.text_input("Celular (WhatsApp)"); domicilio = st.text_input("Barrio o Domicilio")
        
        if st.form_submit_button("Guardar Datos y Generar QR"):
            if nombre and celular:
                id_unico = f"ID-{random.randint(10000, 99999)}"
                if foto is not None:
                    ruta_guardado = os.path.join(CARPETA_FOTOS, f"{id_unico}.jpg")
                    with open(ruta_guardado, "wb") as archivo_foto: archivo_foto.write(foto.getbuffer())
                
                guardar_en_csv({'ID_Mascota': id_unico, 'Nombre_Mascota': nombre, 'Especie': especie, 'Raza': raza, 'Edad': edad, 'Sexo': sexo, 'Castrado': castrado, 'Peso_Kg': peso, 'Vacuna_Antirrabica': fecha_antirrabica, 'Condicion_Medica': condicion, 'Nombre_Contacto': nombre_contacto, 'Celular': celular, 'Domicilio': domicilio})
                
                st.success("¡Ficha guardada!")
                st.error(f"🛑 **¡IMPORTANTE!** El número de identificación de tu mascota es: **{id_unico}**. Anotalo, es tu contraseña para editar datos o reportar extravíos.")
                
                celular_limpio = "".join(filter(str.isdigit, celular))
                mensaje = urllib.parse.quote(f"¡Hola {nombre_contacto}! Encontré a {nombre}. Por favor, comunicate conmigo.")
                imagen_qr = qrcode.make(f"https://wa.me/549{celular_limpio}?text={mensaje}")
                buf = io.BytesIO(); imagen_qr.save(buf, format="PNG"); byte_im = buf.getvalue()
                st.markdown("<h3 style='text-align: center;'>Tu Código QR</h3>", unsafe_allow_html=True)
                col_izq, col_centro, col_der = st.columns([1, 2, 1])
                with col_centro: st.image(byte_im, use_container_width=True)
            else: st.error("Faltan datos obligatorios (Nombre y Celular).")

# ==========================================
# PANTALLA 4: MODIFICAR FICHA
# ==========================================
elif st.session_state.vista == 'modificar':
    st.markdown("<h2 style='text-align: center;'>✏️ Modificar Ficha</h2>", unsafe_allow_html=True)
    st.write("Ingresá el ID de tu mascota para recuperar sus datos y hacer correcciones.")
    
    col_busqueda1, col_busqueda2 = st.columns([3, 1])
    with col_busqueda1:
        id_buscar = st.text_input("ID de la Mascota", placeholder="Ej: ID-45921", label_visibility="collapsed")
    with col_busqueda2:
        btn_buscar = st.button("Buscar Ficha", use_container_width=True)
        
    if btn_buscar and id_buscar:
        diccionario_mascotas = obtener_datos_mascotas()
        if id_buscar in diccionario_mascotas:
            st.session_state.mascota_a_editar = diccionario_mascotas[id_buscar]
            st.success("¡Ficha encontrada! Podés corregir los datos aquí abajo.")
        else:
            st.error("No encontramos ninguna mascota con ese ID. Revisá bien el número.")
            st.session_state.mascota_a_editar = None

    if st.session_state.mascota_a_editar:
        m_edit = st.session_state.mascota_a_editar
        
        with st.form("edicion_mascota"):
            st.markdown("### 🐶 Perfil Público")
            col1, col2 = st.columns(2)
            with col1: 
                nombre_ed = st.text_input("Nombre", value=m_edit['Nombre_Mascota'])
                especies = ["Perro", "Gato", "Otro"]
                idx_esp = especies.index(m_edit['Especie']) if m_edit['Especie'] in especies else 0
                especie_ed = st.selectbox("Especie", especies, index=idx_esp)
            
            with col2: 
                st.info("📸 **Actualizar Foto**")
                foto_ed = st.file_uploader("Subir NUEVA foto (dejar vacío para mantener la actual)", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
                raza_ed = st.text_input("Raza", value=m_edit['Raza'])

            st.markdown("---")
            st.markdown("### 📋 Ficha Clínica")
            col3, col4 = st.columns(2)
            with col3: 
                edad_ed = st.number_input("Edad (años)", 0, 30, int(m_edit['Edad']))
                idx_sexo = 0 if m_edit['Sexo'] == "Macho" else 1
                sexo_ed = st.radio("Sexo", ["Macho", "Hembra"], index=idx_sexo, horizontal=True)
                idx_cast = 0 if m_edit['Castrado'] == "Sí" else 1
                castrado_ed = st.radio("¿Está castrado/a?", ["Sí", "No"], index=idx_cast, horizontal=True) 
            with col4: 
                peso_ed = st.number_input("Peso (kg)", 0.0, 50.0, float(m_edit['Peso_Kg']))
                try: fecha_obj = datetime.datetime.strptime(m_edit['Vacuna_Antirrabica'], '%Y-%m-%d').date()
                except: fecha_obj = datetime.date.today()
                fecha_antirrabica_ed = st.date_input("Última Antirrábica", value=fecha_obj)
                
            condicion_ed = st.text_area("Condición Médica", value=m_edit['Condicion_Medica'])

            st.markdown("---")
            st.markdown("### 📞 Contacto de Emergencia")
            nombre_contacto_ed = st.text_input("Tu nombre", value=m_edit['Nombre_Contacto'])
            celular_ed = st.text_input("Celular (WhatsApp)", value=m_edit['Celular'])
            domicilio_ed = st.text_input("Barrio o Domicilio", value=m_edit['Domicilio'])
            
            if st.form_submit_button("Guardar Cambios"):
                if foto_ed is not None:
                    ruta_guardado = os.path.join(CARPETA_FOTOS, f"{m_edit['ID_Mascota']}.jpg")
                    with open(ruta_guardado, "wb") as archivo_foto: archivo_foto.write(foto_ed.getbuffer())
                
                actualizar_en_csv({
                    'ID_Mascota': m_edit['ID_Mascota'], 'Nombre_Mascota': nombre_ed, 'Especie': especie_ed, 'Raza': raza_ed, 'Edad': edad_ed, 'Sexo': sexo_ed, 'Castrado': castrado_ed, 'Peso_Kg': peso_ed, 'Vacuna_Antirrabica': fecha_antirrabica_ed, 'Condicion_Medica': condicion_ed, 'Nombre_Contacto': nombre_contacto_ed, 'Celular': celular_ed, 'Domicilio': domicilio_ed})
                
                st.success("¡Ficha actualizada con éxito! Podés volver al inicio.")

# ==========================================
# PANTALLA 5: PREGUNTAS FRECUENTES (FAQ)
# ==========================================
elif st.session_state.vista == 'faq':
    st.markdown("<h2 style='text-align: center;'>Preguntas Frecuentes</h2>", unsafe_allow_html=True)
    st.markdown("""<div class='faq-box'><p><strong>¿Mis datos personales son públicos?</strong></p><p>¡Para nada! Esa es la mayor ventaja del código QR...</p></div>""", unsafe_allow_html=True)
