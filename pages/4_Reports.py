import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from services.profile_service import ProfileService

# -------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------

st.set_page_config(
    page_title="Reports",
    page_icon="📊",
    layout="wide"
)

service = ProfileService()

st.title("📊 Reports & Analytics")

st.divider()

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

trainers = service.get_trainers()

stats = service.statistics()

# -------------------------------------------------------
# TOP METRICS
# -------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Trainers",
    stats["total_trainers"]
)

col2.metric(
    "Designations",
    stats["designations"]
)

col3.metric(
    "Qualifications",
    stats["qualifications"]
)

col4.metric(
    "Skills",
    stats["skills"]
)

st.divider()

# -------------------------------------------------------
# DESIGNATION REPORT
# -------------------------------------------------------

st.subheader("Designation Wise Trainers")

designation_df = (
    trainers["Designation"]
    .fillna("N/A")
    .value_counts()
    .reset_index()
)

designation_df.columns = [
    "Designation",
    "Count"
]

st.dataframe(
    designation_df,
    use_container_width=True,
    hide_index=True
)

fig = plt.figure(figsize=(8,4))

plt.bar(
    designation_df["Designation"],
    designation_df["Count"]
)

plt.xticks(rotation=20)

plt.tight_layout()

st.pyplot(fig)

st.divider()

# -------------------------------------------------------
# QUALIFICATION REPORT
# -------------------------------------------------------

st.subheader(
    "Qualification Wise Trainers"
)

qualification_df = (
    trainers["Qualification"]
    .fillna("N/A")
    .value_counts()
    .reset_index()
)

qualification_df.columns = [
    "Qualification",
    "Count"
]

st.dataframe(
    qualification_df,
    use_container_width=True,
    hide_index=True
)

fig = plt.figure(figsize=(8,4))

plt.bar(
    qualification_df["Qualification"],
    qualification_df["Count"]
)

plt.xticks(rotation=25)

plt.tight_layout()

st.pyplot(fig)

st.divider()

# -------------------------------------------------------
# EXPERIENCE REPORT
# -------------------------------------------------------

st.subheader(
    "Experience Distribution"
)

experience_df = (
    trainers["Experience"]
    .fillna("N/A")
    .value_counts()
    .reset_index()
)

experience_df.columns = [
    "Experience",
    "Count"
]

st.dataframe(
    experience_df,
    use_container_width=True,
    hide_index=True
)
# -------------------------------------------------------
# TOP SKILLS
# -------------------------------------------------------

st.divider()

st.subheader(
    "Top Skills"
)

skills = []

for value in trainers["Skills"].fillna(""):

    value = (
        str(value)
        .replace("//", ",")
        .replace("\n", ",")
    )

    for skill in value.split(","):

        skill = skill.strip()

        if skill:

            skills.append(skill)

skills_df = (
    pd.Series(skills)
    .value_counts()
    .reset_index()
)

skills_df.columns = [
    "Skill",
    "Count"
]

st.dataframe(
    skills_df,
    use_container_width=True,
    hide_index=True
)

fig = plt.figure(figsize=(10,4))

plt.bar(
    skills_df["Skill"][:10],
    skills_df["Count"][:10]
)

plt.xticks(rotation=45)

plt.tight_layout()

st.pyplot(fig)

# -------------------------------------------------------
# DATA QUALITY
# -------------------------------------------------------

st.divider()

st.subheader(
    "Data Quality"
)

missing_email = trainers[
    trainers["Company Mail"]
    .fillna("")
    .astype(str)
    .str.strip()
    == ""
]

missing_phone = trainers[
    trainers["Phone Number"]
    .fillna("")
    .astype(str)
    .str.strip()
    == ""
]

missing_image = 0

for _, trainer in trainers.iterrows():

    image = os.path.join(
        "data",
        "CTImages",
        f"{trainer['Emp ID']}.jpg"
    )

    if not os.path.exists(image):

        missing_image += 1

col1, col2, col3 = st.columns(3)

col1.metric(
    "Missing Emails",
    len(missing_email)
)

col2.metric(
    "Missing Phone Numbers",
    len(missing_phone)
)

col3.metric(
    "Missing Images",
    missing_image
)

# -------------------------------------------------------
# OUTPUT SUMMARY
# -------------------------------------------------------

st.divider()

st.subheader(
    "Generated Profiles"
)

output = service.output_summary()

col1, col2 = st.columns(2)

col1.metric(
    "DOCX Profiles",
    output["docx"]
)

col2.metric(
    "PDF Profiles",
    output["pdf"]
)

# -------------------------------------------------------
# DOWNLOAD REPORT
# -------------------------------------------------------

st.divider()

st.subheader(
    "Download Trainer Report"
)

csv = trainers.to_csv(
    index=False
).encode("utf-8")

st.download_button(

    label="📥 Download CSV",

    data=csv,

    file_name="Trainer_Report.csv",

    mime="text/csv",

    use_container_width=True

)

# -------------------------------------------------------
# APPLICATION INFORMATION
# -------------------------------------------------------

st.divider()

st.subheader(
    "Application Information"
)

info = pd.DataFrame(

    [

        [
            "Excel File",
            stats["excel"]
        ],

        [
            "Template",
            stats["template"]
        ],

        [
            "Images Folder",
            stats["images_folder"]
        ]

    ],

    columns=[
        "Property",
        "Value"
    ]

)

st.dataframe(
    info,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------

st.divider()

st.caption(
    "Trainer Profile Generator"
)

st.caption(
    "CodeTantra Tech Solutions Pvt. Ltd."
)