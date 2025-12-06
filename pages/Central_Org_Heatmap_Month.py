import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium
import json

df = pd.read_csv('./data/predict_2025.csv')

st.title('Monthly Heatmap — Central Organization')

# Load Bangkok GeoJSON
with open("geo/bkk_districts.geojson", "r", encoding="utf-8") as f:
    gj = json.load(f)

months = sorted(df['month'].unique())

# ใช้เฉพาะคอลัมน์ที่ไม่ใช่ pred_district_
org_cols_raw = [c for c in df.columns if not c.startswith("pred_district_") and c not in ["year", "month", "district"]]

# แปลงชื่อสำหรับแสดงผล
org_display = {c: c.replace("pred_", "").replace("_count", "") for c in org_cols_raw}

# Dropdown ใช้ชื่อที่ล้างแล้ว แต่ต้องแมปกลับไปหา raw column
month = st.selectbox('Select Month', months)
org_label = st.selectbox('Select Organization', list(org_display.values()))
org = [k for k, v in org_display.items() if v == org_label][0]   # convert back to real column name

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
    legend_name=f"Workload - {org_label} (Month {month})",
).add_to(m)

# Merge GeoJSON properties with workload
for feature in gj["features"]:
    dist = feature["properties"]["district"]
    val = filtered.loc[filtered["district"] == dist, org]
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