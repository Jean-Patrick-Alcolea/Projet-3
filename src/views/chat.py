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
cp_cookie = cookie_manager.get("CP")
if not ville_cookie:
    st.title(
        "Pour parler avec Pommtastique 🍏, pense à sélectionner une ville dans la page d'accueil"
    )
    st.page_link("views/accueil.py", label="🏡 Accueil ↩")
    st.stop()
# ***************************************
df_ville = df_ville.iloc[int(cp_cookie)] if cp_cookie else None
geopoint = df_ville[["geopoint"]].values if df_ville is not None else None

data = import_manager.get_meteo_data(geopoint)
total_rain = import_manager.get_total_rain(data)


summary = [
    f" La ville où est le jardin {ville_cookie}, les informations météo sur les 3 derniers jours {data}, les plantes de mon jardin {mon_jardin_cookie} et les plantes de la base de données {df_plantes}."
]


def submit():
    st.session_state.submitted = True


st.session_state.chat = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                f"Tu es un expert en jardinage et en météo. Tu vas m'aider à choisir ou entretenir les plantes de mon jardin."
                f"Réponds de manière concise et précise, en te basant sur les données fournies."
                f"Réponds de façon bienveillante et amicale."
                f"réponds avec un peu d'argot de la région de la ville {ville_cookie}."
                f"Propose des idées de recettes en fonction des plantes de mon jardin"
                f"Si il y a des plantes avec des propriétés médicinales, propose des remèdes naturels."
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
with st.chat_message("user"):
    user_input = st.text_input(
        "Discute avec ton jardinier virtuel Pommtastique 🍏",
        key="user_prompt",
        on_change=submit,
    )

if st.session_state.get("user_prompt") and st.session_state.get("submitted", False):
    prompt_to_process = st.session_state.user_prompt

    response = st.session_state.chat.send_message(prompt_to_process)

    # Enregistrer dans l'historique, mais ne pas réafficher ici
    st.session_state.history.append(("user", prompt_to_process))
    st.session_state.history.append(("assistant", response.text))

    st.session_state.submitted = False


# Rejoue l’historique
for sender, message in st.session_state.history:
    with st.chat_message(sender):
        st.write(message)


clear_button = st.button("Effacer la conversation")
if clear_button:
    for key in ["history", "chat"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
