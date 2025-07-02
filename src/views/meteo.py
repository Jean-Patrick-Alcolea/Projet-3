import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests
import pendulum
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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
    <h1 style='text-align: center; color: dodgerblue;'>
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

st.markdown(
    """
<style>
.encart {
    background-color: #A70A0A;
    padding-top: 1px;
    padding-bottom: 0px;
    border-radius: 5px;
}
</style>
""",
    unsafe_allow_html=True,
)

if df["alert"][0] != "No alert":
    st.markdown(
        f"""
    <div class="encart">
    <p style = 'text-align : center; font-size: 17px'> <strong> Alerte météo {df['alert_severity'][0]} </strong> : {df["alert"][0]} </p>
    </div>""",
        unsafe_allow_html=True,
    )

col1, col2, col3, col4 = st.columns(4)


with col2:
    st.write("")
    st.write("")
    st.html("""<h2 style='text-align: center; color: white' > Aujourd'hui </h2>""")

with col3:
    st.image(df_meteo["condition_icon"][0], width=150)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Temperature max", f"{df_meteo["max_temp"][0]} °C")
with col2:
    st.metric("Temperature min", f"{df_meteo["min_temp"][0]} °C")
with col3:
    st.metric(f"""Risque de pluie""", f"""{df_meteo["daily_chance_of_rain"][0]} %""")
with col4:
    st.metric("Taux d'humidité", f"{df_meteo['avghumidity'][0]} %")

col1, col2, col3, col4 = st.columns(4)
with col3:
    if df_meteo["daily_chance_of_rain"][0] > 0:
        st.metric("Précipitations", f"""{df_meteo["totalprecip_mm"][0]}mm""")
with col3:
    if df_meteo["daily_chance_of_snow"][0] > 0:
        st.metric("Risque de neige", f"""{df_meteo["daily_chance_of_snow"][0]} %""")

st.write("---")

col1, col2, col3, col4 = st.columns(4)


with col2:
    st.write("")
    st.write("")
    st.html("""<h2 style='text-align: center; color: white' > Demain </h2>""")

with col3:
    st.image(df_meteo["condition_icon"][1], width=150)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Temperature max", f"{df_meteo["max_temp"][1]} °C")
with col2:
    st.metric("Temperature min", f"{df_meteo["min_temp"][1]} °C")
with col3:
    st.metric(f"""Risque de pluie""", f"""{df_meteo["daily_chance_of_rain"][1]} %""")
with col4:
    st.metric("Taux d'humidité", f"{df_meteo['avghumidity'][1]} %")

col1, col2, col3, col4 = st.columns(4)
with col3:
    if df_meteo["daily_chance_of_rain"][1] > 0:
        st.metric("Précipitations", f"""{df_meteo["totalprecip_mm"][1]}mm""")
with col4:
    if df_meteo["daily_chance_of_snow"][1] > 0:
        st.metric("Risque de neige", f"""{df_meteo["daily_chance_of_snow"][1]} %""")

st.write("---")

col1, col2, col3, col4 = st.columns(4)

list_col = [col1, col2, col3, col4]

for i, col in enumerate(list_col):
    with col:
        st.html(
            f"""<p style='text-align: center; color: white; font-size: 18px; margin-bottom: 0' > {df_meteo["jour_fr"][i+2]} </p>"""
        )
        st.html(
            f"""<div style = "text-align : center;"> <img style = "height: 150px" src = "{df_meteo["condition_icon"][i+2]}" </div>"""
        )
        st.html(
            f"""<p style='text-align: center; color: white' > <strong>{df_meteo['max_temp'][i+2]} °</strong>  <i> {df_meteo['min_temp'][i+2]} °</i></p>"""
        )


##### Graphique précipitations

# graphique avec plotly.express
fig = px.area(
    df_meteo,
    x="jour_fr",
    y="totalprecip_mm",
    labels=False,
    title="Prévisions des précipitations (en mm)",
)
fig.update_layout(xaxis_title=None, yaxis_title=None)
fig.update_traces(
    line_color="dodgerblue",
    fillcolor="rgba(30, 144, 255, 0.4)",  # dodgerblue en semi-transparent
)
st.plotly_chart(fig)
