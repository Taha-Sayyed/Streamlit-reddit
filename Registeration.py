import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import date

# Load Firebase credentials
cred = credentials.Certificate("firestore-key.json")

# Initialize Firebase app (only once)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db=firestore.client()

st.write("Firebase Initialized Successfully ✅")


def create_user(email, password, first_name, middle_name, last_name, prn_no, phone_number, year_of_admission, year_of_graduation, birth_date, parent_name, parent_phone_number):
    if not email or not password:
        return "Error: Email and password are required."
    
    try:
        # ✅ Firebase Auth only takes email & password
        user = auth.create_user(email=email, password=password)
        uid = user.uid

        try:
            # ✅ Save all user details in Firestore
            user_doc = {
                "uid": uid,
                "email": email,
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "prn_no": prn_no,
                "phone_number": phone_number,
                "birth_date": str(birth_date),  # Convert date to string
                "year_of_admission": year_of_admission,
                "year_of_graduation": year_of_graduation,
                "parent_name": parent_name,
                "parent_phone_number": parent_phone_number
            }
            db.collection("users").document(uid).set(user_doc)

            return f"User {email} created successfully! ✅ (UID: {uid})"

        except Exception as e:
            return f"Firestore Error: {e}"
        
    except firebase_admin.exceptions.FirebaseError as e:
        return f"Firebase Error: {e}"
    except Exception as e:
        return f"Error: {e}"


# 🔹 Streamlit UI
email = st.text_input("Enter Email")
password = st.text_input("Enter Password", type="password")
first_name = st.text_input("Enter the First Name")
middle_name = st.text_input("Enter the Middle Name")
last_name = st.text_input("Enter the Last Name")
prn_no = st.text_input("Enter PRN Number")
phone_number = st.text_input("Enter Phone Number")

years = list(range(2020, 2031))  # Create a list of years
year_of_admission = st.selectbox("Select Year of Admission", years)

# Ensure graduation year is AFTER admission year
if year_of_admission:
    graduation_years = [y for y in years if y >= year_of_admission]
    year_of_graduation = st.selectbox("Select Year of Graduation", graduation_years)
else:
    year_of_graduation = st.selectbox("Select Year of Graduation", years)  # Default case

default_date = date(2000, 1, 1)
birth_date = st.date_input("Select Your Birth Date", min_value=date(1995, 1, 1), max_value=date.today(), value=default_date)

parent_name = st.text_input("Enter Parent Name")
parent_phone_number = st.text_input("Enter Parent Phone Number")

# 🔹 Register Button
if st.button("Register"):
    result = create_user(
        email, password, first_name, middle_name, last_name, 
        prn_no, phone_number, year_of_admission, 
        year_of_graduation, birth_date, parent_name, parent_phone_number
    )
    st.write(result)

st.warning("Register with a valid Email ID for future updates.")