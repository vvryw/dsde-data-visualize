import json
from collections import defaultdict
from shapely.geometry import shape, mapping
from shapely.ops import unary_union

# 1. โหลดไฟล์ subdistricts.geojson
with open("subdistricts.geojson", "r", encoding="utf-8") as f:
    gj = json.load(f)

# 2. เอาเฉพาะที่อยู่ในจังหวัด "กรุงเทพมหานคร"
bkk_features = [f for f in gj["features"]
                if f["properties"]["pro_th"] == "กรุงเทพมหานคร"]

# 3. รวม polygon ตามชื่อเขต (amp_th)
district_geoms = defaultdict(list)
sample_props = {}

for feat in bkk_features:
    props = feat["properties"]
    amp = props["amp_th"]          # ชื่อเขต เช่น "พระนคร"
    district_geoms[amp].append(shape(feat["geometry"]))
    sample_props.setdefault(amp, props)

# 4. union polygon ในเขตเดียวกันให้เป็น 1 ชิ้น
district_features = []
for amp, geoms in district_geoms.items():
    union_geom = unary_union(geoms)

    # ตรงนี้กำหนดชื่อ field ที่จะใช้ join กับ CSV
    props = {
        "district": amp,                         # เช่น "พระนคร"
        "amp_code": sample_props[amp]["amp_code"],
        "pro_th": sample_props[amp]["pro_th"],
        "pro_en": sample_props[amp]["pro_en"],
    }

    district_features.append({
        "type": "Feature",
        "properties": props,
        "geometry": mapping(union_geom),
    })

bkk_gj = {
    "type": "FeatureCollection",
    "name": "Bangkok Districts",
    "features": district_features,
}

# 5. เซฟไฟล์ใหม่
with open("bkk_districts.geojson", "w", encoding="utf-8") as f:
    json.dump(bkk_gj, f, ensure_ascii=False)

print("Saved bkk_districts.geojson with", len(district_features), "districts")
