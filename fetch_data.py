import time
from datetime import datetime

import requests
import schedule

import utils
from connection import get_db_handle


def fetch_data():
    citiesList = ['Delhi', 'Mumbai', 'Chennai', 'Bengaluru', 'Kolkata', 'Hyderabad']
    weather_data_list = []

    for city in citiesList:
        api_url = utils.openweather_api_url + city + '&appid='
        api_key = utils.api_key
        response = requests.get(api_url + api_key)

        if response.status_code == 200:
            response_data = response.json()
            weather_main = response_data['weather'][0]['main']
            temperature = response_data['main']['temp']
            feels_like = response_data['main']['feels_like']
            date_time_unix = response_data['dt']

            humidity = response_data['main']['humidity']
            wind_speed = response_data['wind']['speed']

            weather_icon_code = response_data['weather'][0]['icon']

            city = response_data['name']

            weather_dict = {
                'weather_main': weather_main,
                'weather_icon_code': weather_icon_code,
                'temperature': temperature,
                'feels_like': feels_like,
                'date_time_unix': date_time_unix,
                'date': datetime.fromtimestamp(date_time_unix).date().isoformat(),
                'humidity': humidity,
                'wind_speed': wind_speed,
                'city': city
            }

            weather_data_list.append(weather_dict)

        elif 400 <= response.status_code <= 504:
            print(f"Error {response.json()['cod']} : {response.json()['message']}")

    db = get_db_handle()
    collection = db['weather_data']
    result = collection.insert_many(weather_data_list)

    if result.acknowledged:
        print('Data inserted', result.inserted_ids)
    else:
        print('Data not inserted')

fetch_data()
schedule.every(5).minutes.do(fetch_data)

while True:
    schedule.run_pending()
    time.sleep(1)
