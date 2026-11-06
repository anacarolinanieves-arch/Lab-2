# This creates the main landing page for the Streamlit application.
# Contains an introduction to the project and guide users to other pages.

# Import Streamlit
import streamlit as st

# st.set_page_config() is used to configure the page's appearance in the browser tab.
# It's good practice to set this as the first Streamlit command in your script.
st.set_page_config(
    page_title="Cosmetic Dashboard",  # The title that appears in the browser tab
    page_icon="💄",         # An emoji that appears as the icon in the browser tab
)

# WELCOME PAGE TITLE
st.title("Welcome to the Cosmetic Dashboard! 💄")

st.header("CS 1301")
st.subheader("Web Development - Section A")
st.subheader("Ana Carolina Nieves Morales")

# INTRODUCTORY TEXT
st.write(""" This application is designed to collect and visualize data about the
top cosmetic brands in the world! You can navigate to the different pages using
the sidebar on the left.
### How to use this app:
- **Visuals Page**: Go here to see the cosmetic brand revenue data visualized in static and interactive graphs.
- **Survey Page**: Go here to input your own data about your favorite brands and how you rate them on a scale from 1-10.
This project is part of CS 1301's Lab 2. """)

# OPTIONAL: ADD AN IMAGE
# 1. Navigate to the 'images' folder in your Lab02 directory.
# 2. Place your image file (e.g., 'welcome_image.png') inside that folder.
# 3. Uncomment the line below and change the filename to match yours.
#
st.image("images/welcome_image.png")
