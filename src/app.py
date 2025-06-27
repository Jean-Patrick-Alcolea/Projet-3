import streamlit as st


# **Page Config**
accueil = st.Page(page="views/accueil.py", title="Accueil", icon="🏡", default=True)

reche = st.Page(page="views/recherche.py", title="Recherche", icon="🔎")

jard = st.Page(page="views/mon_jardin.py", title="Mon jardin", icon="👨‍🌾")

meteo = st.Page(page="views/meteo.py", title="Météo", icon="🌈")

# **Navigation setup**


pg = st.navigation(pages=[accueil, reche, jard, meteo])

pg.run()
