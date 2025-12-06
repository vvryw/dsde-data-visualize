import streamlit as st

st.set_page_config(page_title="Bangkok Workload Dashboard", layout="wide")

st.title("📊 Bangkok Workload Visualization Dashboard")
st.subheader("From citizen reports to city workload insights")

st.markdown(
    """
Welcome to the **Bangkok Workload Dashboard** 👋  

This app turns Traffy Fondue reports (2023–2024) into:
- 🔥 **Heat maps** of workload across Bangkok districts  
- 🏢 **Organization-level views** of who handles what  
- 📅 **Monthly patterns**   

👉 Use the menu on the **left sidebar** to:
1. Explore workload by **district**
2. Compare **organizations**
3. View **time trends** and patterns

Ready? Pick a page on the left and start exploring Bangkok’s hidden workload. 🚦🏙️
"""
)