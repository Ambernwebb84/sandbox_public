import streamlit as st
import requests

st.title("Question generator")

subject = st.selectbox("Select subject", ["Physics", "General", "Language"])

if subject == "Physics":

    user_input = st.text_input("Enter concept name")

    if user_input != "":
    
        response = requests.get(f"https://physwikiquiz.wmflabs.org/api/v1?name={user_input}")

        st.write(response.json())

elif subject == "General":

    user_input = st.text_input("Enter text")