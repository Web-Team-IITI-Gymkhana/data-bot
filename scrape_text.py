from bs4 import BeautifulSoup
import urllib3
import re
import requests
import xml.etree.ElementTree as ET

features = ("gaap","loss","profit","gross","margin")

headers = {
    'user-agent': 'Sample @ <sample@sample.com>',
    'host': 'www.sec.gov'
}

feature_dict = dict()

def scrape_text(cik, form, datea, dateb):
    endpoint = "https://www.sec.gov/cgi-bin/browse-edgar"
    base_url = "https://www.sec.gov/Archives/edgar/data/"
    param = {'action': 'getcompany',
            'CIK': cik,
            'type': "10-K",
            'dateb': "20220101",
            'datea': "20210101",
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
        soup = BeautifulSoup(content, features='lxml')
        reports = soup.find('inputfiles')
        file_name = (reports.find_all("file", attrs={"doctype": "10-K"})[0]).text
        doc_url = gen_url + file_name
        http = urllib3.PoolManager()
        req = http.request("GET",doc_url,headers=headers)
        docsoup = BeautifulSoup(req.data, features='lxml')
        data = docsoup.find_all(["span", "p"])
        for feature in features:
            value = []
            final_values = []
            for i in data:
                regex_string = '.*\s{}'.format(feature)
                feature_match = re.findall(regex_string,i.text.lower())
                if len(feature_match)!=0 and '$' in feature_match[0]:
                    x = feature_match[0].strip()
                    lines = x.split(". ")
                    if len(lines)==1:
                        for i in lines:
                            if feature in i:
                                match = re.findall('\$([0-9\.]*)\s(billion|million|thousand|hundred)', i)
                                if len(match)>0:
            #                         print(match[0][0], "\n")
                                    value.append(f'{match[0][0]} {match[0][1]}')
                    else:
                        for i in lines:
                            if feature in i:
                                match = re.findall('\$([0-9\.]*)\s(billion|million|thousand|hundred)', i)
                                if len(match)>0:
            #                         print(match[0][0])
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
                feature_dict[feature] = list(final_values)[0]
            elif len(final_values)>1:
                feature_dict[feature] = max(list(final_values))

    return feature_dict
print(scrape_text(1459417,"10-K","20210101", "20220101"))