import sys
import os

import streamlit as st # type: ignore
import pandas as pd

from datos import (
    cargar_json,
    filtrar_datos,
    listado_de_estaciones,
    listado_de_mediciones,
    guardar_csv,
)
from estadisticas import calcular_estadisticas
from graficos import generar_grafica

def main():
    st.title("Datos meteorológicos del SMN")
    st.write("Elegí una estación y una medición para ver estadísticas y gráficos.")

    if len(sys.argv) < 2:
        st.error("Uso: streamlit run app.py <ruta_json>")
        st.stop()

    ruta_json = sys.argv[-1]

    try:
        registros = cargar_json(ruta_json)
    except (FileNotFoundError, ValueError) as e:
        st.error(f"Error al cargar el JSON: {e}")
        st.stop()

    estaciones = listado_de_estaciones(registros)
    mediciones = listado_de_mediciones()

    estacion = st.selectbox("Estación", estaciones)
    medicion = st.selectbox("Medición", mediciones)

    try:
        filtrados = filtrar_datos(registros, estacion, medicion)
    except ValueError as e:
        st.error(f"Error: {e}")
        st.stop()

    if len(filtrados) == 0:
        st.warning(f"No hay datos de '{medicion}' para '{estacion}'.")
        st.stop()

    st.header("Estadísticas")
    estadisticas = calcular_estadisticas(filtrados)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cantidad", estadisticas["cantidad"])
    col2.metric("Mínimo", f"{estadisticas['minimo']:.2f}")
    col3.metric("Máximo", f"{estadisticas['maximo']:.2f}")
    col4.metric("Promedio", f"{estadisticas['promedio']:.2f}")

    st.header("Gráfica")
    ruta_png = generar_grafica(filtrados, estacion, medicion)
    st.image(ruta_png, caption = f"{medicion} en {estacion}")

    st.header("Datos filtrados")
    df = pd.DataFrame(filtrados)
    st.dataframe(df, use_container_width=True)

    ruta_csv = guardar_csv(filtrados, estacion, medicion)
    with open(ruta_csv, "rb") as f:
        st.download_button(
            label = "Descargar CSV",
            data = f,
            file_name = os.path.basename(ruta_csv),
            mime = "text/csv",
        )

    st.success("Todo okey.")

main()