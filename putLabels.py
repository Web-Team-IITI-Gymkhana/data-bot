
from asyncio.windows_events import NULL
from cmath import nan
import json
 
f = open('data_10k_table(dummy).json')

 
data = json.load(f)

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

for cik in data:
  if cik == "1585521":
    for dt in data[cik]: 
      print(f"cik: {cik}", end=" ")
      print(f"date: {dt}", end=" \n")
      curDate = int(dt)
      prevDate = curDate - 1
      if data[cik][str(prevDate)] == NULL:
        assert('previous date not available')
    
      # Definitions
      # ============================================================================================ #
      prev = data[cik][str(prevDate)]
      cur = data[cik][dt]

      for keys in cur:
        cur[keys] = float(cur[keys]) + 0.00000000000000001
      
      for keys in prev:
        prev[keys] = float(prev[keys])+0.00000000000000001

      print(cur['NetIncome'])
      cur['ARR'] = (cur['MRR'] * 4)
      prev['ARR'] = (prev['MRR'] * 4)
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
      EBIDTAratio = cur['Revenues'] - cur['TotalCostsAndExpenses'] 
      
      #Churn Rate 
      ChurnRate = cur['CustomerChurn']
      if (ChurnRate == float('nan')):
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
      MarketCap = cur['CommonStock'] * cur['StockPrice']
      
      # Magic Number = Net New MRR * 4 of current quarter/ Sales and Marketing of prev quarter
      MagicNumber = cur['ARR'] / prev['CostOfSales']

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

      print(ratios)

      break
  
f.close()

result = {
  'GrossProfit': nan, 
  'GrossMargin': nan, 
  'WorkingCapitalRatio': 3.8039637577521708, 
  'EarningPerShare': 1818600000000.9998, 
  'DebtToEquityRatio': 0.32635121466796796, 
  'PEratio': nan, 
  'ReturnOfEquity': 0.4710462972774568, 
  'EBIDTAratio': nan, 
  'ChurnRate': nan, 
  'GrowthRate': nan, 
  'ProfitMargin': 33.07478413578729, 
  'RuleOf40': nan, 
  'MarketCap': nan, 
  'MagicNumber': nan
}