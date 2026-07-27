import streamlit as st
import random
import os
import urllib.parse
import io
import qrcode
import datetime
# ¡Agregamos obtener_datos_mascotas a la importación!
from base_datos import guardar_en_csv, obtener_datos_mascotas, CARPETA_FOTOS

def mostrar_formulario():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN (SUPERIOR) ===
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Volver", key="btn_volver_arriba_formulario", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav2:
        if st.button("☰ Menú Principal", key="btn_menu_arriba_formulario", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    st.markdown("---")
    # =========================================
    
    st.markdown("<h2 style='text-align: center;'>Sumar a Mi Manada</h2>", unsafe_allow_html=True)
    
    if 'tutor_celular' not in st.session_state:
        st.error("Error técnico: No encontramos tus datos de contacto en la memoria. Por favor, volvé al inicio.")
        return

    # ==========================================
    # PANTALLA DE VICTORIA (Se activa al guardar)
    # ==========================================
    if st.session_state.get('registro_exitoso', False):
        nombre = st.session_state.get('ultimo_nombre', '')
        id_unico = st.session_state.get('ultimo_id', '')
        byte_im = st.session_state.get('ultimo_qr', None)
        
        st.success(f"¡La ficha de {nombre} se guardó espectacular!")
        if id_unico:
            st.error(f"🛑 **¡IMPORTANTE!** La LLAVE SECRETA de {nombre} es: **{id_unico.split('-')[1]}**. Anotala bien.")
        
        if byte_im:
            st.markdown("<h3 style='text-align: center;'>Tu Código QR (Listo para grabar)</h3>", unsafe_allow_html=True)
            col_izq, col_centro, col_der = st.columns([1, 2, 1])
            with col_centro: 
                st.image(byte_im, use_container_width=True)
                st.download_button(
                    label="⬇️ Descargar Chapita QR",
                    data=byte_im,
                    file_name=f"QR_{nombre}.png",
                    mime="image/png",
                    use_container_width=True
                )
        
        # --- CONTROL DE FLUJO SEGÚN CANTIDAD ---
        registrados = st.session_state.get('tutor_peluditos_registrados_ahora', 1)
        totales = st.session_state.get('tutor_cantidad_peluditos', 1)
        
        st.markdown("---")
        if registrados < totales:
            st.info(f"🐾 ¡Falta registrar {totales - registrados} integrante/s más de tu manada!")
            if st.button("➕ Registrar otro miembro de la manada", use_container_width=True):
                st.session_state.registro_exitoso = False
                st.rerun()
        else:
            st.balloons()
            st.success("🎉 ¡Misión cumplida! Ya registraste a todos los integrantes que nos avisaste.")
            if st.button("🏠 Ir al Inicio para ver a Mi Manada", use_container_width=True):
                st.session_state.registro_exitoso = False
                st.session_state.vista = 'inicio'
                st.rerun()
                
        return

    # ==========================================
    # PANTALLA DEL FORMULARIO DE CARGA
    # ==========================================
    st.markdown("### 🐾 ¿Qué animalito se suma hoy?")
    especie = st.selectbox("Elegí la especie para adaptar la Ficha Clínica:", ["Perro", "Gato", "Otro"], label_visibility="collapsed")
    
    with st.form("registro_mascota"):
        st.markdown("### 🐶 Perfil Público")
        col1, col2 = st.columns(2)
        with col1: 
            nombre = st.text_input("Nombre", placeholder="Ej. Roco")
            raza = st.text_input("Raza", placeholder="Mestizo")
        with col2: 
            st.info("📸 **Subir foto de frente**")
            foto = st.file_uploader("Será su avatar en el Inicio", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

        st.markdown("---")
        st.markdown("### 📋 Ficha Clínica")
        col3, col4 = st.columns(2)
        with col3: 
            # --- NUEVO: SELECTORES DE DÍA Y MES (Rigor Técnico) ---
            st.markdown("**Día y Mes de Festejo**")
            col_dia, col_mes = st.columns([1, 2])
            with col_dia:
                dia_cumple = st.selectbox("Día", list(range(1, 32)), label_visibility="collapsed")
            with col_mes:
                lista_meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
                mes_cumple = st.selectbox("Mes", lista_meses, label_visibility="collapsed")
            
            edad = st.number_input("Edad aproximada (años)", 0, 30, 0)
            sexo = st.radio("Sexo", ["Macho", "Hembra"], horizontal=True)
            castrado = st.radio("¿Está castrado/a?", ["Sí", "No"], horizontal=True) 
        with col4: 
            peso = st.number_input("Peso (kg)", 0.0, 80.0, 0.0)
            st.markdown("**Plan Sanitario al día:**")
            check_antirrabica = st.checkbox("Vacuna Antirrábica")
            check_desparasitacion = st.checkbox("Desparasitación")
            
            if especie == "Perro": check_multiple = st.checkbox("Múltiple (Quíntuple/Séxtuple)")
            elif especie == "Gato": check_multiple = st.checkbox("Triple Felina")
            else: check_multiple = False
            
            condicion = st.text_area("Condición Médica (Opcional)", placeholder="Ej: Alergia, renguera en pata trasera, toma medicación...")

        submit = st.form_submit_button("Guardar Ficha y Generar QR")

    if submit:
        # ==========================================
        # 1. VALIDACIÓN ESTRICTA DE DATOS
        # ==========================================
        if not nombre or not raza or foto is None:
            st.error("🛑 ¡Faltan datos obligatorios! Por favor, completá el Nombre, la Raza y subí una Foto de frente antes de guardar.")
        else: 
            # --- ESCUDO ANTI-DUPLICADOS ---
            mascotas_existentes = obtener_datos_mascotas()
            celular_tutor = st.session_state.tutor_celular
            es_duplicado = False
            
            for mascota in mascotas_existentes.values():
                if mascota['Nombre_Mascota'].strip().lower() == nombre.strip().lower() and mascota['Celular'] == celular_tutor:
                    es_duplicado = True
                    break
            
            if es_duplicado:
                st.warning(f"⚠️ ¡Epa! Parece que **{nombre}** ya forma parte de tu manada. Si querés actualizar sus datos, andá a ⚙️ Configuración.")
            else:
                # ==========================================
                # 2. PROCESAMIENTO Y GUARDADO
                # ==========================================
                id_unico = f"ID-{random.randint(10000, 99999)}"
                
                extension = foto.name.split('.')[-1].lower()
                if extension == 'jpeg':
                    extension = 'jpg'
                
                os.makedirs(CARPETA_FOTOS, exist_ok=True)
                ruta_guardado = os.path.join(CARPETA_FOTOS, f"{id_unico}.{extension}")
                
                with open(ruta_guardado, "wb") as archivo_foto: 
                    archivo_foto.write(foto.getbuffer())
                
                lista_sanitaria = []
                if check_antirrabica: lista_sanitaria.append("Antirrábica")
                if check_desparasitacion: lista_sanitaria.append("Desparasitado")
                if especie == "Perro" and check_multiple: lista_sanitaria.append("Múltiple")
                if especie == "Gato" and check_multiple: lista_sanitaria.append("Triple Felina")
                texto_sanitario = ", ".join(lista_sanitaria) if lista_sanitaria else "Sin datos"
                
                # --- TRADUCCIÓN DEL CUMPLEAÑOS A FORMATO TÉCNICO (DD-MM) ---
                meses_num = {
                    "Enero": "01", "Febrero": "02", "Marzo": "03", "Abril": "04", 
                    "Mayo": "05", "Junio": "06", "Julio": "07", "Agosto": "08", 
                    "Septiembre": "09", "Octubre": "10", "Noviembre": "11", "Diciembre": "12"
                }
                # Esto genera el formato "24-02" para que la base de datos lo lea perfecto
                fecha_nac_tecnica = f"{dia_cumple:02d}-{meses_num[mes_cumple]}"
                
                nombre_contacto = st.session_state.tutor_nombre
                celular = st.session_state.tutor_celular
                domicilio = st.session_state.tutor_domicilio

                datos_nueva_mascota = {
                    'ID_Mascota': id_unico, 'PIN': '', 'Sena_Control': '',
                    'Nombre_Mascota': nombre, 'Especie': especie, 'Raza': raza, 
                    'Edad': edad, 'Sexo': sexo, 'Castrado': castrado, 
                    'Peso_Kg': peso, 'Estado_Sanitario': texto_sanitario, 
                    'Condicion_Medica': condicion, 'Nombre_Contacto': nombre_contacto, 
                    'Celular': celular, 'Domicilio': domicilio,
                    'Fecha_Nacimiento': fecha_nac_tecnica, # Dato blindado
                    'Estado_Vida': 'Vivo'
                }
                
                guardar_en_csv(datos_nueva_mascota)
                
                if 'mis_mascotas' not in st.session_state:
                    st.session_state.mis_mascotas = []
                
                st.session_state.mis_mascotas.append({
                    'nombre': nombre,
                    'foto_ruta': ruta_guardado
                })
                
                celular_limpio = "".join(filter(str.isdigit, celular))
                mensaje = urllib.parse.quote(f"¡Hola {nombre_contacto}! Encontré a {nombre}. Por favor, comunicate conmigo.")
                imagen_qr = qrcode.make(f"https://wa.me/549{celular_limpio}?text={mensaje}")
                buf = io.BytesIO()
                imagen_qr.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                if 'tutor_peluditos_registrados_ahora' in st.session_state:
                    st.session_state.tutor_peluditos_registrados_ahora += 1
                else:
                    st.session_state.tutor_peluditos_registrados_ahora = 1

                st.session_state.registro_exitoso = True
                st.session_state.ultimo_nombre = nombre
                st.session_state.ultimo_id = id_unico
                st.session_state.ultimo_qr = byte_im
                
                st.rerun()

    # === BOTONERA DE NAVEGACIÓN (INFERIOR) ===
    st.markdown("---")
    col_nav3, col_nav4 = st.columns(2)
    with col_nav3:
        if st.button("⬅️ Volver", key="btn_volver_abajo_formulario", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav4:
        if st.button("☰ Menú Principal", key="btn_menu_abajo_formulario", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    # =========================================
