# EDA_PIB_VS_CALIDAD_DE_VIDA

El presente trabajo tiene como objetivo realizar un **análisis exploratorio de datos (EDA)** para estudiar la relación entre el **Producto Interior Bruto (PIB)** y distintos **indicadores de calidad de vida** en las **comunidades autónomas de España**, a lo largo de un período de varios años.

El crecimiento económico suele medirse mediante indicadores agregados como el PIB; sin embargo, este no siempre refleja de forma directa el bienestar de la población. Por este motivo, resulta de interés analizar cómo evoluciona el PIB en relación con variables que aproximan la calidad de vida, y si dichas relaciones se comportan de forma homogénea o desigual entre las distintas comunidades autónomas y a lo largo del tiempo.

Este análisis tiene un enfoque **descriptivo y exploratorio**, orientado a identificar patrones, tendencias y posibles asociaciones entre variables, sin pretender establecer relaciones causales.

## ESTRUCTURA CARPETAS EDA

EDA_proyecto/
│
├── data/
│   ├── raw/            # Datos originales (NO modificar)
│   ├── interim/        # Datos intermedios (limpieza parcial)
│   └── processed/      # Datos listos para análisis/modelado
│
├── notebooks/
│   ├── 01_exploracion.ipynb
│   ├── 02_limpieza.ipynb
│   ├── 03_analisis.ipynb
│   └── 04_conclusiones.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── visualization.py
│   └── utils.py
│
├── reports/
│   ├── figures/        # Gráficas exportadas
│   └── eda_report.md   # Conclusiones en texto
│
├── environment.yml     # (conda) o requirements.txt
├── .gitignore
├── README.md
└── main.py             # (opcional) para ejecutar pipeline


¿Por qué esta estructura funciona bien?
🔹 data/

raw: datos tal como los recibes

processed: datos limpios (los que usas en notebooks)

Evita sobrescribir datos originales ❗

🔹 notebooks/

Ordenados y numerados → flujo claro

Solo lógica de exploración

Poco código repetido (eso va en src/)

🔹 src/

Funciones reutilizables

Limpieza, features, visualizaciones

Evita notebooks gigantes y desordenados

Ejemplo:

# src/data_processing.py
def clean_columns(df):
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df

🔹 reports/

Resultados finales

Gráficas guardadas con plt.savefig()

Conclusiones claras para entregar

Cómo trabajar desde los notebooks

Dentro de un notebook:

import sys
sys.path.append("../src")

from data_processing import clean_columns


O mejor aún (recomendado):

pip install -e .

.gitignore básico para EDA
__pycache__/
.ipynb_checkpoints/
.env
data/raw/*.csv

README.md mínimo
# EDA - Calidad de Vida

## Objetivo
Analizar los factores que influyen en la calidad de vida.

## Estructura
- data/: datos
- notebooks/: análisis
- src/: funciones
