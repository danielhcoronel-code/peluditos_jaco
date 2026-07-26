import streamlit as st
import os
from datetime import datetime

def mostrar_consultas():
    # Título principal
    st.markdown("<h2 style='text-align: center;'>🩺 Consultorio Médico</h2>", unsafe_allow_html=True)
    
    # Creamos dos columnas: una para la foto y otra para el texto general
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Cargamos la imagen de los doctores
        try:
            st.image("doctores-2.png", use_container_width=True)
        except:
            st.info("🖼️ Falta la imagen doctores-2.png en la carpeta")
            
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("Elegí a quién querés consultarle hoy para sacarte las dudas. Recordá que esta es una guía de primeros auxilios y conocimientos generales de la manada. **Ante síntomas severos o dudas urgentes, la revisión final siempre debe hacerla un médico veterinario.**")

    st.markdown("---")

    # Creamos las dos pestañas
    tab_roco, tab_aquita = st.tabs(["🐶 El rincón de Roco", "🐱 Los consejos de Aquí-ta"])

    # ==========================================
    # PESTAÑA DE ROCO
    # ==========================================
    with tab_roco:
        st.markdown("<h3 style='color: #8B4513;'>🐶 Roco te orienta</h3>", unsafe_allow_html=True)
        st.write("¡Guau! Llevo más de 15 años siendo el rey absoluto de mi casa, rodeado de mimos, siestas cómodas y excelente atención. Nunca me faltó nada, así que conozco de primera mano la importancia de una buena cucha, una dieta sana y el calor de una familia. Preguntame lo que necesites sobre nuestros cuidados.")
        
        preguntas_roco = [
            "Elegí una pregunta...",
            "¿Qué hago si encuentro un perro asustado en la calle?",
            "¿Les hace mal a los perros comer las sobras del asado?"
        ]
        
        eleccion_roco = st.selectbox("Tus dudas perrunas:", preguntas_roco, key="select_roco")
        
        if eleccion_roco == "¿Qué hago si encuentro un perro asustado en la calle?":
            st.success("Primero, asegurate de no asustarlo más. Tratá de retenerlo en un lugar seguro sin arriesgarte, sacale una foto y subí urgente la alerta en la sección 'S.O.S Alertas' para que la manada vecinal empiece a buscar a su familia.")
        
        elif eleccion_roco == "¿Les hace mal a los perros comer las sobras del asado?":
            st.warning("¡Mucho cuidado! Los huesos cocidos se astillan súper fácil y nos pueden lastimar gravemente el estómago o los intestinos. Además, la grasa provoca problemas digestivos severos. Si nos querés malcriar, mejor un pedacito de carne magra bien cocida y sin nada de hueso.")

    # ==========================================
    # PESTAÑA DE AQUÍ-TA
    # ==========================================
    with tab_aquita:
        st.markdown("<h3 style='color: #5D4037;'>🐱 Aquí-ta te aconseja</h3>", unsafe_allow_html=True)
        st.write("¡Miau! Desde mi rincón observo todo y la tengo clarísima. Dejame ayudarte con el misterioso mundo felino.")
        
        preguntas_aquita = [
            "Elegí una pregunta...",
            "¿Le hace mal a mi gato comer alimento de perro?",
            "¿Por qué mi gato araña los sillones de casa?"
        ]
        
        eleccion_aquita = st.selectbox("Tus dudas felinas:", preguntas_aquita, key="select_aquita")
        
        if eleccion_aquita == "¿Le hace mal a mi gato comer alimento de perro?":
            st.error("¡Sí, es súper peligroso a largo plazo! Los gatos somos carnívoros estrictos y necesitamos taurina para mantener sano el corazón y la vista. El alimento de perro no trae la cantidad que necesitamos.")
            
        elif eleccion_aquita == "¿Por qué mi gato araña los sillones de casa?":
            st.info("No lo hacemos por maldad. Necesitamos afilar nuestras uñas, estirar bien la columna y dejar marcas olfativas. Conseguinos un buen rascador, ponelo bien cerquita del sillón, y vas a ver cómo dejamos tus muebles en paz.")

    # ==========================================
    # BUZÓN DE NUEVAS CONSULTAS (CAPTURA DE PREGUNTAS)
    # ==========================================
    st.markdown("---")
    st.markdown("<h4 style='text-align: center; color: #5D4037;'>¿No encontraste lo que buscabas?</h4>", unsafe_allow_html=True)
    st.write("Dejale tu pregunta a Roco o a Aquí-ta. El equipo veterinario la revisará y pronto aparecerá en la lista de respuestas.")
    
    with st.form("form_nuevas_consultas", clear_on_submit=True):
        nueva_pregunta = st.text_area("Escribí tu consulta acá:")
        enviado = st.form_submit_button("Enviar consulta a la Manada")
        
        if enviado:
            if nueva_pregunta.strip() == "":
                st.warning("Por favor, escribí una pregunta antes de enviar.")
            else:
                # Se crea y guarda en un archivo de texto dentro de tu carpeta
                with open("nuevas_consultas.txt", "a", encoding="utf-8") as f:
                    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{fecha_hora}] {nueva_pregunta}\n")
                st.success("¡Tu consulta fue enviada con éxito! Próximamente la sumaremos al consultorio.")
