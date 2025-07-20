import streamlit as st
import pydeck as pdk
import json

@st.cache_data

# lê dados de um arquivo json e retorna o 'objeto' descrito no mesmo
def from_data_file(filename: str):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

#carga dos dados (sim, são 6 arquivos)
dadosAIH =  from_data_file("dados/AIH_data.json")
dadosAPAC = from_data_file("dados/APAC_data.json")
dadosBPA =  from_data_file("dados/BPA_data.json")
dadosFluxoAIH =  from_data_file("dados/AIH_flow.json")
dadosFluxoAPAC = from_data_file("dados/APAC_flow.json")
dadosFluxoBPA =  from_data_file("dados/BPA_flow.json")

# cria um gráfico de 'barras hexagonais' do streamlit a partir de um conjunto de dados
def mkHexLayer(theData, color):
    return pdk.Layer(
        "HexagonLayer",
        data=theData,
        get_position=["lng", "lat"],
        get_elevation = "quant * 10000000",
        radius=16000,
        elevation_scale=256,
        get_fill_color = color,
        pickable = True,
        auto_highlight = True,
        elevation_range=[0, 1000],
        extruded=True,
    )
#cria um 'gráfico de arcos' a partir de um conjunto de dados
def mkFlowLayer(theData, color):
    return pdk.Layer(
        "ArcLayer",
        data=theData,
        get_source_position=["lng0", "lat0"],
        get_target_position=["lng", "lat"],
        get_source_color=color,
        get_target_color=color,
        auto_highlight=True,
        width_scale=0.0001,
        get_width="valor",
        width_min_pixels=3,
        width_max_pixels=30,
    ),

try:
    all_layers = {    
        "AIHs":  mkHexLayer(dadosAIH,[200, 120, 200, 120]), # '[valor*5, 140, 200]'),
        "APACs": mkHexLayer(dadosAPAC, [120, 200, 200, 120]), #'[valor*5, 100, 150]'),
        "BPAs":  mkHexLayer(dadosBPA, [120, 120, 200, 200]), #'[valor*5, 60, 100]'),
        "Fluxo AIHs":  mkFlowLayer(dadosFluxoAIH, [200, 120, 200, 120]),
        "Fluxo APACs": mkFlowLayer(dadosFluxoAPAC, [120, 200, 200, 120]),
        "Fluxo BPAs":  mkFlowLayer(dadosFluxoBPA, [120, 120, 200, 200]),
    }



    st.sidebar.subheader("Procedências UNICAMP")
    selected_layers = [
        layer
        for layer_name, layer in all_layers.items()
        if st.sidebar.checkbox(layer_name, (layer_name == 'AIHs'))
    ]
    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_style = None,
                initial_view_state={
                    "latitude": -22.817161, 
                    "longitude":  -47.069752,
                    "zoom": 6,
                    "pitch": 50,
                },
                layers=selected_layers,
            )
        )
    else:
        st.error("Selecione uma das opções à esquerda.")
except Exception as e:
    st.error(
        f"""
        **This demo requires internet access.**
        Connection error: ????
    """
    )