import os
import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------

st.set_page_config(
    page_title="Generation Logs",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Generation Logs")

st.divider()

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "generation_log.csv")

# ----------------------------------------------------
# Create Log File if Missing
# ----------------------------------------------------

if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

if not os.path.exists(LOG_FILE):

    df = pd.DataFrame(columns=[
        "Date",
        "Time",
        "Employee ID",
        "Trainer Name",
        "Status",
        "Output File",
        "Remarks"
    ])

    df.to_csv(LOG_FILE, index=False)

# ----------------------------------------------------
# Read Logs
# ----------------------------------------------------

logs = pd.read_csv(LOG_FILE)

# ----------------------------------------------------
# Dashboard
# ----------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Logs",
    len(logs)
)

if len(logs):

    success = len(logs[logs["Status"] == "SUCCESS"])

    failed = len(logs[logs["Status"] == "FAILED"])

else:

    success = 0
    failed = 0

col2.metric(
    "Success",
    success
)

col3.metric(
    "Failed",
    failed
)

st.divider()

# ----------------------------------------------------
# Filters
# ----------------------------------------------------

status = st.selectbox(
    "Filter",
    [
        "All",
        "SUCCESS",
        "FAILED"
    ]
)

search = st.text_input(
    "Search Employee ID / Trainer Name"
)

filtered = logs.copy()

if status != "All":

    filtered = filtered[
        filtered["Status"] == status
    ]

if search:

    filtered = filtered[
        filtered.astype(str)
        .apply(
            lambda x:
            x.str.contains(
                search,
                case=False
            )
            .any(),
            axis=1
        )
    ]

# ----------------------------------------------------
# Log Table
# ----------------------------------------------------

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ----------------------------------------------------
# Download
# ----------------------------------------------------

csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(

    "📥 Download Logs",

    csv,

    file_name="generation_logs.csv",

    mime="text/csv"

)

# ----------------------------------------------------
# Clear Logs
# ----------------------------------------------------

if st.button(
    "🗑 Clear Logs"
):

    pd.DataFrame(columns=[
        "Date",
        "Time",
        "Employee ID",
        "Trainer Name",
        "Status",
        "Output File",
        "Remarks"
    ]).to_csv(
        LOG_FILE,
        index=False
    )

    st.success(
        "Logs Cleared"
    )

    st.rerun()

st.divider()

st.caption(
    "Trainer Profile Generator"
)