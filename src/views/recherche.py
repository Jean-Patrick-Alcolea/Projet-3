import streamlit as st
import pandas as pd
import difflib


def get_df_plantes():
    if "df_plantes" not in st.session_state:
        df_plantes = pd.read_csv("data/df_plantes_final_url.csv")
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
</style>
""",
    unsafe_allow_html=True,
)


# insérer des filtres
# par types de plantes
import streamlit as st

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

            st.button(
                row.Nom,
                key=row.Index,
                on_click=lambda x=row.Index: st.session_state.update(
                    {"selected_plant": x}
                ),
                use_container_width=True,
            )
            st.write("")
            st.write("")
