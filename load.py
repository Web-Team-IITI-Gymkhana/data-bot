import json
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_form(cik, form_type, form_uid, data):
    db.collection("company").document(cik).collection(form_type).document(form_uid).set(data)

def add_company(cik,data):
    db.collection("company").document(cik).set(data)

for form_type in ("10k","10q"):
    with open(f"json/data_{form_type}_text(dummy).json") as f:
        data = json.load(f)

    for cik in data:
        for year in data[cik]:
            add_form(cik,form_type,year,data[cik][year])
            print(f"pushed company {cik}, year {year}")
