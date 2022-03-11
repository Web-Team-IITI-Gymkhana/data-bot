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
    "shares outstanding",
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
]

mod_to_orig = {
    'Cash equivalents': 'Cash and Cash equivalents', 
    'Marketable securities': 'Marketable securities', 
    'Inventories': 'Inventories',
    'Common stock' : 'Common stock',
    'shares outstanding':'shares outstanding',
    'Total Stockholders Equity':'Total Stockholders Equity',
    'Stock Price':'Stock Price',
    'Total costs expenses':'Total costs and expenses',
    'Sales Cost':'Sales Cost', 
    'Marketing Cost' : 'Marketing Cost',
    'Subscription Revenue' : 'Subscription Revenue',
    'Property equipment': 'Property and equipment net', 
    'Gross property equipment': 'Gross property and equipment', 
    'Total current assets': 'Total current assets', 
    'Total assets': 'Total assets', 
    'Total current liabilities': 'Total current liabilities', 
    'Total equity': 'Total equity', 
    'Total debt': 'Total debt', 
    'total operating expenses': 'total operating expenses', 
    'customer acquisition costs': 'customer acquisition costs', 
    'Customer churn': 'Customer churn', 
    'revenue churn': 'revenue churn', 
    'net income': 'net income', 
    'Revenues': 'Revenues', 
    'Gross profit': 'Gross profit', 
    'Net loss': 'Net loss', 
    'MRR': 'MRR', 
    'goodwill': 'goodwill', 
    'Total property and equipment': 'Total property and equipment', 
    'net operating expenses': 'net operating expenses', 
    'cost of sales': 'cost of sales', 
    'subscriber churn': 'subscriber churn', 
    'GAAP Revenue': 'GAAP Revenue', 
    'EBITDA': 'EBITDA',
    'Non-GAAP Earnings': 'Non-GAAP Earnings', 
    'Recurring Revenue': 'Recurring Revenue',
    'operating income': 'operating income'}


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

                    if flag==True:
                        
                        tds = tr.find_all('td')
                        
                        found = False

                        for td in tds[1:2]:

                            val_list = []

                            if found:
                                break

                            if len(td.text) < 25:
                                td_text = td.text.replace(",","")
                                match_str = re.findall('([0-9\.\(\)]+)',td_text)
                                if len(match_str) != 0:
                                    val_list.append(match_str[0])
                                    
                            if len(val_list)>0:
                                if val_list[0][0]=='(':
                                    if val_list[0][-1]==')':
                                        val_list[0]=val_list[0][1:-1]
                                    else:
                                        val_list[0]=val_list[0][1:]
                                    val_list[0] = '-' + val_list[0]
                                feature_dict[orig_feature] = feature_dict.get(orig_feature,float(val_list[0])*multiplier)
                                found = True
                            
                except Exception as e:
                    print("Exception in scrape_table ",e)
                    continue

    for orig_feature in mod_to_orig.values():
        feature_dict[orig_feature] = feature_dict.get(orig_feature,"NaN")
                
            
    df = pd.DataFrame(list(feature_dict.items()),columns=['Feature','Values'])
    return df

