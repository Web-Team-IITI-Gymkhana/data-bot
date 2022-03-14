from math import perm
import requests
import scrape_table
import scrape_text

quarters = [("0101", "0331"), ("0401", "0630"),
            ("0701", "0930"), ("1001", "1231")]


def get_10k(cik, year):
    year_table = scrape_table.get_sheet(
        cik, "10-K", f"{year}0101", f"{year+1}0101")
    year_text = scrape_text.get_scrape_text(
        cik, "10-K", f"{year}0101", f"{year+1}0101")
    for key in year_table.keys():
        if year_table[key] == 'NaN':
            if key in year_text.keys():
                year_table[key] = year_text[key]
    year_table["ARR"] = year_text["ARR"]
    return year_table


def get_10q(cik, year, quarter):
    quarter_table = scrape_table.get_sheet(
        cik, "10-Q", f"{year}"+quarters[quarter-1][0], f"{year}"+quarters[quarter-1][1])
    quarter_text = scrape_text.get_scrape_text(
        cik, "10-Q", f"{year}"+quarters[quarter-1][0], f"{year}"+quarters[quarter-1][1])
    for key in quarter_table.keys():
        try:
            if quarter_table[key] == 'NaN':
                if key in quarter_text.keys():
                    quarter_table[key] = quarter_text[key]
        except:
            continue
    quarter_table["ARR"] = quarter_text["ARR"]
    return quarter_table


def get_data(cik, form, year, quarter):
    if form == "10-K":
        return get_10k(cik, year)
    elif form == "10-Q":
        return get_10q(cik, year, quarter)


def get_metadata(cik):
    data = dict()
    token = "OPFbGvwobBxjrx0M6MSWMMvFgtz7DKKp"
    metadata_prop = {'vcard:organization-name': "CompanyName", 'hasURL': "URL", 'mdaas:HeadquartersAddress': "Address", 'tr-org:hasHeadquartersFaxNumber': "FaxNumber",
                     'tr-org:hasHeadquartersPhoneNumber': "PhoneNumber", 'hasHoldingClassification': "HoldingType", 'hasIPODate': "IPODate"}
    l = len(str(cik))
    cik = "0"*(10-l)+str(cik)
    perm_id = requests.get(
        "https://api-eit.refinitiv.com/permid/search?q=cik:{}&access-token={}".format(cik, token))
    perm_id_req = requests.get(perm_id.json()['result']['organizations']['entities'][0]['@id'], headers={
                             "Accept": "application/ld+json", "x-ag-access-token": token})
    perm_id_data = perm_id_req.json()
    for prop in metadata_prop.keys():
        try:
            if prop == 'hasHoldingClassification':
                if 'public' in perm_id_data[prop]:
                    print(True)
                    data[metadata_prop[prop]] = "Public"
            elif prop == "mdaas:HeadquartersAddress":
                data[metadata_prop[prop]] = perm_id_data[prop].replace("\n", " ")
            else:
                data[metadata_prop[prop]] = perm_id_data[prop]
        except:
            continue
    for prop in metadata_prop.keys():
        data[metadata_prop[prop]] = data.get(metadata_prop[prop], 'NaN')
    return data