import urllib.request, json 
from bs4 import BeautifulSoup
from fastapi import FastAPI
from datetime import datetime, timedelta
import pandas as pd                        
from pytrends.request import TrendReq
import xml.etree.ElementTree as ET
import re
import requests
import geocoder
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

pytrend = TrendReq()


# Auxiliar functions

def life_expectancy_search(sex, race, year):
    uri = "https://data.cdc.gov/resource/w9j2-ggv5.json?"
    if race:
        if race not in ["Black", "White", "All"]:
            return None
        uri += "&race=" + race
    if sex:
        if sex not in ["Male", "Female", "Both sexes"]:
            return None
        uri += "&sex=" + sex.replace(" ", "%20")
    if year:
        uri += "&year=" + year
    try:
        with urllib.request.urlopen(uri) as url:
            data = json.loads(url.read().decode())
            return data
    except:
        return None

def unemployment_search():
    uri = "https://www.bls.gov/web/laus/lauhsthl.htm"
    response = urllib.request.urlopen(uri)
    soup = BeautifulSoup(response, 'lxml')
    table = soup.find("table", {"class": "regular"}).find("tbody").find_all("tr")
    result_dict = {}
    for row in table:
        result_dict[row.find("th").string.lower()] = row.find_all("td")[0].string
        
    return result_dict

def trends_search(phrase, start_date, end_date):
    N_DAYS_AGO = 14
    today = datetime.now()    
    n_days_ago = today - timedelta(days=N_DAYS_AGO)
    
    try:
        if start_date == "": start_date = n_days_ago
        else: start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date == "": end_date = today
        else: end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except:
        return None
    
    if phrase != "":
        regiondf = pytrend.get_historical_interest([phrase], year_start=start_date.year, month_start=start_date.month, day_start=start_date.day, hour_start=0, year_end=end_date.year, month_end=end_date.month, day_end=end_date.day, hour_end=0, cat=0, geo='', gprop='', sleep=0)
        return {"interest": [int(row[0]) for index, row in regiondf.iterrows()]}
    else:
        return None

def weather_search(location, with_trends=False, phrase=""):
    today = datetime.now()
    resulting_dict = {"city": str(location), "days": []}
    for day_index in range(7):
        d = today - timedelta(days=day_index)
        key = os.environ['TOKEN']
            
        uri = "http://api.weatherapi.com/v1/history.xml?key=" + key + "&q=" + str(location) + "&dt=" + str(d.strftime("%Y-%m-%d"))
        response = requests.get(uri).text
        
        tree = ET.fromstring(response)
        resulting_dict["city"] = tree[0][0].text
        forecastday = tree[1][0]

        hourly_temperature = round(sum([float(i[2].text) for i in forecastday if i.tag == "hour"]) / 24, 2)
        hourly_pressure = round(sum([float(i[10].text) for i in forecastday if i.tag == "hour"]) / 24, 2)
        hourly_wind_speed = round(sum([float(i[7].text) for i in forecastday if i.tag == "hour"]) / 24, 2)
        hourly_humidity = round(sum([float(i[14].text) for i in forecastday if i.tag == "hour"]) / 24, 2)
        hourly_precipitation = round(sum([float(i[12].text) for i in forecastday if i.tag == "hour"]) / 24, 2)
        condition_history = [i[5][0].text for i in forecastday if i.tag == "hour"]

        day = forecastday[0].text

        
        if with_trends:
            interest_result = trends_search(phrase=phrase, start_date=d.strftime("%Y-%m-%d"), end_date=d.strftime("%Y-%m-%d"))
            if len(interest_result["interest"]) == 0: interest_result["interest"].append("Without data")
            resulting_dict["days"].append({"date": day, "interest": interest_result["interest"][0], "weather": {"temperature": hourly_temperature, "pressure": hourly_pressure, "wind": hourly_wind_speed, "precipitations": hourly_precipitation, "humidity": hourly_humidity, "condition_history": condition_history}})
        else:
            resulting_dict["days"].append({day: {"temperature": hourly_temperature, "pressure": hourly_pressure, "wind": hourly_wind_speed, "precipitations": hourly_precipitation, "humidity": hourly_humidity, "condition_history": condition_history}})
    return resulting_dict


# API endpoints

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/life_expectancy/{sex}/{race}/{year}")
async def life_expectancy(sex: str, race: str, year: str):
    search = life_expectancy_search(sex, race, year)
    if search == None:
        return {"error": "Sex or Race are not included in the available ones, or year is not well formed"}
    try:
        return {"average_life_expectancy": float(search[0]["average_life_expectancy"])}
    except:
        return {"error": "Without Data"}

@app.get("/unemployment/{state}")
async def unemployment(state: str):
    result_dict = unemployment_search()
    if state.lower() in result_dict:
        return {"rate": float(result_dict[state.lower()])}
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
    my_location = geocoder.ip('me')
    return {"weather": weather_search(my_location)}

@app.get("/trends_weather")
async def trends_weather(phrase: str = ""):
    my_location = geocoder.ip('me')
    if phrase != "":
        return weather_search(my_location, True, phrase)
    else:
        return {"error": "A phrase is required"}