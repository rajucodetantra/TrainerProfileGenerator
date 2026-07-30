import streamlit as st


def check_login():

    USERNAME = st.secrets["USERNAME"]
    PASSWORD = st.secrets["PASSWORD"]

    if st.session_state.get("logged_in", False):
        return True

    st.title("🔒 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    return False