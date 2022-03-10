import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import pandas as pd

companies = pd.read_csv("CIK_278.csv")
companies = companies.dropna()

headers = {
    'user-agent': 'Sample @ <sample@sample.com>',
    'host': 'www.sec.gov'
}

company_dict = companies.set_index("CIK").T.to_dict()

bad_company_dict = dict()
good_company_dict = dict()

def get_data(cik, type, datea, dateb):
    endpoint = "https://www.sec.gov/cgi-bin/browse-edgar"
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
    if len(root.findall("{http://www.w3.org/2005/Atom}entry")) == 0:
        return True
    else:
        return False

for cik in list(company_dict.keys()):
    if get_data(int(cik), "10-K", "20200101", "20220303"):
        bad_company_dict[cik] = company_dict[cik]['CompanyName']
    else:
        good_company_dict[cik] = company_dict[cik]['CompanyName']

good_company_df = pd.DataFrame(good_company_dict.items(),columns=["CIK","CompanyName"])
good_company_df = good_company_df.set_index("CIK")
good_company_df.to_csv("GoodCom.csv")

bad_company_df = pd.DataFrame(bad_company_dict.items(),columns=["CIK","CompanyName"])
bad_company_df = bad_company_df.set_index("CIK")
bad_company_df.to_csv("BadCom.csv")