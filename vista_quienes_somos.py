import streamlit as st
import os

def mostrar_quienes_somos():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # --- NUEVO TÍTULO CON IDENTIDAD LOCAL ---
    st.markdown("<h2 style='text-align: center; color: #5D4037;'>PELUDITOS: LA RED ANIMAL DE JACOBACCI</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    Esta plataforma no es simplemente una base de datos o una cartelera digital más; es una herramienta comunitaria nacida en Jacobacci para transformar la convivencia entre los vecinos y nuestros animales.

    No estamos armando una planilla fría. **Peluditos es una red vecinal pensada exclusivamente para darle el estatus de familia a nuestros compañeros de cuatro patas.** Nuestro objetivo principal es darte a vos, como tutor, la tranquilidad absoluta de que tu animalito está protegido y respaldado por toda nuestra comunidad, trabajando siempre con datos 100% reales y transparentes.

    Pero además, este proyecto tiene un motor solidario. Al usar la app, formás parte de una gran red de ayuda.
    """)
    
    st.markdown("---")
    st.markdown("### 🐾 ¿Qué vas a encontrar en este sistema?")

    # ==========================================
    # BLOQUE 1: Espacio personal, Ficha y QR
    # ==========================================
    col_texto1, col_img1 = st.columns([2, 1], gap="large")
    
    with col_texto1:
        st.markdown("""
        *   **Tu espacio personal:** Un rincón digital diseñado a medida donde tus animales son los protagonistas. Al registrarte, creás el perfil único de tu manada.
        *   **La Ficha Digital Única:** Es el verdadero "DNI" de tu mascota. Al registrar a tu compañero, el sistema le va a generar un **Número de ID único e irrepetible**, idéntico en su función a nuestro número de documento. Esta base de datos real, honesta y sin intermediarios es la clave para que Zoonosis y el Hospital local puedan agilizar la atención y garantizar la salud pública en Jacobacci.
        *   **La Chapita Inteligente (Código QR):** ¡La columna vertebral del proyecto! Al registrar a tu compañero, el sistema genera automáticamente un Código QR único en alta calidad. Podés imprimirlo o mandarlo a grabar en su chapita de metal. Si alguien lo encuentra en la calle, con solo escanearlo con el celular se abrirá un chat de WhatsApp directo con vos para avisarte al instante.
        """)
        
    with col_img1:
        if os.path.exists("imagen_contexto_1.png"):
            st.image("imagen_contexto_1.png", use_container_width=True)
        else:
            st.info("🖼️ Acá iría tu primera imagen de contexto (ej. un perro y un gato con fondo blanco). Nombre del archivo: imagen_contexto_1.png")

    st.markdown("---")

    # ==========================================
    # BLOQUE 2: SOS, Comercios y Padrinos
    # ==========================================
    col_img2, col_texto2 = st.columns([1, 2], gap="large")
    
    with col_img2:
        if os.path.exists("imagen_contexto_2.png"):
            st.image("imagen_contexto_2.png", use_container_width=True)
        else:
            st.info("🖼️ Acá iría tu segunda imagen de contexto (ej. un logo de red o ayuda solidaria). Nombre del archivo: imagen_contexto_2.png")

    with col_texto2:
        st.markdown("""
        *   **Red de Contención S.O.S.:** Nuestro sistema de alerta rápida. No solo se activa si un compañero se pierde para que todo Jacobacci se entere y ayude a buscarlo, sino que también es una herramienta vital para emitir avisos urgentes sobre cualquier animalito que se encuentre en una situación de riesgo real de vida. Una red de vecinos atentos cuidando a los que no tienen voz.
        *   **Comercios Adheridos:** Vas a notar espacios publicitarios de locales amigos. El valioso aporte de estos comercios adheridos genera ingresos que van destinados directamente a ayudar a la agrupación Patitas Felices, y al mismo tiempo, contribuye al sostenimiento de esta plataforma para que siga activa y gratuita.
        *   **El Botón "Padrinos":** En todas las pantallas vas a ver un botón a disposición por si alguna vez querés y podés hacer un aporte voluntario. Cada granito de arena ayuda a mantener esta red viva.
        """)

    st.markdown("---")

    if st.button("🏠 Volver al Inicio", use_container_width=True):
        st.session_state.vista = 'inicio'
        st.rerun()
