import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

try:

    if not firebase_admin._apps:

        cred = credentials.Certificate(
            dict(st.secrets["firebase"])
        )

        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL":
                "https://esp32-fe8e3-default-rtdb.firebaseio.com/"
            }
        )

    ref = db.reference("/")

    dados = ref.get()

    st.success("Conectado!")

    st.write(dados)

except Exception as e:

    st.error(e)
