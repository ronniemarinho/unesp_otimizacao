import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

st.write("Python funcionando")

try:

    if not firebase_admin._apps:

        firebase_config = json.loads(
            st.secrets["firebase"]
        )

        cred = credentials.Certificate(
            firebase_config
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

    st.success("Firebase OK")

    st.write(dados)

except Exception as e:

    st.error(e)
