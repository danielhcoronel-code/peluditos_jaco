import streamlit as st
import os
import csv
import datetime
from base_datos import obtener_datos_mascotas, CARPETA_FOTOS

# --- FILTRO ANTI-BROMAS ---
PALABRAS_PROHIBIDAS = ["boludo", "pelotudo", "puto", "puta", "mierda", "carajo", "forro", "concha", "idiota", "estupido", "tarado", "cagada"]

def validar_texto(texto):
    texto_min = texto.lower()
    for palabra in PALABRAS_PROHIBIDAS:
        if palabra in texto_min:
            return False
    return True

# --- LÓGICA DE SALUDOS ---
def guardar_saludo(id_mascota, autor, mensaje, emoji):
    archivo = "saludos_cumple.csv"
    existe = os.path.isfile(archivo)
    with open(archivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        if not existe: writer.writerow(['ID_Mascota', 'Autor', 'Mensaje', 'Emoji', 'Fecha'])
        fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y")
        writer.writerow([id_mascota, autor, mensaje, emoji, fecha_hoy])

def obtener_saludos(id_mascota):
    saludos = []
    archivo = "saludos_cumple.csv"
    if os.path.exists(archivo):
        with open(archivo, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_Mascota'] == id_mascota: saludos.append(row)
    return saludos

# --- LÓGICA DE PADRINOS Y DESCUENTOS ---
ARCHIVO_PADRINOS = "padrinos.csv"

def inicializar_padrinos_prueba():
    # Creamos comercios de prueba para que Daniel pueda testear el sistema hoy mismo
    if not os.path.exists(ARCHIVO_PADRINOS):
        with open(ARCHIVO_PADRINOS, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Comercio', 'Descuento', 'Cupones_Usados', 'Mes_Ultimo_Uso'])
            mes_actual = datetime.datetime.now().strftime("%m")
            writer.writerow(['Forrajería El Gauchito', '10%', '0', mes_actual])
            writer.writerow(['Veterinaria Patitas', '5%', '2', mes_actual])
            # Le ponemos 5 a este para que veas cómo el sistema lo oculta porque ya llegó al límite
            writer.writerow(['PetShop Huellas', '5%', '5', mes_actual]) 

def obtener_padrinos_disponibles(mes_actual):
    inicializar_padrinos_prueba()
    disponibles = []
    with open(ARCHIVO_PADRINOS, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Si cambió el mes, reseteamos el contador a cero
            if row['Mes_Ultimo_Uso'] != mes_actual:
                row['Cupones_Usados'] = '0'
                row['Mes_Ultimo_Uso'] = mes_actual
            
            # Solo mostramos si usaron menos de 5 cupones
            if int(row['Cupones_Usados']) < 5:
                disponibles.append(row)
    return disponibles

def reclamar_cupon(comercio_nombre, mes_actual):
    filas = []
    with open(ARCHIVO_PADRINOS, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        campos = reader.fieldnames
        for row in reader:
            if row['Mes_Ultimo_Uso'] != mes_actual:
                row['Cupones_Usados'] = '0'
                row['Mes_Ultimo_Uso'] = mes_actual
                
            if row['Comercio'] == comercio_nombre:
                # Sumamos 1 al contador de ese comercio
                row['Cupones_Usados'] = str(int(row['Cupones_Usados']) + 1)
            filas.append(row)
            
    with open(ARCHIVO_PADRINOS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(filas)

# --- PANTALLA PRINCIPAL ---
def mostrar_cumples():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>🎂 Cumpleañeros del Mes</h2>", unsafe_allow_html=True)
    st.write("¡Dejale un saludo a los animalitos que festejan su vida este mes!")
    
    mes_actual = datetime.datetime.now().strftime("%m")
    mascotas = obtener_datos_mascotas()
    
    cumpleanieros = []
    for m in mascotas.values():
        if m.get('Estado_Vida') == 'Vivo' and m.get('Fecha_Nacimiento'):
            try:
                mes_nac = m['Fecha_Nacimiento'].split('-')[1]
                if mes_nac == mes_actual:
                    cumpleanieros.append(m)
            except IndexError:
                pass
    
    if not cumpleanieros:
        st.info("No hay cumpleaños registrados para este mes. ¡Asegurate de completar la fecha en la ficha de tu mascota!")
        return

    for m in cumpleanieros:
        id_m = m['ID_Mascota']
        with st.container(border=True):
            col_i, col_d = st.columns([1, 3])
            with col_i:
                ruta = os.path.join(CARPETA_FOTOS, f"{id_m}.jpg")
                if os.path.exists(ruta): st.image(ruta)
            with col_d:
                st.subheader(f"🎉 {m['Nombre_Mascota']}")
                st.write(f"**Raza:** {m['Raza']} | **Especie:** {m['Especie']}")
                
                # --- MENSAJES DE LA COMUNIDAD ---
                saludos_previos = obtener_saludos(id_m)
                if saludos_previos:
                    st.markdown("**Mensajes de la comunidad:**")
                    for s in saludos_previos:
                        st.caption(f"{s['Emoji']} *\"{s['Mensaje']}\"* - **{s['Autor']}** ({s['Fecha']})")
                
                # --- BOTONERA DE ACCIONES ---
                with st.expander(f"🎁 Dejarle un saludo"):
                    with st.form(f"form_cumple_{id_m}"):
                        autor = st.text_input("Tu nombre:", key=f"autor_c_{id_m}")
                        mensaje = st.text_area("Tu saludo:", max_chars=200, key=f"msg_c_{id_m}")
                        emoji = st.radio("Regalito virtual:", ["🎂", "🥳", "🎈", "🎁", "🍖", "🦴"], horizontal=True, key=f"emo_c_{id_m}")
                        
                        if st.form_submit_button("Enviar Saludo"):
                            if not autor or not mensaje: st.warning("Completá tu nombre y el mensaje.")
                            elif not validar_texto(mensaje) or not validar_texto(autor): st.error("⚠️ Tu mensaje contiene palabras no permitidas.")
                            else:
                                guardar_saludo(id_m, autor, mensaje, emoji)
                                st.success("¡Saludo enviado!")
                                st.rerun()
                                
                # --- EL GRAN BOTÓN DE REGALOS ---
                with st.expander(f"🎟️ ¿Sos el dueño? ¡Reclamá tu regalo de cumpleaños!"):
                    if not st.session_state.get(f"cupon_{id_m}"):
                        st.write("Ingresá el PIN de tu mascota para desbloquear los descuentos de nuestros Padrinos.")
                        pin_ingresado = st.text_input("PIN de seguridad:", type="password", key=f"pin_regalo_{id_m}")
                        
                        if st.button("Verificar PIN", key=f"btn_regalo_{id_m}"):
                            if pin_ingresado.strip() == str(m.get('PIN', '')):
                                st.session_state[f"pin_ok_{id_m}"] = True
                            else:
                                st.error("PIN incorrecto. Revisá el código que anotaste al registrarla.")
                        
                        if st.session_state.get(f"pin_ok_{id_m}"):
                            st.success("¡PIN verificado! Descuentos habilitados:")
                            padrinos_ok = obtener_padrinos_disponibles(mes_actual)
                            
                            if not padrinos_ok:
                                st.info("¡Guau! Este mes ya se agotaron todos los cupones. ¡Atento al mes que viene!")
                            else:
                                st.write("Elegí tu descuento. **(Solo podés elegir uno)**:")
                                for pad in padrinos_ok:
                                    col_p1, col_p2 = st.columns([3, 1])
                                    with col_p1:
                                        st.write(f"🛍️ **{pad['Comercio']}** ({pad['Descuento']} OFF)")
                                        cupones_restantes = 5 - int(pad['Cupones_Usados'])
                                        st.caption(f"Quedan {cupones_restantes} disponibles este mes.")
                                    with col_p2:
                                        if st.button("Elegir", key=f"recl_{id_m}_{pad['Comercio']}"):
                                            reclamar_cupon(pad['Comercio'], mes_actual)
                                            st.session_state[f"cupon_{id_m}"] = pad['Comercio']
                                            st.rerun()
                    else:
                        comercio_elegido = st.session_state[f"cupon_{id_m}"]
                        st.success(f"🎉 ¡Excelente! Tenés tu descuento en **{comercio_elegido}**.")
                        st.markdown(f"> **CÓDIGO DE CUPÓN: CUMPLE-{id_m.replace('ID-', '')}**")
                        st.info("Sacale captura a esta pantalla y presentala en el local junto con tu DNI para que te hagan el descuento.")
