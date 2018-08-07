
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import json

# Import API key
import api_keys

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

## Generate Cities List

# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Save latitudes for use in analysis
lats = []

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name

    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)
        lats.append(lat_lng[0])
        
# Print the city count to confirm sufficient count
len(cities)

# Output file
cities_df = pd.DataFrame(cities, columns=["Cities"])
cities_df.to_csv(output_data_file, index=False)

## Perform API Calls

# OpenWeatherMap API Key
api_key = api_keys.api_key

# Starting URL for Weather Map API Call
base_url = "http://api.openweathermap.org/data/2.5/weather?units=Imperial&APPID=" + api_key 

# Setup lists for data
temp = []
humidity = []
clouds = []
wind_speed = []
record_num = 0
error_count = 0

# TEST TEST TEST TEST
#test_cities = cities[:50]
#test_lats = lats[:50]
# TEST TEST TEST TEST

# Loop through the cities
print("Beginning Data Retrieval")
print("------------------------")

# Loop through cities
for city in cities:
    city_query = "&q=" + city
    url = base_url + city_query
    print(f'Processing Record {record_num} of Set 1 | {city}')
    print(url)
    
    # increment
    record_num += 1
    
    try:
        # Get data from OpenWeatherMap
        weather_data = requests.get(url).json()
    
        # Save data
        temp.append(weather_data["main"]["temp_max"])
        humidity.append(weather_data["main"]["humidity"])
        clouds.append(weather_data["clouds"]["all"])
        wind_speed.append(weather_data["wind"]["speed"])

    except KeyError:
        print(f'\nCITY NOT FOUND, skipping {city}\n')
        
        # Keep track of total number of errors
        error_count += 1
                
        # Nullify not found city rows
        temp.append(np.nan)
        humidity.append(np.nan)
        clouds.append(np.nan)
        wind_speed.append(np.nan)

    
print("------------------------")
print("Ending Data Retrieval")
print(f'\nTotal Errors: {error_count}')

data_dict = {"City": cities, "Lat": lats, "Temp": temp, "Humidity": humidity, "Clouds": clouds, "Wind_Speed": wind_speed}
city_weather_df = pd.DataFrame(data_dict)

# Drop the not found cities
city_weather_df.dropna(inplace=True)

city_weather_df.head()

# Scatter Plots
# Temperature (F) vs. Latitude
x_axis = city_weather_df['Lat']
data_to_plot = city_weather_df['Temp']

plt.scatter(x_axis, data_to_plot, marker="o", c='b', edgecolors="black", alpha=0.75, label="Temp (F)")

# Save Figure
plt.savefig("temp_vs_Latitude_plot.png", bbox_inches="tight")

# Incorporate the other graph properties
plt.ylim(0, 120)
plt.xlim(-80, 100)
plt.grid(axis='both', alpha=0.5)
plt.xlabel("Latitude")
plt.ylabel("Max Temperature (F)")
plt.title("City Latitude vs Max Temperature (8/5/2018)")

# Show plot
plt.show()

# Scatter Plots
# Humidity vs. Latitude
x_axis = city_weather_df['Lat']
data_to_plot = city_weather_df['Humidity']

plt.scatter(x_axis, data_to_plot, marker="o", c='b', edgecolors="black", alpha=0.75, label="Temp (F)")

# Save Figure
plt.savefig("humidity_vs_Latitude_plot.png", bbox_inches="tight")

# Incorporate the other graph properties
plt.ylim(0, 120)
plt.xlim(-80, 100)
plt.grid(axis='both', alpha=0.5)
plt.xlabel("Latitude")
plt.ylabel("Humidity")
plt.title("City Latitude vs Humidity (8/5/2018)")


# Show plot
plt.show()

# Scatter Plots
# Cloudiness vs. Latitude
x_axis = city_weather_df['Lat']
data_to_plot = city_weather_df['Clouds']

plt.scatter(x_axis, data_to_plot, marker="o", c='b', edgecolors="black", alpha=0.75, label="Temp (F)")

# Save Figure
plt.savefig("clouds_vs_Latitude_plot.png", bbox_inches="tight")

# Incorporate the other graph properties
plt.ylim(-20, 120)
plt.xlim(-80, 100)
plt.grid(axis='both', alpha=0.5)
plt.xlabel("Latitude")
plt.ylabel("Cloudiness")
plt.title("City Latitude vs Cloudiness (8/5/2018)")


# Show plot
plt.show()

# Scatter Plots
# Wind Speed vs. Latitude
x_axis = city_weather_df['Lat']
data_to_plot = city_weather_df['Wind_Speed']

plt.scatter(x_axis, data_to_plot, marker="o", c='b', edgecolors="black", alpha=0.75, label="Temp (F)")

# Save Figure
plt.savefig("wind_speed_vs_Latitude_plot.png", bbox_inches="tight")

# Incorporate the other graph properties
plt.ylim(-5, 40)
plt.xlim(-80, 100)
plt.grid(axis='both', alpha=0.5)
plt.xlabel("Latitude")
plt.ylabel("Wind Speed")
plt.title("City Latitude vs Wind Speed (8/5/2018)")


# Show plot
plt.show()

