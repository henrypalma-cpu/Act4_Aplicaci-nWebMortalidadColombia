# Actividad 4 - HENRY PALMA Y LIDA GARCIA
import json
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, dash_table

# ==========================================================
# CARGA DE DATOS
# ==========================================================

FILE_MORT = "data/Anexo1.NoFetal2019_CE_15-03-23.xlsx"
FILE_COD = "data/Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx"
FILE_DIV = "data/Divipola_CE_.xlsx"
FILE_GEO = "data/departamentos_colombia.geojson"

df = pd.read_excel(FILE_MORT)
codigos = pd.read_excel(FILE_COD)
divipola = pd.read_excel(FILE_DIV)

with open(FILE_GEO, encoding="utf-8") as f:
    geojson = json.load(f)

# ==========================================================
# NORMALIZAR COLUMNAS
# ==========================================================

df.columns = df.columns.str.upper()
codigos.columns = codigos.columns.str.upper()
divipola.columns = divipola.columns.str.upper()