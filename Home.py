import streamlit as st
from pathlib import Path

from login import require_login


# =========================================================
# PAGE CONFIGURATION
# This must be the first Streamlit command
# =========================================================

st.set_page_config(
    page_title="Trainer Profile Generator",
    page_icon="👨‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOGIN PROTECTION
# =========================================================

require_login()


# =========================================================
# PROJECT PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent


# =========================================================
# SAFE PAGE LINK FUNCTION
# =========================================================

def page_button(page_path, label):
    """
    Creates a page link only if the page exists.

    If the page is missing or renamed,
    Home.py will continue working instead of
    producing StreamlitPageNotFoundError.
    """

    full_path = BASE_DIR / page_path

    if full_path.exists():

        st.page_link(
            page_path,
            label=label,
            use_container_width=True
        )

    else:

        st.warning(
            f"⚠️ Page not found: {page_path}"
        )


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main page title */
    .main-title {
        font-size: 40px;
        font-weight: 700;
        color: #1F4E79;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .sub-title {
        font-size: 19px;
        color: #555555;
        margin-bottom: 15px;
    }

    /* Section text */
    .section-description {
        font-size: 16px;
        color: #555555;
        margin-bottom: 15px;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #777777;
        font-size: 13px;
        padding-top: 10px;
        padding-bottom: 10px;
    }

    /* Page-link buttons */
    div[data-testid="stPageLink"] a {
        border: 1px solid #dddddd;
        border-radius: 8px;
        padding: 12px;
        text-decoration: none;
    }

    div[data-testid="stPageLink"] a:hover {
        border: 1px solid #1F4E79;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        👨‍🏫 Trainer Profile Generator
    </div>

    <div class="sub-title">
        Training Operations Management System
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# WELCOME SECTION
# =========================================================

left_col, right_col = st.columns([2.2, 1])


with left_col:

    st.subheader("Welcome")

    st.write(
        """
        Trainer Profile Generator helps the Training Operations
        team manage trainer information, skills, projects,
        profiles and supporting documents from one application.

        Use the modules below to search trainers, generate profiles,
        manage trainer data, work with PDF documents and view reports.
        """
    )


with right_col:

    st.info(
        """
        ### Application Information

        **Application:** Trainer Profile Generator

        **Version:** 1.0.0

        **Platform:** Python + Streamlit

        **Output:** DOCX / PDF
        """
    )


# =========================================================
# TRAINER PROFILE MANAGEMENT
# =========================================================

st.divider()

st.subheader("👨‍🏫 Trainer Profile Management")

st.markdown(
    """
    <div class="section-description">
        Search trainers and generate individual or bulk trainer profiles.
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    page_button(
        "pages/1_Search_trainer.py",
        "🔍 Search Trainer"
    )


with col2:

    page_button(
        "pages/2_Generate_Profiles.py",
        "📄 Generate Profiles"
    )


# =========================================================
# PDF TOOLS
# =========================================================

st.divider()

st.subheader("📑 PDF & Document Tools")

st.markdown(
    """
    <div class="section-description">
        Convert, combine and split Word and PDF documents.
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    page_button(
        "pages/3_Word_to_PDF.py",
        "📄 Word to PDF"
    )


with col2:

    page_button(
        "pages/4_PDF_to_Word.py",
        "📝 PDF to Word"
    )


col1, col2 = st.columns(2)


with col1:

    page_button(
        "pages/5_Combine_PDF.py",
        "📚 Combine PDF"
    )


with col2:

    page_button(
        "pages/6_Split_PDF.py",
        "✂️ Split PDF"
    )


# =========================================================
# TRAINER DATA MANAGEMENT
# =========================================================

st.divider()

st.subheader("🛠️ Trainer Data Management")

st.markdown(
    """
    <div class="section-description">
        Maintain trainer projects, technical skills and profile information.
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:

    page_button(
        "pages/7_Add_Projects.py",
        "➕ Add Projects"
    )


with col2:

    page_button(
        "pages/8_Change_Skills.py",
        "🛠️ Change Skills"
    )


with col3:

    page_button(
        "pages/9_Change_Skills_Add_Projects.py",
        "🔄 Skills + Projects"
    )


# =========================================================
# ADMINISTRATION
# =========================================================

st.divider()

st.subheader("⚙️ Administration")

st.markdown(
    """
    <div class="section-description">
        Configure the application and review application activity.
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    page_button(
        "pages/10_Settings.py",
        "⚙️ Settings"
    )


with col2:

    page_button(
        "pages/11_Logs.py",
        "📋 Logs"
    )


# =========================================================
# REPORTS AND DASHBOARD
# =========================================================

st.divider()

st.subheader("📊 Reports & Analytics")

st.markdown(
    """
    <div class="section-description">
        View reports, application statistics and trainer analytics.
    </div>
    """,
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)


with col1:

    page_button(
        "pages/12_Reports.py",
        "📈 Reports"
    )


with col2:

    page_button(
        "pages/13_Dashboard.py",
        "📊 Dashboard"
    )


# =========================================================
# APPLICATION FEATURES
# =========================================================

st.divider()

st.subheader("✨ Application Features")


col1, col2, col3 = st.columns(3)


with col1:

    st.success("✔ Search Trainer")
    st.success("✔ Generate Trainer Profiles")
    st.success("✔ Bulk Profile Generation")


with col2:

    st.success("✔ Change Trainer Skills")
    st.success("✔ Add Training Projects")
    st.success("✔ Word / PDF Conversion")


with col3:

    st.success("✔ Reports & Analytics")
    st.success("✔ Dashboard")
    st.success("✔ Settings & Logs")


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        © CodeTantra Tech Solutions Pvt. Ltd.
        &nbsp; | &nbsp;
        Training Operations
        &nbsp; | &nbsp;
        Trainer Profile Generator v1.0.0
    </div>
    """,
    unsafe_allow_html=True
)