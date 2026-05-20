import streamlit as st
import firebase_admin
from firebase_admin import credentials

try:

    if not firebase_admin._apps:

        cred = credentials.Certificate(dict(st.secrets["firebase"]))

        firebase_admin.initialize_app(cred)

    st.success("Firebase autenticado com sucesso!")

except Exception as e:
    st.error(e)
