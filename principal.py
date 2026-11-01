import streamlit as st
import pandas as pd
import plotly.express as px
import json

# ========================================
# CONFIGURACIÓN DE PÁGINA
# ========================================

st.set_page_config(
    page_title="Mortalidad Colombia 2019",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# PORTADA
# =====================================================

st.markdown(
    """
    <div style="
        background-color:#111827;
        padding:40px;
        border-radius:15px;
        text-align:center;
        color:white;
        border:2px solid #374151;
        margin-bottom:20px;
    ">

    <h1 style="color:white;">
        UNIVERSIDAD DE LA SALLE
    </h1>

    <h2 style="color:white;">
        ACTIVIDAD 4 APLICACIÓN WEB MORTALIDAD EN COLOMBIA 2019
    </h2>

    <br>

    <h3 style="color:white;">
        Materia: APLICACIONES I - G2
    </h3>

    <br><br>

    <p style="font-size:20px; color:white;">
        <b>Estudiantes:</b>
        LIDA ESPERANZA GARCIA QUINTERO y HENRY ALFONSO PALMA ROJAS
    </p>

    <p style="font-size:20px; color:white;">
        <b>Docente:</b>
        CRISTIAN DUNEY BERMUDEZ QUINTERO
    </p>

    <p style="font-size:20px; color:white;">
        <b>Fecha:</b>
        31 de octubre de 2026
    </p>

    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

st.title("📊 Dashboard de Mortalidad en Colombia 2019")

st.markdown(
    """
    Sistema de análisis y visualización de datos de mortalidad
    en Colombia utilizando información oficial del DANE.
    """
)

st.markdown("---")


# ========================================
# CARGA DE DATOS
# ========================================

@st.cache_data
def cargar_datos():

    mortalidad = pd.read_csv(
        "data/Anexo1.NoFetal2019_CE_15-03-23.csv",
        sep=";",
        encoding="latin1",
        low_memory=False
    )

    causas = pd.read_csv(
        "data/Anexo2.CodigosDeMuerte_CE_15-03-23.csv",
        sep=";",
        encoding="latin1",
        low_memory=False
    )

    div1 = pd.read_csv(
        "data/Divipola_CE_1.csv",
        sep=";",
        encoding="latin1"
    )

    div2 = pd.read_csv(
        "data/Divipola_CE_2.csv",
        sep=";",
        encoding="latin1"
    )

    with open(
        "data/departamentos_colombia.geojson",
        "r",
        encoding="utf-8"
    ) as f:

        geojson = json.load(f)

    return mortalidad, causas, div1, div2, geojson


df, causas, div1, div2, geojson = cargar_datos()

# ========================================
# LIMPIEZA
# ========================================

df.columns = df.columns.str.strip()

causas.columns = causas.columns.str.strip()

div1.columns = div1.columns.str.strip()

div2.columns = div2.columns.str.strip()

divipola = pd.concat(
    [div1, div2],
    ignore_index=True
)

#st.write(divipola.columns.tolist())

##nvo depto
# Relacionar departamento con mortalidad

divipola["COD_DEPARTAMENTO"] = (
    divipola["COD_DEPARTAMENTO"]
    .astype(str)
    .str.zfill(2)
)

df["COD_DEPARTAMENTO"] = (
    df["COD_DEPARTAMENTO"]
    .astype(str)
    .str.zfill(2)
)

departamentos_df = (
    divipola[
        ["COD_DEPARTAMENTO", "DEPARTAMENTO"]
    ]
    .drop_duplicates()
)

df = df.merge(
    departamentos_df,
    on="COD_DEPARTAMENTO",
    how="left"
)

##fin depto

# ========================================
# CÓDIGOS
# ========================================

df["COD_DEPARTAMENTO"] = (
    df["COD_DEPARTAMENTO"]
    .astype(str)
    .str.zfill(2)
)

df["COD_MUNICIPIO"] = (
    df["COD_MUNICIPIO"]
    .astype(str)
    .str.zfill(3)
)

# ========================================
# RELACIÓN CAUSAS DE MUERTE
# ========================================

codigo_col = None
descripcion_col = None

for col in causas.columns:

    if "DESCRIP" in col.upper():
        descripcion_col = col

    if "MORTALIDAD" in col.upper() and "COD" in col.upper():
        codigo_col = col

if codigo_col and descripcion_col:

    causas = causas.rename(
        columns={
            codigo_col: "COD_MUERTE",
            descripcion_col: "DESCRIPCION_CAUSA"
        }
    )

    df = df.merge(
        causas[
            ["COD_MUERTE", "DESCRIPCION_CAUSA"]
        ],
        on="COD_MUERTE",
        how="left"
    )



# ========================================
# FILTRO DEPARTAMENTO
# ========================================
# ========================================
# FILTRO DEPARTAMENTO
# ========================================

st.sidebar.markdown("## 🌎 Ubicación")

departamentos = sorted(
    df["COD_DEPARTAMENTO"]
    .astype(str)
    .dropna()
    .unique()
)

depto = st.sidebar.selectbox(
    "📍 Seleccione un Departamento",
    ["Todos"] + list(departamentos)
)

if depto == "Todos":

    df_filtrado = df.copy()

else:

    df_filtrado = df[
        df["COD_DEPARTAMENTO"].astype(str) == depto
    ]

# ========================================
# INDICADORES
# ========================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Total Registros",
        f"{len(df_filtrado):,}"
    )

with col2:

    if "SEXO" in df_filtrado.columns:

        st.metric(
            "Categorías Sexo",
            df_filtrado["SEXO"].nunique()
        )

with col3:

    if "COD_MUERTE" in df_filtrado.columns:

        st.metric(
            "Causas Registradas",
            df_filtrado["COD_MUERTE"].nunique()
        )

st.markdown("---")

# ========================================
# MAPA COLOMBIA
# ========================================

st.subheader("🗺️ Mortalidad por Departamento")

muertes_departamento = (
    df.groupby("COD_DEPARTAMENTO")
      .size()
      .reset_index(name="TOTAL")
)

try:

    fig_mapa = px.choropleth(
        muertes_departamento,
        geojson=geojson,
        locations="COD_DEPARTAMENTO",
        featureidkey="properties.DPTO_CCDGO",
        color="TOTAL",
        color_continuous_scale="Reds",
        title="Mortalidad por Departamento"
    )

    fig_mapa.update_geos(
        fitbounds="locations",
        visible=False
    )

    st.plotly_chart(
        fig_mapa,
        use_container_width=True
    )

except Exception as e:

    st.error(f"Error generando mapa: {e}")

# ========================================
# MUERTES POR MES
# ========================================

st.subheader("📈 Mortalidad por Mes")

if "MES" in df_filtrado.columns:

    por_mes = (
        df_filtrado.groupby("MES")
        .size()
        .reset_index(name="TOTAL")
        .sort_values("MES")
    )

    fig_mes = px.line(
        por_mes,
        x="MES",
        y="TOTAL",
        markers=True
    )

    st.plotly_chart(
        fig_mes,
        use_container_width=True
    )

# ========================================
# SEXO
# ========================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("👨👩 Distribución por Sexo")

    if "SEXO" in df_filtrado.columns:

        sexo = (
            df_filtrado.groupby("SEXO")
            .size()
            .reset_index(name="TOTAL")
        )

        fig_sexo = px.pie(
            sexo,
            names="SEXO",
            values="TOTAL"
        )

        st.plotly_chart(
            fig_sexo,
            use_container_width=True
        )

with col2:

    st.subheader("📊 Grupo de Edad")

    if "GRUPO_EDAD1" in df_filtrado.columns:

        fig_edad = px.histogram(
            df_filtrado,
            x="GRUPO_EDAD1",
            color="SEXO"
        )

        st.plotly_chart(
            fig_edad,
            use_container_width=True
        )

# ========================================
# TOP 10 CAUSAS
# ========================================

st.subheader("🏥 Top 10 Causas de Muerte")

if "DESCRIPCION_CAUSA" in df_filtrado.columns:

    top_causas = (
        df_filtrado
        .groupby("DESCRIPCION_CAUSA")
        .size()
        .reset_index(name="TOTAL")
        .sort_values(
            "TOTAL",
            ascending=False
        )
        .head(10)
    )

    fig_causas = px.bar(
        top_causas,
        x="TOTAL",
        y="DESCRIPCION_CAUSA",
        orientation="h",
        color="TOTAL"
    )

    st.plotly_chart(
        fig_causas,
        use_container_width=True
    )

# ========================================
# HOMICIDIOS
# ========================================

st.subheader("⚠️ Top 5 Municipios con Homicidios")

if "MANERA_MUERTE" in df_filtrado.columns:

    homicidios = df_filtrado[
        df_filtrado["MANERA_MUERTE"]
        .astype(str)
        .str.contains(
            "HOMIC",
            case=False,
            na=False
        )
    ]

    top_hom = (
        homicidios
        .groupby("COD_MUNICIPIO")
        .size()
        .reset_index(name="TOTAL")
        .sort_values(
            "TOTAL",
            ascending=False
        )
        .head(5)
    )

    fig_hom = px.bar(
        top_hom,
        x="COD_MUNICIPIO",
        y="TOTAL",
        color="TOTAL"
    )

    st.plotly_chart(
        fig_hom,
        use_container_width=True
    )

# ========================================
# TABLA
# ========================================

st.subheader("📋 Vista de Datos")

st.dataframe(
    df_filtrado.head(1000),
    use_container_width=True
)

# ========================================
# DESCARGA CSV
# ========================================

csv = df_filtrado.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇ Descargar Datos Filtrados",
    data=csv,
    file_name="mortalidad_filtrada.csv",
    mime="text/csv"
)