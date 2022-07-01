import urllib.request, json 
from bs4 import BeautifulSoup
from fastapi import FastAPI
from datetime import datetime, timedelta
from pytrends.request import TrendReq

app = FastAPI()

pytrends = TrendReq()


def main_search(sex, race, year):
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
        #result = search_in_data(data, sex, race, year)
        return data

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/life_expectancy/{sex}/{race}/{year}")
async def life_expectancy(sex: str, race: str, year: str):
    search = main_search(sex, race, year)
    try:
        return {"average_life_expectancy": sum(float(d['average_life_expectancy']) for d in search) / len(search)}
    except:
        return {"error": "Without Data"}

@app.get("/unemployment/{state}")
async def unemployment(state: str):
    uri = "https://www.bls.gov/web/laus/lauhsthl.htm"
    response = urllib.request.urlopen(uri)
    soup = BeautifulSoup(response, 'lxml')
    table = soup.find("table", {"class": "regular"}).find("tbody").find_all("tr")
    result_dict = {}
    for row in table:
        result_dict[row.find("th").string] = row.find_all("td")[2].string
    if state in result_dict:
        return {"rate": result_dict[state]}
    else:
        return {"error": "State not found"}

@app.get("/trends")
async def trends(phrase: str = "", start_date: str = "", end_date: str = ""):
    N_DAYS_AGO = 14
    today = datetime.now()    
    n_days_ago = today - timedelta(days=N_DAYS_AGO)
    if start_date == "": start_date = n_days_ago
    if end_date == "": end_date = today
    if phrase != "":
        return {"interest": pytrends.get_historical_interest(phrase.replace(",","").split(" "), year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)}
    else:
        return {"error": "A phrase is required"}