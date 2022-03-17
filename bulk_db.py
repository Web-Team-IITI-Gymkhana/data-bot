import firebase_admin
from firebase_admin import credentials, firestore
import json
import pandas as pd
import scrape
import time

start_time = time.time()

df = pd.read_csv('./csv/GoodCom.csv', index_col="CIK")
ciks = df.index.tolist()

token = "sass-db-firebase-adminsdk-4gh5l-4b1dd3dc87.json"
cred = credentials.Certificate(token)
firebase_admin.initialize_app(cred)
db = firestore.client()

with open('8K_Text_Sentiment.json', 'r') as f:
        data_8k = json.load(f)

def bulk():
    for cik in ciks[2:10]:
        data = scrape.get_data(cik)
        _10k = data.pop("_10k")
        _10q = data.pop("_10q")
        meta = data

        if meta['CompanyName'] == 'NaN':
            meta['CompanyName'] = df.loc[cik]["CompanyName"]
        
        db.collection("company").document(str(cik)).set(meta)

        for filing10k in _10k.keys():
            db.collection("company").document(str(cik)).collection("_10k").document(filing10k).set(_10k[filing10k])
        for filing10q in _10q.keys():
            db.collection("company").document(str(cik)).collection("_10q").document(filing10q).set(_10q[filing10q])  

        if str(cik) in data_8k.keys():
            for year in data_8k[str(cik)].keys():
                db.collection("company").document(str(cik)).collection("_8k").document(str(year)).set(data_8k[str(cik)][year])
        print(f"{cik} DONE")

bulk()

print(f"It took : {time.time()-start_time} seconds")