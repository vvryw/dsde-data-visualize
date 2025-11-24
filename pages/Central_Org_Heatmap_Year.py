import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json

df = pd.read_csv('./data/pred2025_data.csv')

st.title("Yearly Heatmap — Central Organization")

# Load GeoJSON
with open("geo/bkk_districts.geojson", "r", encoding="utf-8") as f:
    gj = json.load(f)


# Central org columns
org_cols = [c for c in df.columns if not c.startswith("district_") and c not in ["year", "month", "district"]]

org = st.selectbox("Select Organization", org_cols)

# Sum whole year (group by district)
sum_df = df.groupby("district")[org].sum().reset_index()

m = folium.Map(location=[13.75, 100.50], zoom_start=11)

m = folium.Map(location=[13.75, 100.50], zoom_start=11)

folium.Choropleth(
    geo_data=gj,
    data=sum_df,
    columns=["district", org],
    key_on="feature.properties.district",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=1,
    legend_name=f"Annual Workload - {org}",
).add_to(m)

st_folium(m, width=900, height=600)