import streamlit as st
import pandas as pd
import requests
import pendulum
import datetime


def get_df_cp():
    """
    Load the DataFrame from a Parquet file and store it in the session state.
    If the DataFrame is already in the session state, return it directly.
    """
    if "df" not in st.session_state:
        df = pd.read_parquet("data/df_departement_clean.gzip")
        st.session_state["df"] = df
    else:
        df = st.session_state["df"]
    return df


def get_meteo_data(geopoint):
    """
    Fetch weather data from the WeatherAPI based on the provided geopoint.
    """
    params = {
        "key": "2fbbaab3e35841d5ba0125329251906",
        "q": geopoint,
        "days": 3,
        "alerts": "yes",
    }

    url = "http://api.weatherapi.com/v1/forecast.json"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch weather data.")
        return None


def history_meteo(geopoint):
    """
    Fetch historical weather data for the last 3 days from the WeatherAPI.
    """
    params = {
        "key": "2fbbaab3e35841d5ba0125329251906",
        "q": "Nantes",
        "dt": (datetime.date.today() - datetime.timedelta(days=4)).strftime("%Y-%m-%d"),
        "end_dt": (datetime.date.today() - datetime.timedelta(days=1)).strftime(
            "%Y-%m-%d"
        ),
    }

    url2 = "http://api.weatherapi.com/v1/history.json"
    response2 = requests.get(url2, params=params)
    if response2.status_code == 200:
        return response2.json()
    else:
        st.error("Failed to fetch weather data.")
        return None


def get_meteo_data_by_city(data):
    df = pd.DataFrame()
    df["lat"] = [data["location"]["lat"]]
    df["lon"] = [data["location"]["lon"]]
    if len(data["alerts"]["alert"]) == 0:
        df["alert"] = ["No alert"]
    else:
        df["alert"] = [data["alerts"]["alert"][0]["event"]]
        df["alert_debut"] = [data["alerts"]["alert"][0]["effective"]]
        df["alert_fin"] = [data["alerts"]["alert"][0]["expires"]]
        df["alert_severity"] = [data["alerts"]["alert"][0]["severity"]]
    return df


def get_meteo_forecast(data):
    """
    Extract and format the weather forecast data from the API response.
    """
    data_2 = []
    for day in data["forecast"]["forecastday"]:
        data_2.append(
            {
                "date": day["date"],
                "max_temp": day["day"]["maxtemp_c"],
                "min_temp": day["day"]["mintemp_c"],
                "avg_temp": day["day"]["avgtemp_c"],
                "totalprecip_mm": day["day"]["totalprecip_mm"],
                "avghumidity": day["day"]["avghumidity"],
                "daily_will_it_rain": day["day"]["daily_will_it_rain"],
                "daily_chance_of_rain": day["day"]["daily_chance_of_rain"],
                "daily_will_it_snow": day["day"]["daily_will_it_snow"],
                "daily_chance_of_snow": day["day"]["daily_chance_of_snow"],
                "condition_text": day["day"]["condition"]["text"],
                "condition_icon": "https:" + day["day"]["condition"]["icon"],
            }
        )
    df_meteo = pd.DataFrame(data_2)
    df_meteo["date"] = pd.to_datetime(df_meteo["date"])
    df_meteo["jour_fr"] = (
        df_meteo["date"]
        .apply(lambda d: pendulum.instance(d).format("dddd", locale="fr"))
        .str.title()
    )
    return df_meteo


def get_total_rain(data):
    """
    Calculate the total precipitation from the weather forecast data.
    """
    total_precipitation = 0
    for day in data["forecast"]["forecastday"]:
        total_precipitation += day["day"]["totalprecip_mm"]
    return total_precipitation
