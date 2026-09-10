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
#
# Home checks authentication.
# Logout is NOT displayed here.
# Selected child page displays Logout.
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
            "pages/13_Dashboard.py",
            title="Dashboard",
            url_path="dashboard"
        ),

    ],


    # =====================================================
    # TRAINER PROFILES
    # =====================================================

    "TRAINER PROFILES": [

        st.Page(
            "pages/1_Search_Trainer.py",
            title="Search Trainer",
            url_path="search-trainer"
        ),

        st.Page(
            "pages/2_Generate_Profiles.py",
            title="Generate Profiles",
            url_path="generate-profiles"
        ),

        st.Page(
            "pages/14_Resume_Profile_Generator.py",
            title="Resume Profile Generator",
            url_path="resume-profile-generator"
        ),

        # -------------------------------------------------
        # PAGE 15 - APTITUDE TRAINER PROFILES
        # -------------------------------------------------

        st.Page(
            "pages/15_Aptitude_Trainers_Profiles.py",
            title="Aptitude Trainer Profiles",
            url_path="aptitude-trainer-profiles"
        ),

    ],


    # =====================================================
    # FEEDBACK & ANALYTICS
    # =====================================================

    "FEEDBACK & ANALYTICS": [

        # -------------------------------------------------
        # PAGE 16 - FEEDBACK ANALYTICS
        # -------------------------------------------------

        st.Page(
            "pages/16_Feedback_Analytics.py",
            title="Feedback Analytics",
            url_path="feedback-analytics"
        ),

    ],


    # =====================================================
    # TRAINER DATA
    # =====================================================

    "TRAINER DATA": [

        st.Page(
            "pages/7_Add_Projects.py",
            title="Add Projects",
            url_path="add-projects"
        ),

        st.Page(
            "pages/8_Change_Skills.py",
            title="Change Skills",
            url_path="change-skills"
        ),

        st.Page(
            "pages/9_Change_Skills_Add_Projects.py",
            title="Change Skills + Projects",
            url_path="change-skills-projects"
        ),

    ],


    # =====================================================
    # DOCUMENT TOOLS
    # =====================================================

    "DOCUMENT TOOLS": [

        st.Page(
            "pages/3_Word_to_PDF.py",
            title="Word to PDF",
            url_path="word-to-pdf"
        ),

        st.Page(
            "pages/4_PDF_to_Word.py",
            title="PDF to Word",
            url_path="pdf-to-word"
        ),

        st.Page(
            "pages/5_Combine_PDF.py",
            title="Combine PDF",
            url_path="combine-pdf"
        ),

        st.Page(
            "pages/6_Split_PDF.py",
            title="Split PDF",
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
            url_path="reports"
        ),

        st.Page(
            "pages/11_Logs.py",
            title="Logs",
            url_path="logs"
        ),

        st.Page(
            "pages/10_Settings.py",
            title="Settings",
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