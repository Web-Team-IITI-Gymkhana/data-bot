import json
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('../serviceAccount.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

<<<<<<< HEAD
# all collections
# for doc in db.collections():
#     print(u'{}'.format(doc.id))

myCollection = db.collection("company")
company_list = []
for doc in myCollection.stream():
    company_list.append(doc.id)
    # print(u'{} => {}'.format(doc.id, doc.to_dict()))
    
print("company_list cik numbers:")
print(company_list)

# all documents.collections
count_to_display = 3
for cik in company_list:
    if count_to_display == 0: break
    for date in ("2021", "2020"):
        x = myCollection.document(cik).collection("10k").document(date).get()
        cur = x.to_dict()
        keys = x.to_dict().keys()
        print(f"{cik} + {date} has MarketableSecurities: {cur['MarketableSecurities']}")
        prevDate = int(date) - 1
        try:
            y = myCollection.document(cik).collection("10k").document(prevDate).get()
        except:
            y = x
        prev = y.to_dict()

        # use cur and prev to get ratios and label company

    count_to_display -= 1

print(keys)





'''
parameters in firebase
dict_keys(['MRR', 
'TotalOperatingExpenses', 
'SalesCost', 
'MarketableSecurities', 
'Non-GAAPEarnings', 
'GAAPRevenue', 
'CustomerChurn', 
'CostOfSales', 
'SharesOutstanding', 
'Revenues', 
'NetOperatingExpenses', 
'StockPrice', 
'TotalPropertyAndEquipment', 
'RecurringRevenue', 
'ARR', 
'Inventories', 
'CustomerAcquisitionCosts', 
'SubscriberChurn', 
'OperatingIncome', 
'EBITDA', 
'SubscriptionRevenue', 
'RevenueChurn', 
'GrossProfit'])
'''

'''
Needed
"2020_3": {
        "CashAndCashEquivalents": 730506000.0,
        "MarketableSecurities": 1141425000.0,
        "TotalCurrentAssets": 2624276000.0,
        "TotalAssets": 3050311000.0,
        "PropertyAndEquipmentNet": 108077000.0,
        "Goodwill": 24340000.0,
        "TotalCurrentLiabilities": 1413948000.0,
        "SharesOutstanding": 198179809.0,
        "TotalStockholdersEquity": 1499918000.0,
        "TotalEquity": 3050311000.0,
        "GrossProfit": 1214178000.0,
        "TotalOperatingExpenses": 810447000.0,
        "NetIncome": 411706000.0,
        "GrossPropertyAndEquipment": 151727000.0,
        "StockPrice": "NaN",
        "SalesAndMarketing": 470886000.0,
        "TotalDebt": "NaN",
        "Revenues": 1768883000.0,
        "CostOfSales": 554705000.0,
        "OperatingIncome": 403731000.0,
        "NetLoss": "NaN",
        "RecurringRevenue": "NaN",
        "ARR": "NaN",
        "GAAPRevenue": "NaN",
        "NonGAAPEarnings": "NaN",
        "MRR": "NaN",
        "date": "2020-12-04",
        "doc_url": "https://www.sec.gov/Archives/edgar/data/1585521/000158552120000299/zm-20201031.htm"
    },
'''
=======
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
>>>>>>> 8fedaacc13dd12d2147e5c676b2107e3badf8a30
