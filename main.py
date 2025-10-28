import requests
import json
import pandas as pd
import glob
import re
from pathlib import Path


def scrap_Runstat(num_json, year):
    URL = f"https://results.timeto.com/storage/results/races/{num_json}/{num_json}.json"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json,*/*",
        "Referer": f"https://results.timeto.com/schneider_electric_marathon_de_paris_{year}/",
    }

    r = requests.get(URL, headers=headers, timeout=60)
    r.raise_for_status()
    data = r.json()

    with open(f"paris_{year}_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


    def json_to_df(obj):
        cols = [h.get("field_name") or h.get("csv_header") or "col" for h in obj["header"]]
        return pd.DataFrame(obj["data"], columns=cols)
    df = json_to_df(data)
    print("Total lignes:", len(df))
    print(df.head(3))

    keep = []
    for name in ["Dossard", "Nom", "Prénom", "Sexe", "Catégorie", "Nationalité", "Temps", "Temps officiel"]:
        if name in df.columns:
            keep.append(name)
    # 6) Exports
    df.to_csv(f"paris_marathon_{year}_fullv2.csv", index=False, encoding="utf-8-sig")
    print("✅ Exports créés :")
    print(f"- paris_marathon_{year}_full.csv (toutes colonnes)")


json_links = {
    "year": [2021, 2022, 2023, 2024, 2025],
    "num_json": [478, 412, 370, 318, 658]
    }


for num_json, year in zip(json_links["num_json"], json_links["year"]):
    scrap_Runstat(num_json, year)


files = glob.glob("/home/onyxia/work/RunStat/paris_marathon_20*.csv")  # ex: "data/*.csv" si besoin

dfs = []
for f in files:
    df = pd.read_csv(f, encoding="utf-8-sig")  
    year_match = re.search(r"(20\d{2})", Path(f).stem)
    year = year_match.group(1) if year_match else None
    if "Année" not in df.columns:
        df["Année"] = year
    dfs.append(df)


merged = pd.concat(dfs, ignore_index=True)

if "Année" in merged.columns:
    merged = merged.sort_values(by=["Année"], ascending=True)

merged.to_csv("marathon_all_years.csv", index=False, encoding="utf-8-sig")
print("OK →", merged.shape, "lignes dans marathon_all_years.csv")
