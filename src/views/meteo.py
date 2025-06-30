import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests

cookie_manager = CookieController()
ville_cookie = cookie_manager.get("ville")

if "df" not in st.session_state:
    df = pd.read_parquet("data/codes_postaux_final.gzip")
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

df_ville = df[df["commune"] == ville_cookie] if ville_cookie else None
geopoint = df_ville.iloc[0][["geopoint"]].values if df_ville is not None else None

params = {
    "key": "2fbbaab3e35841d5ba0125329251906",
    "q": geopoint,
    "days": 7,
    "alerts": "yes",
}

url2 = "http://api.weatherapi.com/v1/forecast.json"
response2 = requests.get(url2, params=params)
print(response2.status_code)
data = response2.json()

st.markdown(
    f"""
    <h1 style='text-align: center; color: teal;'>
        Le point météo de {ville_cookie if ville_cookie else "ta ville"}
    </h1>
    """,
    unsafe_allow_html=True,
)


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
            "condition_icon": day["day"]["condition"]["icon"],
        }
    )
df_meteo = pd.DataFrame(data_2)
df_meteo["date"] = pd.to_datetime(df_meteo["date"])
st.dataframe(df_meteo)
st.dataframe(df)
