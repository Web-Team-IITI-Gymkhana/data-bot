import scrape_text
import pandas as pd
import json
companies = pd.read_csv("GoodCom.csv")
ciks = companies["CIK"].astype(int).tolist()

years = [2022,2021]
months = ["01","03","06","09","12"]

data_10k_text = dict()

for cik in ciks[0:1]:
    year_dict = dict()
    for year in years[0:1]:
        try:
            year_data = scrape_text.get_scrape_text(cik,"10-K",f"{year-1}0101",f"{year}0101")
            year_dict[year] = year_data
        except:
            continue
    data_10k_text[cik] = year_dict
with open("data_10k_text.json", 'w') as f:
    json.dump(data_10k_text, f,indent=4)

data_10q_text = dict()

for cik in ciks[0:1]:
    year_dict = dict()
    for year in years[0:1]:
        for i in range(len(months)-1):
            try:
                quarter_data = scrape_text.get_scrape_text(cik,"10-Q",f"{year-1}" + months[i] +"01",f"{year-1}" + months[i+1] +"01")
                year_dict["Y"+str(year)+" Q"+str(i+1)] = quarter_data
            except:
                continue
    data_10q_text[cik] = year_dict
    
with open("data_10q_text.json", 'w') as f:
    json.dump(data_10q_text, f,indent=4)
