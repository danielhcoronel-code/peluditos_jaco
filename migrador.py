import csv
import os

archivo_original = "base_mascotas.csv"
archivo_temp = "base_mascotas_temp.csv"

# Columnas definitivas
columnas_nuevas = [
    'ID_Mascota', 'Nombre_Mascota', 'Especie', 'Raza', 'Edad', 'Sexo', 
    'Castrado', 'Peso_Kg', 'Vacuna_Antirrabica', 'Condicion_Medica', 
    'Nombre_Contacto', 'Celular', 'Domicilio', 'Fecha_Nacimiento', 'Estado_Vida'
]

if os.path.isfile(archivo_original):
    with open(archivo_original, mode='r', encoding='utf-8') as f_in:
        lector = csv.DictReader(f_in)
        
        with open(archivo_temp, mode='w', newline='', encoding='utf-8') as f_out:
            escritor = csv.DictWriter(f_out, fieldnames=columnas_nuevas)
            escritor.writeheader()
            
            for fila in lector:
                # Agregamos los datos nuevos con valores por defecto
                fila['Fecha_Nacimiento'] = fila.get('Fecha_Nacimiento', '')
                fila['Estado_Vida'] = fila.get('Estado_Vida', 'Vivo')
                
                # Escribimos la fila actualizada
                escritor.writerow(fila)
    
    # Reemplazamos el viejo por el nuevo
    os.remove(archivo_original)
    os.rename(archivo_temp, archivo_original)
    print("¡Éxito! La base de datos se ha actualizado con las nuevas columnas.")
else:
    print("No se encontró el archivo base_mascotas.csv. ¡Cuidado!")
