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
gdf_mapa = gdf.merge(data[["MUNICÍPIO","TOTAL AT", "TOTAL DA", "TOTAL SALAS"]], left_on='NM_MUN', right_on='MUNICÍPIO', how='left')


# formatando os números

gdf_mapa["TOTAL_AT_fmt"] = gdf_mapa["TOTAL AT"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
gdf_mapa["TOTAL_DA_fmt"] = gdf_mapa["TOTAL DA"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
gdf_mapa["TOTAL_SALAS_fmt"] = gdf_mapa["TOTAL SALAS"].apply(lambda x: f"{x:,.0f}".replace(",", "."))

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
    bairro_shp = gdf.loc[gdf['NM_MUN']  ==  local[0]]
    geojson_bairro = bairro_shp.to_json()
    # Adicionar o segundo GeoJSON ao mapa com uma cor diferente
    folium.GeoJson(
        geojson_bairro,
    name='shapefile',
    style_function=lambda x: {
        'color': 'purple',        # cor da borda
        'weight': 6,              # espessura da borda
        'opacity': 1.0,           # opacidade da borda
        'fillColor': 'purple',    # cor de preenchimento
        'fillOpacity': 0.7
    }
    ).add_to(m)

# Camada com contornos dos bairros
folium.GeoJson(
gdf_mapa,
name="Municípios",
style_function=lambda feature: {
    'fillOpacity': 0,
    'color': 'black',
    'weight': 0.7
        },
    tooltip=folium.GeoJsonTooltip(
    fields=['NM_MUN', 'TOTAL_AT_fmt', 'TOTAL_DA_fmt', 'TOTAL_SALAS_fmt'],
    aliases=['Município', 'Total de Atendimento:', 'Déficite de Atendimento:', 'Salas Necessárias:'],
    max_width=100,
    style=(
        "background-color: white; "
        "color: #333333; "
        "font-family: Arial; "
        "font-size: 42px; "
        "padding: 8px;"
    ))
).add_to(m)

# Controles
folium.LayerControl().add_to(m)


st_folium(m, width=1000, returned_objects=[])

