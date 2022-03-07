import pandas as pd
import scrape_table

companies = pd.read_csv("CIK_278.csv")
companies = companies.dropna()

ciks = companies["CIK"].astype(int).tolist()

for cik in ciks:
    try:
        df = scrape_table.get_sheet(cik,"10-K","20200101", "20210101")
        df.to_csv("./results/{}.csv".format(str(cik)+" 10-K"),index=False)
    except:
        continue

for cik in ciks:
    try:
        df = scrape_table.get_sheet(cik,"10-Q","20200101", "20210101")
        df.to_csv("./results/{}.csv".format(str(cik) + " 10-Q"),index=False)
    except:
        continue

print("Done with bulk scraping")