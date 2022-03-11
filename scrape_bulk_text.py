import scrape_text
import pandas as pd
import json
companies = pd.read_csv("GoodCom.csv")
ciks = companies["CIK"].astype(int).tolist()

years = [2022,2021]

data = dict()

for cik in ciks:
    year_dict = dict()
    for year in years:
        try:
            x = scrape_text.get_scrape_text(cik,"10-K",f"{year-1}0101",f"{year}0101")
            year_dict[year] = x
        except:
            continue
    data[cik] = year_dict
with open("data.json", 'w') as f:
    json.dump(data, f)
