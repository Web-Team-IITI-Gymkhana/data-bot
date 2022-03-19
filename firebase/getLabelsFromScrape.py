import json
import firebase_admin
import pandas as pd
from firebase_admin import credentials, firestore
from scrape import get_data

# this file gets filing by data scraping and generate data file for ml

import access_util as au
epsilon = 1e-20

cred = credentials.Certificate('../serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

myCollection = db.collection("company")
company_list = []
for doc in myCollection.stream():
    company_list.append(doc.id)

# cik list from csv    
comps = pd.read_csv('..\csv\GoodCom.csv')
company_list = comps['CIK'].to_numpy().astype('int').astype('str')

print("company_list cik numbers:")
print(company_list)

# all documents.collections
count_to_display = 1000
netcsv = []
netvalues = []
for cik in company_list:
    if count_to_display == 0: break
    for date in ("2021", "2020"):
        print(f"year: {date}, cik = {cik}")
        try:
            x = get_data(cik, "10-K", int(date))
            cur = x[(date)]
            keys = x.keys()
            prevDate = int(date) - 1
            try:
                y = get_data(cik, "10-K", int(prevDate))
                prev = y[(prevDate)]
            except:
                y = x
                prev = y[(date)]
        except:
            continue
        # use cur and prev to get ratios and label company
        rf = au.ratios

        ratios, rato = rf.setup_ratios(cur, prev)

        ratiodf= pd.DataFrame(cur.items())
        ratiodf, ratiodf.columns= ratiodf.T, cur.keys()
        ratiodf.drop(index=ratiodf.index[0],axis=0, inplace=True)

        rider_provider = cik + '_' + date
        rato.insert(0,'rider_provider', rider_provider)
        rato.set_index('rider_provider')
        ratiodf.insert(0,'rider_provider', rider_provider)
        ratiodf.set_index('rider_provider')
        netcsv.append(rato)
        netvalues.append(ratiodf)

    count_to_display -= 1

result = pd.concat(netcsv)
result.to_csv("labels.csv", index = True) 

result = pd.concat(netvalues)
result.to_csv("data_values.csv", index = True) 
