# DSDE Data Visualization Dashboard (Streamlit)

Dashboard show workload of each organization consisting of central and district organizations

## Page 1: District Workload Comparison
User can choose:

- Month
- District

System will show Bar Chart sorting the workload of each organization from data csv

## Page 2: Central Organization Heatmap (Monthly)
User can choose:

- Month
- Central Organization

System will show Heatmap of workload of the selected organization
By using district of Bangkok (GeoJSON)

## Page 3: Central Organization Heatmap (Yearly)
User can choose:

- Central Organization

System will show yearly workload Heatmap of the selected organization
By using district of Bangkok (GeoJSON)


---


# How to run locally

## 1. Setup Dependencies

```
pip install -r requirements.txt
```

## 2. Run Streamlit

```
streamlit run app.py
```