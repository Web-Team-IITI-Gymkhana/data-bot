# A better way of getting all the records in Pandas DataFrame

from doctest import master
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
import pandas as pd


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
    cwd = os.getcwd()
    cdir = os.path.join(cwd,'data\\{}'.format(cik))
    tcdir = os.path.join(cwd,'data\\{}\\{}'.format(cik,type))
    if not os.path.exists(cdir):
        os.makedirs(cdir)
    if not os.path.exists(tcdir):
        os.makedirs(tcdir)
    response = requests.get(url = endpoint, params = param, headers=headers)
    with open("./data/{}/{}.xml".format(cik,type),'w') as f:
        f.write(response.text)
    tree = ET.parse("./data/{}/{}.xml".format(cik,type))
    root = tree.getroot()
    for child in root.findall("{http://www.w3.org/2005/Atom}entry"):
        accn = (child.find("{http://www.w3.org/2005/Atom}content")).find("{http://www.w3.org/2005/Atom}accession-number").text
        gen_url = base_url + "{}/{}/".format(cik,accn.replace("-",""))
        xml_summary = gen_url + "FilingSummary.xml"
        content = requests.get(xml_summary, headers=headers).content
        soup = BeautifulSoup(content, 'lxml')

        reports = soup.find('myreports')
        master_reports = []

        for report in reports.find_all('report')[:-1]:
            report_dict = {}
            report_dict['name_short'] = report.shortname.text
            report_dict['name_long'] = report.longname.text
            report_dict['position'] = report.position.text
            report_dict['category'] = report.menucategory.text
            report_dict['url'] = gen_url + report.htmlfilename.text

            master_reports.append(report_dict)
#             print('-'*100)
#             print(gen_url + report.htmlfilename.text)
#             print(report.longname.text)
#             print(report.shortname.text)
#             print(report.menucategory.text)
#             print(report.position.text)
    return master_reports


def get_sheet(stype):
    reps = get_data(1108524, "10-K", "20210204", "20220202")
    for i in reps:
        if i["name_short"]==stype:
            statement_data = {}
            statement_data['headers'] = []
            statement_data['sections'] = []
            statement_data['data'] = []

            content = requests.get(i["url"], headers=headers).content
            bs_table = BeautifulSoup(content)
            print(i["url"])
            for index, row in enumerate(bs_table.table.find_all('tr')):

                cols = row.find_all('td')
        
                if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0): 
                    reg_row = [ele.text.strip() for ele in cols]
                    statement_data['data'].append(reg_row)
            
                elif (len(row.find_all('th')) == 0 and len(row.find_all('strong')) != 0):
                    sec_row = cols[0].text.strip()
                    statement_data['sections'].append(sec_row)
            
                elif (len(row.find_all('th')) != 0):            
                    hed_row = [ele.text.strip() for ele in row.find_all('th')]
                    statement_data['headers'].append(hed_row)
            
                else:            
                    print('We encountered an error.')

    df = clean_df(statement_data)
    print(df)

def clean_df(data):
    df = pd.DataFrame(data['data'])
    df.index = df[0]
    df = df.drop(0, axis=1)
    df = df.replace('[\$,)]','', regex=True )\
                     .replace( '[(]','-', regex=True)\
                     .replace( '', 'NaN', regex=True)
    df = df.astype(float)
    df.columns = data['headers'][0][1:]
    return df

get_sheet("Consolidated Balance Sheets")