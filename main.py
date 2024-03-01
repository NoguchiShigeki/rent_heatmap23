# Imports
import folium as f
import streamlit as st
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd

# Variables
GEOJSON_PATH = "./data/tokyo23.json"
DATASET_PATH = "./csvs/data.csv"

# Cashing data and geojson
@st.cache_data
def load_data():
    return pd.read_csv(DATASET_PATH)

@st.cache_data
def load_geojson():
    return gpd.read_file(GEOJSON_PATH)

st.set_page_config(
    page_title="Rent Mapper",
    page_icon="🗾",
    layout="wide"
)

map = f.Map(
    location=(35.685175, 139.7528),
    tiles="cartodbpositron",
    zoom_start=11
)

# Geojson
geojson = load_geojson()

df = load_data()
# Accumulate the average rent by ward
df_group = df.groupby("Ward").aggregate({"SumoAveRent": "mean"}).reset_index()

# Then hand over the data to the choropleth
f.Choropleth(
    geo_data=geojson,
    data=df_group,
    columns=["Ward", "SumoAveRent"],
    key_on="feature.properties.N03_004",
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Average Rent'
).add_to(map)

st_folium(map, use_container_width=True, height=720, returned_objects=[])