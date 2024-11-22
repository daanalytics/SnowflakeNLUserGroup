import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO
import requests

# URL of the Excel file in GitHub
EXCEL_URL = "https://raw.githubusercontent.com/daanalytics/SnowflakeNLUserGroup/main/SnowflakeUGEventsNL.xlsx"

# Function to load the Excel file
@st.cache_data
def load_events():
    response = requests.get(EXCEL_URL)
    response.raise_for_status()
    return pd.read_excel(BytesIO(response.content))

# Streamlit app
st.title("Event Overview")

# Load existing events into session state if not already loaded
if "events" not in st.session_state:
    try:
        st.session_state.events = load_events()
    except Exception as e:
        st.error(f"Could not load the Excel file: {e}")
        st.session_state.events = pd.DataFrame(columns=["Subject", "Short description", "Presentor", "Period"])

# Display the current list of events
st.subheader("Planned Events")
st.dataframe(st.session_state.events)

# Add a new event form
st.subheader("Add a New Event")
with st.form("event_form", clear_on_submit=True):
    subject = st.text_input("Subject")
    short_description = st.text_area("Short description")
    presentor = st.text_input("Presentor")
    period = st.text_input("Period (e.g. May 2025)")

    submitted = st.form_submit_button("Add Event")

# If the form is submitted
if submitted:
    if subject and short_description and presentor and period:
        # Create a new event as a dictionary
        new_event = {
            "Subject": subject,
            "Short description": short_description,
            "Presentor": presentor,
            "Period": period
        }
        # Add the new event to the session state DataFrame
        st.session_state.events = pd.concat(
            [st.session_state.events, pd.DataFrame([new_event])],
            ignore_index=True
        )

        # Display success message
        st.success("Event successfully added!")

        # Rerun the app to refresh the displayed table
        st.experimental_rerun()
    else:
        st.error("Please fill out all fields to add a new event.")