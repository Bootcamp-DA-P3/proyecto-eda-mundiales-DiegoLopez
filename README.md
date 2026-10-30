# Análisis Exploratorio de Datos (EDA) - Los Mundiales de Fútbol

## 📝 Descripción del Proyecto
Este proyecto realiza un análisis exploratorio profundo sobre el volumen histórico, la normalización de goles y los perfiles de las selecciones combinadas a lo largo de la historia de los mundiales. El objetivo es proporcionar una perspectiva objetiva y cuantitativa sobre la evolución del torneo.

👉 **[Ver World Cup Intelligence Hub en Streamlit](https://proyecto-eda-mundiales-diegolopez-4tst4uj4zxmnt9u4jdalqm.streamlit.app/)**

---

## 📂 Estructura del Repositorio
*Actualización: Se ha incorporado el módulo interactivo de visualización en la carpeta de datos junto con los datasets fuente.*

- **`data/`**: Contiene los datasets en formato CSV con los registros históricos de partidos y resúmenes de equipos, además del código de la interfaz:
  - `app.py`: Script interactivo en Streamlit que despliega el dashboard web con filtros dinámicos, métricas y gráficos en tiempo real.
  - `2026_team_summaries.csv`: Métricas agregadas y resúmenes por selección.
  - `WorldCupMatches-selected-columns.csv`: Registros históricos detallados de encuentros.
- **`notebooks/`**: Contiene el Jupyter Notebook (`analisis.ipynb`) con todo el desarrollo del código, análisis exploratorio, gráficas y la síntesis final.
- **`requirements.txt`**: Archivo con las dependencias necesarias para replicar el entorno de trabajo tanto localmente como en el despliegue cloud.

---

## 🛠️ Tecnologías y Librerías Utilizadas
- **Python 3**
- **Streamlit** (Desarrollo y despliegue del dashboard web interactivo)
- **Pandas** (Manipulación y limpieza de datos)
- **Matplotlib / Seaborn** (Visualización estática de datos)
- **Jupyter Notebook** (Entorno exploratorio inicial)

---

## 📊 Conclusiones Principales
- **Tendencia en el volumen de goles:** Se observa un incremento en el total de goles por torneo a lo largo de las décadas debido a la expansión del formato y al aumento del número de partidos jugados, estabilizándose los promedios en las ediciones más recientes.
- **Evolución competitiva:** La normalización de los datos muestra una mayor paridad en los resultados durante el siglo XXI, reduciéndose la frecuencia de las grandes goleadas que eran comunes en las primeras ediciones del torneo (décadas de 1930 a 1950).

---

**Autor:** Diego López  
**Bootcamp:** Bootcamp DA P3
