from operator import index
import pandas as pd

class ideal_extract:
  def wce(self, r):
    if r>=1 and r<=2:
      return 1
    else: 
      return 0  
  "================================================"
  def de(self, r):
    if r>=0.5 and r<=1.5:
      return 1
    else: 
      return 0 
  "================================================"
  def eps(self, r):
    if r>=1 and r<=99:
      return 1
    else: 
      return 0 
  "================================================"
  def pe(self, r):
    if r>13:
      return 1
    else: 
      return 0
  "================================================"
  def roe(self, r):
    if r>15:
      return 1
    else: 
      return 0
  "================================================"
  def ro40(self, r):
    if r>40:
      return 1
    else: 
      return 0
  "================================================"
  def market_cap(self, r):
    if r>2000000000:
      return 1
    else: 
      return 0
  "================================================"
  def growth_rate(self, r):
    if r>60:
      return 1
    else: 
      return 0
  "================================================"
  def profit_margin(self, r):
    if r>20:
      return 1
    else: 
      return 0
  "================================================"
  def gross_margin(self, r):
    if r>0.5:
      return 1
    else: 
      return 0
  "================================================"
  def magic_num(self, r):
    if r>1:
      return 1
    else: 
      return 0
  "================================================"
  def chun_rate(self, r):
    try:
      if r<1:
        return 1
      else: 
        return 0
    except:
      return 0  

  "================================================"
  def ev_ebidta(self, r):
    try:
      if r<10:
        return 1
      else: 
        return 0
    except:
      return 0  

class ratios:
  def setup_ratios(cur, prev):
      epsilon = 1e-20
      for keys in cur:
        try:
          cur[keys] = float(cur[keys]) + epsilon
        except:
          pass
      
      for keys in prev:
        try:
          prev[keys] = float(prev[keys]) + epsilon
        except:
          pass

      cur['ARR'] = (cur['MRR'] * 12)
      cur['ARR'] = (cur['NetIncome'])
      prev['ARR'] = (prev['MRR'] * 12)
      prev['ARR'] = (prev['NetIncome'])

      # ============================================================================================= #

      # Gross Profit = Revenue - Cost of Goods Sold
      GrossProfit = (cur['Revenues'] - cur['CostOfSales'])

      # Gross Margin = (Revenue - Cost of Goods Sold) / Revenue
      GrossMargin = (cur['Revenues'] - cur['CostOfSales']) / cur['Revenues']

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
      EBIDTAratio = cur['Revenues'] - cur['TotalOperatingExpenses']
      
      #Churn Rate
      try: 
        ChurnRate = cur['CustomerChurn']
      except:
        try: 
          ChurnRate = (cur['NetIncome'] - prev['NetIncome']) / prev['NetIncome']
        except:
          ChurnRate = 0.99

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

      # EV = Marketcap + Total Stockholders' Equity + Total Debt - Total Cash
      EvRatio = MarketCap + cur['TotalStockholdersEquity'] + cur['TotalDebt'] - cur['CashAndCashEquivalents']

      # EV / Ebidta
      EVbyEbidta = EvRatio / EBIDTAratio 
      
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
        "EvRatio": EvRatio,
        "EVbyEbidta": EVbyEbidta,
        'ChurnRate':ChurnRate,
        'GrowthRate': GrowthRate, 
        'ProfitMargin':ProfitMargin,
        'RuleOf40':RuleOf40,
        'MarketCap':MarketCap,
        'MagicNumber':MagicNumber,       
      }

      rfex = ideal_extract()
      rato= pd.DataFrame(ratios.items())
      rato, rato.columns= rato.T, ratios.keys()
      rato.drop(index=rato.index[0],axis=0, inplace=True)
      #print(rato)
      rato['wce_label']=rato['WorkingCapitalRatio'].apply(rfex.wce)
      rato['eps_label']=rato['EarningPerShare'].apply(rfex.eps)
      rato['de_label']=rato['DebtToEquityRatio'].apply(rfex.de)
      rato['pe_label']=rato['PEratio'].apply(rfex.pe)
      rato['roe_label']=rato['ReturnOfEquity'].apply(rfex.roe)
      rato['growth_rate_label']=rato['GrowthRate'].apply(rfex.growth_rate)
      rato['profitm_label']=rato['ProfitMargin'].apply(rfex.profit_margin)
      rato['grossm_label']=rato['GrossMargin'].apply(rfex.gross_margin)
      rato['ro40_label']=rato['RuleOf40'].apply(rfex.ro40)
      rato['churnrate_label']=rato['ChurnRate'].apply(rfex.chun_rate)
      rato['EVbyEbidta_label']=rato['EVbyEbidta'].apply(rfex.ev_ebidta)
      rato['marketCap_label']=rato['MarketCap'].apply(rfex.market_cap)
      rato['magicNum_label']=rato['MagicNumber'].apply(rfex.magic_num)

      return ratios, rato