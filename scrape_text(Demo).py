from bs4 import BeautifulSoup
import urllib3
import re

http = urllib3.PoolManager()
req = http.request("GET","https://www.sec.gov/Archives/edgar/data/796343/000079634322000032/adbe-20211203.htm",headers={
    'user-agent': 'Sample @ <sample@sample.com>',
    'host': 'www.sec.gov'
})
soup = BeautifulSoup(req.data)

data = soup.find_all("span")

features = ("arr")

for feature in features:
    value = []
    for i in data:
        regex_string = '.*\s{}'.format(feature)
        feature_match = re.findall(regex_string,i.text.lower())
        if len(feature_match)!=0 and '$' in feature_match[0]:
            x = feature_match[0].strip()
            lines = x.split(". ")
            if len(lines)==1:
                for i in lines:
                    if feature in i:
                        match = re.findall('\$([0-9\.]*\s(billion|million|thousand|hundred))', i)
                        if len(match)>0:
    #                         print(match[0][0], "\n")
                            value.append(match[0][0])
            else:
                for i in lines:
                    if feature in i and "total" in i:
                        match = re.findall('\$([0-9\.]*\s(billion|million|thousand|hundred))', i)
                        if len(match)>0:
    #                         print(match[0][0])
                            value.append(match[0][0])

    value_final = set(value)
    if len(value_final)==1:
        print(list(value_final)[0])
    elif len(value_final)>1:
        print(max(list(value_final)))