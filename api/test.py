#import the libraries
import pandas as pd                        
from pytrends.request import TrendReq
pytrend = TrendReq()

#provide your search terms
kw_list=['open spotify']

#search interest per region
#run model for keywords (can also be competitors)
regiondf1 = pytrend.get_historical_interest(kw_list, year_start=2018, month_start=1, day_start=1, hour_start=0, year_end=2018, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
# Interest by Region
regiondf = pytrend.interest_by_region()
print(regiondf1)
#looking at rows where all values are not equal to 0
for index, row in regiondf1.iterrows():
    print(row[0])