import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium
import json

df = pd.read_csv('./data/pred2025_data.csv')

st.title('Central Organization by Month')

# Load Bangkok GeoJSON
with open("geo/bkk_districts.geojson", "r", encoding="utf-8") as f:
    gj = json.load(f)

months = sorted(df['month'].unique())

org_cols = [c for c in df.columns if not c.startswith("district_") and c not in ["year", "month", "district"]]

month = st.selectbox('Select Month', months)
org = st.selectbox('Select Oragnization', org_cols)

filtered = df[df["month"] == month]

# ------------------------------------------
# Build Folium map

m = folium.Map(location=[13.75, 100.50], zoom_start=11)

folium.Choropleth(
    geo_data=gj,
    data=filtered,
    columns=["district", org],
    key_on="feature.properties.district",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=1,
    legend_name=f"Workload - {org} (Month {month})",
).add_to(m)

st_folium(m, width=900, height=600)