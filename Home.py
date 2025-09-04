import streamlit as st
from streamlit_folium import st_folium
import os

current_working_directory = os.getcwd()

path_logo = os.path.join(current_working_directory, "cest_logo.jpeg")

st.title("NECESSIDADE DE CONSTRUÇÃO")

st.write("Mapa interativo da necessidade de construção de escolas do Amazonas")

st.markdown(""" 
Bem-vindo ao **Mapa das Necessidades de Construção de Escolas**!  

Este aplicativo interativo apresenta, de forma **geográfica e visual**, os **bairros e municípios do estado** com maior demanda por novas unidades escolares.  

### 🔍 O que você pode fazer aqui:
- 📍 Visualizar a distribuição espacial das necessidades de salas e escolas;  
- 📊 Comparar a capacidade atual de atendimento com a demanda existente;  
- 🎯 Identificar áreas prioritárias para planejamento e investimentos em educação.  

Nosso objetivo é **facilitar a análise e a tomada de decisão**, oferecendo uma ferramenta intuitiva, acessível e baseada em dados atualizados.  
""")


st.sidebar.image(path_logo, use_column_width=True)