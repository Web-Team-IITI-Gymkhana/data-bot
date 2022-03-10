# A better way of getting all the records in Pandas DataFrame
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import pandas as pd
import re

features = [
    "Cash equivalents",
    "Marketable securities",
    "Inventories",
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
    "churn",
    "GAAP Revenue",
    "EBITDA",
    "Non-GAAP Earnings"
]

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
            for feature in features:
                
                try:
                    feature = feature.lower()
                    featureWords = feature.split(" ")

                    flag = True
                    for word in featureWords:
                        if word not in tr_text:
                            flag = False
                            break
                    if flag==True:
                        tds = tr.find_all('td')
                        val_list = []
                        if len(tds[1].text) < 20:
                            td_text = tds[1].text.replace(",","")
                            match_str = re.findall('([0-9\.\(\)]+)',td_text)
                            if len(match_str) != 0:
                                val_list.append(match_str[0])
                        if len(val_list)>0:
                            feature_dict[tds[0].text+" table = "+table['name_short']]=float(val_list[0])*multiplier

                except:
                    continue
                
            
    df = pd.DataFrame(list(feature_dict.items()),columns=['Feature','Values'])
    return df

#print(get_sheet(1459417,"10-K","20210101", "20220101"))
# print(feature_dict)