import folium
from folium import Choropleth
from folium import Choropleth, GeoJson, LayerControl
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import HeatMap
import pandas as pd
import math
import os
from shapely.geometry import Point


st.set_page_config(page_title="MAPA - INTERIOR",
                   layout="wide"
)


current_working_directory = os.getcwd()

data_path = os.path.join(current_working_directory, "BASE_INTERIOR.xlsx")

path_logo = os.path.join(current_working_directory, "cest_logo.jpeg")

shp_path = os.path.join(current_working_directory, "AM_Municipios_2024.shp")

# Carregar os dados
data = pd.read_excel(data_path)

st.title("NECESSIDADE DE CONSTRUÇÃO - INTERIOR DO AMAZONAS")

#st.write("Mapa interativo das escolas estaduais (cor azul) e municipais (cor laranja) da cidade de Manaus")

st.sidebar.image(path_logo, use_container_width=True)

# Ler o shapefile
gdf = gpd.read_file(shp_path).to_crs("EPSG:4326")

gdf['NM_MUN'] = gdf['NM_MUN'].str.upper()


# Criar mapa base
m = folium.Map(location=[-3.057334413281103, -64.98600479911497], zoom_start=5.50)

# Unir com o shapefile
gdf_mapa = gdf.merge(
    data[[  
        "MUNICÍPIO",
        "TOTAL P",
        "0-3 AT", "4-5 AT", "6-10 AT", "11-14 AT", "15-17 AT", "TOTAL AT",
        "0-3 DA", "4-5 DA", "6-10 DA", "11-14 DA", "15-17 DA", "TOTAL DA", "TOTAL DA - POS",
        "0-3 SALAS", "4-5 SALAS", "6-10 SALAS", "11-14 SALAS", "15-17 SALAS", "TOTAL SALAS"
    ]],
    left_on="NM_MUN",
    right_on="MUNICÍPIO",
    how="left"
)

# Listar todas as colunas numéricas que precisam ser formatadas
colunas_para_formatar = [
    "TOTAL P",
    "0-3 AT", "4-5 AT", "6-10 AT", "11-14 AT", "15-17 AT", "TOTAL AT",
    "0-3 DA", "4-5 DA", "6-10 DA", "11-14 DA", "15-17 DA", "TOTAL DA", "TOTAL DA - POS",
    "0-3 SALAS", "4-5 SALAS", "6-10 SALAS", "11-14 SALAS", "15-17 SALAS", "TOTAL SALAS"
]

# Criar versões formatadas
for col in colunas_para_formatar:
    gdf_mapa[f"{col}_fmt"] = gdf_mapa[col].apply(lambda x: f"{x:,.0f}".replace(",", ".") if pd.notnull(x) else "0")

# Filtro lateral
local = st.sidebar.multiselect('Escolha o Município:', gdf['NM_MUN'].unique())

if (len(local) > 1) or (len(local) == 0):
   print(local)

   # Adicionar o mapa coroplético
   Choropleth(
        geo_data=gdf_mapa.to_json(),
        name='choropleth',
        data=gdf_mapa,
        columns=['NM_MUN', 'TOTAL SALAS'],
        key_on='feature.properties.NM_MUN',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Salas Necessárias',
        nan_fill_color='white'
    ).add_to(m)
   
else:
    print(local)
    mun_shp = gdf.loc[gdf['NM_MUN'] == local[0]]
    geojson_mun = mun_shp.to_json()
    # Adicionar o segundo GeoJSON ao mapa com cor diferente
    folium.GeoJson(
        geojson_mun,
        name='shapefile',
        style_function=lambda x: {
            'color': 'purple',
            'weight': 6,
            'opacity': 1.0,
            'fillColor': 'purple',
            'fillOpacity': 0.7
        }
    ).add_to(m)

# Camada com contornos dos municípios
folium.GeoJson(
    gdf_mapa,
    name="Municípios",
    style_function=lambda feature: {
        'fillOpacity': 0,
        'color': 'black',
        'weight': 0.7
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['NM_MUN', 'TOTAL AT_fmt', 'TOTAL DA - POS_fmt', 'TOTAL SALAS_fmt',
                '0-3 SALAS_fmt', '4-5 SALAS_fmt', '6-10 SALAS_fmt', '11-14 SALAS_fmt', '15-17 SALAS_fmt'],
        aliases=['Município', 'Total de Atendimento:', 'Déficite de Atendimento:',
                 'Salas Necessárias (S.N):', 'S.N - 0 a 3 anos:', 'S.N - 4 a 5 anos:',
                 'S.N - 6 a 10 anos:', 'S.N - 11 a 14 anos:', 'S.N - 15 a 17 anos:'],
        max_width=300,
        style=(
            "background-color: white; "
            "color: #333333; "
            "font-family: Arial; "
            "font-size: 42px; "
            "padding: 8px;"
        )
    )
).add_to(m)

# Controles
folium.LayerControl().add_to(m)

# Exibir no Streamlit
st_folium(m, width=1000, returned_objects=[])








