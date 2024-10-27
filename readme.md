# Real-Time Data Processing System for Weather Monitoring with Rollups and Aggregates

## **Installing Dependencies**

The modules are added in requirements.txt. To install run,

	pip install -r requirements.txt

## **API Keys**

The following API key is required:

- Open Weather API Key (https://openweathermap.org/api)

Add the key in the utils.py file located in the project folder.

	api_key = ADD YOUR API KEY  

## **Tools & Technologies**

- Python
- PyQt6
- MongoDB Cloud

## Running CodeBase and Web App

To start a server run,
	
`python fetch_data.py`

PyQt6 is used to create UI, to run web app:  

   `python maingui.py`

## Configuring MongoDb Database

- Signup on mogodb cloud (https://www.mongodb.com/products/platform/cloud)
- Create a new organization.
- Create a new project, say - `weather_app` and a cluster say - `data`.
- Create a new database.
- Add connection string in connection.py and database password in utils.py. 


## **Functionality & Description**

- The OpenWeatherMap API is used to retrieve real-time weather data for major metros in India, including Delhi, Mumbai, Chennai, Bangalore, Kolkata, and Hyderabad. The API is called at 5-minute intervals to ensure up-to-date information.

- The following weather parameters are taken: 
    - `weather.main`: Group of weather parameters
    - `weather.icon`: Weather icon id
    - `main.temp`: Temperature in Kelvin
    - `main.feels_like`: Temperature (human perception of weather) in Kelvin.
    - `dt`: Time of data calculation, unix, UTC
    - `main.humidity`: Humidity in %
    - `wind.speed`: Wind speed in meter/sec

- The below images shows the wheather updates for various cities:

<kbd>![](/README_images/img_1_Delhi.PNG)</kbd>

<kbd>![](/README_images/img_2_Mumbai.PNG)</kbd>

<kbd>![](/README_images/img_3_Bengaluru.PNG)</kbd>

#### Rollups and Aggregates

- For each city, a daily report is prepared by aggregating the weather parameters. It includes:
    - **Average temperature** - The average temperature for a day is calculated by taking the average of all the temperature values recorded at five-minute intervals.
    - **Maximum temperature** - The maximum temperature for a day is calculated by identifying the highest value among all the temperature readings recorded at five-minute intervals.
    - **Minimum temperature** - The minimum temperature for a day is calculated by identifying the lowest value among all the temperature readings recorded at five-minute intervals.
    - **Dominant weather condition** - To identify the dominant weather condition, the mode (most frequently occurring weather condition) is selected.

#### Alerting Thresholds

- A user-configurable threshold for temperature is implemented: the user sets a threshold value, and an alert is triggered if the temperature difference between two consecutive updates exceeds this threshold.

- The images below show how the user sets up the threshold value, and an alert is triggered when the threshold is reached.

<kbd>![](/README_images/img_4_threshold.PNG)</kbd>

<kbd>![](/README_images/img_5_alert.PNG)</kbd>

#### Visualizations

- An interactive GUI-based application displays daily weather summaries in an appealing manner.
- An alert dialog is displayed if the threshold is breached.
- The user can click on the temperature to change the units from Celsius to Kelvin or Fahrenheit.


## **References**

1. <https://openweathermap.org/current>
2. <https://www.riverbankcomputing.com/static/Docs/PyQt6/>
3. <https://www.mongodb.com/products/platform/cloud>
4. <https://github.com/rodrigokamada/openweathermap>
