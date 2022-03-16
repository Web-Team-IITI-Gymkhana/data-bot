import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import scrape

ciks = pd.read_csv('./csv/GoodCom.csv')["CIK"].astype(int).tolist()

token = "sass-db-firebase-adminsdk-4gh5l-4b1dd3dc87.json"
cred = credentials.Certificate(token)
firebase_admin.initialize_app(cred)
db = firestore.client()

def bulk():
    for cik in ciks:
        data = scrape.get_data(cik)
        _10k = data.pop("_10k")
        _10q = data.pop("_10q")
        meta = data
        
        db.collection("company").document(str(cik)).set(meta)

        for filing10k in _10k.keys():
            db.collection("company").document(str(cik)).collection("_10k").document(filing10k).set(_10k[filing10k])
        for filing10q in _10q.keys():
            db.collection("company").document(str(cik)).collection("_10q").document(filing10q).set(_10q[filing10q])  
        print(f"{cik} DONE")
bulk()