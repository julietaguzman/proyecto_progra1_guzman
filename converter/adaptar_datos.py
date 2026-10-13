
import sys
import json
import validaciones
import os

def procesar_txt(ruta_txt):
    registros_validos = []
    registros_invalidos = []
    
    try:
        with open(ruta_txt, "r", encoding="latin-1") as archivo:
            for numero_linea, linea in enumerate(archivo, start=1):
                if validaciones.encabezado_o_vacia(linea):
                    continue

                registro, error = validaciones.parsear_linea(linea)

                if registro is not None:
                    registros_validos.append(registro)
                else:
                    registros_invalidos.append({
                        "numero_de_linea": numero_linea,
                        "linea_original": linea,
                        "motivo_del_error": error
                    })
    except FileNotFoundError:
        print(f"No se encontro el archivo: {ruta_txt}")
        sys.exit(1)

    return registros_validos, registros_invalidos

def generar_json(registros_validos, registros_invalidos, ruta_salida):
    total = len(registros_validos) + len(registros_invalidos)
    datos_json = {
        "total_de_registros": total,
        "cantidad_registros_validos": len (registros_validos),
        "cantidad_registros_invalidos": len(registros_invalidos),
        "registros_validos": registros_validos,
        "registros_invalidos": registros_invalidos 
    }

    try:
        carpeta = os.path.dirname(ruta_salida)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok = True)
        
        with open(ruta_salida, "w", encoding = "utf-8") as archivo_salida:
            json.dump(datos_json, archivo_salida, indent=4, ensure_ascii=False)
    
    except Exception as e:
        print(f"Error al guardar el archivo JSON '{ruta_salida}': {e}")
        sys.exit(1)

def main():
    if len(sys.argv) != 3:
        print("Ingreso de datos: python adaptar_datos.py observaciones.txt observaciones.json")
        sys.exit(1)

    ruta_entrada = sys.argv[1]
    ruta_salida = sys.argv[2]

    registros_validos, registros_invalidos = procesar_txt(ruta_entrada)
    generar_json(registros_validos, registros_invalidos, ruta_salida)

    total = len(registros_validos) + len(registros_invalidos)
    print(f"Total de registros leidos: {total}")
    print(f"Registros validos {len(registros_validos)}")
    print(f"Registros invalidos {len(registros_invalidos)}")
    print(f"Archivo generado en: {ruta_salida}")

if __name__ == "__main__":
    main()

# El parámetro encoding="latin-1" le indica a Python qué tabla de caracteres utilizar
# para traducir los bytes crudos del archivo de texto a letras y símbolos legibles.