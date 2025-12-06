import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv('./data/predict_2025.csv')

st.title('District Workload')

# Dropdowns
months = sorted(df['month'].unique())
districts = sorted(df['district'].unique())

month = st.selectbox('Select Month', months)
district = st.selectbox('Select District', districts)

# Filter by month & district
filtered = df[(df['month'] == month) & (df['district'] == district)]

# --- Select only pred_district_ columns ---
cols = [c for c in df.columns if c.startswith('pred_district_')]

# Melt into long format
melted = filtered[cols].melt(var_name="organization", value_name="workload")

# Clean organization names (remove prefix + remove _count)
melted['organization'] = (
    melted['organization']
    .str.replace("pred_district_", "", regex=False)
    .str.replace("_count", "", regex=False)
)

st.subheader(f"ผลการประเมินเขต: {district} เดือน {month}")

# Altair Bar Chart
chart = (
    alt.Chart(melted)
    .mark_bar()
    .encode(
        x=alt.X("workload:Q", title="Workload"),
        y=alt.Y("organization:N", sort="-x", title="Organization"),
        color=alt.Color("workload:Q", scale=alt.Scale(scheme='blues')),
        tooltip=["organization", "workload"]
    )
    .properties(height=500)
)

st.altair_chart(chart, use_container_width=True)
