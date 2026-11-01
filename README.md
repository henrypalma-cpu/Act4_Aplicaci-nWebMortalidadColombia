[README.md](https://github.com/user-attachments/files/34229064/README.md)
# 📊 Dashboard de Mortalidad en Colombia 2019

## Universidad de La Salle

### Actividad 4 - Aplicación Web

**Materia:** Aplicaciones I - G2

**Estudiantes:**
- Lida Esperanza García Quintero
- Henry Alfonso Palma Rojas

**Docente:** Cristian Duney Bermúdez Quintero

**Fecha:** 31 de octubre de 2026

---

## 📖 Descripción del Proyecto

Esta aplicación web desarrolla un sistema interactivo para el análisis y visualización de los datos de mortalidad en Colombia correspondientes al año 2019, utilizando información oficial del DANE.

La solución fue construida con Streamlit y permite explorar indicadores de mortalidad mediante filtros, gráficos estadísticos y mapas geográficos interactivos.

---

## 🎯 Objetivos

- Analizar la mortalidad en Colombia durante el año 2019.
- Visualizar la distribución geográfica de los registros.
- Identificar las principales causas de muerte.
- Explorar tendencias por sexo, edad y período del año.
- Facilitar el acceso a la información mediante un dashboard interactivo.

---

## 🛠 Tecnologías Utilizadas

- Python 3
- Streamlit
- Pandas
- Plotly Express
- GeoJSON

---

## 📂 Estructura del Proyecto

```text
Proyecto/
├── principal.py
├── requirements.txt
├── README.md
├── data/
│   ├── Anexo1.NoFetal2019_CE_15-03-23.csv
│   ├── Anexo2.CodigosDeMuerte_CE_15-03-23.csv
│   ├── Divipola_CE_1.csv
│   ├── Divipola_CE_2.csv
│   └── departamentos_colombia.geojson
└── .streamlit/
    └── config.toml
```

---

## 🚀 Instalación

```bash
pip install -r requirements.txt
streamlit run principal.py
```

---

## 👨‍🎓 Autores

- Lida Esperanza García Quintero
- Henry Alfonso Palma Rojas

Universidad de La Salle
