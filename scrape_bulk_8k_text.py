import pandas as pd
import scrape_8k_text
import json
from textblob import TextBlob
import re

companies = pd.read_csv("./csv/GoodCom.csv")

ciks = companies["CIK"].astype(int).tolist()

json_file_name = "data_8k_text_mihir_1.json" #name of json file obtained from bulk scraping
lb = 130 #start of range
ub = -1 #end of range

years = [2022, 2021]

def mustHave(sentence):
    return (('0' in sentence) or ('1' in sentence) or ('2' in sentence) or
           ('3' in sentence) or ('4' in sentence) or ('5' in sentence) or
           ('6' in sentence) or ('7' in sentence) or ('8' in sentence) or 
           ('9' in sentence))

data_8k_text = dict()

for cik in ciks[lb:]:
    year_dict = dict()
    
    for year in years:
        try:
            paragraph = ""
            sentences = scrape_8k_text.get_scrape_text(cik, "8-K", f"{year-1}0101", f"{year}0101")
            chosen = []
            for sentence in sentences:
                result = TextBlob(sentence).sentiment
                subjectivity = result.subjectivity
                if subjectivity>=0.4 and mustHave(sentence):
                    sentence = sentence.capitalize()
                    chosen.append(sentence)
            
            chosen = list(set(chosen))
            year_dict[f"{year-1}" + " Sentences"] = chosen
        except Exception as e:
            print(e)
            continue
    print("cik ",cik," completed")
    data_8k_text[cik] = year_dict

with open(f"json/{json_file_name}", 'w') as f:
    json.dump(data_8k_text, f, indent=4)
