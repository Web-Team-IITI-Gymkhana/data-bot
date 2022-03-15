import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import pandas as pd
import re


mod_features = [
    "Cash equivalents",
    "Marketable securities",
    "Inventories",
    "Common stock",
    "Total Stockholders Equity",
    "Stock Price",
    "Total costs expenses",
    "Sales Cost",
    "Marketing Cost",
    "Subscription Revenue",
    "Property equipment",
    "Gross property equipment",
    "Total current assets",
    "Total assets",
    "Total current liabilities",
    "Total equity",
    "Total debt",
    "total operating expenses",
    "customer acquisition costs",
    "Customer churn",
    "revenue churn",
    "net income",
    "Revenues",
    "Gross profit",
    "Net loss",
    "MRR",
    "goodwill",
    "Total property and equipment",
    "net operating expenses",
    "cost of sales",
    "subscriber churn",
    "GAAP Revenue",
    "EBITDA",
    "Non-GAAP Earnings",
    "Recurring Revenue",
    "operating income",
    "shares outstanding",
]

mod_to_orig = {
    'Cash equivalents': 'CashAndCashEquivalents', 
    'Marketable securities': 'MarketableSecurities', 
    'Inventories': 'Inventories',
    'Common stock' : 'CommonStock',
    'Total Stockholders Equity':'TotalStockholdersEquity',
    'Stock Price':'StockPrice',
    'Total costs expenses':'TotalCostsAndExpenses',
    'Sales Cost':'SalesCost', 
    'Marketing Cost' : 'MarketingCost',
    'Subscription Revenue' : 'SubscriptionRevenue',
    'Property equipment': 'PropertyAndEquipmentNet', 
    'Gross property equipment': 'GrossPropertyAndEquipment', 
    'Total current assets': 'TotalCurrentAssets', 
    'Total assets': 'TotalAssets', 
    'Total current liabilities': 'TotalCurrentLiabilities', 
    'Total equity': 'TotalEquity', 
    'Total debt': 'TotalDebt', 
    'total operating expenses': 'TotalOperatingExpenses', 
    'customer acquisition costs': 'CustomerAcquisitionCosts', 
    'Customer churn': 'CustomerChurn', 
    'revenue churn': 'RevenueChurn', 
    'net income': 'NetIncome', 
    'Revenues': 'Revenues', 
    'Gross profit': 'GrossProfit', 
    'Net loss': 'NetLoss', 
    'MRR': 'MRR', 
    'goodwill': 'Goodwill', 
    'Total property and equipment': 'TotalPropertyAndEquipment', 
    'net operating expenses': 'NetOperatingExpenses', 
    'cost of sales': 'CostOfSales', 
    'subscriber churn': 'SubscriberChurn', 
    'GAAP Revenue': 'GAAPRevenue', 
    'EBITDA': 'EBITDA',
    'Non-GAAP Earnings': 'Non-GAAPEarnings', 
    'Recurring Revenue': 'RecurringRevenue',
    'operating income': 'OperatingIncome',
    'shares outstanding':'SharesOutstanding'}


headers = {
    'user-agent': 'Sample @ <sample@sample.com>',
    'host': 'www.sec.gov'
}

def get_data(cik, type, datea, dateb):
    endpoint = "https://www.sec.gov/cgi-bin/browse-edgar"
    base_url = "https://www.sec.gov/Archives/edgar/data/"
    param = {'action': 'getcompany',
             'CIK': cik,
             'type': type,
             'dateb': dateb,
             'datea': datea,
             'owner': 'exclude',
             'output': 'atom',
             'count': '100',
             }
    response = requests.get(url=endpoint, params=param, headers=headers)
    tree = ET.ElementTree(ET.fromstring(response.text))
    root = tree.getroot()
    master_reports = []
    for child in root.findall("{http://www.w3.org/2005/Atom}entry"):
        accn = (child.find("{http://www.w3.org/2005/Atom}content")
                ).find("{http://www.w3.org/2005/Atom}accession-number").text
        gen_url = base_url + "{}/{}/".format(cik, accn.replace("-", ""))
        xml_summary = gen_url + "FilingSummary.xml"
        content = requests.get(xml_summary, headers=headers).content
        soup = BeautifulSoup(content, 'lxml')

        reports = soup.find('myreports')
        

        for report in reports.find_all('report')[:-1]:
            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['url'] = gen_url + report.htmlfilename.text

            shortname = report_dict['name_short']
            shortname = shortname.lower()

            if 'summary' in shortname:
                continue

            master_reports.append(report_dict)
    return master_reports


def get_sheet(cik, form, datea, dateb):
    feature_dict = dict()

    list_tables = get_data(cik, form, datea, dateb)
    
    for table in list_tables:

        content = requests.get(table["url"], headers=headers).content
        bs_table = BeautifulSoup(content, features='lxml')
        trs = bs_table.table.find_all('tr')

        multiplier = 1

        for tr in trs:
            
            tr_text = tr.text.lower()

            if "million" in tr_text:
                multiplier = 1000000
            elif "billion" in tr_text:
                multiplier = 1000000000
            elif "thousand" in tr_text:
                multiplier = 1000
            elif "hundred" in tr_text:
                multiplier = 100

            for mod_feature in mod_features:

                orig_feature = mod_to_orig[mod_feature]

                try:
                    mod_feature = mod_feature.lower()
                    featureWords = mod_feature.split(" ")

                    flag = True
                    for word in featureWords:
                        if word not in tr_text:
                            flag = False
                            break
                    
                    if orig_feature=="NetIncome":
                        ind1 = tr_text.find("net")
                        ind2 = tr_text.find("income")

                        if ind1>ind2:
                            flag = False
                            

                    if flag==True:
                        
                        tds = tr.find_all('td')
                        
                        found = False
                        
                        for td in tds[1:5]:

                            val_list = []

                            if found:
                                break

                            if len(td.text) < 25:
                                td_text = td.text.replace(",","")
                                match_str = re.findall('([0-9\.\(\)\,]+)',td_text)
                                if len(match_str) != 0:
                                    val_list.append(match_str[0])
                                
                                    
                            if len(val_list)>0:
                                if val_list[0][0]=='(':
                                    if val_list[0][-1]==')':
                                        val_list[0]=val_list[0][1:-1]
                                    else:
                                        val_list[0]=val_list[0][1:]
                                    val_list[0] = '-' + val_list[0]
                                val_list[0] = val_list[0].replace(",", "")
                                if orig_feature=='SharesOutstanding' or orig_feature=='CommonStock' :
                                    feature_dict[orig_feature] = feature_dict.get(orig_feature,float(val_list[0]))
                                else:
                                    feature_dict[orig_feature] = feature_dict.get(orig_feature,float(val_list[0])*multiplier)
                                found = True
                            
                except Exception as e:
                    print("Exception in scrape_table ",e)
                    continue

    for orig_feature in mod_to_orig.values():
        feature_dict[orig_feature] = feature_dict.get(orig_feature,"NaN")
                
            
    return feature_dict
