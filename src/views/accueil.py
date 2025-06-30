import streamlit as st
import pandas as pd
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

if "df" not in st.session_state:
    df = pd.read_parquet("data/codes_postaux_final.gzip")
    st.session_state["df"] = df
else:
    df = st.session_state["df"]

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
