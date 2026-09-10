import sys
import uuid
import re
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Resume Profile Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROJECT ROOT
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(ROOT_DIR)
    )


# =========================================================
# LOGIN PROTECTION
# =========================================================

try:
    from login import require_login

    require_login()

except ImportError:
    pass


# =========================================================
# IMPORT NEW INDEPENDENT MODULES
# =========================================================

from resume_generator.pdf_extractor import (
    extract_pdf_text,
    extract_candidate_photo
)

from resume_generator.resume_parser import (
    parse_resume
)

from resume_generator.profile_generator import (
    generate_profile
)

from resume_generator.pdf_converter import (
    convert_docx_to_pdf,
    get_pdf_conversion_status
)


# =========================================================
# PATH CONFIGURATION
# =========================================================

TEMPLATE_DIR = ROOT_DIR / "templates"

OUTPUT_ROOT = (
    ROOT_DIR
    / "output"
    / "Resume_Profiles"
)

TEMP_DIR = (
    OUTPUT_ROOT
    / "_temp"
)

TECHNICAL_OUTPUT_DIR = (
    OUTPUT_ROOT
    / "Technical"
)

APTITUDE_OUTPUT_DIR = (
    OUTPUT_ROOT
    / "Aptitude"
)


# =========================================================
# CREATE REQUIRED FOLDERS
# =========================================================

for folder in [
    OUTPUT_ROOT,
    TEMP_DIR,
    TECHNICAL_OUTPUT_DIR,
    APTITUDE_OUTPUT_DIR
]:

    folder.mkdir(
        parents=True,
        exist_ok=True
    )


# =========================================================
# TEMPLATE FILES
# =========================================================

TECHNICAL_TEMPLATE = (
    TEMPLATE_DIR
    / "Resume_Technical_Trainer_Template.docx"
)

APTITUDE_TEMPLATE = (
    TEMPLATE_DIR
    / "Aptitude_Trainer_Profile_Template.docx"
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def safe_filename(value):
    """
    Convert trainer name / employee ID
    into safe file name.
    """

    value = str(value).strip()

    value = re.sub(
        r'[<>:"/\\|?*]',
        "",
        value
    )

    value = re.sub(
        r"\s+",
        "_",
        value
    )

    if not value:
        return "Trainer"

    return value


def read_file_bytes(file_path):
    """
    Read generated file for Streamlit
    download button.
    """

    with open(
        file_path,
        "rb"
    ) as file:

        return file.read()


def rating_to_stars(rating):
    """
    Convert rating:
    5 -> ★★★★★
    4 -> ★★★★
    """

    try:

        rating = int(rating)

        if rating <= 0:
            return ""

        return "★" * rating

    except Exception:

        return str(rating)


def cleanup_dataframe_value(value):
    """
    Convert NaN values safely to blank.
    """

    if pd.isna(value):
        return ""

    value = str(value).strip()

    if value.lower() == "nan":
        return ""

    return value


# =========================================================
# PAGE TITLE
# =========================================================

st.markdown(
    """
    <h1 style="
        color:#1F4E79;
        margin-bottom:0px;
    ">
        📄 Resume → Trainer Profile Generator
    </h1>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Independent module for generating "
    "Technical Trainer and Aptitude Trainer profiles."
)

st.info(
    "This page works independently. "
    "It does not modify Trainers.xlsx, Projects.xlsx, "
    "or your existing profile-generation pages."
)


# =========================================================
# STEP 1 - PROFILE TYPE
# =========================================================

st.markdown("---")

st.subheader(
    "Step 1: Select Trainer Type"
)

profile_type = st.radio(
    "Select Profile Type",
    [
        "Technical Trainer",
        "Aptitude Trainer"
    ],
    horizontal=True
)


# =========================================================
# SELECT TEMPLATE
# =========================================================

if profile_type == "Technical Trainer":

    selected_template = (
        TECHNICAL_TEMPLATE
    )

else:

    selected_template = (
        APTITUDE_TEMPLATE
    )


# =========================================================
# TEMPLATE STATUS
# =========================================================

if selected_template.exists():

    st.success(
        f"Template available: "
        f"{selected_template.name}"
    )

else:

    st.error(
        f"Template not found:\n"
        f"{selected_template}"
    )


# =========================================================
# STEP 2 - UPLOAD PDF
# =========================================================

st.markdown("---")

st.subheader(
    "Step 2: Upload Resume"
)

uploaded_file = st.file_uploader(
    "Upload Trainer Resume PDF",
    type=["pdf"],
    help=(
        "Upload one trainer resume in PDF format."
    )
)


# =========================================================
# EXTRACT BUTTON
# =========================================================

if uploaded_file is not None:

    extract_button = st.button(
        "🔍 Extract Resume",
        type="primary"
    )

    if extract_button:

        try:

            pdf_bytes = (
                uploaded_file.getvalue()
            )

            # ---------------------------------------------
            # Extract PDF text
            # ---------------------------------------------

            raw_text = extract_pdf_text(
                pdf_bytes
            )

            if not raw_text.strip():

                st.error(
                    "No readable text was found "
                    "inside this PDF."
                )

                st.stop()

            # ---------------------------------------------
            # Parse resume
            # ---------------------------------------------

            parsed_data = parse_resume(
                raw_text,
                profile_type
            )

            # ---------------------------------------------
            # Extract candidate photo
            # ---------------------------------------------

            temp_photo_name = (
                f"{uuid.uuid4().hex}.png"
            )

            photo_file = (
                TEMP_DIR
                / temp_photo_name
            )

            photo_path = (
                extract_candidate_photo(
                    pdf_bytes,
                    str(photo_file)
                )
            )

            # ---------------------------------------------
            # Save additional information
            # ---------------------------------------------

            parsed_data[
                "Photo Path"
            ] = photo_path

            parsed_data[
                "Profile Type"
            ] = profile_type

            parsed_data[
                "Original File Name"
            ] = uploaded_file.name

            # ---------------------------------------------
            # Store in session
            # ---------------------------------------------

            st.session_state[
                "resume_profile_data"
            ] = parsed_data

            st.session_state[
                "generated_resume_files"
            ] = {}

            st.success(
                "Resume extracted successfully."
            )

        except Exception as error:

            st.error(
                "Resume extraction failed."
            )

            st.exception(
                error
            )


# =========================================================
# GET EXTRACTED DATA
# =========================================================

data = st.session_state.get(
    "resume_profile_data"
)


# =========================================================
# REVIEW FORM
# =========================================================

if data:

    if (
        data.get(
            "Profile Type"
        )
        != profile_type
    ):

        st.warning(
            "You changed the trainer type after extraction. "
            "Please click Extract Resume again."
        )

        st.stop()


    st.markdown("---")

    st.subheader(
        "Step 3: Review / Edit Extracted Information"
    )


    # =====================================================
    # PHOTO PREVIEW
    # =====================================================

    photo_path = data.get(
        "Photo Path"
    )

    if (
        photo_path
        and Path(
            photo_path
        ).exists()
    ):

        photo_col1, photo_col2 = (
            st.columns(
                [1, 4]
            )
        )

        with photo_col1:

            st.image(
                photo_path,
                width=150,
                caption="Extracted Photo"
            )

        with photo_col2:

            st.success(
                "Candidate photo detected."
            )

            st.caption(
                "The photo will be inserted "
                "into the template automatically."
            )

    else:

        st.warning(
            "Candidate photo was not detected. "
            "The generated profile will remain "
            "without a photo unless we add "
            "manual photo upload later."
        )


    # =====================================================
    # FORM START
    # =====================================================

    with st.form(
        "resume_profile_form"
    ):

        # =================================================
        # BASIC DETAILS
        # =================================================

        st.markdown(
            "### Basic Details"
        )

        col1, col2 = (
            st.columns(2)
        )


        with col1:

            name = st.text_input(
                "Name",
                value=data.get(
                    "Name",
                    ""
                )
            )

            emp_id = st.text_input(
                "Employee ID",
                value=data.get(
                    "Emp ID",
                    ""
                ),
                placeholder="Example: CT0935"
            )

            designation = (
                st.text_input(
                    "Designation",
                    value=profile_type,
                    disabled=True
                )
            )

            qualification = (
                st.text_input(
                    "Qualification",
                    value=data.get(
                        "Qualification",
                        ""
                    )
                )
            )

            date_of_joining = (
                st.text_input(
                    "Date of Joining",
                    value=data.get(
                        "Date of Joining",
                        ""
                    ),
                    placeholder="DD-MM-YYYY"
                )
            )


        with col2:

            experience = (
                st.text_input(
                    "Experience",
                    value=data.get(
                        "Experience",
                        ""
                    )
                )
            )

            company_mail = (
                st.text_input(
                    "Company Mail",
                    value=data.get(
                        "Company Mail",
                        ""
                    ),
                    placeholder=(
                        "trainer@codetantra.in"
                    )
                )
            )

            phone_number = (
                st.text_input(
                    "Phone Number",
                    value=data.get(
                        "Phone Number",
                        ""
                    )
                )
            )

            personal_email = (
                st.text_input(
                    "Personal Email",
                    value=data.get(
                        "Personal Email",
                        ""
                    ),
                    disabled=True
                )
            )

            rating = (
                st.selectbox(
                    "Trainer Rating",
                    options=[
                        0,
                        1,
                        2,
                        3,
                        4,
                        5
                    ],
                    index=0,
                    format_func=lambda value:
                    (
                        "Not Assigned"
                        if value == 0
                        else "★" * value
                    )
                )
            )


        # =================================================
        # LINKEDIN
        # =================================================

        linkedin = (
            st.text_input(
                "LinkedIn",
                value=data.get(
                    "LinkedIn",
                    ""
                ),
                disabled=True
            )
        )


        # =================================================
        # CORE SKILLS
        # =================================================

        st.markdown(
            "### Core Skills"
        )

        skills = st.text_area(
            "Core Skills",
            value=data.get(
                "Skills",
                ""
            ),
            height=100,
            label_visibility="collapsed"
        )


        # =================================================
        # PROFESSIONAL SUMMARY
        # =================================================

        st.markdown(
            "### Professional Summary"
        )

        summary = st.text_area(
            "Professional Summary",
            value=data.get(
                "Summary",
                ""
            ),
            height=180,
            label_visibility="collapsed"
        )


        # =================================================
        # CERTIFICATIONS
        # =================================================

        st.markdown(
            "### Professional Certifications"
        )

        certifications = (
            st.text_area(
                "Professional Certifications",
                value=data.get(
                    "Certifications",
                    ""
                ),
                height=140,
                label_visibility="collapsed"
            )
        )


        # =================================================
        # PROFESSIONAL HIGHLIGHTS
        # =================================================

        st.markdown(
            "### Professional Highlights"
        )

        highlights = (
            st.text_area(
                "Professional Highlights",
                value=data.get(
                    "Professional Highlights",
                    ""
                ),
                height=180,
                label_visibility="collapsed"
            )
        )


        # =================================================
        # APTITUDE TRAINER FIELDS
        # =================================================

        subjects_handled = ""
        exam_expertise = ""
        languages = ""

        leetcode = ""
        problems_done = ""
        other_profiles = ""


        if profile_type == (
            "Aptitude Trainer"
        ):

            st.markdown(
                "### Subjects Handled"
            )

            subjects_handled = (
                st.text_area(
                    "Subjects Handled",
                    value=data.get(
                        "Subjects Handled",
                        ""
                    ),
                    height=150,
                    label_visibility="collapsed"
                )
            )


            st.markdown(
                "### Exam / Placement Expertise"
            )

            exam_expertise = (
                st.text_area(
                    "Exam / Placement Expertise",
                    value=data.get(
                        "Exam Placement Expertise",
                        ""
                    ),
                    height=150,
                    label_visibility="collapsed"
                )
            )


            st.markdown(
                "### Languages"
            )

            languages = (
                st.text_input(
                    "Languages",
                    value=data.get(
                        "Languages",
                        ""
                    ),
                    label_visibility="collapsed"
                )
            )


        # =================================================
        # TECHNICAL TRAINER FIELDS
        # =================================================

        else:

            st.markdown(
                "### Competitive Coding Profiles"
            )

            leetcode = (
                st.text_input(
                    "LeetCode Profile Link",
                    value=data.get(
                        "LeetCode Profile Link",
                        ""
                    )
                )
            )

            problems_done = (
                st.text_input(
                    "No of Problems Solved",
                    value=data.get(
                        "No of Problems Done",
                        ""
                    )
                )
            )

            other_profiles = (
                st.text_area(
                    "Other Profiles",
                    value=data.get(
                        "Other Profiles",
                        ""
                    ),
                    height=100
                )
            )


        # =================================================
        # TRAINING EXPERTISE
        # =================================================

        st.markdown(
            "### Training Expertise"
        )

        training_expertise = (
            st.text_area(
                "Training Expertise",
                value=data.get(
                    "Training Expertise",
                    ""
                ),
                height=170,
                label_visibility="collapsed"
            )
        )


        # =================================================
        # CORE COMPETENCIES
        # =================================================

        st.markdown(
            "### Core Competencies"
        )

        core_competencies = (
            st.text_area(
                "Core Competencies",
                value=data.get(
                    "Core Competencies",
                    ""
                ),
                height=170,
                label_visibility="collapsed"
            )
        )


        # =================================================
        # TRAINING PROJECTS
        # =================================================

        st.markdown(
            "### Training Projects"
        )

        project_data = data.get(
            "Training Projects",
            []
        )

        if project_data:

            project_df = (
                pd.DataFrame(
                    project_data
                )
            )

        else:

            project_df = (
                pd.DataFrame(
                    [
                        {
                            "College / Client": "",
                            "Location": "",
                            "Domain / Subject Area": ""
                        }
                    ]
                )
            )


        edited_projects = (
            st.data_editor(
                project_df,
                num_rows="dynamic",
                hide_index=True,
                use_container_width=True,
                column_order=[
                    "College / Client",
                    "Location",
                    "Domain / Subject Area"
                ]
            )
        )


        # =================================================
        # OUTPUT TYPE
        # =================================================

        st.markdown(
            "### Output Format"
        )

        output_type = (
            st.radio(
                "Generate",
                [
                    "Word",
                    "PDF",
                    "Word + PDF"
                ],
                horizontal=True
            )
        )


        # =================================================
        # PDF STATUS
        # =================================================

        pdf_status = (
            get_pdf_conversion_status()
        )

        if output_type in [
            "PDF",
            "Word + PDF"
        ]:

            if pdf_status[
                "available"
            ]:

                st.success(
                    "PDF conversion available: "
                    + pdf_status[
                        "method"
                    ]
                )

            else:

                st.warning(
                    "PDF conversion is currently "
                    "not available: "
                    + pdf_status[
                        "method"
                    ]
                )


        # =================================================
        # GENERATE BUTTON
        # =================================================

        generate_button = (
            st.form_submit_button(
                "🚀 Generate Profile",
                type="primary",
                use_container_width=True
            )
        )


    # =====================================================
    # GENERATION
    # =====================================================

    if generate_button:

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not selected_template.exists():

            st.error(
                "Selected Word template "
                "does not exist."
            )

            st.stop()


        if not name.strip():

            st.error(
                "Trainer Name is required."
            )

            st.stop()


        # =================================================
        # FINAL DATA
        # =================================================

        final_data = {

            "Name":
                name.strip(),

            "Emp ID":
                emp_id.strip(),

            "Designation":
                profile_type,

            "Qualification":
                qualification.strip(),

            "Date of Joining":
                date_of_joining.strip(),

            "Experience":
                experience.strip(),

            "Company Mail":
                company_mail.strip(),

            "Phone Number":
                phone_number.strip(),

            "Rating":
                rating_to_stars(
                    rating
                ),

            "Skills":
                skills.strip(),

            "Summary":
                summary.strip(),

            "Certifications":
                certifications.strip(),

            "Professional Highlights":
                highlights.strip(),

            "Subjects Handled":
                subjects_handled.strip(),

            "Exam Placement Expertise":
                exam_expertise.strip(),

            "Languages":
                languages.strip(),

            "Training Expertise":
                training_expertise.strip(),

            "Core Competencies":
                core_competencies.strip(),

            "LeetCode Profile Link":
                leetcode.strip(),

            "No of Problems Done":
                problems_done.strip(),

            "Other Profiles":
                other_profiles.strip()
        }


        # =================================================
        # CLEAN PROJECT DATA
        # =================================================

        projects = []

        for _, row in (
            edited_projects.iterrows()
        ):

            college = (
                cleanup_dataframe_value(
                    row.get(
                        "College / Client",
                        ""
                    )
                )
            )

            location = (
                cleanup_dataframe_value(
                    row.get(
                        "Location",
                        ""
                    )
                )
            )

            subject = (
                cleanup_dataframe_value(
                    row.get(
                        "Domain / Subject Area",
                        ""
                    )
                )
            )

            if (
                college
                or location
                or subject
            ):

                projects.append(
                    {
                        "College / Client":
                            college,

                        "Location":
                            location,

                        "Domain / Subject Area":
                            subject
                    }
                )


        # =================================================
        # OUTPUT DIRECTORY
        # =================================================

        if profile_type == (
            "Aptitude Trainer"
        ):

            output_dir = (
                APTITUDE_OUTPUT_DIR
            )

        else:

            output_dir = (
                TECHNICAL_OUTPUT_DIR
            )


        # =================================================
        # FILE NAME
        # =================================================

        trainer_name = (
            safe_filename(
                name
            )
        )

        employee_id = (
            safe_filename(
                emp_id
            )
        )


        if emp_id.strip():

            base_filename = (
                f"{employee_id}_"
                f"{trainer_name}"
            )

        else:

            base_filename = (
                trainer_name
            )


        docx_path = (
            output_dir
            / (
                base_filename
                + ".docx"
            )
        )

        pdf_path = (
            output_dir
            / (
                base_filename
                + ".pdf"
            )
        )


        # =================================================
        # GENERATE WORD PROFILE
        # =================================================

        try:

            generated_docx = (
                generate_profile(
                    template_path=
                        selected_template,

                    output_path=
                        docx_path,

                    data=
                        final_data,

                    profile_type=
                        profile_type,

                    photo_path=
                        photo_path,

                    projects=
                        projects
                )
            )


            generated_files = {
                "docx":
                    generated_docx
            }


            # =================================================
            # GENERATE PDF
            # =================================================

            if output_type in [
                "PDF",
                "Word + PDF"
            ]:

                try:

                    generated_pdf = (
                        convert_docx_to_pdf(
                            generated_docx,
                            pdf_path
                        )
                    )

                    generated_files[
                        "pdf"
                    ] = generated_pdf

                except Exception as error:

                    st.warning(
                        "Word profile was generated "
                        "successfully, but PDF "
                        "conversion failed."
                    )

                    st.error(
                        str(error)
                    )


            # =================================================
            # SAVE GENERATED FILES
            # =================================================

            st.session_state[
                "generated_resume_files"
            ] = generated_files


            st.success(
                "Trainer profile generated successfully."
            )

        except Exception as error:

            st.error(
                "Profile generation failed."
            )

            st.exception(
                error
            )


# =========================================================
# DOWNLOAD SECTION
# =========================================================

generated_files = (
    st.session_state.get(
        "generated_resume_files",
        {}
    )
)


if generated_files:

    st.markdown("---")

    st.subheader(
        "Step 4: Download Generated Profile"
    )

    col_word, col_pdf = (
        st.columns(2)
    )


    # =====================================================
    # WORD DOWNLOAD
    # =====================================================

    docx_file = (
        generated_files.get(
            "docx"
        )
    )

    if docx_file:

        docx_file = Path(
            docx_file
        )

        if docx_file.exists():

            with col_word:

                st.download_button(
                    label=(
                        "⬇️ Download Word"
                    ),
                    data=(
                        read_file_bytes(
                            docx_file
                        )
                    ),
                    file_name=(
                        docx_file.name
                    ),
                    mime=(
                        "application/"
                        "vnd.openxmlformats-"
                        "officedocument."
                        "wordprocessingml."
                        "document"
                    ),
                    use_container_width=True
                )


    # =====================================================
    # PDF DOWNLOAD
    # =====================================================

    pdf_file = (
        generated_files.get(
            "pdf"
        )
    )

    if pdf_file:

        pdf_file = Path(
            pdf_file
        )

        if pdf_file.exists():

            with col_pdf:

                st.download_button(
                    label=(
                        "⬇️ Download PDF"
                    ),
                    data=(
                        read_file_bytes(
                            pdf_file
                        )
                    ),
                    file_name=(
                        pdf_file.name
                    ),
                    mime="application/pdf",
                    use_container_width=True
                )


# =========================================================
# RAW TEXT
# =========================================================

if data:

    with st.expander(
        "View Raw Extracted Resume Text"
    ):

        st.text(
            data.get(
                "Raw Text",
                ""
            )
        )