import streamlit as st
import random
import os
import urllib.parse
import io
import qrcode
from base_datos import guardar_en_csv, CARPETA_FOTOS

def mostrar_formulario():
    st.markdown("<h2 style='text-align: center;'>Formulario de Registro</h2>", unsafe_allow_html=True)
    
    st.markdown("### 🐾 ¿Qué animalito vamos a registrar?")
    especie = st.selectbox("Elegí la especie para adaptar la Ficha Clínica:", ["Perro", "Gato", "Otro"], label_visibility="collapsed")
    
    with st.form("registro_mascota"):
        st.markdown("### 🐶 Perfil Público")
        col1, col2 = st.columns(2)
        with col1: 
            nombre = st.text_input("Nombre", placeholder="Ej. Roco")
            raza = st.text_input("Raza", placeholder="Mestizo")
        with col2: 
            st.info("📸 **Subir foto de la mascota**")
            foto = st.file_uploader("Debe ser clara y de frente", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

        st.markdown("---")
        st.markdown("### 📋 Ficha Clínica")
        col3, col4 = st.columns(2)
        with col3: 
            edad = st.number_input("Edad (años)", 0, 30, 0)
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

        st.markdown("---")
        st.markdown("### 📞 Contacto de Emergencia")
        st.warning("🔒 Tus datos personales son confidenciales. Solo se usarán en el código QR y de forma interna.")
        nombre_contacto = st.text_input("Tu nombre")
        celular = st.text_input("Celular (WhatsApp)", placeholder="Ej: 2944123456")
        domicilio = st.text_input("Barrio o Domicilio")
        
        if st.form_submit_button("Guardar Datos y Generar QR"):
            if nombre and celular:
                id_unico = f"ID-{random.randint(10000, 99999)}"
                if foto is not None:
                    ruta_guardado = os.path.join(CARPETA_FOTOS, f"{id_unico}.jpg")
                    with open(ruta_guardado, "wb") as archivo_foto: archivo_foto.write(foto.getbuffer())
                
                lista_sanitaria = []
                if check_antirrabica: lista_sanitaria.append("Antirrábica")
                if check_desparasitacion: lista_sanitaria.append("Desparasitado")
                if especie == "Perro" and check_multiple: lista_sanitaria.append("Múltiple")
                if especie == "Gato" and check_multiple: lista_sanitaria.append("Triple Felina")
                texto_sanitario = ", ".join(lista_sanitaria) if lista_sanitaria else "Sin datos"
                
                datos_nueva_mascota = {
                    'ID_Mascota': id_unico, 'PIN': '', 'Sena_Control': '',
                    'Nombre_Mascota': nombre, 'Especie': especie, 'Raza': raza, 
                    'Edad': edad, 'Sexo': sexo, 'Castrado': castrado, 
                    'Peso_Kg': peso, 'Estado_Sanitario': texto_sanitario, 
                    'Condicion_Medica': condicion, 'Nombre_Contacto': nombre_contacto, 
                    'Celular': celular, 'Domicilio': domicilio,
                    'Fecha_Nacimiento': '', 'Estado_Vida': 'Vivo'
                }
                
                guardar_en_csv(datos_nueva_mascota)
                st.success("¡Ficha guardada correctamente!")
                st.error(f"🛑 **¡IMPORTANTE!** La LLAVE SECRETA de tu mascota es el número: **{id_unico.split('-')[1]}**. Anotalo, es tu contraseña para editar datos o reportar extravíos.")
                
                celular_limpio = "".join(filter(str.isdigit, celular))
                mensaje = urllib.parse.quote(f"¡Hola {nombre_contacto}! Encontré a {nombre}. Por favor, comunicate conmigo.")
                imagen_qr = qrcode.make(f"https://wa.me/549{celular_limpio}?text={mensaje}")
                buf = io.BytesIO()
                imagen_qr.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.markdown("<h3 style='text-align: center;'>Tu Código QR</h3>", unsafe_allow_html=True)
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
            else: 
                st.error("Faltan datos obligatorios (Nombre de la mascota y tu número de Celular).")
