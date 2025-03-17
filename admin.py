import firebase_admin
from firebase_admin import credentials,firestore
import streamlit as st
import json
import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()
api_key=os.getenv('API_KEY')
admin_gmail=os.getenv('ADMIN_GMAIL')

# Login ----------------------------------------------------------------------------------


# Function to authenticate user
def login_user(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, data=json.dumps(payload))
    return response.json()

# Streamlit UI
st.title("Firebase Authentication with Streamlit")

# If user is already logged in, show welcome message
if "user" in st.session_state:
    st.write(f"👋 Welcome Admin {st.session_state['user']['email']}")
    
    # Logout Button
    if st.button("Logout"):
        del st.session_state["user"]  # Remove session data
        st.rerun()  # Refresh app to update UI

else:
    # Login UI
    email = st.text_input("Enter Email")
    password = st.text_input("Enter Password", type="password")
    
    if st.button("Login"):
        result = login_user(email, password)
        
        if "idToken" in result:
            st.session_state["user"] = {"email": email, "idToken": result["idToken"]}  # Store session
            st.rerun()  # Refresh app to update UI
        else:
            st.write("❌ Login Failed:", result.get("error", {}).get("message", "Unknown error"))


# Login ----------------------------------------------------------------------------------
#Intialize firebase admin SDK
if not firebase_admin._apps:  # Prevent re-initialization error
    cred = credentials.Certificate("firestore-key.json")
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


#✅ Fetch Notifications from Firestore
#We’ll create a function to retrieve notifications from the Firestore "notifications" collection.

def get_notifications():
    docs = db.collection("notifications").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
    return [
        {
            "id": doc.id,  
            "sender": doc.to_dict()["sender"], 
            "message": doc.to_dict()["message"], 
            "timestamp": doc.to_dict().get("timestamp"),
            "status": doc.to_dict().get("status", "unread")
        } 
        for doc in docs
    ]

#We'll modify each notification in Firestore by adding a status field (e.g., unread → read).

def mark_as_read(notification_id):
    db.collection("notifications").document(notification_id).update({"status": "read"})

#We'll allow the admin to remove notifications they no longer need.

def delete_notification(notification_id):
    db.collection("notifications").document(notification_id).delete()



#Display Notifications in the Streamlit UI
# Streamlit UI for Admin

st.title("Admin Dashboard - View Notifications")



if "user" in st.session_state and st.session_state["user"]["email"] == admin_gmail:  # Replace with admin email
    
    notifications = get_notifications()

    if st.button("Refresh Notifications"):
        st.rerun()
    if notifications:
        st.subheader("📩 Notifications")
        for note in notifications:
            with st.expander(f"📧 From: {note['sender']} (Status: {note['status']})"):
                st.write(f"💬 Message: {note['message']}")
                st.write(f"⏰ Time: {note['timestamp']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if note["status"] == "unread":
                        if st.button(f"✅ Mark as Read", key=f"read_{note['id']}"):
                            mark_as_read(note["id"])
                            st.rerun()
                with col2:
                    if st.button(f"🗑️ Delete", key=f"del_{note['id']}"):
                        delete_notification(note["id"])
                        st.rerun()
                st.markdown("---")
    else:
        st.write("🎉 No new notifications!")        
                
else:
    st.warning("⚠️ You must be logged in as an admin to view notifications.")
