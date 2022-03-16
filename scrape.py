import scrape_utils
from bs4 import BeautifulSoup
import urllib3
import time

start_time = time.time()

http = urllib3.PoolManager()

headers = {
    'user-agent': 'Sample @ <sample@sample.com>',
    'host': 'www.sec.gov'
}

def get_data(cik):
    meta_data = scrape_utils.get_metadata(cik)
    years = [2021,2020,2019]
    stock_prices = scrape_utils.get_all_stock_price(cik)
    forms = {"10-K": "_10k", "10-Q" : "_10q"}
    form_data = dict()
    for form in forms.keys():
        year_wise_data = dict()
        for year in years:
            try:
                accn_date_list = scrape_utils.get_accn(cik, form, year)
                quarter = 3
                for accn, date in accn_date_list:
                    data = dict()
                    complete_data = dict()
                    try:
                        data["FilingDate"] = date

                        data["DocURL"], filing_data = scrape_utils.get_doc_url(cik, accn, form)

                        req = http.request("GET",data["DocURL"],headers=headers)
                        doc_soup = BeautifulSoup(req.data, features='lxml')
                        
                        table_data = scrape_utils.get_table_data(doc_soup, year, form)
                        text_data = scrape_utils.get_text_data(doc_soup)
                        
                        if table_data['StockPrice'] == "NaN":
                            if form == "10-K":
                                for stock_date in stock_prices.keys():
                                    if stock_date.split("-")[1] == '01' and stock_date.split("-")[0] == str(year+1):
                                        table_data['StockPrice'] = float(stock_prices[stock_date]['4. close'])
                                        break
                            elif form == "10-Q":
                                stock_quarter = ["04", "07", "10"]
                                for stock_date in stock_prices.keys():
                                    if stock_date.split("-")[1] == stock_quarter[quarter-1] and stock_date.split("-")[0] == str(year):
                                        table_data['StockPrice'] = float(stock_prices[stock_date]['4. close'])
                                        break

                        data = {**table_data, **text_data, **data}
                        complete_data["features"] = data
                        complete_data["sec_filing"] = filing_data

                        if form=="10-Q":
                            year_wise_data[f"{year}_{quarter}"] = complete_data
                            quarter -= 1 
                        else:
                            year_wise_data[f"{year}"] = complete_data
                        print(f"ACCN:{accn}, FORM: {form}, YEAR: {year}, CIK: {cik} DONE")
                    except: continue  
            except: continue
        form_data[forms[form]] = year_wise_data

    companies_data = {**meta_data, **form_data}
    return companies_data