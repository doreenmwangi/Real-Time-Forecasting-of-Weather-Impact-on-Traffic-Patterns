import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 51.454514,
	"longitude": -2.58791,
	"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation_probability", "precipitation", "rain", "showers", "snowfall", "snow_depth", "pressure_msl", "surface_pressure", "cloud_cover", "cloud_cover_low", "visibility", "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m", "wind_direction_10m", "wind_direction_80m", "wind_direction_120m", "wind_direction_180m", "wind_gusts_10m", "temperature_80m"]
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(4).ValuesAsNumpy()
hourly_precipitation = hourly.Variables(5).ValuesAsNumpy()
hourly_rain = hourly.Variables(6).ValuesAsNumpy()
hourly_showers = hourly.Variables(7).ValuesAsNumpy()
hourly_snowfall = hourly.Variables(8).ValuesAsNumpy()
hourly_snow_depth = hourly.Variables(9).ValuesAsNumpy()
hourly_pressure_msl = hourly.Variables(10).ValuesAsNumpy()
hourly_surface_pressure = hourly.Variables(11).ValuesAsNumpy()
hourly_cloud_cover = hourly.Variables(12).ValuesAsNumpy()
hourly_cloud_cover_low = hourly.Variables(13).ValuesAsNumpy()
hourly_visibility = hourly.Variables(14).ValuesAsNumpy()
hourly_wind_speed_10m = hourly.Variables(15).ValuesAsNumpy()
hourly_wind_speed_80m = hourly.Variables(16).ValuesAsNumpy()
hourly_wind_speed_120m = hourly.Variables(17).ValuesAsNumpy()
hourly_wind_speed_180m = hourly.Variables(18).ValuesAsNumpy()
hourly_wind_direction_10m = hourly.Variables(19).ValuesAsNumpy()
hourly_wind_direction_80m = hourly.Variables(20).ValuesAsNumpy()
hourly_wind_direction_120m = hourly.Variables(21).ValuesAsNumpy()
hourly_wind_direction_180m = hourly.Variables(22).ValuesAsNumpy()
hourly_wind_gusts_10m = hourly.Variables(23).ValuesAsNumpy()
hourly_temperature_80m = hourly.Variables(24).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["dew_point_2m"] = hourly_dew_point_2m
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["precipitation_probability"] = hourly_precipitation_probability
hourly_data["precipitation"] = hourly_precipitation
hourly_data["rain"] = hourly_rain
hourly_data["showers"] = hourly_showers
hourly_data["snowfall"] = hourly_snowfall
hourly_data["snow_depth"] = hourly_snow_depth
hourly_data["pressure_msl"] = hourly_pressure_msl
hourly_data["surface_pressure"] = hourly_surface_pressure
hourly_data["cloud_cover"] = hourly_cloud_cover
hourly_data["cloud_cover_low"] = hourly_cloud_cover_low
hourly_data["visibility"] = hourly_visibility
hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
hourly_data["wind_speed_120m"] = hourly_wind_speed_120m
hourly_data["wind_speed_180m"] = hourly_wind_speed_180m
hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
hourly_data["wind_direction_80m"] = hourly_wind_direction_80m
hourly_data["wind_direction_120m"] = hourly_wind_direction_120m
hourly_data["wind_direction_180m"] = hourly_wind_direction_180m
hourly_data["wind_gusts_10m"] = hourly_wind_gusts_10m
hourly_data["temperature_80m"] = hourly_temperature_80m

hourly_dataframe = pd.DataFrame(data = hourly_data)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import openmeteo_requests
import requests_cache
from retry_requests import retry

# ========== 🌍 Setup Open-Meteo API ==========
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# Function to fetch live weather data
def fetch_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 51.454514,
        "longitude": -2.58791,
        "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "precipitation", "cloud_cover"],
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        ),
        "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
        "humidity_2m": hourly.Variables(1).ValuesAsNumpy(),
        "wind_speed_10m": hourly.Variables(2).ValuesAsNumpy(),
        "precipitation": hourly.Variables(3).ValuesAsNumpy(),
        "cloud_cover": hourly.Variables(4).ValuesAsNumpy(),
    }
    
    return pd.DataFrame(data)

# ========== 🚦 Dynamic Background with Traffic Animation ==========
def set_background(weather_condition):
    """Set background based on weather conditions with dynamic traffic"""
    if weather_condition == "Sunny":
        bg_color = "#FFD700"  # Gold
        effect = "background: url('https://media.giphy.com/media/3o7TKzM6iTxkJlyuVG/giphy.gif'); background-size: cover;"  # Moving cars
    elif weather_condition == "Cloudy":
        bg_color = "#A9A9A9"  # Gray
        effect = "background: url('https://media.giphy.com/media/3o7TKMuc4IJ4z1RZ3y/giphy.gif'); background-size: cover;"  # Moving traffic lights
    elif weather_condition == "Rainy":
        bg_color = "#4682B4"  # Steel blue
        effect = "background: url('https://media.giphy.com/media/3o6gbbuLW76jkt8vIc/giphy.gif'); background-size: cover;"  # Rain with cars
    elif weather_condition == "Windy":
        bg_color = "#87CEFA"  # Light blue
        effect = "background: url('https://media.giphy.com/media/l3vR1miOgoVAhv1kc/giphy.gif'); background-size: cover;"  # Windy streets
    else:
        bg_color = "#F0F0F0"  # Default light gray
        effect = ""

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {bg_color};
            {effect}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# ========== 📌 Streamlit App Layout ==========
st.set_page_config(page_title="Weather & Traffic Live Dashboard", layout="wide")

st.title("🚗 Weather & Traffic Live Dashboard 🌦️")

# Fetch real-time weather data
weather_df = fetch_weather()
current_weather = weather_df.iloc[0]  # Latest data

# Set background dynamically
set_background("Sunny" if current_weather["precipitation"] == 0 else "Rainy")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌦️ Current Weather")
    st.markdown(f"**Temperature:** {current_weather['temperature_2m']}°C")
    st.markdown(f"**Humidity:** {current_weather['humidity_2m']}%")
    st.markdown(f"**Wind Speed:** {current_weather['wind_speed_10m']} km/h")
    st.markdown(f"**Precipitation:** {current_weather['precipitation']} mm")
    st.markdown(f"**Cloud Cover:** {current_weather['cloud_cover']}%")

with col2:
    st.subheader("🚦 Traffic Update")
    traffic_status = np.random.choice(["No Issues", "Minor Congestion", "Heavy Traffic", "Accident Reported"])
    st.markdown(f"**Traffic Condition:** {traffic_status}")

# ========== 🗺️ User Inputs ==========
st.sidebar.title("📍 Travel Inputs")
travel_date = st.sidebar.date_input("Select Travel Date", datetime.date.today())
travel_time = st.sidebar.time_input("Select Travel Time", datetime.datetime.now().time())
travel_location = st.sidebar.text_input("Enter Location", "Bristol")

# ========== 📊 Interactive Weather Plot ==========
st.subheader("📊 Live Weather Trends")

# Convert datetime for plotting
weather_df["date"] = weather_df["date"].dt.tz_convert("Europe/London")

# Melt the dataframe for plotting
weather_long = weather_df.melt(id_vars=["date"], var_name="Weather Variable", value_name="Value")

fig = px.line(weather_long, x="date", y="Value", color="Weather Variable", title="Weather Trends Over Time")
st.plotly_chart(fig)

# ========== 🔍 Forecast Weather & Traffic for User Input ==========
if st.sidebar.button("Get Forecast"):
    future_weather = fetch_weather().iloc[-1]  # Simulating future forecast

    st.subheader(f"📍 Forecast for {travel_location} on {travel_date} at {travel_time}")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌦️ Predicted Weather")
        st.markdown(f"**Temperature:** {future_weather['temperature_2m']}°C")
        st.markdown(f"**Humidity:** {future_weather['humidity_2m']}%")
        st.markdown(f"**Wind Speed:** {future_weather['wind_speed_10m']} km/h")
        st.markdown(f"**Precipitation:** {future_weather['precipitation']} mm")
        st.markdown(f"**Cloud Cover:** {future_weather['cloud_cover']}%")

    with col2:
        st.subheader("🚦 Predicted Traffic")
        future_traffic = np.random.choice(["Smooth", "Moderate", "Heavy", "Severe Delays"])
        st.markdown(f"**Traffic Prediction:** {future_traffic}")

# ========== 🔗 Footer ==========
st.markdown("""
---
💡 *This interactive Weather & Traffic Dashboard is built using Streamlit and Open-Meteo API.*  
🚀 Developed for a **Data Science Group Project** 📊
""")
