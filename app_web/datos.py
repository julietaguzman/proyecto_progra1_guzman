import json
import os
from datetime import datetime
import csv

mediciones = {
    "temperatura": "temperatura",
    "humedad": "humedad",
    "presion": "presion",
    "viento": "velocidad_del_viento",
}

def cargar_json(archivo_salida_json):
    if not os.path.exists(archivo_salida_json):
        raise FileNotFoundError(f"No existe el archivo: {archivo_salida_json}")
    
    with open (archivo_salida_json, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos["registros_validos"]

def listado_de_estaciones (registros):
    estaciones = set()
    for registro in registros:
        estaciones.add(registro["estacion"])
    return sorted(estaciones)

def listado_de_mediciones():
    resultado = []
    for clave in mediciones:
        resultado.append(clave)
    return resultado

def construir_fecha(registro):
    fecha = datetime.strptime(registro["fecha"], "%d%m%Y")
    return fecha.replace(hour = registro["hora"], minute = 0, second = 0)

def obtener_fecha(filtrado):
    return filtrado["fecha_hora"]

def filtrar_datos(registros, estacion, medicion):
    if medicion not in mediciones:
        raise ValueError(f"Medicion desconocida: {medicion}")

    campo = mediciones[medicion]
    filtrados = []

    for registro in registros:
        if registro["estacion"] != estacion:
            continue
        if campo not in registro:
            continue

        filtrados.append({
            "fecha_hora": construir_fecha(registro),
            "valor": registro[campo],
        })

    filtrados.sort(key = obtener_fecha)
    return filtrados

def guardar_csv(filtrados, estacion, medicion, carpeta_salidas = "salidas"):
    if not os.path.exists(carpeta_salidas):
        os.makedirs(carpeta_salidas)

    hoy = datetime.now().strftime("%Y-%m-%d")
    estaciones = estacion.lower().replace(" ", "_")

    ruta_csv = os.path.join(
        carpeta_salidas,
        f"{hoy}_{estaciones}_{medicion}.csv"
    )
    
    with open(ruta_csv, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["fecha_hora", "valor"])
        for fila in filtrados:
            escritor.writerow([fila["fecha_hora"], fila["valor"]])

    return ruta_csv