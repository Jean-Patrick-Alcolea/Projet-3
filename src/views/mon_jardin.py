import streamlit as st
import pandas as pd
import time
from streamlit_cookies_controller import CookieController
import helpers.import_manager as import_manager


def get_df_plantes():
    if "df_plantes" not in st.session_state:
        df_plantes = pd.read_parquet("data/df_plantes_clean.gzip")
        st.session_state["df_plantes"] = df_plantes
    else:
        df_plantes = st.session_state["df_plantes"]
    return df_plantes


current_view = "mon_jardin"

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


history_rain = import_manager.history_meteo(geopoint)
history_rain = import_manager.get_total_rain(history_rain)
total_rain += history_rain

mon_jardin = mon_jardin_cookie.split(",") if mon_jardin_cookie else []

df_mon_jardin = df_plantes[df_plantes["Nom"].isin(mon_jardin)]
sol_ville = df_ville.iloc[0]["Grands types de sols"]


def arrosage(besoins_en_eau, sol, total_rain):
    if besoins_en_eau == "Faible":
        arrosage = [5, 10]
    elif besoins_en_eau == "Moyen":
        arrosage = [10, 20]
    else:
        arrosage = [20, 40]

    if ("Sableux, Argileux") == sol:
        arrosage = (arrosage[0] + arrosage[1]) / 2
    elif "Argileux" == sol:
        arrosage = arrosage[0]
    elif "Sableux" == sol:
        arrosage = arrosage[1]
    else:
        arrosage = (arrosage[0] + arrosage[1]) / 2

    return arrosage - total_rain


df_mon_jardin["Arrossage"] = df_mon_jardin["Besoin en eau"].apply(
    lambda x: arrosage(x, sol_ville, total_rain)
)
# ******************titre****************
st.markdown(
    f"""
    <h1 style='text-align: center; color: #57bb8a;font-family: "Economica";'>
        Mon jardin 👨‍🌾
          </h1>
    """,
    unsafe_allow_html=True,
)

# ************detail plante************
if st.query_params.get("page") == "detail":

    id_plante = int(st.query_params.get("selected_plant"))
    selected_plant = df_mon_jardin.loc[id_plante]
    ############### TITRE ################
    st.html(
        f"""<h2 style='text-align: center; color: white;font-family: "Economica"' > {selected_plant["Nom"]} </h2> """
    )

    zone_climat = {
        "H1": "Continental ou Montagnard",
        "H2": "Océanique",
        "H3": "Méditerranéen",
    }

    besoin_eau = {
        "Moyen": "10 à 20 L/m²/semaine",
        "Faible": " 5 à 10 L/m²/semaine",
        "Élevé": "20 à 40 L/m²/semaine",
    }
    if mon_jardin_cookie:
        mon_jardin = mon_jardin_cookie.split(",")
    else:
        mon_jardin = []
    col1, col2 = st.columns(2)
    with col2:

        st.markdown('<div class="centered-image">', unsafe_allow_html=True)
        st.image(f"{selected_plant['image_y']}", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        if sol_ville is not None:

            st.markdown(
                f"<p style='text-align: left; color: #57bb8a;'>Sol de votre ville : {sol_ville} </p>",
                unsafe_allow_html=True,
            )

        if not pd.isna(selected_plant["Arrossage"]):
            if selected_plant["Arrossage"] > 0:
                st.markdown(
                    f"<p style='text-align: left; color: #57bb8a;'>Au regard de l'historique et des prévisions météo pour cette semaine : </p>\n\n <p style='text-align: left; color: #57bb8a;'> Arrosage nécessaire : {int(selected_plant['Arrossage'])} L/m²</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<p style='text-align: left; color: #57bb8a;'>Pas besoin d'arrosage supplémentaire cette semaine ! 🌧️</p>",
                    unsafe_allow_html=True,
                )
        if mon_jardin_cookie and selected_plant["Nom"] in mon_jardin:
            if st.button(
                "Supprimer de mon jardin 🗑️",
                key=selected_plant["Nom"],
                use_container_width=True,
            ):
                mon_jardin.remove(selected_plant["Nom"])
                cookie_manager.set("mon_jardin", ",".join(mon_jardin))
                st.success(
                    f"{selected_plant['Nom']} a été supprimé de votre jardin ! 🗑️",
                    icon="✅",
                )
                st.query_params.clear()
                time.sleep(2)
                st.rerun()
        elif st.button(
            "Ajouter à mon jardin 👨‍🌾",
            key=selected_plant["Nom"],
            use_container_width=True,
        ):
            mon_jardin.append(selected_plant["Nom"])
            mon_jardin = list(set(mon_jardin))
            cookie_manager.set("mon_jardin", ",".join(mon_jardin))
            st.success(
                f"{selected_plant['Nom']} a été ajouté à votre jardin ! 🌱",
                icon="✅",
            )

    with col1:
        st.markdown(f"**Type** : *{selected_plant['Type']}*")
        if not pd.isna(selected_plant["Exposition"]):
            st.markdown(f" **Exposition** : *{selected_plant['Exposition']}*")
        st.markdown(f"**Rusticité** : *{selected_plant['Rusticité']}*")
        if not pd.isna(selected_plant["Profondeur"]):
            st.markdown(
                f"**Profondeur de semis** : *{selected_plant['Profondeur']} cm*"
            )
        if not pd.isna(selected_plant["Espacement"]):
            st.markdown(f"**Espacement** : *{selected_plant['Espacement']} cm*")
        if not pd.isna(selected_plant["Temps_levée"]):
            st.markdown(
                f"**Temps de levée** : *{int(selected_plant['Temps_levée'])} jours*"
            )
        if not pd.isna(selected_plant["Temperature"]):
            st.markdown(
                f"**Temperature de levée** : *{int(selected_plant['Temperature'])} °C*"
            )
        if not pd.isna(selected_plant["delai_recolte"]):
            st.markdown(
                f"**Delai de recolte** : *{int(selected_plant['delai_recolte'])} jours*"
            )
        if not pd.isna(selected_plant["Zone climatique idéale"]):
            zone = selected_plant["Zone climatique idéale"].split(", ")
            climat = []
            for z in zone:
                climat.append(zone_climat[z])
            st.markdown(f"**Zone climatique idéale** : *{', '.join(climat)}*")
        if not pd.isna(selected_plant["Sol requis"]):
            st.markdown(f"**Sol requis** : *{selected_plant['Sol requis']}*")

        if not pd.isna(selected_plant["Besoin en eau"]):
            st.markdown(
                f"**Besoin en eau** : *{selected_plant['Besoin en eau']} ({besoin_eau[selected_plant['Besoin en eau']]})*"
            )
    st.markdown("<hr style='border: 0.5px solid #57bb8a;'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        ##### CALENDRIER#####
        mois = [
            "jan",
            "fév",
            "mar",
            "avr",
            "mai",
            "jui",
            "juil",
            "aoû",
            "sep",
            "oct",
            "nov",
            "déc",
        ]
        mois_complet = [
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "décembre",
        ]

        def render_calendar(semis):
            row = ""
            for m in mois_complet:
                if m in semis:
                    row += f"<td style='background-color: #57bb8a; width: 25px; height: 20px;'></td>"
                else:
                    row += f"<td style='background-color: #eee; width: 25px; height: 20px;'></td>"
            return row

        semis = selected_plant["Calendrier_Semis"]
        st.markdown(f"<strong>Périodes de semis </strong>", unsafe_allow_html=True)

        html = f"""
            <table style='border-collapse: collapse;'>
                <tr>{"".join([f"<th style='padding: 2px; font-size: 12px;'>{m.capitalize()}</th>" for m in mois])}</tr>
                <tr>{render_calendar(semis)}</tr>
            </table>
            """
        st.markdown(html, unsafe_allow_html=True)
        st.write("")
    with col2:
        #### RECOLTE #####
        recolte = selected_plant["Calendrier_Recolte"]
        st.markdown(f"<strong>Périodes de récolte </strong>", unsafe_allow_html=True)

        html = f"""
            <table style='border-collapse: collapse;'>
                <tr>{"".join([f"<th style='padding: 2px; font-size: 12px;'>{m.capitalize()}</th>" for m in mois])}</tr>
                <tr>{render_calendar(recolte)}</tr>
            </table>
            """
        st.markdown(html, unsafe_allow_html=True)


st.markdown("<hr style='border: 1px solid #57bb8a;'>", unsafe_allow_html=True)
################


# ************Afichage des plantes du jardin************
# pagination

items_per_page = 30

total_pages = (len(df_mon_jardin) - 1) // items_per_page + 1


if "last_view" not in st.session_state:
    st.session_state["last_view"] = current_view
    st.session_state["page_key"] = 1
elif st.session_state["last_view"] != current_view:
    st.session_state["page_key"] = 1
    st.session_state["last_view"] = current_view

st.write("")
st.write("")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if (
        st.button("◀︎ Avant", use_container_width=True)
        and st.session_state["page_key"] > 1
    ):
        st.session_state["page_key"] -= 1
with col5:
    if (
        st.button("Suivant ▶︎", use_container_width=True)
        and st.session_state["page_key"] < total_pages
    ):
        st.session_state["page_key"] += 1

with col3:
    st.markdown(
        f"<div style='text-align: center;'>Page {st.session_state['page_key']} sur {total_pages}</div>",
        unsafe_allow_html=True,
    )

current_page = st.session_state["page_key"]
start_idx = (current_page - 1) * items_per_page
end_idx = start_idx + items_per_page
page_df = df_mon_jardin.iloc[start_idx:end_idx]
images_per_row = 5


for i in range(0, len(page_df), images_per_row):
    cols = st.columns(images_per_row)
    for idx, row in enumerate(page_df[i : i + images_per_row].itertuples()):
        with cols[idx]:

            st.image(row.image_y)

            if st.button(
                row.Nom,
                key=row.Index,
                on_click=lambda x=row.Index: st.session_state.update(
                    {"selected_plant": x}
                ),
                use_container_width=True,
            ):
                st.query_params.update({"page": "detail", "selected_plant": row.Index})
                st.rerun()
            st.write("")
            st.write("")
