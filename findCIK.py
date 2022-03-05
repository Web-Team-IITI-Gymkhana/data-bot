import pandas as pd
import re

def withRepeat():
    companyNames = pd.read_csv('Software Company List v2.csv')
    names = companyNames['Company'].tolist()
    data = {'CompanyName':[],'CIK':[]}
    data_file = pd.DataFrame(data)
    for name in names:
        pattern = name
        pattern = pattern.strip()
        fhand = open('cik-lookup-data.txt')
        for line in fhand:
            target = line.strip()

            target = target.replace(',','')

            hit = re.findall('^{}'.format(pattern),target)
            
            if len(hit) == 0:
                continue
            else:
                cik = re.findall(':(000.*):',target)
                details = {'CompanyName': pattern , 'CIK': cik[0]}
                data_file = data_file.append(details, ignore_index = True)         
        
        fhand.close()


    data_file.to_csv('Result_Repeat.csv',index=False)
            
    print("Done Repeat")     

   
def noRepeat():
    companyCIK = dict()
    companyNames = pd.read_csv('Software Company List v2.csv')
    names = companyNames['Company'].tolist()
    for name in names:
        pattern = name
        pattern = pattern.strip()
        fhand = open('cik-lookup-data.txt')
        for line in fhand:
            target = line.strip()

            target = target.replace(',','')

            hit = re.findall('^{}'.format(pattern),target)
            
            if len(hit) == 0:
                continue
            else:
                cik = re.findall(':(000.*):',target)
                companyCIK[pattern] = companyCIK.get(pattern,cik[0])
        fhand.close()
    
    result = pd.DataFrame(list(companyCIK.items()), columns=['CompanyName', 'CIK'])
    result.to_csv('Result_No_Repeat.csv',index=False)
            
    print("Done No Repeat")  


noRepeat()