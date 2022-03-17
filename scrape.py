import scrape_utils
from bs4 import BeautifulSoup
import urllib3
from dateutil import parser

http = urllib3.PoolManager()

headers = {
    'user-agent': 'Sample @ <sample@sample.com>',
    'host': 'www.sec.gov'
}

def get_data(cik):
    meta_data, stock_prices = scrape_utils.get_meta_stock(cik)
    years = [2021,2020,2019]
    forms = {"10-K": "_10k", "10-Q" : "_10q"}
    form_data = dict()
    for form in forms.keys():
        try:
            year_wise_data = dict()
            for year in years:
                try:
                    accn_date_list = scrape_utils.get_accn(cik, form, year)
                    quarter = 3
                    for accn, date in accn_date_list:
                        data = dict()
                        complete_data = dict()
                        try:
                            
                            complete_data["FilingDate"] = date
                            complete_data["DocURL"], filing_data = scrape_utils.get_doc_url(cik, accn, form)

                            req = http.request("GET",complete_data["DocURL"],headers=headers)
                            doc_soup = BeautifulSoup(req.data, features='lxml')
                            
                            filing_for_date_tag = doc_soup.find_all("ix:nonnumeric", {"name": "dei:DocumentPeriodEndDate"})
                            if len(filing_for_date_tag)>0:
                                try:
                                    date_text = filing_for_date_tag[0].text.replace("&nbsp;", " ")
                                    complete_data["FilingForDate"] = parser.parse(date_text).strftime('%Y-%m-%d')
                                    table_data = scrape_utils.get_table_data(doc_soup, year, form, complete_data["FilingForDate"])
                                except:
                                    complete_data["FilingForDate"] = filing_for_date_tag[0].text
                                    table_data = scrape_utils.get_table_data(doc_soup, year, form)
                            else:
                                complete_data["FilingForDate"] = "NaN"
                                table_data = scrape_utils.get_table_data(doc_soup, year, form)
                            
                            text_data = scrape_utils.get_text_data(doc_soup)

                            if table_data['StockPrice'] == "NaN" and bool(stock_prices):
                                if form == "10-K":
                                    for stock_date in stock_prices.keys():
                                        try:
                                            if stock_date.split("-")[1] == '01' and stock_date.split("-")[0] == str(year+1):
                                                table_data['StockPrice'] = float(stock_prices[stock_date]['4. close'])
                                                break
                                        except: continue
                                elif form == "10-Q":
                                    stock_quarter = ["04", "07", "10"]
                                    for stock_date in stock_prices.keys():
                                        try:
                                            if stock_date.split("-")[1] == stock_quarter[quarter-1] and stock_date.split("-")[0] == str(year):
                                                table_data['StockPrice'] = float(stock_prices[stock_date]['4. close'])
                                                break
                                        except: continue

                            data = {**table_data, **text_data, **data}
                            complete_data["features"] = data
                            complete_data["sec_filing"] = filing_data
                            
                            if complete_data["FilingForDate"] != "NaN":
                                key = complete_data["FilingForDate"]
                                year_wise_data[f"{key}"] = complete_data
                            elif complete_data["FilingDate"] != "NaN":
                                complete_data["FilingDate"]
                                year_wise_data[f"{key}"] = complete_data
                            else:
                                if form=="10-Q":
                                    year_wise_data[f"{year}_{quarter}"] = complete_data
                                    quarter -= 1 
                                else:
                                    year_wise_data[f"{year}"] = complete_data
                            print(f"ACCN:{accn}, FORM: {form}, YEAR: {year}, CIK: {cik} DONE")
                        except: continue  
                except: continue
            form_data[forms[form]] = year_wise_data
        except: continue
    companies_data = {**meta_data, **form_data}
    return companies_data

# import json
# with open("trynew3.json", "w") as f:
#     json.dump(get_data(796343), f, indent=4)