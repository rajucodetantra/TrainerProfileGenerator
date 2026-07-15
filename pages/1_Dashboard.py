import streamlit as st
import pandas as pd
from pathlib import Path

from modules.excel_reader import read_excel

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard")

st.divider()

# -------------------------------------------------
# Load Trainer Data
# -------------------------------------------------

try:
    df = read_excel()
except Exception as e:
    st.error(f"Unable to read Excel file.\n\n{e}")
    st.stop()

# -------------------------------------------------
# Folder Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

IMAGE_FOLDER = BASE_DIR / "data" / "CTImages"
DOCX_FOLDER = BASE_DIR / "output" / "DOCX"
PDF_FOLDER = BASE_DIR / "output" / "PDF"

# -------------------------------------------------
# Statistics
# -------------------------------------------------

total_trainers = len(df)

image_count = 0
docx_count = 0
pdf_count = 0

if IMAGE_FOLDER.exists():
    image_count = len(
        list(IMAGE_FOLDER.glob("*.jpg"))
        + list(IMAGE_FOLDER.glob("*.jpeg"))
        + list(IMAGE_FOLDER.glob("*.png"))
    )

if DOCX_FOLDER.exists():
    docx_count = len(list(DOCX_FOLDER.glob("*.docx")))

if PDF_FOLDER.exists():
    pdf_count = len(list(PDF_FOLDER.glob("*.pdf")))

missing_images = max(total_trainers - image_count, 0)

# -------------------------------------------------
# Dashboard Cards
# -------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👨‍🏫 Total Trainers",
    total_trainers
)

col2.metric(
    "🖼 Images Available",
    image_count
)

col3.metric(
    "📄 Word Profiles",
    docx_count
)

col4.metric(
    "📕 PDF Profiles",
    pdf_count
)

st.divider()

col1, col2 = st.columns(2)

col1.metric(
    "❌ Missing Images",
    missing_images
)

col2.metric(
    "📊 Completion",
    f"{round((docx_count/total_trainers)*100,1) if total_trainers else 0}%"
)

# -------------------------------------------------
# Recent Trainers
# -------------------------------------------------

st.subheader("Recent Trainers")

st.dataframe(
    df.head(10),
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------
# Technology Distribution
# -------------------------------------------------

st.divider()

st.subheader("Technology Distribution")

if "Core Skills" in df.columns:

    skills = []

    for value in df["Core Skills"].fillna(""):

        value = (
            str(value)
            .replace("//", ",")
            .replace("\n", ",")
        )

        skills.extend(
            [
                x.strip()
                for x in value.split(",")
                if x.strip()
            ]
        )

    if skills:

        skill_df = (
            pd.Series(skills)
            .value_counts()
            .reset_index()
        )

        skill_df.columns = [
            "Technology",
            "Count"
        ]

        st.dataframe(
            skill_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No technology information available.")

else:

    st.warning(
        "'Core Skills' column not found in Excel."
    )

# -------------------------------------------------
# Missing Data Report
# -------------------------------------------------

st.divider()

st.subheader("Data Quality")

missing = []

for column in df.columns:

    count = df[column].isna().sum()

    missing.append(
        {
            "Column": column,
            "Missing Values": count
        }
    )

missing_df = pd.DataFrame(missing)

st.dataframe(
    missing_df,
    use_container_width=True,
    hide_index=True
)

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.divider()

st.caption(
    "Trainer Profile Generator • Dashboard"
)