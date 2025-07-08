import streamlit as st
import pandas as pd
import helpers.import_manager as import_manager
from streamlit_cookies_controller import CookieController

cookie_manager = CookieController()
ville_cookie = cookie_manager.get("ville")

st.markdown(
    """
    <h1 style='text-align: center; color: teal;'>
        TITRE
    </h1>
    """,
    unsafe_allow_html=True,
)

df = import_manager.get_df_cp()

st.dataframe(df)

CP = st.selectbox(
    options=df["code_postal"].unique(),
    placeholder="Code Postal",
    label="Saisis ton code postal :",
)
ville = None
if CP:
    villes = df[df["code_postal"] == CP]
    if len(villes) > 1:
        ville = st.selectbox(
            options=villes["commune"], label="Sélectionne ta commune : "
        )
    else:
        ville = villes["commune"].iloc[0]

if ville:
    st.write(ville)

if st.button("Enregistrer ma ville"):
    cookie_manager.set("ville", ville)
