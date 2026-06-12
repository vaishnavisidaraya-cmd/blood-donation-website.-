import streamlit as st
import pandas as pd
from datetime import datetime
import os

FILE = "donors.csv"

# Create CSV if not exists
if not os.path.exists(FILE):
    df = pd.DataFrame(columns=[
        "Name","Age","Weight","Blood Group","City","Phone","Email","Date"
    ])
    df.to_csv(FILE, index=False)

menu = st.sidebar.selectbox(
    "Menu",
    ["Home","Register Donor","View Donors","Search Blood Group","Blood Request","Total Donors","Certificate"]
)

# ---------------- HOME ----------------
if menu == "Home":
    st.title("🩸 Blood Donation System")

    st.image("blood.jpeg", use_container_width=True)

    st.write("Welcome ❤️ Save Lives by Donating Blood")

# ---------------- REGISTER ----------------
elif menu == "Register Donor":

    st.header("Register Donor")

    st.image("donation.jpeg", use_container_width=True)

    name = st.text_input("Name")
    age = st.number_input("Age", 1, 100)
    weight = st.number_input("Weight (kg)", 20, 150)

    blood_group = st.selectbox(
        "Blood Group",
        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )

    city = st.text_input("City")
    phone = st.text_input("Phone")
    email = st.text_input("Email")

    if st.button("Register"):

        if age < 18:
            st.error("❌ Age must be 18+")
        elif weight < 40:
            st.error("❌ Weight must be 40kg+")
        else:
            new_data = pd.DataFrame([{
                "Name": name,
                "Age": age,
                "Weight": weight,
                "Blood Group": blood_group,
                "City": city,
                "Phone": phone,
                "Email": email,
                "Date": datetime.now().strftime("%d-%m-%Y")
            }])

            new_data.to_csv(FILE, mode="a", header=False, index=False)
            st.success("✅ Registered Successfully")

# ---------------- VIEW + DELETE + GRAPH ----------------
elif menu == "View Donors":

    st.header("Registered Donors")

    st.image("donation.jpeg", use_container_width=True)

    df = pd.read_csv(FILE)

    if df.empty:
        st.info("No donors found")
    else:
        st.dataframe(df)

        st.info(f"Total Donors: {len(df)}")

        # DELETE
        name_del = st.selectbox("Delete Donor", df["Name"])

        if st.button("Delete"):
            df = df[df["Name"] != name_del]
            df.to_csv(FILE, index=False)
            st.success("Deleted Successfully")
            st.rerun()

        # 📊 GRAPH
        st.subheader("Blood Group Distribution")
        st.bar_chart(df["Blood Group"].value_counts())

# ---------------- SEARCH ----------------
elif menu == "Search Blood Group":

    st.header("Search Donors")

    st.image("donation.jpeg", use_container_width=True)

    df = pd.read_csv(FILE)

    bg = st.selectbox(
        "Blood Group",
        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )

    if st.button("Search"):
        result = df[df["Blood Group"] == bg]

        st.info(f"Total Found: {len(result)}")

        st.dataframe(result)

# ---------------- BLOOD REQUEST ----------------
elif menu == "Blood Request":

    st.header("Blood Request")

    st.image("donation.jpeg", use_container_width=True)

    df = pd.read_csv(FILE)

    bg = st.selectbox(
        "Blood Group",
        ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    )

    city = st.text_input("City")

    if st.button("Find"):
        result = df[
            (df["Blood Group"] == bg) &
            (df["City"].str.lower() == city.lower())
        ]

        st.info(f"Total Found: {len(result)}")

        st.dataframe(result)

# ---------------- TOTAL ----------------
elif menu == "Total Donors":

    st.header("Total Donors")

    df = pd.read_csv(FILE)

    st.info(f"Total Registered Donors: {len(df)}")

# ---------------- CERTIFICATE ----------------
elif menu == "Certificate":

    st.header("Certificate Generator")

    df = pd.read_csv(FILE)

    name = st.text_input("Enter Donor Name")

    if st.button("Generate"):

        donor = df[df["Name"].str.lower() == name.lower()]

        if not donor.empty:
            d = donor.iloc[0]

            st.success(f"""
🏅 CERTIFICATE

This is to certify that {d['Name']}
is a registered blood donor.

Blood Group: {d['Blood Group']}
City: {d['City']}
Phone: {d['Phone']}
Email: {d['Email']}
Date: {d['Date']}

Thank you ❤️
""")
        else:
            st.error("Donor not found")
