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

headers = {
    'user-agent': 'Sample @ <sample@sample.com>',
    'host': 'www.sec.gov'
}

def get_scrape_text(cik, form, datea, dateb):
    feature_dict = dict()
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
            data = docsoup.find_all(["span", "p"])
            for feature in mod_to_orig.keys():
                value = []
                final_values = []
                orig = feature
                feature = feature.lower()
                for i in data:
                    regex_string = '.*\s{}\s'.format(feature)
                    feature_match = re.findall(regex_string,i.text.lower())
                    if len(feature_match)!=0 and '$' in feature_match[0]:
                        x = feature_match[0].strip()
                        lines = x.split(". ")
                        if len(lines)==1:
                            for line in lines:
                                if feature in line:
                                    match = re.findall('\$([0-9\.]*)\s(billion|million|thousand|hundred)', line)
                                    if len(match)>0:
                                        value.append(f'{match[0][0]} {match[0][1]}')
                        else:
                            for line in lines:
                                if feature in line:
                                    match = re.findall('\$([0-9\.]*)\s(billion|million|thousand|hundred)', line)
                                    if len(match)>0:
                                        value.append(f'{match[0][0]} {match[0][1]}')

                for figure in value:
                    num, multiplier = figure.split(" ")
                    if multiplier == "billion":
                        num = float(num)*1000000000
                    elif multiplier == "million":
                        num = float(num)*1000000
                    elif multiplier == "thousand":
                        num = float(num)*1000
                    elif multiplier == "hundred":
                        num = float(num)*100
                    else:
                        num = float(num)
                    final_values.append(num)
                final_values=set(final_values)
                if len(final_values)==1:
                    feature_dict[mod_to_orig[orig]] = feature_dict.get(mod_to_orig[orig],list(final_values)[0])
                elif len(final_values)>1:
                    feature_dict[mod_to_orig[orig]] = feature_dict.get(mod_to_orig[orig],max(list(final_values)))
        except:
            continue
    for feature in mod_to_orig.keys():
        feature_dict[mod_to_orig[feature]] = feature_dict.get(mod_to_orig[feature],'NaN')

    return feature_dict
