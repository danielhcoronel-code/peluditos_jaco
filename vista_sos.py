import streamlit as st
import random
import folium
from streamlit_folium import st_folium
import urllib.parse
import os
import datetime
import smtplib # Nuevo para la Vía Silenciosa
from email.message import EmailMessage
# ---> Acá conectamos con tu ruta de fotos oficial <---
from base_datos import guardar_alerta_csv, CARPETA_FOTOS

# Función de triangulación de doble vía (Vía Silenciosa - Email)
def enviar_email_alerta(id_sos, telefono_tutor):
    # CONFIGURÁ ESTOS DATOS CON TU CUENTA GMAIL
    email_user = "tu_email@gmail.com" 
    email_pass = "tu_app_password" 
    destinatario = "celular_sos@gmail.com"
    
    msg = EmailMessage()
    msg['Subject'] = f"🚨 URGENCIA: Reporte del PIN {id_sos}"
    msg['From'] = email_user
    msg['To'] = destinatario
    msg.set_content(f"🚨 URGENCIA: Reporte del PIN {id_sos}. Teléfono del tutor para triangular: {telefono_tutor}")
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
    except Exception as e:
        st.error(f"Error al enviar aviso silencioso: {e}")

def mostrar_sos():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #D32F2F;'>🚨 S.O.S. Animalito en Peligro</h2>", unsafe_allow_html=True)

    # --- NUEVA INTRODUCCIÓN AMIGABLE Y CLARA (UX) ---
    st.markdown("""
    <div style='background-color: #ffe6e6; padding: 15px; border-radius: 8px; text-align: center; margin-bottom: 20px; border: 1px solid #ffcccc;'>
    ⚠️ <b>¡Tu ayuda salva vidas!</b><br>
    Esta sección es exclusiva para reportar <b>urgencias de animalitos en la calle</b> (por ejemplo, si están atropellados, perdidos, o en peligro inminente). <br><br>
    📍 <b>¿Cómo funciona?</b> Marcá el lugar en el mapa, subí una foto de la situación y dejá tus datos para que los rescatistas puedan contactarte de inmediato.
    </div>
    """, unsafe_allow_html=True)

    # --- PASO 1: MAPA ---
    st.markdown("### 📍 ¿Dónde es la emergencia?")
    mapa_sos = folium.Map(location=[-41.332, -69.545], zoom_start=15)
    mapa_datos = st_folium(mapa_sos, height=300, width=700, key="mapa_emergencia_sos")
    
    lat_click, lon_click = "", ""
    if mapa_datos and mapa_datos.get("last_clicked"):
        lat_click = mapa_datos["last_clicked"]["lat"]
        lon_click = mapa_datos["last_clicked"]["lng"]
        st.success("✅ Ubicación marcada.")

    # --- PASO 2: FORMULARIO ---
    with st.form("form_sos"):
        st.markdown("### 📸 Detalles de la situación")
        foto_sos = st.file_uploader("Subir foto del animalito", type=['png', 'jpg', 'jpeg'])
        detalles = st.text_area("Describí qué pasó")
        
        col_id1, col_id2 = st.columns(2)
        with col_id1:
            nombre_den = st.text_input("Nombre y Apellido")
            dni_den = st.text_input("DNI")
        with col_id2:
            celular_den = st.text_input("Tu Celular")

        if st.form_submit_button("📢 Publicar Alerta S.O.S.", type="primary"):
            if not lat_click or not detalles or not nombre_den or not celular_den:
                st.error("⚠️ Faltan datos obligatorios (Marcá el lugar en el mapa y completá tus datos).")
