import streamlit as st

def mostrar_tutor():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # Actualizado con la nueva identidad
    st.markdown("<h2 style='text-align: center;'>Bienvenido a Peluditos</h2>", unsafe_allow_html=True)
    
    # ==========================================
    # BOTÓN DE SALIDA (Si el tutor ya está en memoria)
    # ==========================================
    if st.session_state.get('tutor_registrado', False):
        st.success(f"¡Hola {st.session_state.tutor_nombre}! Tu sesión está activa.")
        st.info(f"Tenés agendado registrar {st.session_state.tutor_cantidad_peluditos} peluditos hoy.")
        
        if st.button("🔄 Cerrar Sesión / Soy otro tutor", use_container_width=True):
            # Limpiamos toda la memoria de la sesión actual
            claves_a_borrar = [
                'tutor_nombre', 'tutor_dni', 'tutor_celular', 'tutor_correo', 
                'tutor_domicilio', 'tutor_cantidad_peluditos', 
                'tutor_peluditos_registrados_ahora', 'tutor_registrado'
            ]
            for clave in claves_a_borrar:
                if clave in st.session_state:
                    del st.session_state[clave]
            st.rerun()
            
        # Cortamos la ejecución acá para que no vea el formulario de abajo
        return 

    # ==========================================
    # FORMULARIO DE INGRESO (Si la memoria está limpia)
    # ==========================================
    st.markdown("### 👤 Tu Perfil (Paso Obligatorio)")
    st.info("Antes de presentar a tus animales, necesitamos armar tu red de contacto. Esto se carga por única vez y es nuestro puente para avisarte ante cualquier urgencia.")

    with st.form("registro_tutor"):
        nombre_tutor = st.text_input("Tu Nombre y Apellido")
        # NUEVO CAMPO: DNI para validar existencia física
        dni = st.text_input("DNI (Sin puntos, solo números)", placeholder="Ej: 24555666") 
        celular = st.text_input("Celular (WhatsApp)", placeholder="Ej: 2944123456")
        correo = st.text_input("Correo Electrónico (Fundamental para emergencias)", placeholder="Ej: mi_correo@gmail.com")
        domicilio = st.text_input("Barrio o Domicilio exacto")
        
        # Pregunta mágica para el bucle
        cantidad_peluditos = st.number_input("¿Cuántos peluditos vas a registrar hoy?", min_value=1, max_value=10, value=1, step=1)

        submit = st.form_submit_button("Guardar mis datos e ingresar")

        if submit:
            # 1. Chequeamos que no falte nada (ahora incluye DNI)
            if not nombre_tutor or not dni or not celular or not correo or not domicilio:
                st.error("🛑 ¡Epa! Faltan datos. Por favor completá todas las casillas para que la red funcione.")
            
            # 2. Chequeamos que el nombre SOLO tenga letras y espacios
            elif not all(letra.isalpha() or letra.isspace() for letra in nombre_tutor.strip()):
                st.error("🛑 El nombre solo puede contener letras. Revisá que no se haya colado un número.")
            
            # 3. NUEVO: Validación técnica de DNI argentino
            elif not dni.isdigit() or len(dni) < 7 or len(dni) > 8:
                st.error("🛑 El DNI debe contener solo entre 7 y 8 números, sin puntos ni letras.")
            
            # 4. Chequeamos que el celular SOLO tenga números
            elif not celular.isdigit():
                st.error("🛑 El celular solo debe contener números (sin espacios, puntos ni guiones).")
                
            # 5. Chequeamos que el correo tenga formato básico
            elif "@" not in correo or "." not in correo:
                st.error("🛑 Por favor, ingresá un correo electrónico válido.")
            
            # Si pasó todas las pruebas, guardamos y avanzamos
            else:
                st.session_state.tutor_nombre = nombre_tutor
                st.session_state.tutor_dni = dni
                st.session_state.tutor_celular = celular
                st.session_state.tutor_correo = correo.strip().lower()
                st.session_state.tutor_domicilio = domicilio
                
                # Guardamos la cantidad y preparamos el contador para el formulario
                st.session_state.tutor_cantidad_peluditos = cantidad_peluditos
                st.session_state.tutor_peluditos_registrados_ahora = 0 
                
                st.session_state.tutor_registrado = True
                
                st.success(f"¡Perfil creado! Vamos a registrar a tu manada ({cantidad_peluditos} peludito/s)...")
                st.session_state.vista = 'formulario'
                st.rerun()
