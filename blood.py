import streamlit as st
import pandas as pd
import os
from datetime import datetime

FILE = "donors.csv"

if not os.path.exists(FILE):
    df = pd.DataFrame(columns=[
        "Name","Age","Blood Group",
        "City","Phone","Email",
        "Availability","Date"
    ])
    df.to_csv(FILE,index=False)

donors_df = pd.read_csv(FILE)

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Home",
        "Register Donor",
        "Blood Camp",
        "View Donors",
        "Search Blood Group",
        "Eligibility Check",
        "Blood Request",
        "Total Donors",
        "Certificate"
    ]
)

# HOME PAGE
if menu == "Home":

    st.title("🩸 Blood Donation System")

    if os.path.exists("blood.jpeg"):
        st.image("blood.jpeg",
                 use_container_width=True)

    else:
        st.warning("blood.jpeg not found")

    st.write(
        "Welcome to Blood Donation System ❤️"
    )

# REGISTER DONOR
elif menu == "Register Donor":

    if os.path.exists("donation.jpeg"):
        st.image(
            "donation.jpeg",
            use_container_width=True
        )

    st.header("Donor Registration")

    name = st.text_input("Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100
    )

    blood_group = st.selectbox(
        "Blood Group",
        [
            "A+","A-","B+","B-",
            "O+","O-","AB+","AB-"
        ]
    )

    city = st.text_input("City")
    phone = st.text_input("Phone")
    email = st.text_input("Email")

    availability = st.selectbox(
        "Availability",
        ["Available","Not Available"]
    )

    if st.button("Register"):

        new_donor = {
            "Name": name,
            "Age": age,
            "Blood Group": blood_group,
            "City": city,
            "Phone": phone,
            "Email": email,
            "Availability": availability,
            "Date": datetime.now().strftime("%d-%m-%Y")
        }

        donors_df.loc[
            len(donors_df)
        ] = new_donor

        donors_df.to_csv(
            FILE,
            index=False
        )

        st.success(
            "Registered Successfully!"
        )

# BLOOD CAMP
elif menu == "Blood Camp":

    if os.path.exists("donation.jpeg"):
        st.image(
            "donation.jpeg",
            use_container_width=True
        )

    st.header("Blood Donation Camp")

    camp = st.text_input(
        "Camp Name"
    )

    location = st.text_input(
        "Location"
    )

    date = st.date_input(
        "Camp Date"
    )

    if st.button("Create Camp"):

        st.success(
            f"{camp} created at {location}"
        )
# VIEW DONORS
elif menu == "View Donors":

    if os.path.exists("donation.jpeg"):
        st.image(
            "donation.jpeg",
            use_container_width=True
        )

    st.header("Registered Donors")

    if len(donors_df) > 0:
        st.dataframe(donors_df)

    else:
        st.info("No donors")

# SEARCH
elif menu == "Search Blood Group":

    if os.path.exists("donation.jpeg"):
        st.image(
            "donation.jpeg",
            use_container_width=True
        )

    bg = st.selectbox(
        "Blood Group",
        [
            "A+","A-","B+","B-",
            "O+","O-","AB+","AB-"
        ]
    )

    if st.button("Search"):

        result = donors_df[
            donors_df["Blood Group"] == bg
        ]

        if len(result) > 0:
            st.dataframe(result)

        else:
            st.warning(
                "No donors found"
            )

# ELIGIBILITY
elif menu == "Eligibility Check":

    if os.path.exists("donation.jpeg"):
        st.image(
            "donation.jpeg",
            use_container_width=True
        )

    age = st.number_input(
        "Enter Age",
        1,
        100
    )

    if st.button("Check"):

        if 18 <= age <= 65:
            st.success(
                "Eligible ✅"
            )

        else:
            st.error(
                "Not Eligible ❌"
            )

# BLOOD REQUEST
elif menu == "Blood Request":

    if os.path.exists("donation.jpeg"):
        st.image(
            "donation.jpeg",
            use_container_width=True
        )

    bg = st.selectbox(
        "Required Blood Group",
        [
            "A+","A-","B+","B-",
            "O+","O-","AB+","AB-"
        ]
    )

    city = st.text_input(
        "City"
    )

    if st.button(
        "Find Donors"
    ):

        result = donors_df[
            (donors_df["Blood Group"] == bg)
            &
            (
                donors_df["City"]
                .str.lower()
                == city.lower()
            )
            &
            (
                donors_df["Availability"]
                == "Available"
            )
        ]

        if len(result) > 0:
            st.dataframe(result)

        else:
            st.warning(
                "No matching donors"
            )

# TOTAL DONORS
elif menu == "Total Donors":

    if os.path.exists("donation.jpeg"):
        st.image(
            "donation.jpeg",
            use_container_width=True
        )

    st.info(
        f"Total Donors: {len(donors_df)}"
    )

# CERTIFICATE
elif menu == "Certificate":

    if os.path.exists("donation.jpeg"):
        st.image(
            "donation.jpeg",
            use_container_width=True
        )

    donor_name = st.text_input(
        "Donor Name"
    )

    if st.button(
        "Generate"
    ):

        donor = donors_df[
            donors_df["Name"]
            .str.lower()
            ==
            donor_name.lower()
        ]

        if len(donor) > 0:

            st.markdown(
f"""
# 🏅 Certificate

Name:
**{donor.iloc[0]['Name']}**

Blood Group:
**{donor.iloc[0]['Blood Group']}**

Thank You ❤️
"""
            )

        else:
            st.error(
                "Donor not found"
            )