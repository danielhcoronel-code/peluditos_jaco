import streamlit as st
import os
from PIL import Image

# Función auxiliar para cargar imágenes de forma segura
def cargar_imagen(ruta):
    if os.path.exists(ruta):
        return Image.open(ruta)
    return None

def mostrar_manual():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN (SUPERIOR) ===
    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("⬅️ Volver", key="btn_volver_arriba_manual", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav2:
        if st.button("☰ Menú Principal", key="btn_menu_arriba_manual", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    st.markdown("---")
    # =========================================
    
    # Estilos CSS para el manual (Formal y legible con toques de color)
    st.markdown("""
        <style>
        .manual-header { text-align: center; color: #5d4037; margin-bottom: 30px; font-weight: bold; }
        .manual-title { color: #d35400; font-weight: bold; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #d35400; padding-bottom: 5px; }
        .manual-subtitle { color: #8d6e63; font-weight: bold; margin-top: 25px; margin-bottom: 10px; }
        .manual-text { color: #333; line-height: 1.7; font-size: 15px; text-align: justify; }
        .manual-tip { background-color: #e8f5e9; padding: 15px; border-left: 5px solid #2e7d32; border-radius: 5px; margin: 20px 0; font-size: 14px;}
        .manual-obj { background-color: #fff3e0; padding: 10px; border-left: 5px solid #e65100; border-radius: 5px; margin: 10px 0; color: #333; font-size: 14px;}
        .manual-step { background-color: #f5f5f5; padding: 10px; border-radius: 5px; color: #5d4037; font-weight: bold; margin-top: 10px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='manual-header'>📖 Guía de Usabilidad y Objetivos</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #795548;'>Red Mascotera de Ingeniero Jacobacci</h4>", unsafe_allow_html=True)

    # ==========================================
    # SECCIÓN 1: OBJETIVOS DEL SOFTWARE (PISADO ANTERIOR)
    # ==========================================
    st.markdown("<h2 class='manual-title'>🎯 Filosofía y Objetivos de 'Mi Mascota y Yo'</h2>", unsafe_allow_html=True)
    st.markdown("<p class='manual-text'>Esta plataforma no es simplemente una base de datos o una cartelera digital; es una herramienta comunitaria nacida en Jacobacci para transformar la convivencia entre vecinos y sus animales. Nuestros objetivos son:</p>", unsafe_allow_html=True)

    st.markdown("<div class='manual-obj'>🚨 centralizando el pedido de S.O.S.</div>", unsafe_allow_html=True)
    st.markdown("<div class='manual-obj'>📋 <b>Objetivo 2:</b> Organizar y formalizar la información mascotera (un padrón real) para campañas de salud o adopción.</div>", unsafe_allow_html=True)
    st.markdown("<div class='manual-obj'>🩺 <b>Objetivo 3:</b> Educar y prevenir, centralizando la información médica verificada (de Zoonosis).</div>", unsafe_allow_html=True)

    # ESPACIO PARA LA IMAGEN 2: Objetivos
    img2 = cargar_imagen("manual_img2.png")
    if img2:
        st.image(img2, caption="Imagen 2: El impacto real de los objetivos comunales", use_container_width=True)

    st.markdown("---")

    # ==========================================
    # SECCIÓN 2: EL MANUAL (VISTA USUARIO)
    # ==========================================
    st.markdown("<h2 class='manual-title'>👤 Manual del Vecino (Usuario)</h2>", unsafe_allow_html=True)
    
    # 1. Pimeros Pasos (Pisado anterior)
    st.markdown("<h3 class='manual-subtitle'>1. Instalación y Primeros Pasos</h3>", unsafe_allow_html=True)
    st.markdown("<p class='manual-text'>Recordá crear un acceso directo en tu pantalla de inicio para tener la app siempre a mano, como un ícono más de tu teléfono.</p>", unsafe_allow_html=True)

    # 2. El Padrón (NUEVO CAPÍTULO)
    st.markdown("<h3 class='manual-subtitle'>2. El Padrón: Cómo registrar a tu mascota</h3>", unsafe_allow_html=True)
    
    st.markdown("<p class='manual-text'>Para que la red funcione y podamos proteger a tu compañero, lo primero que necesitamos es crearle su DNI digital. Este padrón unificado le permite a Zoonosis y a Patitas Felices saber quiénes somos y cómo contactarnos.</p>", unsafe_allow_html=True)

    st.markdown("<div class='manual-step'>Paso 1: Ingresá al Padrón</div>", unsafe_allow_html=True)
    st.markdown("<p class='manual-text'>En la pantalla principal, tocá el botón verde que dice <b>'➕ Registrar Mascota'</b>. Esto abrirá un formulario seguro.</p>", unsafe_allow_html=True)

    st.markdown("<div class='manual-step'>Paso 2: Completá los datos básicos</div>", unsafe_allow_html=True)
    st.markdown("<p class='manual-text'>Llená el formulario con el nombre de tu mascota, su especie (perro/gato), sexo y tu información de contacto (nombre y teléfono). Estos datos son <b>fundamentales</b> para contactarte si tu mascota se extravía.</p>", unsafe_allow_html=True)

    st.markdown("<div class='manual-step'>Paso 3: Tomá la foto (Lo más importante)</div>", unsafe_allow_html=True)
    st.markdown("<p class='manual-text'>Llegamos al punto clave. Necesitamos una foto clara para que sea reconocible al instante. El sistema te permite elegir entre usar la cámara de tu celular en ese momento o subir una foto que ya tengas guardada.</p>", unsafe_allow_html=True)

    # ESPACIO PARA LA IMAGEN 3: Registro (Mascota image_5.png)
    img3 = cargar_imagen("manual_img3.png") # Asegurate de guardar image_5.png con este nombre
    if img3:
        st.image(img3, caption="Imagen 3: Usando la cámara para el registro", use_container_width=True)
    else:
        st.info("🖼️ (Aquí cargaremos la Imagen 3: Ilustrando el uso de la cámara para el registro, Mascota `image_5.png`)")

    st.markdown("<p class='manual-text'>Al tocar el botón de '📸 Tomar Foto', se activará la cámara de tu teléfono. Buscá un ángulo con buena luz donde se le vea bien la carita (como muestra la imagen). Una vez capturada, el sistema procesará la imagen automáticamente.</p>", unsafe_allow_html=True)

    st.markdown("<div class='manual-step'>Paso 4: Finalizá el registro</div>", unsafe_allow_html=True)
    st.markdown("<p class='manual-text'>Revisá que todos los datos estén bien y tocá el botón de <b>'Guardar Registro'</b>. ¡Listo! Tu mascota ya es parte del padrón municipal.</p>", unsafe_allow_html=True)

    st.markdown("<div class='manual-tip'>💡 <b>TIP DE USABILIDAD:</b> Si tu mascota es difícil de fotografiar porque no se queda quieta, te recomendamos que primero le saques una buena foto con la aplicación de la cámara normal de tu celular y luego, al momento de registrarla, elijas la opción de <b>'Subir foto existente'</b>.</div>", unsafe_allow_html=True)


    # === BOTONERA DE NAVEGACIÓN (INFERIOR) ===
    st.markdown("---")
    col_nav3, col_nav4 = st.columns(2)
    with col_nav3:
        if st.button("⬅️ Volver", key="btn_volver_abajo_manual", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col_nav4:
        if st.button("☰ Menú Principal", key="btn_menu_abajo_manual", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
    # =========================================
