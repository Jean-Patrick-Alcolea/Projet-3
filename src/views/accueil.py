import streamlit as st
import pandas as pd

st.markdown(
    """
    <h1 style='text-align: center; color: teal;'>
        TITRE
    </h1>
    """,
    unsafe_allow_html=True,
)

if "df" not in st.session_state:
    df = pd.read_parquet("../data/)
    st.session_state["df"] = df
else:
    df = st.session_state["df"]