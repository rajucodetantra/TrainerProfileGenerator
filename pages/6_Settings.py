import os
import streamlit as st

from services.config_service import ConfigService

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Settings",
    page_icon="⚙️",
    layout="wide"
)

config = ConfigService()

st.title("⚙️ Application Settings")

st.divider()

# -------------------------------------------------------
# General Settings
# -------------------------------------------------------

st.header("General Settings")

col1, col2 = st.columns(2)

with col1:

    company_name = st.text_input(
        "Company Name",
        value=config.company_name
    )

    application_name = st.text_input(
        "Application Name",
        value=config.application_name
    )

    version = st.text_input(
        "Version",
        value=config.version
    )

with col2:

    default_rating = st.slider(
        "Default Rating",
        min_value=1,
        max_value=5,
        value=config.default_rating
    )

    default_output = st.selectbox(
        "Default Output Format",
        [
            "Word",
            "PDF",
            "Both"
        ],
        index=[
            "Word",
            "PDF",
            "Both"
        ].index(config.default_output)
    )

st.divider()

# -------------------------------------------------------
# File Paths
# -------------------------------------------------------

st.header("Project Paths")

excel_file = st.text_input(
    "Trainer Excel File",
    value=config.excel_file
)

sheet_name = st.text_input(
    "Sheet Name",
    value=config.sheet_name
)

template_file = st.text_input(
    "Word Template",
    value=config.template_file
)

image_folder = st.text_input(
    "Images Folder",
    value=config.image_folder
)

docx_output = st.text_input(
    "DOCX Output Folder",
    value=config.docx_output
)

pdf_output = st.text_input(
    "PDF Output Folder",
    value=config.pdf_output
)

logo = st.text_input(
    "Company Logo (Optional)",
    value=config.logo
)

st.divider()

# -------------------------------------------------------
# Validate Paths
# -------------------------------------------------------

st.header("Path Validation")

path_data = [

    ("Excel File", excel_file),

    ("Template", template_file),

    ("Images Folder", image_folder),

    ("DOCX Folder", docx_output),

    ("PDF Folder", pdf_output)

]

for title, path in path_data:

    if os.path.exists(path):

        st.success(f"✅ {title} Found")

    else:

        st.error(f"❌ {title} Not Found")
# -------------------------------------------------------
# Save Settings
# -------------------------------------------------------

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "💾 Save Settings",
        use_container_width=True
    ):

        settings = {

            "company_name": company_name,

            "application_name": application_name,

            "version": version,

            "excel_file": excel_file,

            "sheet_name": sheet_name,

            "template_file": template_file,

            "image_folder": image_folder,

            "docx_output": docx_output,

            "pdf_output": pdf_output,

            "logo": logo,

            "default_rating": default_rating,

            "default_output": default_output

        }

        config.save(settings)

        st.success(
            "Settings saved successfully."
        )

with col2:

    if st.button(
        "🔄 Reload Settings",
        use_container_width=True
    ):

        st.rerun()

with col3:

    if st.button(
        "♻ Reset to Default",
        use_container_width=True
    ):

        config.reset()

        st.success(
            "Default settings restored."
        )

        st.rerun()

# -------------------------------------------------------
# Current Configuration
# -------------------------------------------------------

st.divider()

st.header("Current Configuration")

st.json(
    config.config
)

# -------------------------------------------------------
# Folder Information
# -------------------------------------------------------

st.divider()

st.header("Project Information")

folder_info = [

    ("Excel File", excel_file),

    ("Template", template_file),

    ("Images", image_folder),

    ("DOCX Output", docx_output),

    ("PDF Output", pdf_output)

]

for title, path in folder_info:

    col1, col2 = st.columns([1,3])

    with col1:

        st.write(f"**{title}**")

    with col2:

        st.code(path)

# -------------------------------------------------------
# Output Folder Summary
# -------------------------------------------------------

st.divider()

st.header("Output Summary")

docx_count = 0
pdf_count = 0

if os.path.exists(docx_output):

    docx_count = len([
        f
        for f in os.listdir(docx_output)
        if f.lower().endswith(".docx")
    ])

if os.path.exists(pdf_output):

    pdf_count = len([
        f
        for f in os.listdir(pdf_output)
        if f.lower().endswith(".pdf")
    ])

c1, c2 = st.columns(2)

c1.metric(
    "DOCX Files",
    docx_count
)

c2.metric(
    "PDF Files",
    pdf_count
)
# -------------------------------------------------------
# Application Information
# -------------------------------------------------------

st.divider()

st.header("Application Information")

info_col1, info_col2 = st.columns(2)

with info_col1:

    st.info(f"""
**Application**

{application_name}

**Version**

{version}

**Company**

{company_name}
""")

with info_col2:

    st.info(f"""
**Excel File**

{excel_file}

**Template**

{template_file}

**Images**

{image_folder}
""")

# -------------------------------------------------------
# Configuration Status
# -------------------------------------------------------

st.divider()

st.header("Configuration Status")

checks = {
    "Excel File": os.path.isfile(excel_file),
    "Template File": os.path.isfile(template_file),
    "Images Folder": os.path.isdir(image_folder),
    "DOCX Output Folder": os.path.isdir(docx_output),
    "PDF Output Folder": os.path.isdir(pdf_output)
}

all_ok = True

for item, status in checks.items():

    if status:

        st.success(f"✅ {item}")

    else:

        all_ok = False

        st.error(f"❌ {item}")

st.divider()

if all_ok:

    st.success(
        "Application is configured correctly."
    )

else:

    st.warning(
        "Some required files/folders are missing. Please verify the paths before generating profiles."
    )

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.divider()

st.caption(
    f"{application_name} | Version {version}"
)

st.caption(
    f"© {company_name}"
)