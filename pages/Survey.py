# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os 

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Broncos Fan Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")


with st.form("survey_form", clear_on_submit= True):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("Which opponent was your favorite Broncos game against?")
    value_input = st.text_input("Rate the Broncos' 2025 season from 1-10:")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
       if category_input != "" and value_input.isdigit() and 1 <= int(value_input) <= 10:
           f = open("data.csv", "a")
           f.write(category_input.strip().title() + "," + value_input.strip() + "\n")
           f.close()
        
           st.success("Your data has been submitted!")
           st.write(f"You entered: **Category:** {category_input}, **Value:** {value_input}")
       else:
           st.error("Please enter a team and a rating from 1-10.")
         


# DATA DISPLAY
st.divider() 
st.header("Current Data in CSV")

if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    current_data_df = pd.read_csv('data.csv')
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")