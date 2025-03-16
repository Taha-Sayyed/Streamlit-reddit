import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Load Firebase credentials
cred = credentials.Certificate("firestore-key.json")

# Initialize Firebase app (only once)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

st.write("Firebase Initialized Successfully ✅")


def create_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return f"User {email} created successfully! ✅"
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
email = st.text_input("Enter Email")
password = st.text_input("Enter Password", type="password")
if st.button("Register"):
    st.write(create_user(email, password))
