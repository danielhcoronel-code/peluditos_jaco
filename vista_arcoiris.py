import streamlit as st
import os
import csv
import datetime
from base_datos import obtener_datos_mascotas, CARPETA_FOTOS

PALABRAS_PROHIBIDAS = ["boludo", "pelotudo", "puto", "puta", "mierda", "carajo", "forro", "concha", "idiota", "estupido", "tarado", "cagada"]

def validar_texto(texto):
    texto_min = texto.lower()
    for palabra in PALABRAS_PROHIBIDAS:
        if palabra in texto_min:
            return False
    return True

def guardar_tributo(id_mascota, autor, mensaje, emoji):
    archivo = "tributos_arcoiris.csv"
    existe = os.path.isfile(archivo)
    with open(archivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        if not existe:
            writer.writerow(['ID_Mascota', 'Autor', 'Mensaje', 'Emoji', 'Fecha'])
        fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y")
        writer.writerow([id_mascota, autor, mensaje, emoji, fecha_hoy])

def obtener_tributos(id_mascota):
    tributos = []
    archivo = "tributos_arcoiris.csv"
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_Mascota'] == id_mascota:
                    tributos.append(row)
    return tributos

def mostrar_arcoiris():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #9C27B0;'>🌈 Puente Arco Iris</h2>", unsafe_allow_html=True)
    st.write("Un espacio para recordar con amor a nuestros compañeros que ya cruzaron el puente. Dejales un mensaje y un símbolo de cariño.")
    
    mascotas = obtener_datos_mascotas()
    fallecidos = [m for m in mascotas.values() if m.get('Estado_Vida') == 'Arco Iris']
    
    if not fallecidos:
        st.info("Aún no hay mascotas en el Puente Arco Iris.")
        return

    for m in fallecidos:
        id_m = m['ID_Mascota']
        with st.container(border=True):
            col_i, col_d = st.columns([1, 3])
            with col_i:
                ruta = os.path.join(CARPETA_FOTOS, f"{id_m}.jpg")
                if os.path.exists(ruta): st.image(ruta)
            with col_d:
                st.subheader(f"✨ {m['Nombre_Mascota']}")
                st.write(f"**Raza:** {m['Raza']} | **Especie:** {m['Especie']}")
                
                tributos_previos = obtener_tributos(id_m)
                if tributos_previos:
                    st.markdown("**Mensajes de la comunidad:**")
                    for t in tributos_previos:
                        st.caption(f"{t['Emoji']} *\"{t['Mensaje']}\"* - **{t['Autor']}** ({t['Fecha']})")
                
                with st.expander(f"🕊️ Dejar un mensaje para {m['Nombre_Mascota']}"):
                    with st.form(f"form_tributo_{id_m}"):
                        autor = st.text_input("Tu nombre:", key=f"autor_{id_m}")
                        mensaje = st.text_area("Tu mensaje:", max_chars=200, key=f"msg_{id_m}")
                        emoji = st.radio("Elegí un símbolo:", ["🌈", "🕊️", "💔", "🕯️", "🐾", "⭐"], horizontal=True, key=f"emo_{id_m}")
                        
                        if st.form_submit_button("Enviar Homenaje"):
                            if not autor or not mensaje:
                                st.warning("Completá tu nombre y el mensaje.")
                            elif not validar_texto(mensaje) or not validar_texto(autor):
                                st.error("⚠️ Tu mensaje contiene palabras no permitidas. Por favor, modificalo.")
                            else:
                                guardar_tributo(id_m, autor, mensaje, emoji)
                                st.success("¡Mensaje publicado!")
                                st.rerun()
