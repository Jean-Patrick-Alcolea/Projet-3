import streamlit as st
import pandas as pd


def get_df_plantes():
    if "df_plantes" not in st.session_state:
        df_plantes = pd.read_parquet(
            "data/df_plantes_w_calendrier.gzip",
        )
        st.session_state["df_plantes"] = df_plantes
    else:
        df_plantes = st.session_state["df_plantes"]
    return df_plantes


df_plantes = get_df_plantes()
st.dataframe(df_plantes)


st.markdown(
    """
<style>
.st-emotion-cache-11byp7q {border : 1px solid #57bb8a}
.st-emotion-cache-11byp7q:hover {
border-color: #FFFFFF;
color: #57bb8a;
}
.st-dr {
    background-color: #57bb8a;}
.st-cs{border-bottom-color: #57bb8a;}
.st-cr{border-top-color: #57bb8a;}
.st-cq{border-right-color: #57bb8a;}
.st-cp{border-left-color: #57bb8a;}

@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');
        .metric-title {
            font-family: 'Open Sans', sans-serif;
            font-size: 16px;
            font-weight: 600;
            text-align: center;
        }
        .metric-value {
            font-family: 'Open Sans', sans-serif;
            font-size: 15px;
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

if st.query_params.get("page") == "detail":
    id_plante = int(st.query_params.get("selected_plant"))
    selected_plant = df_plantes.loc[id_plante]
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
        "Elevé": "20 à 40 L/m²/semaine",
    }

    col1, col2 = st.columns(2)
    with col1:
        st.image(selected_plant["image_y"], width=500)
    with col2:
        st.markdown(f"**Type** : *{selected_plant['Type']}*")
        if not pd.isna(selected_plant["Exposition"]):
            st.markdown(f" **Exposition** : *{selected_plant["Exposition"]}*")
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
        if not pd.isna(selected_plant["Calendrier des semis"]):
            st.markdown(
                f"**Calendrier des semis** : *{selected_plant['Calendrier des semis']}*"
            )
        if not pd.isna(selected_plant["Calendrier des récoltes"]):
            st.markdown(
                f"**Calendrier des récoltes** : *{selected_plant['Calendrier des récoltes']}*"
            )


# insérer des filtres
# par types de plantes

type = st.multiselect(
    "Filtrer par type de plantes", df_plantes["Type"].unique().tolist()
)

if type:
    df_plantes = df_plantes[df_plantes["Type"].isin(type)]
# barre de recherche
search = st.text_input(
    "Rechercher une plante par son nom", placeholder="Entrez le nom de la plante"
)
if search:
    df_plantes = df_plantes[
        df_plantes["Nom"].str.contains(search, case=False, na=False)
    ]

# recherche par mois de semis
Mois = [
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
reponse = st.multiselect("Mois de semis", Mois)
if reponse:
    df_plantes = df_plantes[
        df_plantes["Calendrier_Semis"].apply(lambda x: reponse in x)
    ]

# recherche par mois de recolte
# Mois = ["Tous","janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
# reponse_recol = st.radio("Mois de récolte", Mois, horizontal=True)
# if reponse_recol == "Tous":
#  df_plantes = get_df_plantes()
# else:
#  df_plantes = df_plantes[df_plantes["Calendrier_Recolte"].apply(lambda x: reponse_recol in x)]

# pagination

items_per_page = 30

total_pages = (len(df_plantes) - 1) // items_per_page + 1

if "page_key" not in st.session_state:
    st.session_state["page_key"] = 1

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
page_df = df_plantes.iloc[start_idx:end_idx]
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
