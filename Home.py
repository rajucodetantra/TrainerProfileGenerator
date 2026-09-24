import streamlit as st
from login import require_login


# =========================================================
# APPLICATION CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Trainer Profile Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOGIN PROTECTION
# =========================================================

require_login(
    show_logout_button=False
)


# =========================================================
# APPLICATION NAVIGATION
# =========================================================

pages = {

    # =====================================================
    # GENERAL
    # =====================================================

    "GENERAL": [

        st.Page(
            "pages/1_Dashboard.py",
            title="Dashboard",
            icon="🏠",
            url_path="dashboard"
        ),

    ],


    # =====================================================
    # TRAINER PROFILES
    # =====================================================

    "TRAINER PROFILES": [

        st.Page(
            "pages/2_Search_Trainer.py",
            title="Search Trainer",
            icon="🔍",
            url_path="search-trainer"
        ),

        st.Page(
            "pages/3_Generate_Profiles.py",
            title="Generate Profiles",
            icon="👤",
            url_path="generate-profiles"
        ),

        st.Page(
            "pages/14_Resume_Profile_Generator.py",
            title="Resume Profile Generator",
            icon="📄",
            url_path="resume-profile-generator"
        ),

        st.Page(
            "pages/15_Aptitude_Trainers_Profiles.py",
            title="Aptitude Trainer Profiles",
            icon="🎯",
            url_path="aptitude-trainer-profiles"
        ),

    ],


    # =====================================================
    # FEEDBACK & ANALYTICS
    # =====================================================

    "FEEDBACK & ANALYTICS": [

        st.Page(
            "pages/16_Feedback_Analytics.py",
            title="Feedback Analytics",
            icon="📊",
            url_path="feedback-analytics"
        ),

    ],


    # =====================================================
    # TRAINER DATA
    # =====================================================

    "TRAINER DATA": [

        st.Page(
            "pages/4_Add_Projects.py",
            title="Add Projects",
            icon="➕",
            url_path="add-projects"
        ),

        st.Page(
            "pages/5_Change_Skills.py",
            title="Change Skills",
            icon="🛠️",
            url_path="change-skills"
        ),

        st.Page(
            "pages/9_Change_Skills_Add_Projects.py",
            title="Change Skills + Projects",
            icon="📝",
            url_path="change-skills-projects"
        ),

    ],


    # =====================================================
    # DOCUMENT TOOLS
    # =====================================================

    "DOCUMENT TOOLS": [

        st.Page(
            "pages/7_Word_to_PDF.py",
            title="Word to PDF",
            icon="📄",
            url_path="word-to-pdf"
        ),

        st.Page(
            "pages/8_PDF_to_Word.py",
            title="PDF to Word",
            icon="📝",
            url_path="pdf-to-word"
        ),

        st.Page(
            "pages/6_Combine_PDF.py",
            title="Combine PDF",
            icon="📚",
            url_path="combine-pdf"
        ),

        st.Page(
            "pages/13_Split_PDF.py",
            title="Split PDF",
            icon="✂️",
            url_path="split-pdf"
        ),

    ],


    # =====================================================
    # ADMINISTRATION
    # =====================================================

    "ADMINISTRATION": [

        st.Page(
            "pages/12_Reports.py",
            title="Reports",
            icon="📈",
            url_path="reports"
        ),

        st.Page(
            "pages/11_Logs.py",
            title="Logs",
            icon="📋",
            url_path="logs"
        ),

        st.Page(
            "pages/10_Settings.py",
            title="Settings",
            icon="⚙️",
            url_path="settings"
        ),

    ],
}


# =========================================================
# START NAVIGATION
# =========================================================

navigation = st.navigation(
    pages,
    position="sidebar",
    expanded=True
)

navigation.run()