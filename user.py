import firebase_admin
from firebase_admin import credentials,firestore
import streamlit as st
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key=os.getenv('API_KEY')

#Intialize firebase admin SDK
if not firebase_admin._apps:  # Prevent re-initialization error
    cred = credentials.Certificate("firestore-key.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


#This function allows a user to send a notification to the admin.
def send_notification(sender_email, message):
    doc_ref = db.collection("notifications").add({
        "sender": sender_email,
        "message": message,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    return doc_ref


#Store Notifications from Streamlit UI
# Streamlit UI
st.title("Send Notification to Admin")

email = st.text_input("Your Email")
message = st.text_area("Enter Your Message")

if st.button("Send Notification"):
    if email and message:
        send_notification(email, message)
        st.success("✅ Notification Sent!")
    else:
        st.warning("⚠️ Please enter both email and message.")

