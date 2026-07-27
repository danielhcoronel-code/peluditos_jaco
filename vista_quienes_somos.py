import streamlit as st
import os

def mostrar_quienes_somos():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #8B4513;'>🐾 <span style=\"font-family: 'Nunito', sans-serif; font-weight: 800;\">Peluditos</span>: La Red Animal de Jacobacci</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #fdf4e3; padding: 20px; border-radius: 10px; border: 1px solid #e8dcc4; margin-bottom: 20px;'>
        <p style='font-size: 16px; color: #5D4037; line-height: 1.6;'>
        Esta plataforma no es simplemente una base de datos o una cartelera digital más; es una <b>herramienta comunitaria nacida en Jacobacci</b> para transformar la convivencia entre los vecinos y nuestros animales.
        </p>
        <p style='font-size: 16px; color: #5D4037; line-height: 1.6;'>
        No estamos armando una planilla fría. <span style="font-family: 'Nunito', sans-serif; font-weight: 800;">Peluditos</span> es una red vecinal pensada exclusivamente para darle el estatus de familia a nuestros compañeros de cuatro patas. Nuestro objetivo principal es darte a vos, como tutor, la <b>tranquilidad absoluta de que tu animalito está protegido y respaldado por toda nuestra comunidad</b>, trabajando siempre con datos 100% reales y transparentes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🤝 Un Motor 100% Solidario")
    st.markdown("""
    Al usar la app, formás parte de una gran red de ayuda para vos en caso de que la necesites por cualquier infortunio, y para el grupo de chicas que integran **PATITAS FELICES**. Quienes, con un enorme e inquebrantable esfuerzo, trabajan día a día para lograr que **hayan menos patitas tristes deambulando solas por nuestra localidad**.
    
    Para ello hemos dispuesto que cada auspiciante se transforme en un colaborador de Patitas Felices, porque su aporte ayudará a sostener su proyecto y esta app que cariñosamente hemos llamado <span style="font-family: 'Nunito', sans-serif; font-weight: 800;">Peluditos</span>.
    
    Además, en la plataforma vas a encontrar botones de **Mercado Pago** para que, de forma totalmente voluntaria, te conviertas en "Padrino" de la agrupación, aportando las veces que quieras y el monto que puedas.
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 ¿Qué vas a encontrar en este sistema?")
    
    st.markdown("""
    * 👤 **Tu espacio personal:** Un rincón digital diseñado a medida donde tus animales son los protagonistas. Primero deberás registrarte vos como tutor y luego a tus mascotas. Así creás tu perfil único dentro de <span style="font-family: 'Nunito', sans-serif; font-weight: 800;">Peluditos</span>.
    * 🪪 **La Ficha Digital Única:** Es el verdadero "DNI" de tu mascota. Al registrar a tu compañero, el sistema le va a generar un Número de ID único e irrepetible, idéntico en su función a nuestro número de documento. Esta base de datos real, honesta y sin intermediarios es la clave para que Zoonosis y el Hospital local puedan agilizar la atención y garantizar la salud pública en Jacobacci.
    * 📱 **La Chapita Inteligente (Código QR):** ¡La columna vertebral del proyecto! Al registrar a tu compañero, el sistema genera automáticamente un Código QR único en alta calidad. Podés imprimirlo o mandarlo a grabar en su chapita de metal. Si alguien lo encuentra en la calle, con solo escanearlo con el celular se abrirá un chat de WhatsApp directo con vos para avisarte al instante.
    """, unsafe_allow_html=True)

    # Imagen 1 (Tutor con el perrito y celular S.O.S.) + Epígrafe de Extravío
    if os.path.exists("imagen_contexto_1.png"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("imagen_contexto_1.png", use_container_width=True)
        st.markdown("""
        <p style='text-align: center; font-size: 15px; color: #795548; font-style: italic; margin-top: 5px; margin-bottom: 15px;'>
        📖 En el <b>Manual de Uso</b> te explicamos paso a paso cómo actuar y activar la red comunitaria en caso de <b>extravío</b>.
        </p>
        """, unsafe_allow_html=True)

    st.markdown("""
    * 🚨 **Red de Contención S.O.S.:** Nuestro sistema de alerta rápida. No solo se activa si un compañero se pierde para que todo Jacobacci se entere y ayude a buscarlo, sino que también es una herramienta vital para emitir avisos urgentes sobre cualquier animalito que se encuentre en una situación de riesgo real de vida. Una red de vecinos atentos cuidando a los que no tienen voz. En el momento exacto que des el aviso, **la noticia impactará inmediatamente en nuestra PÁGINA DE FACEBOOK "PELUDITOS EN RED"**.
    """)

    # Imagen de Peluditos en Red (Facebook)
    if os.path.exists("peluditosenred.png"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("peluditosenred.png", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    * 🏪 **Comercios Adheridos:** Vas a notar espacios publicitarios de locales amigos. El valioso aporte de estos comercios genera ingresos que van destinados directamente a ayudar a Patitas Felices y contribuye al sostenimiento de esta plataforma para que siga activa y gratuita. Podrás solicitar ser parte de esta app con solo un clic en el botón de WhatsApp dispuesto para ello.
    * 💖 **El Botón "Padrinos":** En distintas pantallas vas a ver un botón a disposición por si alguna vez querés y podés hacer un aporte voluntario. ¡Cada granito de arena ayuda a mantener esta red viva!
    """)

    # Imagen 2 + Epígrafe de Socorrismo + Frase final
    if os.path.exists("imagen_contexto_2.png"):
        st.markdown("<br>", unsafe_allow_html=True)
        st.image("imagen_contexto_2.png", use_container_width=True)
        st.markdown("""
        <p style='text-align: center; font-size: 15px; color: #795548; font-style: italic; margin-top: 5px; margin-bottom: 15px;'>
        📖 En el <b>Manual de Uso</b> te detallamos cómo proceder ante situaciones de <b>socorrismo y rescate</b> según corresponda.
        </p>
        """, unsafe_allow_html=True)
        
        # Frase destacada única e infalible al final
        st.markdown("""
        <div style='background-color: #f7e6d4; padding: 15px; border-radius: 8px; border-left: 5px solid #8B4513; text-align: center; margin: 15px 0;'>
            <p style='font-size: 18px; font-weight: 800; color: #5D4037; font-style: italic; margin: 0;'>
            "Salvar a un animal de la calle no cambiará el mundo... pero para él, su mundo entero cambia para siempre."
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # === BOTONERA DE NAVEGACIÓN ===
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Volver", key="btn_volver_quienes", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col2:
        if st.button("☰ Menú Principal", key="btn_menu_quienes", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
