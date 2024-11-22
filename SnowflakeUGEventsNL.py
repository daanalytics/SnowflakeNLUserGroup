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

    if submitted:
        if subject and short_descripton and presentor and period:
            # Voeg het nieuwe event toe aan de DataFrame
            new_event = {
                "Subject": subject,
                "Short description": short_descripton,
                "Presentor": presentor,
                "Period": period
            }
            events = events.append(new_event, ignore_index=True)

            # Sla het bijgewerkte Excelbestand lokaal op
            excel_data = save_to_excel(events)

            # Toon een knop om het bijgewerkte Excelbestand te downloaden
            st.success("Event succesvol toegevoegd!")
            st.download_button(
                label="Download bijgewerkt Excelbestand",
                data=excel_data,
                file_name="SnowflakeUGEventsNL.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("Fill all fields to add a new event.")