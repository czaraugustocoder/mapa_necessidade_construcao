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

Processo de Cálculo da Necessidade de Construção de Novas Salas de Aula no Estado do Amazonas
1. Municípios do Interior
Para os municípios do interior, adotou-se como base:
	a estimativa populacional dos municípios para 2024 - IBGE;
	a estimativa da população por idade no Estado do Amazonas para o mesmo ano - IBGE.
Etapas da metodologia
	Definição das faixas etárias por nível de ensino:
	0 a 3 anos – Creche
	4 a 5 anos – Pré-escola
	6 a 10 anos – Ensino Fundamental – Anos Iniciais
	11 a 14 anos – Ensino Fundamental – Anos Finais
	15 a 17 anos – Ensino Médio
	Cálculo da população dos municípios por faixa etária, por meio da seguinte fórmula:
PopMFe=PopTAm/PopAmFe.PopM
Legenda dos termos:
	PopMFe = população do município por faixa etária
	PopTAm = população total do Amazonas
	PopAmFe = população do Amazonas por faixa etária
	PopM = população total do município
	Apuração do déficit de atendimento: diferença entre a população da faixa etária correspondente a cada nível de ensino e o número de matrículas registradas em 2024.
	Cálculo da necessidade de salas de aula: divisão do déficit de atendimento pela capacidade pedagógica estabelecida pela Lei Estadual nº 257/2015, que define o número máximo de alunos por turma em cada etapa.
	Ressalta-se que os cálculos foram realizados considerando o atendimento em um único turno.
2. Capital – Manaus
Para o município de Manaus, cuja estimativa populacional de 2024 encontra-se disponível apenas o total, foi necessária a projeção da população por bairros da área urbana.

Etapas da metodologia
	Fontes de referência: Censos Demográficos de 2010 e 2022.
	Técnica utilizada: aplicação do método AiBi, empregado pela Prefeitura do Rio de Janeiro (referência).
	O método AiBi consiste no cálculo de fatores de proporção, utilizados para distribuir a população entre bairros, ajustando-a para o ano de 2024.
	Ajustes específicos:
	No bairro Glória, observou-se forte decréscimo populacional entre os Censos de 2010 e 2022. Para evitar distorções, aplicou-se um fator multiplicador de 10 sobre a projeção.
	Nos demais bairros, manteve-se integralmente a metodologia original, sem ajustes adicionais.
	Aplicação da metodologia de cálculo: com a população estimada por bairro, seguiu-se o mesmo procedimento utilizado nos municípios do interior:
	estimativa da população por faixa etária;
	comparação com as matrículas de 2024;
	cálculo do déficit de atendimento;
	definição da necessidade de novas salas de aula com base na Lei Estadual nº 257/2015.
	Considerou-se o atendimento em um único turno
""")



st.sidebar.image(path_logo, use_container_width=True)

