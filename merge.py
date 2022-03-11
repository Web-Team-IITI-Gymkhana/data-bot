import json

table_data = {
    "123" : {
        "2021" : {
            "f1" : 23,
            "f2" : "NaN",
            "f3" : 100
        },
        "2022" : {
            "f1" : "NaN",
            "f2" : "NaN",
            "f3" : "NaN"
        }
    }
}

text_data = {
    "123" : {
        "2021" : {
            "f1" : 24,
            "f2" : 500,
            "f3" : "NaN"
        },
        "2022" : {
            "f1" : "NaN",
            "f2" : 50,
            "f3" : 100
        }
    }
}

years = ["2022","2021"]

features = ("f1","f2","f3")

# features = ("EBITDA","ARR","MRR",
#             "Marketable securities",
#             "Inventories",
#             "Stock Price",
#             "Total costs and expenses",
#             "Marketing Cost",
#             "Subscription Revenue",
#             "Gross property and equipment",
#             "Total debt",
#             "customer acquisition costs",
#             "Customer churn",
#             "revenue churn",
#             "Revenues",
#             "Total property and equipment",
#             "net operating expenses",
#             "subscriber churn",
#             "GAAP Revenue",
#             "Non-GAAP Earnings",
#             "Recurring Revenue",
#             "operating income")


ciks = table_data.keys()

for cik in ciks:
    try:
        table_company = table_data[cik]
        text_company = text_data[cik]

        for year in years:
            table_year = table_company[year]
            text_year = text_company[year]

            for feature in features:
                if table_year[feature]=="NaN":
                    table_data[cik][year][feature] = text_year[feature]
    except:
        continue

with open("data_10k.json", 'w') as f:
    json.dump(table_data, f,indent=4)
    
