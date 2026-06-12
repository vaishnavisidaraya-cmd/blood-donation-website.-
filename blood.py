import streamlit as st
import pandas as pd
from datetime import datetime

# SESSION STATE
if "donors" not in st.session_state:
    st.session_state.donors = []

# MENU
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Home",
        "Register Donor",
        "View Donors",
        "Search Blood Group",
        "Blood Request",
        "Total Donors",
        "Certificate"
    ]
)

# ---------------- HOME ----------------
if menu == "Home":
    st.title("🩸 Blood Donation System")
    st.write("Welcome ❤️ Help save lives")

# ---------------- REGISTER ----------------
elif menu == "Register Donor":

    st.header("Register Donor")

    name = st.text_input("Name")
    age = st.number_input("Age", 1, 100)
    weight = st.number_input("Weight (kg)", 20, 150)
    blood_group = st.selectbox(
        "Blood Group",
        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )
    city = st.text_input("City")

    phone = st.text_input("Phone Number")
    email = st.text_input("Email ID")

    if st.button("Register"):

        if name == "":
            st.error("Enter Name")
        elif len(phone) != 10:
            st.error("❌ Invalid Phone Number")
        elif "@" not in email:
            st.error("❌ Invalid Email ID")
        elif age < 18:
            st.error("❌ Not Eligible (Age must be 18+)")
        elif weight < 40:
            st.error("❌ Not Eligible (Weight must be 40kg+)")
        else:
            st.session_state.donors.append({
                "Name": name,
                "Age": age,
                "Weight": weight,
                "Blood Group": blood_group,
                "City": city,
                "Phone": phone,
                "Email": email,
                "Date": datetime.now().strftime("%d-%m-%Y")
            })

            st.success("✅ Registered Successfully")

# ---------------- VIEW + DELETE + GRAPH ----------------
elif menu == "View Donors":

    st.header("Registered Donors")

    if st.session_state.donors:

        df = pd.DataFrame(st.session_state.donors)
        st.dataframe(df)

        st.info(f"Total Donors: {len(df)}")

        # DELETE
        delete_name = st.selectbox("Delete Donor", df["Name"])

        if st.button("Delete"):
            st.session_state.donors = [
                d for d in st.session_state.donors
                if d["Name"] != delete_name
            ]
            st.success("Deleted Successfully")
            st.rerun()

        # GRAPH 📊
        st.subheader("Blood Group Distribution")
        st.bar_chart(df["Blood Group"].value_counts())

    else:
        st.info("No donors registered")

# ---------------- SEARCH ----------------
elif menu == "Search Blood Group":

    st.header("Search Donors")

    bg = st.selectbox(
        "Blood Group",
        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )

    if st.button("Search"):

        results = [
            d for d in st.session_state.donors
            if d["Blood Group"] == bg
        ]

        st.info(f"Total Found: {len(results)}")

        if results:
            st.dataframe(pd.DataFrame(results))
        else:
            st.warning("No donors found")

# ---------------- BLOOD REQUEST ----------------
elif menu == "Blood Request":

    st.header("Blood Request")

    bg = st.selectbox(
        "Blood Group",
        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )

    city = st.text_input("City")

    if st.button("Find"):

        results = [
            d for d in st.session_state.donors
            if d["Blood Group"] == bg and d["City"].lower() == city.lower()
        ]

        st.info(f"Total Found: {len(results)}")

        if results:
            st.dataframe(pd.DataFrame(results))
        else:
            st.warning("No matching donors")

# ---------------- TOTAL ----------------
elif menu == "Total Donors":

    st.header("Total Donors")

    st.info(f"Total Registered Donors: {len(st.session_state.donors)}")

# ---------------- CERTIFICATE ----------------
elif menu == "Certificate":

    st.header("Certificate Generator")

    name = st.text_input("Enter Donor Name")

    if st.button("Generate"):

        donor = next(
            (d for d in st.session_state.donors if d["Name"].lower() == name.lower()),
            None
        )

        if donor:
            st.success(f"""
🏅 CERTIFICATE

This is to certify that {donor['Name']}
is a registered blood donor.

Blood Group: {donor['Blood Group']}
City: {donor['City']}
Phone: {donor['Phone']}
Email: {donor['Email']}
Date: {donor['Date']}

Thank you for saving lives ❤️
""")
        else:
            st.error("Donor not found")
