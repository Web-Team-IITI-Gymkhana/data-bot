from cgitb import text
from operator import mod
from telnetlib import EC
from bs4 import BeautifulSoup
import urllib3
import re
import requests
import xml.etree.ElementTree as ET

mod_to_orig = {
    'Marketable securities': 'MarketableSecurities', 
    'Inventories': 'Inventories',
    'shares outstanding':'SharesOutstanding',
    'Stock Price':'StockPrice',
    'Sales Cost':'SalesCost', 
    'Subscription Revenue' : 'SubscriptionRevenue',
    'total operating expenses': 'TotalOperatingExpenses', 
    'customer acquisition costs': 'CustomerAcquisitionCosts', 
    'Customer churn': 'CustomerChurn', 
    'revenue churn': 'RevenueChurn', 
    'Revenues': 'Revenues', 
    'Gross profit': 'GrossProfit', 
    'MRR': 'MRR', 
    'Total property and equipment': 'TotalPropertyAndEquipment', 
    'net operating expenses': 'NetOperatingExpenses', 
    'cost of sales': 'CostOfSales', 
    'subscriber churn': 'SubscriberChurn', 
    'GAAP Revenue': 'GAAPRevenue', 
    'EBITDA': 'EBITDA',
    'Non-GAAP Earnings': 'Non-GAAPEarnings', 
    'Recurring Revenue': 'RecurringRevenue',
    'operating income': 'OperatingIncome',
    'ARR': 'ARR'}

sentiment_features = ('$','%','unit','ten','hundred','thousand','million','billion','revenue','loss','profit',
                        'growth','potential','income','percent','customer')

headers = {
    'user-agent': 'Sample @ <sample@sample.com>',
    'host': 'www.sec.gov'
}

def get_scrape_text(cik, form, datea, dateb):
    final_sentences = []

    endpoint = "https://www.sec.gov/cgi-bin/browse-edgar"
    base_url = "https://www.sec.gov/Archives/edgar/data/"
    param = {'action': 'getcompany',
            'CIK': cik,
            'type': form,
            'dateb': dateb,
            'datea': datea,
            'owner': 'exclude',
            'output': 'atom',
            'count': '100',
            }
    response = requests.get(url=endpoint, params=param, headers=headers)
    tree = ET.ElementTree(ET.fromstring(response.text))
    root = tree.getroot()
    for child in root.findall("{http://www.w3.org/2005/Atom}entry"):
        try:   
            accn = (child.find("{http://www.w3.org/2005/Atom}content")
                    ).find("{http://www.w3.org/2005/Atom}accession-number").text
            gen_url = base_url + "{}/{}/".format(cik, accn.replace("-", ""))
            xml_summary = gen_url + "FilingSummary.xml"
            content = requests.get(xml_summary, headers=headers).content
            soup = BeautifulSoup(content, features='lxml')
            reports = soup.find('inputfiles')
            file_name = (reports.find_all("file", attrs={"doctype": form})[0]).text
            doc_url = gen_url + file_name
            http = urllib3.PoolManager()
            req = http.request("GET",doc_url,headers=headers)
            docsoup = BeautifulSoup(req.data, features='lxml')

            text_tags = docsoup.find_all(["span", "p","font","li"])
            anchor_tags = docsoup.find_all(["a"])


            for tag in text_tags:  
                try:
                    txt = tag.text.lower()
                    
                    if len(txt.split(' '))<=5:
                        continue

                    valid = False
                    for feature in sentiment_features:
                        if feature in txt:
                            valid = True
                            break

                    if 'check mark' in txt:
                        valid = False
                    
                    if valid==True:
                        txt = txt.encode("utf-8")
                        txt = txt.decode("utf-8","ignore")
                        final_sentences.append(txt)
                        # print(txt)
                except Exception as e:
                    continue

            for anchor_tag in anchor_tags:
                try:
                    txt = anchor_tag.text.lower()
                    if ('press' in txt) and ('release' in txt):
                        press_release_filename = anchor_tag['href']
                        press_release_url = gen_url + press_release_filename
                        pr_req = http.request("GET",press_release_url,headers=headers)
                        press_release_docsoup = BeautifulSoup(pr_req.data, features='lxml')
                        press_release_text_tags = press_release_docsoup.find_all(["span", "p","font","li"])

                        for tag in press_release_text_tags:
                            
                            txt = tag.text.lower()

                            if len(txt.split(' '))<=5:
                                continue

                            valid = False
                            for feature in sentiment_features:
                                if feature in txt:
                                    valid = True
                                    break

                            if 'check mark' in txt:
                                valid = False
                            
                            if valid==True:
                                txt = txt.encode("utf-8")
                                txt = txt.decode("utf-8","ignore")
                                final_sentences.append(txt)
                                # print(txt)
                except Exception as e:
                    continue

        except Exception as e:
            continue

    return final_sentences

# get_scrape_text(1459417,"8-K","20210101","20220101")