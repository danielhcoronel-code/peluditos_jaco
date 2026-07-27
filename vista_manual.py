import streamlit as st

def mostrar_manual():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #8B4513;'>📖 Manual de Uso y Filosofía</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-weight: bold; font-size: 16px;'>Red Mascotera de Ing. Jacobacci</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #fdf4e3; padding: 20px; border-radius: 10px; border: 1px solid #e8dcc4; margin-bottom: 20px;'>
        <h3 style='color: #8B4513; margin-top: 0; text-align: center;'>🎯 Filosofía y Objetivos de <span style="font-family: 'Nunito', sans-serif; font-weight: 800;">Peluditos</span></h3>
        <p style='font-size: 16px; color: #5D4037; line-height: 1.6;'>
        Esta plataforma no es simplemente una base de datos o una cartelera digital; es una herramienta comunitaria nacida en Jacobacci para transformar la convivencia entre vecinos y sus animales. Nuestros objetivos son:
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("#### 🚨 Objetivo 1: Contención y Urgencias")
        st.write("Centralizar los pedidos de S.O.S., extraviados y situaciones de peligro para actuar en red de forma inmediata.")

    with st.container(border=True):
        st.markdown("#### 🪪 Objetivo 2: Padrón y Fichas Digitales")
        st.write("Organizar y formalizar la información mascotera (un padrón real) para campañas de salud, zoonosis o adopción.")

    with st.container(border=True):
        st.markdown("#### 📚 Objetivo 3: Educación y Prevención")
        st.write("Educar y prevenir, centralizando la información útil sobre tenencia responsable y cuidados comunitarios.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # === BOTONERA DE NAVEGACIÓN ===
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Volver", key="btn_volver_manual", use_container_width=True):
            st.session_state.vista = st.session_state.get('vista_anterior', 'menu')
            st.rerun()
    with col2:
        if st.button("☰ Menú Principal", key="btn_menu_manual", use_container_width=True):
            st.session_state.vista_anterior = st.session_state.vista
            st.session_state.vista = 'menu'
            st.rerun()
