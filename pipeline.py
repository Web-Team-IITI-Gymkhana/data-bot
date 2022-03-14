import scrape_table
import scrape_text

cik = 796343

years = [2022, 2021]
quarter = [("0101","0331"), ("0401", "0630"), ("0701", "0930"), ("1001", "1231")]

def get_10k():
    data = dict()
    year_dict = dict()

    for year in years:
        try:
            year_table = scrape_table.get_sheet(cik, "10-K", f"{year-1}0101", f"{year}0101")
            year_text = scrape_text.get_scrape_text(cik,"10-K",f"{year-1}0101",f"{year}0101")

            for key in year_table.keys():
                if year_table[key] == 'NaN':
                    if key in year_text.keys():
                        year_table[key] = year_text[key]
            year_table["ARR"] = year_text["ARR"]
            year_dict[year] = year_table
        except:
            continue
    data[cik] = year_dict
    print(cik," 10k Done")
    return data

def get_10q():
    data = dict()
    quarter_dict = dict()

    for year in years:
        for i in range(len(quarter)):
            try:
                quarter_table = scrape_table.get_sheet(cik, "10-Q", f"{year-1}"+quarter[i][0], f"{year-1}"+quarter[i][1])
                quarter_text = scrape_text.get_scrape_text(cik,"10-Q", f"{year-1}"+quarter[i][0], f"{year-1}"+quarter[i][1])
            except:
                continue
            for key in quarter_table.keys():
                try:
                    if quarter_table[key] == 'NaN':
                        if key in quarter_text.keys():
                            quarter_table[key] = quarter_text[key]
                except:
                    continue
            quarter_table["ARR"] = quarter_text["ARR"]
            quarter_dict[f"{year-1}_{i+1}"] = quarter_table

    data[cik] = quarter_dict
    print(cik," 10q Done")
    return data
