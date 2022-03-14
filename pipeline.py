import scrape_table
import scrape_text

quarters = [("0101","0331"), ("0401", "0630"), ("0701", "0930"), ("1001", "1231")]

def get_10k(cik, year):
    year_table = scrape_table.get_sheet(cik, "10-K", f"{year}0101", f"{year+1}0101")
    year_text = scrape_text.get_scrape_text(cik,"10-K",f"{year}0101",f"{year+1}0101")
    for key in year_table.keys():
        if year_table[key] == 'NaN':
            if key in year_text.keys():
                year_table[key] = year_text[key]
    year_table["ARR"] = year_text["ARR"]
    return year_table

def get_10q(cik, year, quarter):
    quarter_table = scrape_table.get_sheet(cik, "10-Q", f"{year}"+quarters[quarter-1][0], f"{year}"+quarters[quarter-1][1])
    quarter_text = scrape_text.get_scrape_text(cik,"10-Q", f"{year}"+quarters[quarter-1][0], f"{year}"+quarters[quarter-1][1])
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
    if form=="10-K":
        return get_10k(cik,year)
    elif form=="10-Q":
        return get_10q(cik,year,quarter)