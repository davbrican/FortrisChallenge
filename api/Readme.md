# Python Challenge API
This is an API to get a great sort of information about different kind of data.

The API can be run on docker just from the root folder with the command "docker-compose up -d" or by running:
- cd api 
- pip install -r requirements.txt
- uvicorn main:app --reload

### GETTERS
**_/_**
>Welcome endpoint with no useful information

**_/life_expectancy/{sex}/{race}/{year}_**
>A life expectancy getter. It returns the avarage of life expectancy depending of some factors given in the parameters of the request. Those parameteres are:
-sex: Including just "Male", "Female" and "Both sexes"
-race: Including just "Black", "White" and "All"
-year: Where the year must be 1900 <= year <= 2018

Example: http://API_URL/life_expectancy/Male/White/2010

**_/unemployment/{state}_**
>A rate value of the unemployment of the specified state from USA

Example: http://API_URL/unemployment/Alabama

**_/trends_**
>A hourly global trends of a given phrase. To use this get, the phrase must be specified in the query and the start and end date can be specified too (but those 2 are optionals):
-phrase: A text to be searched
-start_date: A date with the format YYYY-mm-dd
-end_date: A date with the format YYYY-mm-dd

Example: http://API_URL/trends?phrase=hello%20world&start_date=2022-06-20&end_date=2022-06-25

**_/weather_**
>Returns the climate in the last 7 days in your location

Example: http://API_URL/weather

**_/trends_weather_**
>Returns the climate in your location and a phrase given trends in the last 7 days

Example: http://API_URL/trends_weather?phrase=hello%20world

### TESTS
To run all the tests run the command "pytest ./test.py" into the folder ./api
