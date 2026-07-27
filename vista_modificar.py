import streamlit as st
import os
import io
import qrcode
import urllib.parse
from base_datos import obtener_datos_mascotas, actualizar_en_csv, CARPETA_FOTOS

def mostrar_modificar():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN (SUPERIOR) ===
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Volver", key="btn_volver_arriba_modificar", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav2:
        if st.button("☰ Menú Principal", key="btn_menu_arriba_modificar", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    st.markdown("---")
    # =========================================
    
    st.markdown("<h2 style='text-align: center;'>✏️ Modificar Ficha</h2>", unsafe_allow_html=True)
    st.write("Ingresá el número de tu mascota para recuperar sus datos, hacer correcciones o **recuperar tu código QR**.")
    
    col_busqueda1, col_busqueda2 = st.columns([3, 1])
    with col_busqueda1:
        entrada_buscar = st.text_input("Número de la Mascota", placeholder="Ej: 45921", label_visibility="collapsed")
    with col_busqueda2:
        btn_buscar = st.button("Buscar Ficha", use_container_width=True)
        
    if btn_buscar and entrada_buscar:
        num_limpio = "".join(filter(str.isdigit, entrada_buscar))
        id_buscar = f"ID-{num_limpio}"
        
        diccionario_mascotas = obtener_datos_mascotas()
        if id_buscar in diccionario_mascotas:
            st.session_state.mascota_a_editar = diccionario_mascotas[id_buscar]
            st.success("¡Ficha encontrada! Podés corregir los datos aquí abajo.")
        else:
            st.error("No encontramos ninguna mascota con ese número. Revisalo bien.")
            st.session_state.mascota_a_editar = None

    if st.session_state.get('mascota_a_editar'):
        m_edit = st.session_state.mascota_a_editar
        
        with st.expander("📲 Ver / Recuperar Código QR de la Chapita", expanded=False):
            st.write("Si perdiste la chapita, acá tenés el QR para volver a imprimirla:")
            cel_limpio = "".join(filter(str.isdigit, m_edit.get('Celular', '')))
            msg = urllib.parse.quote(f"¡Hola {m_edit.get('Nombre_Contacto', '')}! Encontré a {m_edit.get('Nombre_Mascota', '')}. Por favor, comunicate conmigo.")
            img_qr = qrcode.make(f"https://wa.me/549{cel_limpio}?text={msg}")
            buffer = io.BytesIO()
            img_qr.save(buffer, format="PNG")
            img_bytes = buffer.getvalue()
            
            col_qr_izq, col_qr_cen, col_qr_der = st.columns([1, 2, 1])
            with col_qr_cen:
                st.image(img_bytes, use_container_width=True)
                st.download_button(
                    label="⬇️ Descargar Chapita QR",
                    data=img_bytes,
                    file_name=f"QR_{m_edit.get('Nombre_Mascota', 'Mascota')}.png",
                    mime="image/png",
                    use_container_width=True
                )

        st.markdown("### 🐾 Especie")
        especies = ["Perro", "Gato", "Otro"]
        idx_esp = especies.index(m_edit['Especie']) if m_edit['Especie'] in especies else 0
        especie_ed = st.selectbox("Modificar Especie (si hubo un error):", especies, index=idx_esp, key="sel_esp_ed")
        
        with st.form("edicion_mascota"):
            st.markdown("### 🐶 Perfil Público")
            col1, col2 = st.columns(2)
            with col1: 
                nombre_ed = st.text_input("Nombre", value=m_edit['Nombre_Mascota'])
                raza_ed = st.text_input("Raza", value=m_edit['Raza'])
            with col2: 
                st.markdown("**📸 Actualizar Foto**")
                foto_ed = st.file_uploader("Subir foto nueva", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
                
            st.markdown("---")
            st.markdown("### 📋 Ficha Clínica")
            col3, col4 = st.columns(2)
            with col3: 
                try: edad_val = int(m_edit['Edad'])
                except: edad_val = 0
                edad_ed = st.number_input("Edad (años)", 0, 30, edad_val)
                
                idx_sexo = 0 if m_edit['Sexo'] == "Macho" else 1
                sexo_ed = st.radio("Sexo", ["Macho", "Hembra"], index=idx_sexo, horizontal=True)
                idx_cast = 0 if m_edit['Castrado'] == "Sí" else 1
                castrado_ed = st.radio("¿Está castrado/a?", ["Sí", "No"], index=idx_cast, horizontal=True) 
            with col4: 
                try: peso_val = float(m_edit['Peso_Kg'])
                except: peso_val = 0.0
                peso_ed = st.number_input("Peso (kg)", 0.0, 50.0, peso_val)
                
                estado_actual = m_edit.get('Estado_Sanitario', '')
                st.markdown("**Plan Sanitario al día:**")
                check_antirrabica_ed = st.checkbox("Vacuna Antirrábica", value=("Antirrábica" in estado_actual))
                check_desparasitacion_ed = st.checkbox("Desparasitación", value=("Desparasitado" in estado_actual))
                
                if especie_ed == "Perro": check_multiple_ed = st.checkbox("Múltiple (Quíntuple/Séxtuple)", value=("Múltiple" in estado_actual))
                elif especie_ed == "Gato": check_multiple_ed = st.checkbox("Triple Felina", value=("Triple" in estado_actual))
                else: check_multiple_ed = False
                
                condicion_ed = st.text_area("Condición Médica", value=m_edit.get('Condicion_Medica', ''))

            st.markdown("---")
            st.markdown("### 📞 Contacto de Emergencia")
            nombre_contacto_ed = st.text_input("Tu nombre", value=m_edit.get('Nombre_Contacto', ''))
            celular_ed = st.text_input("Celular (WhatsApp)", value=m_edit.get('Celular', ''))
            domicilio_ed = st.text_input("Barrio o Domicilio", value=m_edit.get('Domicilio', ''))
            
            if st.form_submit_button("Guardar Cambios"):
                if foto_ed is not None:
                    ruta_guardado = os.path.join(CARPETA_FOTOS, f"{m_edit['ID_Mascota']}.jpg")
                    with open(ruta_guardado, "wb") as archivo_foto: archivo_foto.write(foto_ed.getbuffer())
                
                lista_sanitaria_ed = []
                if check_antirrabica_ed: lista_sanitaria_ed.append("Antirrábica")
                if check_desparasitacion_ed: lista_sanitaria_ed.append("Desparasitado")
                if especie_ed == "Perro" and check_multiple_ed: lista_sanitaria_ed.append("Múltiple")
                if especie_ed == "Gato" and check_multiple_ed: lista_sanitaria_ed.append("Triple Felina")
                texto_sanitario_ed = ", ".join(lista_sanitaria_ed) if lista_sanitaria_ed else "Sin datos"
                
                actualizar_en_csv({
                    'ID_Mascota': m_edit['ID_Mascota'], 
                    'PIN': m_edit.get('PIN', ''),
                    'Sena_Control': m_edit.get('Sena_Control', ''),
                    'Nombre_Mascota': nombre_ed, 'Especie': especie_ed, 'Raza': raza_ed, 
                    'Edad': edad_ed, 'Sexo': sexo_ed, 'Castrado': castrado_ed, 
                    'Peso_Kg': peso_ed, 'Estado_Sanitario': texto_sanitario_ed, 
                    'Condicion_Medica': condicion_ed, 'Nombre_Contacto': nombre_contacto_ed, 
                    'Celular': celular_ed, 'Domicilio': domicilio_ed,
                    'Fecha_Nacimiento': m_edit.get('Fecha_Nacimiento', ''),
                    'Estado_Vida': m_edit.get('Estado_Vida', 'Vivo')
                })
                st.success("¡Ficha actualizada con éxito! Ya podés volver al inicio.")

    # === BOTONERA DE NAVEGACIÓN (INFERIOR) ===
    st.markdown("---")
    col_nav3, col_nav4 = st.columns(2)
    with col_nav3:
        if st.button("⬅️ Volver", key="btn_volver_abajo_modificar", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav4:
        if st.button("☰ Menú Principal", key="btn_menu_abajo_modificar", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    # =========================================
