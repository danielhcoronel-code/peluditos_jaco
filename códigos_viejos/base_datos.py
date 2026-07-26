import csv
import os
import base64

ARCHIVO_CSV = "base_mascotas.csv"
ARCHIVO_ALERTAS = "base_alertas.csv" 
CARPETA_FOTOS = "fotos_mascotas" 

os.makedirs(CARPETA_FOTOS, exist_ok=True)

def guardar_en_csv(datos_mascota):
    archivo_existe = os.path.isfile(ARCHIVO_CSV)
    with open(ARCHIVO_CSV, mode='a', newline='', encoding='utf-8') as archivo:
        nombres_columnas = ['ID_Mascota', 'Nombre_Mascota', 'Especie', 'Raza', 'Edad', 'Sexo', 'Castrado', 'Peso_Kg', 'Vacuna_Antirrabica', 'Condicion_Medica', 'Nombre_Contacto', 'Celular', 'Domicilio']
        escritor = csv.DictWriter(archivo, fieldnames=nombres_columnas)
        if not archivo_existe: escritor.writeheader()
        escritor.writerow(datos_mascota)

def actualizar_en_csv(datos_actualizados):
    mascotas = []
    if os.path.isfile(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            mascotas = list(lector)
            
    nombres_columnas = ['ID_Mascota', 'Nombre_Mascota', 'Especie', 'Raza', 'Edad', 'Sexo', 'Castrado', 'Peso_Kg', 'Vacuna_Antirrabica', 'Condicion_Medica', 'Nombre_Contacto', 'Celular', 'Domicilio']
    
    for i, mascota in enumerate(mascotas):
        if mascota['ID_Mascota'] == datos_actualizados['ID_Mascota']:
            mascotas[i] = datos_actualizados
            break
            
    with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=nombres_columnas)
        escritor.writeheader()
        escritor.writerows(mascotas)

def guardar_alerta_csv(datos_alerta):
    archivo_existe = os.path.isfile(ARCHIVO_ALERTAS)
    with open(ARCHIVO_ALERTAS, mode='a', newline='', encoding='utf-8') as archivo:
        nombres_columnas = ['ID_Mascota', 'Detalles_Extra', 'Latitud', 'Longitud']
        escritor = csv.DictWriter(archivo, fieldnames=nombres_columnas)
        if not archivo_existe: escritor.writeheader()
        escritor.writerow(datos_alerta)

def obtener_datos_mascotas():
    mascotas = {}
    if os.path.isfile(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                mascotas[fila['ID_Mascota']] = fila
    return mascotas

def obtener_alertas():
    alertas = []
    if os.path.isfile(ARCHIVO_ALERTAS):
        with open(ARCHIVO_ALERTAS, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                alertas.append(fila)
    return alertas

def codificar_foto_base64(ruta_imagen):
    if os.path.isfile(ruta_imagen):
        with open(ruta_imagen, "rb") as archivo_img:
            return base64.b64encode(archivo_img.read()).decode()
    return None
