import streamlit as st
from streamlit_cookies_controller import CookieController
import pandas as pd
import requests
import pendulum
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import helpers.import_manager as import_manager
import helpers.visual_manager as visual_manager


cookie_manager = CookieController()
ville_cookie = cookie_manager.get("ville")

if not ville_cookie:
    st.title(
        "Pour voir la météo, pense à sélectionner une ville dans la page d'accueil"
    )
    st.page_link("views/accueil.py", label="🏡 Accueil ↩")
    st.stop()

df = import_manager.get_df_cp()

df_ville = df[df["commune"] == ville_cookie] if ville_cookie else None
geopoint = df_ville.iloc[0][["geopoint"]].values if df_ville is not None else None

data = import_manager.get_meteo_data(geopoint)

st.markdown(
    f"""
    <h1 style='text-align: center; color: #57bb8a;font-family: "Economica";'>
        Le point météo de {ville_cookie if ville_cookie else "ta ville"}
    </h1>
    """,
    unsafe_allow_html=True,
)


df = import_manager.get_meteo_data_by_city(data)

df_meteo = import_manager.get_meteo_forecast(data)


st.markdown(
    """
<style>
.encart {
    background-color: rgba(167, 10, 10, 0.4);
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
else:
    st.markdown(
        f"""
    <div class="encart">
    <p style = 'text-align : center; font-size: 17px'> <strong> Pas d'alerte météo </strong> </p>
    </div>""",
        unsafe_allow_html=True,
    )
col1, col2, col3, col4 = st.columns(4)


with col3:
    st.write("")
    st.write("")
    st.html(
        """<h2 style='text-align: center; color: white;font-family: "Economica"' > Aujourd'hui </h2>"""
    )

with col2:
    st.image(df_meteo["condition_icon"][0], width=150)

# Inclure la police Open Sans depuis Google Fonts et definir les metrics et titres
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');
        .metric-title {
            font-family: 'Open Sans', sans-serif;
            font-size: 16px;
            font-weight: 600;
            text-align: center;
        }
        .metric-value {
            font-family: 'Open Sans', sans-serif;
            font-size: 20px;
            font-weight: 400;
            text-align: center;
        }
        .stMetric {
            text-align: center;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Création des 5 colonnes
col1, col2, col3, col4, col5 = st.columns(5)

# Affichage des éléments dans chaque colonne
with col1:
    st.markdown('<p class="metric-title">Température max</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="metric-value">{df_meteo["max_temp"][0]} °C</p>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown('<p class="metric-title">Température min</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="metric-value">{df_meteo["min_temp"][0]} °C</p>',
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        '<p class="metric-title">Taux<br>d\'humidité</p>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="metric-value">{df_meteo["avghumidity"][0]} %</p>',
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        '<p class="metric-title">Risque<br>de pluie</p>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="metric-value">{df_meteo["daily_chance_of_rain"][0]} %</p>',
        unsafe_allow_html=True,
    )
with col5:
    st.markdown(
        '<p class="metric-title">Quantité <br>de pluie</p>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="metric-value">{df_meteo["totalprecip_mm"][0]} mm</p>',
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border: 0.5px solid #57bb8a;'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col3:
    st.write("")
    st.write("")
    st.html(
        """<h2 style='text-align: center; color: white;font-family: "Economica"' > Demain </h2>"""
    )

with col2:
    st.image(df_meteo["condition_icon"][1], width=150)

# Création des 5 colonnes
col1, col2, col3, col4, col5 = st.columns(5)

# Affichage des éléments dans chaque colonne
with col1:
    st.markdown('<p class="metric-title">Température max</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="metric-value">{df_meteo["max_temp"][1]} °C</p>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown('<p class="metric-title">Température min</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="metric-value">{df_meteo["min_temp"][1]} °C</p>',
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        '<p class="metric-title">Taux<br>d\'humidité</p>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="metric-value">{df_meteo["avghumidity"][1]} %</p>',
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        '<p class="metric-title">Risque<br>de pluie</p>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="metric-value">{df_meteo["daily_chance_of_rain"][1]} %</p>',
        unsafe_allow_html=True,
    )
with col5:
    st.markdown(
        '<p class="metric-title">Quantité <br>de pluie</p>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="metric-value">{df_meteo["totalprecip_mm"][1]} mm</p>',
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border: 0.5px solid #57bb8a;'>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col3:
    st.write("")
    st.write("")
    st.html(
        f"""<h2 style='text-align: center; color: white;font-family: "Economica"' > {df_meteo['jour_fr'][2]} </h2>"""
    )

with col2:
    st.image(df_meteo["condition_icon"][2], width=150)


# Création des 5 colonnes
col1, col2, col3, col4, col5 = st.columns(5)

# Affichage des éléments dans chaque colonne
with col1:
    st.markdown('<p class="metric-title">Température max</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="metric-value">{df_meteo["max_temp"][2]} °C</p>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown('<p class="metric-title">Température min</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="metric-value">{df_meteo["min_temp"][2]} °C</p>',
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        '<p class="metric-title">Taux<br>d\'humidité</p>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="metric-value">{df_meteo["avghumidity"][2]} %</p>',
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        '<p class="metric-title">Risque<br>de pluie</p>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="metric-value">{df_meteo["daily_chance_of_rain"][2]} %</p>',
        unsafe_allow_html=True,
    )
with col5:
    st.markdown(
        '<p class="metric-title">Quantité <br>de pluie</p>', unsafe_allow_html=True
    )
    st.markdown(
        f'<p class="metric-value">{df_meteo["totalprecip_mm"][2]} mm</p>',
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border: 0.5px solid #57bb8a;'>", unsafe_allow_html=True)

##### Graphique précipitations

# graphique avec plotly.express
fig = visual_manager.plot_meteo_forecast(data)
st.plotly_chart(fig)


# Affichage du total de pluie
total_precipitation = import_manager.get_total_rain(data)
st.write(
    f"**Total de pluie estimé sur les 3 prochains jours : {total_precipitation} mm**"
)
