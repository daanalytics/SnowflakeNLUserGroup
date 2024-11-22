import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO
import requests

# URL van het Excelbestand in GitHub (vervang door jouw URL)
EXCEL_URL = "https://raw.githubusercontent.com/daanalytics/SnowflakeNLUserGroup/main/SnowflakeUGEventsNL.xlsx"

# Functie om het Excelbestand te laden
@st.cache_data
def load_events():
    response = requests.get(EXCEL_URL)
    response.raise_for_status()
    return pd.read_excel(BytesIO(response.content))

# Functie om een bijgewerkt Excelbestand te genereren
def save_to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False, sheet_name="SnowflakeUGEventsNL")
    return output.getvalue()

# Streamlit-app
st.title("Event Overzicht")

# Laad de huidige events
try:
    events = load_events()
except Exception as e:
    st.error(f"Could not load the Excelfile: {e}")
    events = pd.DataFrame(columns=["Subject", "Short description", "Presentor", "Period"])

# Toon het overzicht
st.subheader("Planned Events")
st.dataframe(events)

# Voeg een nieuw event toe
st.subheader("Add a new event")

with st.form("event_form", clear_on_submit=True):
    subject = st.text_input("Subject")
    short_descripton = st.text_area("Short description")
    presentor = st.text_input("Presentor")
    period = st.text_input("Period (e.g. May 2025)")

    submitted = st.form_submit_button("Add event")

    # If the form is submitted
if submitted:
    if subject and short_descripton and presentor and period:
        # Create a new row as a dictionary
        new_event = {
            "Subject": subject,
            "Short description": short_descripton,
            "Presentor": presentor,
            "Period": period
        }
        # Add the new event to the DataFrame
        events = pd.concat([events, pd.DataFrame([new_event])], ignore_index=True)

        # Save the updated DataFrame to Excel
        excel_data = save_to_excel(events)

        # Display success message and download button
        st.success("Event successfully added!")
        st.download_button(
            label="Download updated Excel file",
            data=excel_data,
            file_name="SnowflakeUGEventsNL.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("Fill all fields to add a new event.")