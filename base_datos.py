import csv
import os
import base64

ARCHIVO_CSV = "base_mascotas.csv"
ARCHIVO_ALERTAS = "base_alertas.csv" 
CARPETA_FOTOS = "fotos_mascotas" 
CARPETA_AVISTAMIENTOS = "fotos_avistamientos"

# Agregamos 'Estado_Sanitario' y sacamos las columnas viejas de vacunas
COLUMNAS = [
    'ID_Mascota', 'PIN', 'Sena_Control', 'Nombre_Mascota', 'Especie', 'Raza', 'Edad', 'Sexo', 
    'Castrado', 'Peso_Kg', 'Estado_Sanitario', 'Condicion_Medica', 
    'Nombre_Contacto', 'Celular', 'Domicilio', 'Fecha_Nacimiento', 'Estado_Vida'
]

os.makedirs(CARPETA_FOTOS, exist_ok=True)
os.makedirs(CARPETA_AVISTAMIENTOS, exist_ok=True)

def guardar_en_csv(datos_mascota):
    datos_mascota.setdefault('Fecha_Nacimiento', '')
    datos_mascota.setdefault('Estado_Vida', 'Vivo')
    datos_mascota.setdefault('PIN', '')
    datos_mascota.setdefault('Sena_Control', '')
    datos_mascota.setdefault('Estado_Sanitario', '')
    
    archivo_existe = os.path.isfile(ARCHIVO_CSV)
    with open(ARCHIVO_CSV, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        if not archivo_existe: escritor.writeheader()
        escritor.writerow(datos_mascota)

def actualizar_en_csv(datos_actualizados):
    mascotas = []
    if os.path.isfile(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            mascotas = list(lector)
    
    for i, mascota in enumerate(mascotas):
        if mascota['ID_Mascota'] == datos_actualizados['ID_Mascota']:
            mascotas[i] = datos_actualizados
            break
            
    with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(mascotas)

def guardar_alerta_csv(datos_alerta):
    nombres_columnas_alertas = ['ID_Mascota', 'Tipo_Alerta', 'Detalles_Extra', 'Latitud', 'Longitud', 'Foto_Avistamiento', 'Estado']
    
    # Valores por defecto para evitar errores
    datos_alerta.setdefault('Tipo_Alerta', 'Extravio_Dueno')
    datos_alerta.setdefault('Foto_Avistamiento', '')
    datos_alerta.setdefault('Estado', 'Activa')
    
    alertas = []
    if os.path.isfile(ARCHIVO_ALERTAS):
        with open(ARCHIVO_ALERTAS, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                # Nos aseguramos de que las filas viejas tengan las claves nuevas
                fila.setdefault('Foto_Avistamiento', '')
                fila.setdefault('Estado', 'Activa')
                # Si por algún motivo el CSV viejo tiró datos extra a la clave None, los limpiamos
                if None in fila:
                    del fila[None]
                alertas.append(fila)

    # Buscamos si la alerta ya existe (para actualizarla y no duplicarla)
    actualizada = False
    for i, alerta in enumerate(alertas):
        if alerta.get('ID_Mascota') == datos_alerta['ID_Mascota']:
            alertas[i].update(datos_alerta)
            actualizada = True
            break
            
    # Si no existía, la agregamos al final de la lista
    if not actualizada:
        alertas.append(datos_alerta)

    # Reescribimos el archivo completo, bien ordenado y sin duplicados
    with open(ARCHIVO_ALERTAS, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=nombres_columnas_alertas)
        escritor.writeheader()
        escritor.writerows(alertas)

def obtener_datos_mascotas():
    mascotas = {}
    if os.path.isfile(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                fila.setdefault('Fecha_Nacimiento', '')
                fila.setdefault('Estado_Vida', 'Vivo')
                fila.setdefault('PIN', '')
                fila.setdefault('Sena_Control', '')
                fila.setdefault('Estado_Sanitario', '')
                mascotas[fila['ID_Mascota']] = fila
    return mascotas

def obtener_alertas():
    alertas = []
    if os.path.isfile(ARCHIVO_ALERTAS):
        with open(ARCHIVO_ALERTAS, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                fila.setdefault('Tipo_Alerta', 'Extravio_Dueno')
                fila.setdefault('Foto_Avistamiento', '')
                fila.setdefault('Estado', 'Activa')
                alertas.append(fila)
    return alertas

def codificar_foto_base64(ruta_imagen):
    if os.path.isfile(ruta_imagen):
        with open(ruta_imagen, "rb") as archivo_img:
            return base64.b64encode(archivo_img.read()).decode()
    return None

def guardar_rescate(id_mascota, nombre_mascota, nombre_rescatista):
    import csv
    import datetime
    
    archivo = "base_rescates.csv"
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    
    file_exists = os.path.isfile(archivo)
    with open(archivo, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Fecha', 'ID_Mascota', 'Nombre_Mascota', 'Rescatista'])
        writer.writerow([fecha, id_mascota, nombre_mascota, nombre_rescatista])
