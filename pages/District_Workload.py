import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv('./data/pred2025_data.csv')

st.title('District Workload')

# Dropdowns
months = sorted(df['month'].unique())
districts = sorted(df['district'].unique())

month = st.selectbox('Select Month', months)
district = st.selectbox('Select District', districts)

filtered = df[(df['month'] == month) & (df['district'] == district)]


# Select only columns starting with district_
cols = [c for c in df.columns if c.startswith('district_') and c not in ["district_lat", "district_lon"]]
melted = filtered[cols].melt(var_name="organization", value_name="workload")
melted['organization'] = melted['organization'].str.replace("district_", "")

st.subheader(f"ผลการประเมินเขต: {district} เดือน {month}")

chart = (
    alt.Chart(melted)
    .mark_bar()
    .encode(
        x=alt.X("workload:Q", title="Workload"),
        y=alt.Y("organization:N", sort="-x", title="Organization"),
        color="workload"
    )
    .properties(height=500)
)


st.altair_chart(chart, use_container_width=True)