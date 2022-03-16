import pandas as pd
from asyncio.windows_events import NULL
from cmath import nan
import json
 
f = open('json/data_10k_table(dummy).json')

 
data = json.load(f)

def wce(r):
  if r>=1.5 and r<=2:
    return 1
  else: 
    return 0  
"================================================"
def de(r):
  if r>=0.5 and r<=1.5:
    return 1
  else: 
    return 0 
"================================================"
def eps(r):
  if r>=1 and r<=99:
    return 1
  else: 
    return 0 
"================================================"
def pe(r):
  if r>13:
    return 1
  else: 
    return 0
"================================================"
def roe(r):
  if r>15:
    return 1
  else: 
    return 0
"================================================"
def ro40(r):
  if r>40:
    return 1
  else: 
    return 0
"================================================"
def market_cap(r):
  if r>2000000000:
    return 1
  else: 
    return 0
"================================================"
def growth_rate(r):
  if r>60:
    return 1
  else: 
    return 0
"================================================"
def profit_margin(r):
  if r>20:
    return 1
  else: 
    return 0
"================================================"
def gross_margin(r):
  if r>0.5:
    return 1
  else: 
    return 0
"================================================"
def magic_num(r):
  if r>1:
    return 1
  else: 
    return 0
"================================================"
def chun_rate(r):
  try:
    if r<1:
      return 1
    else: 
      return 0
  except:
    return 0  

"=============================================="
'''
Working Capital Ratio	= Total Current Assets / Total Current Liabilities 
Earning Per Share	= Profit ( or Income ) / Ang common outstanding shares 
Debt to Equity Ratio	= Total Liabilities / Total Shareholders' (or Stockholders') equity 
P / E ratio = Share Price / Earning per share 
Return of Equity	 (Net Earnings / Shareholders' (or Stockholders') Equity) x 100
EBIDTA = Revenue - Cost of Goods - Operating Costs 
Churn Rate	= (Current Subscription Revenue - Previous Subscription Revenue) / Previous Subscription Revenue  
Rule of 40 = growth rate + profit margin 	
EV = Marketcap + Total Stockholders' Equity + Total Debt - Total Cash
Market Cap	= Total Outstanding Share * Share Price
Magic Number = Net New MRR * 4 of current quarter/ Sales and Marketing of prev quarter 
Gross Profit = Revenue - Cost of Goods Sold
Gross Margin = (Revenue - Cost of Goods Sold) / Revenue 
'''
epsilon = 0.000000000000000000001

for cik in data:
  if cik == "1108524":
    for dt in data[cik]: 
      print(f"cik: {cik}", end=" ")
      print(f"date: {dt}", end=" \n")
      curDate = int(dt)
      prevDate = curDate - 1
      if str(prevDate) not in data[cik]:
        prevDate = curDate # just to prevent NaN error
    
      # Definitions
      # ============================================================================================ #
      prev = data[cik][str(prevDate)]
      cur = data[cik][dt]

      for keys in cur:
        cur[keys] = float(cur[keys]) + epsilon
      
      for keys in prev:
        prev[keys] = float(prev[keys]) + epsilon

      cur['ARR'] = (cur['MRR'] * 12)
      prev['ARR'] = (prev['MRR'] * 12)
      # ============================================================================================= #

      # Gross Profit = Revenue - Cost of Goods Sold
      GrossProfit = (cur['Revenues'] - cur['SalesCost'])

      # Gross Margin = (Revenue - Cost of Goods Sold) / Revenue
      GrossMargin = (cur['Revenues'] - cur['SalesCost']) / cur['Revenues']

      # Working capital ratio
      WorkingCapitalRatio = cur['TotalCurrentAssets'] / cur['TotalCurrentLiabilities' ] 

      # Earning Per Share
      EarningPerShare = cur['NetIncome'] / cur['SharesOutstanding']
      
      # Debt to Equity Ratio
      DebtToEquityRatio = cur['TotalCurrentLiabilities'] / cur ['TotalStockholdersEquity']

      # P / E ratio
      PEratio = cur['StockPrice'] / EarningPerShare 

      # Return of Equity
      ReturnOfEquity = (cur['NetIncome'] /  cur ['TotalStockholdersEquity']) * 100 

      # EBIDTA
      EBIDTAratio = cur['Revenues'] - cur['NetOperatingExpenses']
      
      #Churn Rate 
      ChurnRate = cur['CustomerChurn']
      if (ChurnRate):
        ChurnRate = (cur['SubscriptionRevenue'] - prev['SubscriptionRevenue']) / prev['SubscriptionRevenue']

      # Growth Rate 
      if(cur['ARR'] != "NaN"): 
        GrowthRate =((cur['ARR'] - prev['ARR']) / prev['ARR']) * 100
      else:
        GrowthRate =((cur['EBITDAratio'] - prev['EBITDAratio']) / prev['EBITDAratio']) * 100

      # Profit Margin 
      ProfitMargin =((cur['NetIncome'] - prev['NetIncome']) / prev['NetIncome']) * 100 

      # Rule of 40 
      RuleOf40 = GrowthRate + ProfitMargin
      
      
      # Market Cap	= Total Outstanding Share * Share Price
      MarketCap = cur['SharesOutstanding'] * cur['StockPrice']
      
      # Magic Number = Net New MRR * 4 of current quarter/ Sales and Marketing of prev quarter
      MagicNumber = cur['ARR'] / prev['SalesCost']

      ratios = {
        'GrossProfit':GrossProfit,
        'GrossMargin':GrossMargin,
        'WorkingCapitalRatio':WorkingCapitalRatio,
        'EarningPerShare':EarningPerShare,
        'DebtToEquityRatio':DebtToEquityRatio,
        'PEratio':PEratio, 
        'ReturnOfEquity':ReturnOfEquity,
        'EBIDTAratio': EBIDTAratio, 
        'ChurnRate':ChurnRate,
        'GrowthRate': GrowthRate, 
        'ProfitMargin':ProfitMargin,
        'RuleOf40':RuleOf40,
        'MarketCap':MarketCap,
        'MagicNumber':MagicNumber,       
      }

      rato= pd.DataFrame(ratios.items())
      rato, rato.columns= rato.T, ratios.keys()
      rato.drop(index=rato.index[0],axis=0, inplace=True)
      #print(rato)
      rato['wce_label']=rato['WorkingCapitalRatio'].apply(wce)
      rato['eps_label']=rato['EarningPerShare'].apply(eps)
      rato['de_label']=rato['DebtToEquityRatio'].apply(de)
      rato['pe_label']=rato['PEratio'].apply(pe)
      rato['roe_label']=rato['ReturnOfEquity'].apply(roe)
      rato['growth_rate_label']=rato['GrowthRate'].apply(growth_rate)
      rato['profitm_label']=rato['ProfitMargin'].apply(profit_margin)
      rato['grossm_label']=rato['GrossMargin'].apply(gross_margin)
      rato['ro40_label']=rato['RuleOf40'].apply(ro40)
      rato['churnrate_label']=rato['ChurnRate'].apply(chun_rate)
      rato['marketCap_label']=rato['MarketCap'].apply(market_cap)
      rato['magicNum_label']=rato['MagicNumber'].apply(magic_num)

      print(rato.iloc[:,-9:])
    break


f.close()
