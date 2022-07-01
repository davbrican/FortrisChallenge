import urllib.request, json 
from bs4 import BeautifulSoup
from fastapi import FastAPI
from datetime import datetime, timedelta
import pandas as pd                        
from pytrends.request import TrendReq
import xml.etree.ElementTree as ET
import re
import requests

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

def weather_search():
    today = datetime.now()
    resulting_dict = {}
    for day_index in range(7):
        d = today - timedelta(days=day_index)
        key = "0e8b6d7ec08b49bbb8b85340220107"
        uri = "http://api.weatherapi.com/v1/history.xml?key=" + key + "&q=Sevilla&dt=" + str(d.strftime("%Y-%m-%d"))
        response = requests.get(uri).text
        
        tree = ET.fromstring(response)
        location = tree[0]
        forecastday = tree[1][0]
        if "city" not in resulting_dict:
            resulting_dict["city"] = location[0].text
        if "days" not in resulting_dict:
            resulting_dict["days"] = []

        hourly_temperature = 0
        hourly_pressure = 0
        hourly_wind_speed = 0
        hourly_humidity = 0
        hourly_precipitation = 0
        condition_history = []
        hours = 0

        for i in forecastday:
            if i.tag == "hour":
                hourly_temperature += float(i[2].text)
                hourly_pressure += float(i[10].text)
                hourly_wind_speed += float(i[7].text)
                hourly_humidity += float(i[14].text)
                hourly_precipitation += float(i[12].text)
                conditions = i[5]
                condition_history.append(conditions[0].text)
                hours += 1
                
        hourly_temperature = round((hourly_temperature / hours), 2)
        hourly_pressure = round((hourly_pressure / hours), 2)
        hourly_wind_speed = round((hourly_wind_speed / hours), 2)
        hourly_humidity = round((hourly_humidity / hours), 2)
        hourly_precipitation = round((hourly_precipitation / hours), 2)


        day = forecastday[0].text

        resulting_dict["days"].append({day: {"temperature": hourly_temperature, "pressure": hourly_pressure, "wind": hourly_wind_speed, "precipitations": hourly_precipitation, "humidity": hourly_humidity, "condition_history": condition_history}})
    return resulting_dict

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
    
@app.get("/weather")
async def weather():
    return {"weather": weather_search()}