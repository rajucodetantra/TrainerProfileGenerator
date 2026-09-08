import streamlit as st
from pathlib import Path

from login import require_login


# =========================================================
# PAGE CONFIGURATION
# IMPORTANT: This should be the first Streamlit command.
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
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #1F4E79;
    }

    .sub-title {
        font-size: 20px;
        color: #555555;
        margin-bottom: 15px;
    }

    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #F5F7FA;
        border: 1px solid #DDDDDD;
        margin-bottom: 20px;
    }

    .footer {
        text-align: center;
        color: gray;
        font-size: 14px;
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
    <div class='main-title'>
        👨‍🏫 Trainer Profile Generator
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='sub-title'>
        Training Operations Management System
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# WELCOME SECTION
# =========================================================

col1, col2 = st.columns(
    [2, 1]
)


with col1:

    st.markdown(
        "### Welcome"
    )

    st.write(
        """
        This application helps the Training Operations team
        efficiently manage trainer profiles.

        Using this application you can:

        - Generate Trainer Profiles
        - Generate Word Documents
        - Generate PDF Documents
        - Search Trainers
        - Preview Profiles
        - Generate Profiles in Bulk
        - View Reports
        - Manage Templates
        - Maintain Trainer Database
        - Change Trainer Skills
        - Add Training Projects
        """
    )


with col2:

    st.info(
        """
        ### Application Information

        **Version:** 1.0

        **Platform:** Python + Streamlit

        **Document:** Microsoft Word

        **Output:** DOCX / PDF
        """
    )


# =========================================================
# QUICK ACTIONS
# =========================================================

st.divider()

st.subheader(
    "Quick Actions"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.page_link(
        "pages/1_Dashboard.py",
        label="📊 Dashboard",
        use_container_width=True
    )


with c2:

    st.page_link(
        "pages/2_Search_Trainer.py",
        label="🔍 Search Trainer",
        use_container_width=True
    )


with c3:

    st.page_link(
        "pages/3_Generate_Profiles.py",
        label="📄 Generate Profiles",
        use_container_width=True
    )


with c4:

    st.page_link(
        "pages/4_Reports.py",
        label="📈 Reports",
        use_container_width=True
    )


# =========================================================
# SECOND QUICK ACTION ROW
# =========================================================

q1, q2, q3, q4 = st.columns(4)


with q1:

    # Change filename if your actual name differs
    change_projects_page = (
        Path(__file__).parent
        / "pages"
        / "12_Change_Skills_Add_Projects.py"
    )

    if change_projects_page.exists():

        st.page_link(
            "pages/12_Change_Skills_Add_Projects.py",
            label="🛠️ Skills + Projects",
            use_container_width=True
        )


# =========================================================
# APPLICATION FEATURES
# =========================================================

st.divider()

st.subheader(
    "Application Features"
)


col1, col2 = st.columns(2)


with col1:

    st.success(
        "✔ Trainer Profile Generation"
    )

    st.success(
        "✔ Individual Profile Generation"
    )

    st.success(
        "✔ Bulk Profile Generation"
    )

    st.success(
        "✔ Word Document Export"
    )

    st.success(
        "✔ PDF Export"
    )

    st.success(
        "✔ Change Core Skills"
    )


with col2:

    st.success(
        "✔ Smart Trainer Search"
    )

    st.success(
        "✔ Reports & Analytics"
    )

    st.success(
        "✔ Image Management"
    )

    st.success(
        "✔ Template Management"
    )

    st.success(
        "✔ Settings"
    )

    st.success(
        "✔ Add Training Projects"
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class='footer'>
        © CodeTantra Tech Solutions Pvt. Ltd.
        | Training Operations
    </div>
    """,
    unsafe_allow_html=True
)