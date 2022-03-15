import json
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('../serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def load_forms():
    for form_type in ("10k","10q"):
        with open(f"json/data_{form_type}_text(dummy).json") as f:
            data = json.load(f)

        for cik in data:
            for year in data[cik]:
                print(f"pushed company {cik}, year {year}")

def load_company():
    with open(f"json/data_10k_table(dummy).json") as f:
        data = json.load(f)

        for cik in data:
            add_company(cik)
            print(f"pushed company {cik}")

load_company()