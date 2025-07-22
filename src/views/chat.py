import google.generativeai as genai
import streamlit as st
import pandas as pd
from streamlit_cookies_controller import CookieController
import helpers.import_manager as import_manager

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")


def get_df_plantes():
    if "df_plantes" not in st.session_state:
        df_plantes = pd.read_parquet("data/df_plantes_clean.gzip")
        st.session_state["df_plantes"] = df_plantes
    else:
        df_plantes = st.session_state["df_plantes"]
    return df_plantes


df_plantes = get_df_plantes()
df_ville = import_manager.get_df_cp()

# ***************Cookies****************
cookie_manager = CookieController()
mon_jardin_cookie = cookie_manager.get("mon_jardin")
ville_cookie = cookie_manager.get("ville")
# ***************************************
df_ville = df_ville[df_ville["commune"] == ville_cookie] if ville_cookie else None
geopoint = df_ville.iloc[0][["geopoint"]].values if df_ville is not None else None

data = import_manager.get_meteo_data(geopoint)
total_rain = import_manager.get_total_rain(data)


summary = [
    f" La ville où est le jardin {ville_cookie}, les informations météo sur les 3 derniers jours {data}, les plantes de mon jardin {mon_jardin_cookie} et les plantes de la base de données {df_plantes}."
]


def submit():
    user_input = st.session_state.user_prompt
    if user_input:
        # Ici tu appelles ton chatbot
        response = st.session_state.chat.send_message(user_input)
        st.session_state.history.append(("User", user_input))
        st.session_state.history.append(("Pommtastique 🍏", response.text))
        st.session_state.user_prompt = ""


if "chat" not in st.session_state:

    st.session_state.chat = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Tu es un expert en jardinage et en météo. Tu vas m'aider à choisir ou entretenir les plantes de mon jardin."
                    "Réponds de manière concise et précise, en te basant sur les données fournies."
                    "Réponds de façon bienveillante et amicale."
                    "réponds avec un peu d'argot de la région de la ville {ville_cookie}."
                    "Propose des idées de recettes en fonction des plantes de mon jardin"
                    "Si il y a des plantes avec des propriétés médicinales, propose des remèdes naturels."
                ],
            },
            {"role": "user", "parts": summary},
        ]
    )

if "history" not in st.session_state:
    st.session_state.history = []

# ******************Mise en page******************
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("src/img/plantastique_logo.png", use_container_width=True)

st.write(f"Pommtastique 🍏, ton jardinier virtuel, sait que tu es à {ville_cookie} !")
st.write(f"Il a déjà repéré tes plantes : {mon_jardin_cookie}.")
st.write(
    "Ps : il peut te conseiller tant sur le jardinage que sur la dégustation qui va suivre!"
)


# *******************Chat Interface******************
user_input = st.text_input(
    "Discute avec ton jardinier virtuel Pommtastique 🍏",
    key="user_prompt",
    on_change=submit,
)
if user_input:
    response = st.session_state.chat.send_message(user_input)
    st.session_state.history.append(("User", user_input))
    st.session_state.history.append(("Pommtastique 🍏", response.text))


for sender, message in st.session_state.history:
    if sender == "User":
        st.markdown(f"**Toi :** {message}")
    else:
        st.markdown(f"**Pommtastique 🍏 :** {message}")

clear_button = st.button("Effacer la conversation")
if clear_button:
    for key in ["history", "chat"]:
        if key in st.session_state:
            del st.session_state[key]
    st.cache_data.clear()
    st.rerun()
