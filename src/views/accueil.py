import streamlit as st
import pandas as pd
import time
import helpers.import_manager as import_manager
from streamlit_cookies_controller import CookieController

cookie_manager = CookieController()
ville_cookie = cookie_manager.get("ville")

df = import_manager.get_df_cp()

st.markdown(
    """
    <h1 style='text-align: center; font-size: 40px;'>
        Bienvenue sur
    </h1>
    """,
    unsafe_allow_html=True,
)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("src/img/plantastique_logo.png", use_container_width=True)
st.markdown(
    """
    <p style='text-align: justify; font-size: 20px;'>
        Découvrez nos conseils personnalisés et nos astuces pratiques pour jardiner facilement
        selon le climat et les particularités de votre région. Que vous soyez débutant ou passionné,
        cultivez un jardin qui vous ressemble !
    </p>
    """,
    unsafe_allow_html=True,
)
st.markdown("<hr style='border: 1px solid #57bb8a;'>", unsafe_allow_html=True)
st.markdown(
    f"""
    <p style='text-align: center; font-size: 20px;'>
        Ville enregistrée : {ville_cookie}
    </p>
    """,
    unsafe_allow_html=True,
)
CP = st.selectbox(
    options=df["code_postal"].unique(),
    placeholder="Sélectionne ton code postal",
    index=None,
    label="Saisis ton code postal :",
    label_visibility="hidden",
)
ville = None
unique_villes = df[df["code_postal"] == CP]["commune"].unique()
if CP:
    villes = df[df["code_postal"] == CP]
    if len(villes) > 1 and unique_villes.size > 1:
        ville = st.selectbox(
            options=villes["commune"],
            label="Sélectionne ta commune : ",
            placeholder="Sélectionne ta commune",
            index=None,
            label_visibility="hidden",
        )
    else:
        ville = villes["commune"].iloc[0]
col1, col2, col3 = st.columns(3)
with col2:
    if ville:
        if st.button("Enregistre ta ville", use_container_width=True):
            cookie_manager.set("ville", ville)
            st.success(f"Ville {ville} enregistrée avec succès !")
            time.sleep(1)
            st.rerun()
