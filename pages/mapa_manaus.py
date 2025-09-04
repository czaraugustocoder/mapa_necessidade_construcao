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


st.set_page_config(page_title="MAPA - MANAUS",
                   layout="wide"
)


current_working_directory = os.getcwd()

data_path = os.path.join(current_working_directory, "ESCOLAS_LOCATION_NEW.xlsx")

data_semed = os.path.join(current_working_directory, "semed_escolas_loc_adaptado.xlsx")

path_logo = os.path.join(current_working_directory, "cest_logo.jpeg")

shp_path = os.path.join(current_working_directory, "BAIRROS.shp")

censo_path = os.path.join(current_working_directory, "CENSO 2010 E 2022.xlsx")

# Carregar os dados
data = pd.read_excel(data_path)
data.rename(columns={
    'Latitude': 'LATITUDE',
    'Longitude': 'LONGITUDE',
    'Escola': 'ESCOLA'
}, inplace=True)

dados_semed = pd.read_excel(data_semed)

def identificar_bairro_por_coordenada(lat, lon, gdf_bairros):
    """
    Retorna o nome do bairro correspondente à coordenada (lat, lon),
    usando o GeoDataFrame com os bairros.
    """
    ponto = Point(lon, lat)
    ponto_gdf = gpd.GeoDataFrame(geometry=[ponto], crs="EPSG:4326")

    # Faz a junção espacial ponto-polígono
    resultado = gpd.sjoin(ponto_gdf, gdf_bairros, how="left", predicate="within")

    # Retorna o nome do bairro (ou None se não encontrado)
    return resultado.iloc[0]['NOME_BAIRR'] if not resultado.empty else None

st.title("NECESSIDADE DE CONSTRUÇÃO - MANAUS")

#st.write("Mapa interativo das escolas estaduais (cor azul) e municipais (cor laranja) da cidade de Manaus")

st.sidebar.image(path_logo, use_column_width=True)

# Ler o shapefile
gdf = gpd.read_file(shp_path).to_crs("EPSG:4326")

# Identificar bairros e adicionar ao DataFrame
data['BAIRRO'] = data.apply(
    lambda row: identificar_bairro_por_coordenada(row['LATITUDE'], row['LONGITUDE'], gdf),
    axis=1
)

dados_semed['BAIRRO'] = dados_semed.apply(
    lambda row: identificar_bairro_por_coordenada(row['LATITUDE'], row['LONGITUDE'], gdf),
    axis=1
)

# Contar número de escolas por bairro
escolas_por_bairro = data.groupby('BAIRRO')['SIGEAM_Escola'].nunique().reset_index()
escolas_por_bairro.rename(columns={'SIGEAM_Escola': 'NUM_ESCOLAS'}, inplace=True)

escolas_por_bairro_semed = dados_semed.groupby('BAIRRO')['SIGEAM_ESCOLA'].nunique().reset_index()
escolas_por_bairro_semed.rename(columns={'SIGEAM_ESCOLA': 'NUM_ESCOLAS_SEMED'}, inplace=True)

censo = pd.read_excel(censo_path)

# Criar mapa base
m = folium.Map(location=[-3.057334413281103, -59.98600479911497], zoom_start=11.50)

# Unir com o shapefile
gdf_mapa = gdf.merge(censo[["BAIRRO","TOTAL AT", "TOTAL DA", "TOTAL SALAS"]], left_on='NOME_BAIRR', right_on='BAIRRO', how='left')

# Juntar a contagem de escolas ao GeoDataFrame
gdf_mapa = gdf_mapa.merge(escolas_por_bairro, left_on='NOME_BAIRR', right_on='BAIRRO', how='left')
gdf_mapa['NUM_ESCOLAS'] = gdf_mapa['NUM_ESCOLAS'].fillna(0).astype(int)

gdf_mapa = gdf_mapa.merge(escolas_por_bairro_semed, left_on='NOME_BAIRR', right_on='BAIRRO', how='left')
gdf_mapa['NUM_ESCOLAS_SEMED'] = gdf_mapa['NUM_ESCOLAS_SEMED'].fillna(0).astype(int)

# formatando os números

gdf_mapa["TOTAL_AT_fmt"] = gdf_mapa["TOTAL AT"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
gdf_mapa["TOTAL_DA_fmt"] = gdf_mapa["TOTAL DA"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
gdf_mapa["TOTAL_SALAS_fmt"] = gdf_mapa["TOTAL SALAS"].apply(lambda x: f"{x:,.0f}".replace(",", "."))

local = st.sidebar.multiselect('Escolha o bairro:', gdf['NOME_BAIRR'].unique())

if (len(local) > 1) or (len(local) == 0):
   print(local)

   # Adicionar o mapa coroplético
   Choropleth(
        geo_data=gdf_mapa.to_json(),
        name='choropleth',
        data=gdf_mapa,
        columns=['NOME_BAIRR', 'TOTAL SALAS'],
        key_on='feature.properties.NOME_BAIRR',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Salas Necessárias',
        nan_fill_color='white'
    ).add_to(m)
   
else:
    print(local)
    bairro_shp = gdf.loc[gdf['NOME_BAIRR']  ==  local[0]]
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
name="Bairros",
style_function=lambda feature: {
    'fillOpacity': 0,
    'color': 'black',
    'weight': 0.7
        },
    tooltip=folium.GeoJsonTooltip(
    fields=['NOME_BAIRR', 'NUM_ESCOLAS', 'NUM_ESCOLAS_SEMED', 'TOTAL_AT_fmt', 'TOTAL_DA_fmt', 'TOTAL_SALAS_fmt'],
    aliases=['Bairro', 'Escolas Estaduais', 'Escolas Municipais', 'Total de Atendimento:', 'Déficite de Atendimento:', 'Salas Necessárias:'],
    max_width=300,
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