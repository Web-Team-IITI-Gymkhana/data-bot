import pandas as pd
import scrape_table
import json

companies = pd.read_csv("GoodCom.csv")

ciks = companies["CIK"].astype(int).tolist()

years = [2022,2021]
months = ["01","03","06","09","12"]

data_10k_table = dict()

for cik in ciks:
    year_dict = dict()
    for year in years:
        try:
            year_data = scrape_table.get_sheet(cik,"10-K",f"{year-1}0101",f"{year}0101")
            year_dict[year-1] = year_data
        except:
            continue
    data_10k_table[cik] = year_dict
    
with open("data_10k_table.json", 'w') as f:
    json.dump(data_10k_table, f , indent=4)


data_10q_table = dict()

for cik in ciks:
    year_dict = dict()
    for year in years:
        for i in range(len(months)-1):
            try:
                quarter_data = scrape_table.get_sheet(cik,"10-Q",f"{year-1}" + months[i] +"01",f"{year-1}" + months[i+1] +"01")
                year_dict["Y"+str(year-1)+" Q"+str(i+1)] = quarter_data
            except:
                continue
    data_10q_table[cik] = year_dict
    
with open("data_10q_table.json", 'w') as f:
    json.dump(data_10q_table, f,indent=4)

print("Done with bulk scraping")
