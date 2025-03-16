# Login Users Using REST API in Streamlit:
# from dotenv import load_dotenv
# import os
# import requests
# import json
# import streamlit as st

# load_dotenv()
# api_key=os.getenv('API_KEY')

# def login_user(email, password):
#     url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
#     payload = {"email": email, "password": password, "returnSecureToken": True}
#     response = requests.post(url, data=json.dumps(payload))
#     return response.json()

# # Streamlit UI
# email = st.text_input("Enter Email")
# password = st.text_input("Enter Password", type="password")
# if st.button("Login"):
#     result = login_user(email, password)
#     if "idToken" in result:
#         st.session_state["user"] = result  # Store session
#         st.write(f"✅ Logged in as {email}")
#     else:
#         st.write("❌ Login Failed:", result.get("error", {}).get("message", "Unknown error"))


from dotenv import load_dotenv
import os
import requests
import json
import streamlit as st

# Load API Key from .env file
load_dotenv()
api_key = os.getenv('API_KEY')

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
    st.write(f"👋 Welcome, {st.session_state['user']['email']}")
    
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
