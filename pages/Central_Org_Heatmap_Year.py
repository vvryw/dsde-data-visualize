import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json

df = pd.read_csv('./data/predict_2025.csv')

st.title("Yearly Heatmap — Central Organization")

# Load GeoJSON
with open("geo/bkk_districts.geojson", "r", encoding="utf-8") as f:
    gj = json.load(f)

# Raw columns
org_cols_raw = [c for c in df.columns if not c.startswith("pred_district_") and c not in ["year", "month", "district"]]

# Clean display names
org_display = {c: c.replace("pred_", "").replace("_count", "") for c in org_cols_raw}

org_label = st.selectbox("Select Organization", list(org_display.values()))

# Convert display name → real column name
org = [k for k, v in org_display.items() if v == org_label][0]

# Sum for whole year
sum_df = df.groupby("district")[org].sum().reset_index()

m = folium.Map(location=[13.75, 100.50], zoom_start=11)

folium.Choropleth(
    geo_data=gj,
    data=sum_df,
    columns=["district", org],
    key_on="feature.properties.district",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=1,
    legend_name=f"Annual Workload - {org_label}",
).add_to(m)

# Add workload to GeoJSON
for feature in gj["features"]:
    dist = feature["properties"]["district"]
    val = sum_df.loc[sum_df["district"] == dist, org]
    feature["properties"]["workload"] = float(val.values[0]) if len(val) else None

# Tooltip layer
folium.GeoJson(
    gj,
    style_function=lambda feature: {
        "fillColor": "transparent",
        "color": "black",
        "weight": 1,
        "fillOpacity": 0,
    },
    highlight_function=lambda feature: {
        "weight": 5,
        "color": "#68BBE3",
        "fillOpacity": 0.3,
    },
    tooltip=folium.features.GeoJsonTooltip(
        fields=["district", "workload"],
        aliases=["District:", f"{org_label}:"],
        localize=True
    ),
).add_to(m)

st_folium(m, width=900, height=600)