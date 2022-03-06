import pandas as pd
import scrape_table

companies = pd.read_csv("CIK_278.csv")
companies = companies.dropna()

ciks = companies["CIK"].astype(int).tolist()

for i in ciks[0:1]:
    try:
        df = scrape_table.get_sheet(i,"10-K","20210101", "20220101")
        df.to_csv("./data/{}.csv".format(i))
    except:
        continue