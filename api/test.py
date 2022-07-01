import xml.etree.ElementTree as ET
tree = ET.parse('test.xml')
root = tree.getroot()
location = root[0]
forecastday = root[1][0]


'''
JSON FORMAT
{
    city: cityName,
    days: [
        day1: {
            temperature: avg(hourly_temperature) in celcius,
            pressure: avg(hourly_pressure) in mb,
            wind: avg(hourly_wind_speed) in kph,
            precipitations: avg(hourly_precipitations) in mm,
            humidity: avg(hourly_humidity) in %,
            condition_history: [All conditions during all hours] 
        },
        day2: {
            ...
        },
        day3: {
            ...
        }...
        dayN: {
            ...
        }
    ]
}
'''

resulting_dict = {"city": root[0][0].text, "days": []}

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
