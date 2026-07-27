import streamlit as st
import pandas as pd
import os
import datetime

def mostrar_hdt():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN (SUPERIOR) ===
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Volver", key="btn_volver_arriba_hdt", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav2:
        if st.button("☰ Menú Principal", key="btn_menu_arriba_hdt", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    st.markdown("---")
    # =========================================
    
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🏡 Sumate a la Red de Hogares de Tránsito (H.D.T.)</h2>", unsafe_allow_html=True)
    
    # ==========================================
    # FASE 1: DERRIBANDO MITOS (Educativa)
    # ==========================================
    st.markdown("""
    <div style='background-color: #f1f8e9; padding: 20px; border-radius: 10px; border-left: 5px solid #8bc34a; margin-bottom: 20px;'>
        <h4 style='color: #33691e; margin-top: 0;'>¿Qué es ser un Hogar de Tránsito? 🤔</h4>
        <p>Es abrir la puerta de tu patio o de tu casa <b>por un ratito</b> para evitar que un peludito pase la noche en la calle o corra peligro, mientras el sistema busca a su familia o le consigue un hogar definitivo.</p>
        <hr>
        <h4 style='color: #33691e;'>Derribando Mitos:</h4>
        <ul style='color: #444;'>
            <li><b>"Me lo voy a tener que quedar para siempre":</b> ¡NO! ❌ El tránsito es temporal (generalmente 24 a 72hs). Nuestro compromiso es mover cielo y tierra para reubicarlo.</li>
            <li><b>"Me va a salir carísimo darle de comer":</b> ¡NO! ❌ La red y la comunidad te acercan el alimento y cubren cualquier gasto veterinario urgente. Vos solo ponés el lugar y el cariño.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Ficha de Inscripción Voluntaria")
    st.write("Completá estos datos sin compromiso. Cuando haya una urgencia cerca tuyo, te mandamos un mensajito para ver si justo ese día podés dar una mano.")

    # ==========================================
    # FASE 2: FORMULARIO DE CAPTURA
    # ==========================================
    with st.form("form_hdt"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre y Apellido")
            celular = st.text_input("Celular (Ej: 2944123456)")
        with col2:
            barrio = st.text_input("¿En qué barrio vivís?")
            
        st.markdown("---")
        st.markdown("**Unos detalles sobre tu espacio:**")
        
        # ==========================================
        # ACÁ ESTÁN LAS PREGUNTAS QUE PEDISTE
        # ==========================================
        patio_cerrado = st.radio("¿Tenes patio cerrado?", ["Sí", "No"])
        otras_mascotas = st.radio("¿Hay otros peluditos en tu casa con los que pueda convivir?", ["Sí", "No"])
        # ==========================================
        
        tipo_mascota = st.selectbox("¿Qué preferís recibir?", ["Solo Perros", "Solo Gatos", "Perros y Gatos", "Lo que haga falta de urgencia"])
        
        observaciones = st.text_area("¿Alguna observación? (Ej: 'Tengo un perro un poco gruñón', 'Solo puedo los fines de semana', etc.)")
        
        submit_hdt = st.form_submit_button("🙋‍♂️ ¡Quiero ser Hogar de Tránsito!", type="primary")
        
        if submit_hdt:
            if not nombre or not celular or not barrio:
                st.error("🛑 Por favor, completá tu nombre, celular y barrio para que podamos contactarte.")
            else:
                # Armamos los datos a guardar
                nuevo_registro = {
                    "Fecha": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "Nombre": nombre,
                    "Celular": celular,
                    "Barrio": barrio,
                    "Patio_Cerrado": patio_cerrado,
                    "Otras_Mascotas": otras_mascotas,
                    "Tipo_Admitido": tipo_mascota,
                    "Observaciones": observaciones
                }
                
                # Archivo donde vamos a guardar los voluntarios
                archivo_hdt = "base_hdt.csv"
                
                # Si el archivo no existe, lo creamos. Si existe, agregamos la fila.
                if not os.path.exists(archivo_hdt):
                    df = pd.DataFrame([nuevo_registro])
                    df.to_csv(archivo_hdt, index=False, encoding='utf-8-sig')
                else:
                    df = pd.read_csv(archivo_hdt, encoding='utf-8-sig')
                    df_nuevo = pd.DataFrame([nuevo_registro])
                    df = pd.concat([df, df_nuevo], ignore_index=True)
                    df.to_csv(archivo_hdt, index=False, encoding='utf-8-sig')
                
                st.success(f"🎉 ¡Gracias de corazón, {nombre}! Ya sos parte de la Red de Rescate. Tu ayuda vale oro.")

    # === BOTONERA DE NAVEGACIÓN (INFERIOR) ===
    st.markdown("---")
    col_nav3, col_nav4 = st.columns(2)
    with col_nav3:
        if st.button("⬅️ Volver", key="btn_volver_abajo_hdt", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav4:
        if st.button("☰ Menú Principal", key="btn_menu_abajo_hdt", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    # =========================================
