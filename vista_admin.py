import streamlit as st
import json
import os
import datetime
import csv 

ARCHIVO_NOVEDADES = "novedades.json"
ARCHIVO_ANUNCIOS = "anuncios.json" 
ARCHIVO_COMERCIOS = "comercios.json" 
ARCHIVO_CITAS = "citas.json" 
ARCHIVO_INTERES = "interes_gral.json" 
ARCHIVO_SALUD = "salud.json"
ARCHIVO_RESCATES = "rescates.json" 
ARCHIVO_MASCOTAS = "base_mascotas.csv" 
ARCHIVO_RAZAS = "razas.json" 
DIRECTORIO_FOTOS = "fotos_anuncios"
DIRECTORIO_FOTOS_RAZAS = "fotos_razas" 

if not os.path.exists(DIRECTORIO_FOTOS):
    os.makedirs(DIRECTORIO_FOTOS)
if not os.path.exists(DIRECTORIO_FOTOS_RAZAS):
    os.makedirs(DIRECTORIO_FOTOS_RAZAS)

def cargar_datos(archivo):
    if not os.path.exists(archivo): return []
    with open(archivo, 'r', encoding='utf-8') as f: return json.load(f)

def guardar_datos(archivo, datos):
    with open(archivo, 'w', encoding='utf-8') as f: json.dump(datos, f, ensure_ascii=False, indent=4)

def mostrar_admin():
    # --- LA BANDERITA DE DESTINO PARA EL ASCENSOR ---
    st.markdown("<div id='tope-pagina'></div>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #5D4037;'>⚙️ Panel de Control</h2>", unsafe_allow_html=True)
    
    if 'admin_logeado' not in st.session_state: st.session_state.admin_logeado = False

    if not st.session_state.admin_logeado:
        st.info("🔒 Ingreso exclusivo para la Administración General, Zoonosis y Patitas Felices.")
        clave = st.text_input("Ingrese su clave de acceso:", type="password")
        if st.button("Ingresar", use_container_width=True):
            if clave == "daniel2026": 
                st.session_state.admin_logeado, st.session_state.rol = True, "dios"
                st.rerun()
            elif clave == "patitas2026": 
                st.session_state.admin_logeado, st.session_state.rol = True, "patitas"
                st.rerun()
            elif clave == "zoonosis2026":
                st.session_state.admin_logeado, st.session_state.rol = True, "zoonosis"
                st.rerun()
            else: st.error("❌ Clave incorrecta. Intente nuevamente.")
    else:
        st.success(f"✅ Sesión iniciada. Nivel de acceso: {st.session_state.rol.upper()}")
        if st.button("Cerrar Sesión"):
            st.session_state.admin_logeado = False
            st.rerun()
            
        st.markdown("---")
        
        titulos_pestanas = []
        if st.session_state.rol == "dios": 
            titulos_pestanas = ["📰 Noticias", "📢 Comunicados", "💎 Patrocinios", "🤍 Citas", "💡 Interés Gral.", "🩺 Salud", "🐾 Base de Datos", "📖 Libro de Actas", "📚 Gestor de Razas"]
        elif st.session_state.rol == "patitas": 
            titulos_pestanas = ["📢 Comunicados", "💎 Patrocinios", "📖 Libro de Actas"]
        elif st.session_state.rol == "zoonosis": 
            titulos_pestanas = ["📢 Comunicados", "🩺 Salud", "🐾 Base de Datos"]

        pestanas = st.tabs(titulos_pestanas)
        dic_pestanas = dict(zip(titulos_pestanas, pestanas))

        # ==========================================
        # 1. NOTICIAS 
        # ==========================================
        if "📰 Noticias" in dic_pestanas:
            with dic_pestanas["📰 Noticias"]:
                st.info("ℹ️ **¿Para qué sirve esto?** Aquí podés agregar textos cortos que aparecerán rotando en la pantalla principal de los vecinos.")
                st.markdown("### Agregar nueva noticia a la rotación diaria")
                nueva_noticia = st.text_area("Texto de la noticia:", height=100)
                if st.button("➕ Agregar Noticia", type="primary"):
                    if nueva_noticia.strip() != "":
                        novedades = cargar_datos(ARCHIVO_NOVEDADES)
                        novedades.append(nueva_noticia)
                        guardar_datos(ARCHIVO_NOVEDADES, novedades)
                        st.success("¡Guardada con éxito!")
                        st.rerun()
                st.markdown("---")
                novedades = cargar_datos(ARCHIVO_NOVEDADES)
                for i, nov in enumerate(novedades):
                    col_t, col_b = st.columns([5, 1])
                    with col_t: st.info(nov)
                    with col_b:
                        if st.button("🗑️", key=f"b_nov_{i}"):
                            novedades.pop(i)
                            guardar_datos(ARCHIVO_NOVEDADES, novedades)
                            st.rerun()

        # ==========================================
        # 2. COMUNICADOS 
        # ==========================================
        if "📢 Comunicados" in dic_pestanas:
            with dic_pestanas["📢 Comunicados"]:
                st.info("ℹ️ **¿Para qué sirve esto?** Para emitir avisos oficiales con foto (ej. Campañas de vacunación, eventos). Recordá borrar los avisos viejos para no saturar la cartelera.")
                st.markdown("### Emitir un Aviso a la Comunidad")
                
                opciones_emisor = ["Zoonosis / Hospital", "Patitas Felices", "Administración"]
                if st.session_state.rol == "zoonosis": opciones_emisor = ["Zoonosis / Hospital"]
                elif st.session_state.rol == "patitas": opciones_emisor = ["Patitas Felices"]

                emisor = st.selectbox("¿Quién emite el comunicado?", opciones_emisor)
                texto_corto = st.text_input("Titular o mensaje corto:")
                texto_largo = st.text_area("Desarrollo de la noticia (Opcional):", height=150)
                
                foto_subida, ruta_foto = None, ""
                if emisor == "Patitas Felices":
                    foto_subida = st.file_uploader("Elegir imagen", type=['jpg', 'jpeg', 'png'], key="foto_aviso")
                
                if st.button("📢 Publicar Comunicado", type="primary"):
                    if texto_corto.strip() != "":
                        if foto_subida is not None:
                            nombre_archivo = f"aviso_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                            ruta_foto = os.path.join(DIRECTORIO_FOTOS, nombre_archivo)
                            with open(ruta_foto, "wb") as f: f.write(foto_subida.getbuffer())

                        anuncios = cargar_datos(ARCHIVO_ANUNCIOS)
                        anuncios.append({"emisor": emisor, "texto_corto": texto_corto, "texto_largo": texto_largo, "foto_ruta": ruta_foto})
                        guardar_datos(ARCHIVO_ANUNCIOS, anuncios)
                        st.success("¡Aviso publicado!")
                        st.rerun()
                
                st.markdown("---")
                anuncios = cargar_datos(ARCHIVO_ANUNCIOS)
                for i, an in enumerate(anuncios):
                    if st.session_state.rol == "dios" or (st.session_state.rol == "patitas" and an['emisor'] == "Patitas Felices") or (st.session_state.rol == "zoonosis" and an['emisor'] == "Zoonosis / Hospital"):
                        st.write(f"**{an['emisor']}:** {an['texto_corto']}")
                        if st.button("🗑️ Levantar aviso", key=f"b_an_{i}"):
                            anuncios.pop(i)
                            guardar_datos(ARCHIVO_ANUNCIOS, anuncios)
                            st.rerun()

        # ==========================================
        # 3. PATROCINIOS Y COMERCIOS 
        # ==========================================
        if "💎 Patrocinios" in dic_pestanas:
            with dic_pestanas["💎 Patrocinios"]:
                st.info("ℹ️ **¿Para qué sirve esto?** Para gestionar los comercios amigos de Jacobacci. El sistema controlará las fechas y dará de baja solos a los que se venzan.")
                st.markdown("### Alta de Auspiciante o Padrino")
                
                categoria = st.selectbox("Categoría de Apoyo:", ["Sponsor Premium (Aparece en el Inicio)", "Comercio Amigo (Aparece en Cuponera)", "Padrino de Corazón (Aparece en Agradecimientos)"])
                nombre_comercio = st.text_input("Nombre del Comercio o Padrino:")
                beneficio = st.text_input("Aporte o Beneficio:", placeholder="Ej: 15% de desc. o Aporte mensual")
                direccion = st.text_input("Dirección o contacto (Opcional):")
                
                st.warning("📅 Elegí la fecha límite. El sistema ocultará la publicidad si se pasa el día.")
                fecha_vencimiento = st.date_input("Fecha de finalización:", value=datetime.date.today() + datetime.timedelta(days=30))
                
                foto_comercio = st.file_uploader("Logo o foto (Opcional):", type=['jpg', 'jpeg', 'png'], key="foto_com")
                
                if st.button("💎 Cargar al Sistema", type="primary"):
                    if nombre_comercio.strip() != "" and beneficio.strip() != "":
                        ruta_comercio = ""
                        if foto_comercio is not None:
                            nombre_arch = f"comercio_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                            ruta_comercio = os.path.join(DIRECTORIO_FOTOS, nombre_arch)
                            with open(ruta_comercio, "wb") as f: f.write(foto_comercio.getbuffer())

                        comercios = cargar_datos(ARCHIVO_COMERCIOS)
                        comercios.append({
                            "categoria": categoria,
                            "nombre": nombre_comercio, 
                            "beneficio": beneficio, 
                            "direccion": direccion, 
                            "vencimiento": fecha_vencimiento.strftime("%Y-%m-%d"),
                            "foto_ruta": ruta_comercio
                        })
                        guardar_datos(ARCHIVO_COMERCIOS, comercios)
                        st.success(f"¡{nombre_comercio} cargado correctamente!")
                        st.rerun()
                        
                st.markdown("---")
                st.markdown("### Auspiciantes Activos")
                comercios = cargar_datos(ARCHIVO_COMERCIOS)
                hoy = datetime.date.today()
                
                if 'editando_comercio' not in st.session_state:
                    st.session_state.editando_comercio = None

                for i, com in enumerate(comercios):
                    fecha_ven = datetime.datetime.strptime(com.get('vencimiento', '2099-01-01'), "%Y-%m-%d").date()
                    estado = "✅ Activo" if fecha_ven >= hoy else "❌ VENCIDO"
                    
                    if st.session_state.editando_comercio == i:
                        st.markdown(f"#### ✏️ Editando: {com['nombre']}")
                        nuevo_nombre = st.text_input("Nombre", value=com['nombre'], key=f"edit_nom_{i}")
                        nuevo_ben = st.text_input("Beneficio", value=com['beneficio'], key=f"edit_ben_{i}")
                        nueva_fecha = st.date_input("Nueva Fecha", value=fecha_ven, key=f"edit_fec_{i}")
                        
                        col_g, col_c = st.columns(2)
                        with col_g:
                            if st.button("💾 Guardar Cambios", key=f"save_edit_{i}", type="primary"):
                                comercios[i]['nombre'] = nuevo_nombre
                                comercios[i]['beneficio'] = nuevo_ben
                                comercios[i]['vencimiento'] = nueva_fecha.strftime("%Y-%m-%d")
                                guardar_datos(ARCHIVO_COMERCIOS, comercios)
                                st.session_state.editando_comercio = None 
                                st.rerun()
                        with col_c:
                            if st.button("❌ Cancelar", key=f"cancel_edit_{i}"):
                                st.session_state.editando_comercio = None
                                st.rerun()
                        st.markdown("---")
                    else:
                        col1, col2, col3 = st.columns([5, 1, 1])
                        with col1:
                            st.write(f"**{com['nombre']}** ({com.get('categoria', 'Comercio Amigo')}) - {estado}")
                            st.write(f"Vence: {com.get('vencimiento', 'N/A')}")
                        with col2:
                            if st.button("✏️ Editar", key=f"e_com_{i}"):
                                st.session_state.editando_comercio = i
                                st.rerun()
                        with col3:
                            if st.button("🗑️ Baja", key=f"b_com_{i}"):
                                comercios.pop(i)
                                guardar_datos(ARCHIVO_COMERCIOS, comercios)
                                st.rerun()

        # ==========================================
        # 4. CITAS INSPIRACIONALES 
        # ==========================================
        if "🤍 Citas" in dic_pestanas:
            with dic_pestanas["🤍 Citas"]:
                st.info("ℹ️ **¿Para qué sirve esto?** Sumá frases lindas o reflexiones sobre animales que rotarán en el encabezado de inicio.")
                nueva_cita = st.text_area("Nueva cita:", placeholder="Ej: El perro es el único ser en el mundo...")
                if st.button("➕ Sumar Cita", type="primary"):
                    if nueva_cita.strip() != "":
                        citas = cargar_datos(ARCHIVO_CITAS)
                        citas.append(nueva_cita.strip())
                        guardar_datos(ARCHIVO_CITAS, citas)
                        st.success("¡Cita agregada!")
                        st.rerun()
                st.markdown("---")
                citas_guardadas = cargar_datos(ARCHIVO_CITAS)
                for i, cita in enumerate(citas_guardadas):
                    col_f_texto, col_f_borrar = st.columns([5, 1])
                    with col_f_texto: st.write(f"_{cita}_")
                    with col_f_borrar:
                        if st.button("🗑️", key=f"b_cita_{i}"):
                            citas_guardadas.pop(i)
                            guardar_datos(ARCHIVO_CITAS, citas_guardadas)
                            st.rerun()

        # ==========================================
        # 4.5 INTERÉS GENERAL (Tips y Noticias)
        # ==========================================
        if "💡 Interés Gral." in dic_pestanas:
            with dic_pestanas["💡 Interés Gral."]:
                st.info("ℹ️ **¿Para qué sirve esto?** Sumá tips rápidos, consejos y noticias curiosas que rotarán en la sección 'De interés Gral.' de la página principal.")
                nuevo_tip = st.text_area("Nuevo dato útil:", placeholder="Ej: 💡 Tip del día: ¡Cuidado con el calor!...")
                if st.button("➕ Sumar Dato Útil", type="primary"):
                    if nuevo_tip.strip() != "":
                        tips = cargar_datos(ARCHIVO_INTERES)
                        tips.append(nuevo_tip.strip())
                        guardar_datos(ARCHIVO_INTERES, tips)
                        st.success("¡Dato útil agregado!")
                        st.rerun()
                st.markdown("---")
                tips_guardados = cargar_datos(ARCHIVO_INTERES)
                for i, tip in enumerate(tips_guardados):
                    col_t_texto, col_t_borrar = st.columns([5, 1])
                    with col_t_texto: st.write(f"_{tip}_")
                    with col_t_borrar:
                        if st.button("🗑️", key=f"b_tip_{i}"):
                            tips_guardados.pop(i)
                            guardar_datos(ARCHIVO_INTERES, tips_guardados)
                            st.rerun()

        # ==========================================
        # 5. SALUD Y BIENESTAR
        # ==========================================
        if "🩺 Salud" in dic_pestanas:
            with dic_pestanas["🩺 Salud"]:
                st.info("ℹ️ **¿Para qué sirve esto?** Sección ideal para que los profesionales de Zoonosis desmitifiquen creencias populares o respondan consultas frecuentes.")
                st.markdown("### Cargar Mito, Verdad o Consulta Frecuente")
                pregunta = st.text_input("Pregunta / Mito:")
                respuesta = st.text_area("Respuesta profesional / Verdad:", height=150)
                
                if st.button("🩺 Publicar Consulta", type="primary"):
                    if pregunta.strip() != "" and respuesta.strip() != "":
                        salud = cargar_datos(ARCHIVO_SALUD)
                        salud.append({"pregunta": pregunta, "respuesta": respuesta})
                        guardar_datos(ARCHIVO_SALUD, salud)
                        st.success("¡Consulta médica guardada!")
                        st.rerun()
                
                st.markdown("---")
                st.markdown("### Consultorio Activo")
                salud = cargar_datos(ARCHIVO_SALUD)
                
                if 'editando_salud' not in st.session_state:
                    st.session_state.editando_salud = None
                    
                for i, s in enumerate(salud):
                    if st.session_state.editando_salud == i:
                        st.markdown("#### ✏️ Editando Consulta")
                        nueva_preg = st.text_input("Pregunta", value=s['pregunta'], key=f"edit_preg_{i}")
                        nueva_resp = st.text_area("Respuesta", value=s['respuesta'], key=f"edit_resp_{i}", height=150)
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("💾 Guardar", key=f"save_salud_{i}", type="primary"):
                                salud[i]['pregunta'] = nueva_preg
                                salud[i]['respuesta'] = nueva_resp
                                guardar_datos(ARCHIVO_SALUD, salud)
                                st.session_state.editando_salud = None
                                st.rerun()
                        with c2:
                            if st.button("❌ Cancelar", key=f"cancel_salud_{i}"):
                                st.session_state.editando_salud = None
                                st.rerun()
                        st.markdown("---")
                    else:
                        with st.expander(f"❓ {s['pregunta']}"):
                            st.write(s['respuesta'])
                            c_edit, c_del = st.columns(2)
                            with c_edit:
                                if st.button("✏️ Editar", key=f"e_salud_{i}"):
                                    st.session_state.editando_salud = i
                                    st.rerun()
                            with c_del:
                                if st.button("🗑️ Borrar", key=f"d_salud_{i}"):
                                    salud.pop(i)
                                    guardar_datos(ARCHIVO_SALUD, salud)
                                    st.rerun()

        # ==========================================
        # 6. BASE DE DATOS (NUEVO - ZOONOSIS)
        # ==========================================
        if "🐾 Base de Datos" in dic_pestanas:
            with dic_pestanas["🐾 Base de Datos"]:
                st.info("ℹ️ **¿Para qué sirve esto?** Padrón general de lectura de mascotas. Usá los filtros para buscar rápidamente perros o gatos registrados en el sistema.")
                st.markdown("### 🔍 Buscador del Registro Civil Animal")
                
                if os.path.exists(ARCHIVO_MASCOTAS):
                    with open(ARCHIVO_MASCOTAS, newline='', encoding='utf-8') as f:
                        lector = csv.DictReader(f)
                        lista_mascotas = list(lector)
                    
                    if len(lista_mascotas) > 0:
                        filtro = st.text_input("🔍 Escribí un nombre de mascota, tutor o raza para filtrar:")
                        
                        datos_a_mostrar = []
                        for mascota in lista_mascotas:
                            fila_texto = " ".join(str(val).lower() for val in mascota.values())
                            if filtro.lower() in fila_texto:
                                datos_a_mostrar.append(mascota)
                        
                        st.markdown(f"*Mostrando {len(datos_a_mostrar)} registros.*")
                        st.dataframe(datos_a_mostrar, use_container_width=True)
                    else:
                        st.warning("⚠️ El archivo CSV existe pero todavía no tiene mascotas cargadas.")
                else:
                    st.error(f"❌ No se encontró el archivo '{ARCHIVO_MASCOTAS}'. Asegurate de que los vecinos estén registrando mascotas.")

        # ==========================================
        # 7. LIBRO DE ACTAS (NUEVO - PATITAS FELICES)
        # ==========================================
        if "📖 Libro de Actas" in dic_pestanas:
            with dic_pestanas["📖 Libro de Actas"]:
                st.info("ℹ️ **¿Para qué sirve esto?** Registro interno exclusivo para llevar la cuenta de los rescates, tránsitos y adopciones logradas.")
                st.markdown("### 📝 Nuevo Registro de Rescate")
                
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    nombre_rescate = st.text_input("Nombre / Apodo del animalito:")
                with col_r2:
                    estado_rescate = st.selectbox("Estado actual del caso:", ["🚨 Urgencia / En calle", "🏥 En recuperación", "🏠 Buscando Tránsito", "🛋️ En Tránsito", "🎉 ¡Adoptado!"])
                
                detalles_rescate = st.text_area("Detalles del caso (Ubicación, veterinario interviniente, necesidades):")
                
                if st.button("💾 Guardar en Libro de Actas", type="primary"):
                    if nombre_rescate.strip() != "":
                        rescates = cargar_datos(ARCHIVO_RESCATES)
                        rescates.append({
                            "fecha": str(datetime.date.today()), 
                            "nombre": nombre_rescate, 
                            "estado": estado_rescate, 
                            "detalles": detalles_rescate
                        })
                        guardar_datos(ARCHIVO_RESCATES, rescates)
                        st.success("¡Registro de rescate guardado exitosamente!")
                        st.rerun()
                    else:
                        st.error("⚠️ El nombre del animalito es obligatorio.")

                st.markdown("---")
                st.markdown("### 📋 Historial de Casos (Del más nuevo al más viejo)")
                rescates = cargar_datos(ARCHIVO_RESCATES)
                if len(rescates) == 0:
                    st.write("No hay casos registrados todavía.")
                else:
                    for i, res in enumerate(reversed(rescates)):
                        indice_real = len(rescates) - 1 - i 
                        
                        col_hist_1, col_hist_2 = st.columns([5, 1])
                        with col_hist_1:
                            st.markdown(f"**🐾 {res['nombre']}** - Fecha: {res['fecha']}")
                            st.markdown(f"**Estado:** {res['estado']}")
                            st.write(f"_{res['detalles']}_")
                        with col_hist_2:
                            if st.button("🗑️ Borrar", key=f"b_res_{indice_real}"):
                                rescates.pop(indice_real)
                                guardar_datos(ARCHIVO_RESCATES, rescates)
                                st.rerun()
                        st.markdown("---")

        # ==========================================
        # 8. GESTOR DE RAZAS (ACTUALIZADO CON EDICIÓN Y SLIDERS)
        # ==========================================
        if "📚 Gestor de Razas" in dic_pestanas:
            with dic_pestanas["📚 Gestor de Razas"]:
                st.info("ℹ️ **Gestor del Catálogo:** Cargá o modificá las fichas técnicas. Los números del 1 al 5 se verán como huellas.")
                
                catalogo = cargar_datos(ARCHIVO_RAZAS)
                
                if 'raza_en_edicion' not in st.session_state:
                    st.session_state.raza_en_edicion = None

                st.markdown("### 📋 Razas Cargadas")
                if len(catalogo) == 0:
                    st.write("Aún no hay razas cargadas.")
                else:
                    for i, raza in enumerate(catalogo):
                        col_rn, col_be, col_bb = st.columns([4, 1, 1])
                        with col_rn:
                            st.write(f"**{raza.get('nombre', 'Sin nombre')}** - _{raza.get('origen', '')}_")
                        with col_be:
                            if st.button("✏️ Editar", key=f"edit_r_{i}"):
                                st.session_state.raza_en_edicion = i
                                st.rerun()
                        with col_bb:
                            if st.button("🗑️ Borrar", key=f"del_r_{i}"):
                                catalogo.pop(i)
                                guardar_datos(ARCHIVO_RAZAS, catalogo)
                                if st.session_state.raza_en_edicion == i:
                                    st.session_state.raza_en_edicion = None
                                st.rerun()

                st.markdown("---")
                
                # --- ZONA DE FORMULARIO (ALTA O EDICIÓN) ---
                modo_edicion = st.session_state.raza_en_edicion is not None
                idx = st.session_state.raza_en_edicion
                
                if modo_edicion:
                    st.markdown(f"### ✏️ Editando Ficha: {catalogo[idx].get('nombre', '')}")
                    raza_edit = catalogo[idx]
                    if st.button("❌ Cancelar Edición"):
                        st.session_state.raza_en_edicion = None
                        st.rerun()
                else:
                    st.markdown("### 🐕 Nueva Ficha Técnica")
                    raza_edit = {} 

                # Valores por defecto basados en si editamos o creamos
                def_nombre = raza_edit.get("nombre", "")
                def_resumen = raza_edit.get("resumen", "")
                def_desc = raza_edit.get("descripcion", "")
                def_tam = raza_edit.get("tamano", "Grande")
                def_pelo = raza_edit.get("pelo", "Corto")
                def_origen = raza_edit.get("origen", "")
                
                # Rescate a prueba de balas: si había texto viejo, lo convertimos a un 3 por defecto
                try: def_ninos = int(raza_edit.get("ninos", 4))
                except: def_ninos = 4
                try: def_salud = int(raza_edit.get("salud", 5))
                except: def_salud = 5
                try: def_energia = int(raza_edit.get("energia", 5))
                except: def_energia = 5
                try: def_inte = int(raza_edit.get("inteligencia", 4))
                except: def_inte = 4

                with st.form("form_raza"):
                    r_nombre = st.text_input("Nombre de la raza:", value=def_nombre)
                    r_resumen = st.text_input("Resumen corto:", value=def_resumen)
                    r_descripcion = st.text_area("Descripción completa:", value=def_desc, height=100)
                    
                    st.markdown("#### 🟢 Apariencia")
                    col_ap1, col_ap2, col_ap3 = st.columns(3)
                    with col_ap1:
                        ops_tam = ["Pequeño", "Mediano", "Grande", "Gigante"]
                        idx_tam = ops_tam.index(def_tam) if def_tam in ops_tam else 2
                        r_tamano = st.selectbox("Tamaño:", ops_tam, index=idx_tam)
                    with col_ap2:
                        ops_pelo = ["Corto", "Largo", "Medio", "Duro", "Rizado", "Variable"]
                        idx_pelo = ops_pelo.index(def_pelo) if def_pelo in ops_pelo else 3
                        r_pelo = st.selectbox("Tipo de Pelo:", ops_pelo, index=idx_pelo)
                    with col_ap3:
                        r_origen = st.text_input("País de Origen:", value=def_origen)

                    st.markdown("#### 🐾 Puntuación Técnica (1 al 5)")
                    col_pt1, col_pt2 = st.columns(2)
                    with col_pt1:
                        r_ninos = st.slider("Convivencia con niños:", 1, 5, def_ninos)
                        r_salud = st.slider("Salud / Rusticidad:", 1, 5, def_salud)
                    with col_pt2:
                        r_energia = st.slider("Nivel de Energía / Espacio:", 1, 5, def_energia)
                        r_inteligencia = st.slider("Inteligencia / Apego:", 1, 5, def_inte)
                    
                    st.write("*(Nota: Para cambiar la foto, subí una nueva. Si no subís nada, se mantiene la que ya tenías).*")
                    r_foto = st.file_uploader("Foto de la raza (Ideal apaisada):", type=['jpg', 'jpeg', 'png'])
                    
                    btn_txt = "💾 Guardar Cambios" if modo_edicion else "💾 Guardar Nueva Raza"
                    submit_raza = st.form_submit_button(btn_txt)

                if submit_raza:
                    if r_nombre.strip() != "":
                        nombre_foto = raza_edit.get("foto_archivo", "") 
                        if r_foto is not None:
                            extension = r_foto.name.split('.')[-1]
                            nombre_foto = f"raza_{r_nombre.replace(' ', '_').lower()}.{extension}"
                            ruta_foto_raza = os.path.join(DIRECTORIO_FOTOS_RAZAS, nombre_foto)
                            with open(ruta_foto_raza, "wb") as f:
                                f.write(r_foto.getbuffer())
                        
                        nueva_data = {
                            "nombre": r_nombre,
                            "resumen": r_resumen,
                            "descripcion": r_descripcion,
                            "tamano": r_tamano,
                            "pelo": r_pelo,
                            "origen": r_origen,
                            "ninos": r_ninos,
                            "energia": r_energia,
                            "salud": r_salud,
                            "inteligencia": r_inteligencia,
                            "foto_archivo": nombre_foto
                        }

                        if modo_edicion:
                            catalogo[idx] = nueva_data
                            st.session_state.raza_en_edicion = None
                            st.success(f"¡Ficha de '{r_nombre}' actualizada!")
                        else:
                            catalogo.append(nueva_data)
                            st.success(f"¡Ficha de '{r_nombre}' creada con éxito!")
                            
                        guardar_datos(ARCHIVO_RAZAS, catalogo)
                        st.rerun()
                    else:
                        st.error("⚠️ El nombre de la raza es obligatorio.")
