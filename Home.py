import streamlit as st
from pathlib import Path

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Trainer Profile Generator",
    page_icon="👨‍🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>

.main-title{
    font-size:40px;
    font-weight:bold;
    color:#1F4E79;
}

.sub-title{
    font-size:20px;
    color:#555555;
}

.card{
    padding:20px;
    border-radius:10px;
    background-color:#F5F7FA;
    border:1px solid #DDDDDD;
    margin-bottom:20px;
}

.footer{
    text-align:center;
    color:gray;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------

st.markdown(
    "<div class='main-title'>👨‍🏫 Trainer Profile Generator</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Training Operations Management System</div>",
    unsafe_allow_html=True
)

st.divider()

# -------------------------------
# Welcome Section
# -------------------------------

col1, col2 = st.columns([2, 1])

with col1:

    st.markdown("### Welcome")

    st.write("""
This application helps the Training Operations team to efficiently manage
trainer profiles.

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
""")

with col2:

    st.info("""
### Application Information

**Version :** 1.0

**Platform :** Python + Streamlit

**Document :** Microsoft Word

**Output :** DOCX / PDF
""")

# -------------------------------
# Quick Actions
# -------------------------------

st.divider()

st.subheader("Quick Actions")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.page_link(
        "pages/1_Dashboard.py",
        label="📊 Dashboard"
    )

with c2:
    st.page_link(
        "pages/2_Search_Trainer.py",
        label="🔍 Search Trainer"
    )

with c3:
    st.page_link(
        "pages/3_Generate_Profiles.py",
        label="📄 Generate Profiles"
    )

with c4:
    st.page_link(
        "pages/4_Reports.py",
        label="📈 Reports"
    )

# -------------------------------
# Features
# -------------------------------

st.divider()

st.subheader("Application Features")

col1, col2 = st.columns(2)

with col1:

    st.success("✔ Trainer Profile Generation")

    st.success("✔ Individual Profile Generation")

    st.success("✔ Bulk Profile Generation")

    st.success("✔ Word Document Export")

    st.success("✔ PDF Export")

with col2:

    st.success("✔ Smart Trainer Search")

    st.success("✔ Reports & Analytics")

    st.success("✔ Image Management")

    st.success("✔ Template Management")

    st.success("✔ Settings")

# -------------------------------
# Footer
# -------------------------------

st.divider()

st.markdown(
    "<div class='footer'>© CodeTantra Tech Solutions Pvt. Ltd. | Training Operations</div>",
    unsafe_allow_html=True
)