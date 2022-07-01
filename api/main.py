import urllib.request, json 
from bs4 import BeautifulSoup
from fastapi import FastAPI
from datetime import datetime, timedelta
import pandas as pd                        
from pytrends.request import TrendReq
import re

app = FastAPI()

from pytrends.request import TrendReq

# Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()



def life_expectancy_search(sex, race, year):
    uri = "https://data.cdc.gov/resource/w9j2-ggv5.json?"
    if race:
        uri += "&race=" + race
    if sex:
        uri += "&sex=" + sex
    if year:
        uri += "&year=" + year
    result = []
    with urllib.request.urlopen(uri) as url:
        data = json.loads(url.read().decode())
        return data
    
def unemployment_search():
    uri = "https://www.bls.gov/web/laus/lauhsthl.htm"
    response = urllib.request.urlopen(uri)
    soup = BeautifulSoup(response, 'lxml')
    table = soup.find("table", {"class": "regular"}).find("tbody").find_all("tr")
    result_dict = {}
    for row in table:
        result_dict[row.find("th").string] = row.find_all("td")[2].string
        
    return result_dict
    
def trends_search(phrase, start_date, end_date):
    N_DAYS_AGO = 14
    today = datetime.now()    
    n_days_ago = today - timedelta(days=N_DAYS_AGO)
    
    if start_date == "": start_date = n_days_ago
    else:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        except:
            return None
    if end_date == "": end_date = today
    else:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
        except:
            return None
    if phrase != "":
        kw_list=[phrase]
        time_frame = ''
        regiondf = pytrend.get_historical_interest(kw_list, year_start=start_date.year, month_start=start_date.month, day_start=start_date.day, hour_start=0, year_end=end_date.year, month_end=end_date.month, day_end=end_date.day, hour_end=0, cat=0, geo='', gprop='', sleep=0)
        result = []
        for index, row in regiondf.iterrows():
            result.append(int(row[0]))
        return {"interest": result}
    else:
        return None



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/life_expectancy/{sex}/{race}/{year}")
async def life_expectancy(sex: str, race: str, year: str):
    search = life_expectancy_search(sex, race, year)
    try:
        return {"average_life_expectancy": sum(float(d['average_life_expectancy']) for d in search) / len(search)}
    except:
        return {"error": "Without Data"}

@app.get("/unemployment/{state}")
async def unemployment(state: str):
    result_dict = unemployment_search()
    if state in result_dict:
        return {"rate": result_dict[state]}
    else:
        return {"error": "State not found"}

@app.get("/trends")
async def trends(phrase: str = "", start_date: str = "", end_date: str = ""):
    result = trends_search(phrase, start_date, end_date)
    if result != None:
        return result
    else:
        return {"error": "A phrase is required or dates are badformed (Correct way: YYYY-mm-dd)"}