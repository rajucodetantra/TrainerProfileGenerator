import sys
import uuid
import re
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from login import require_login

import pandas as pd
import streamlit as st

from ui_styles import apply_global_styles


# =========================================================
# PROJECT ROOT
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


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
# LOGIN / GLOBAL STYLE
# =========================================================

require_login()

try:
    apply_global_styles()
except Exception:
    pass


# =========================================================
# IMPORT INDEPENDENT MODULES
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
# HELPERS
# =========================================================

def safe_filename(value):
    value = str(value or "").strip()

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

    return value or "Trainer"


def read_file_bytes(file_path):
    with open(file_path, "rb") as file:
        return file.read()


def rating_to_stars(rating):
    try:
        rating = int(rating)

        if rating <= 0:
            return ""

        return "★" * rating

    except Exception:
        return str(rating or "")


def cleanup_dataframe_value(value):
    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass

    value = str(value).strip()

    if value.lower() in [
        "nan",
        "none"
    ]:
        return ""

    return value


def make_experience_dataframe(experience_data):
    if experience_data:
        df = pd.DataFrame(experience_data)
    else:
        df = pd.DataFrame(
            [
                {
                    "Name of Organization": "",
                    "Years Worked": ""
                }
            ]
        )

    for required_column in [
        "Name of Organization",
        "Years Worked"
    ]:
        if required_column not in df.columns:
            df[required_column] = ""

    return df[
        [
            "Name of Organization",
            "Years Worked"
        ]
    ]


def make_projects_dataframe(project_data):
    if project_data:
        df = pd.DataFrame(project_data)
    else:
        df = pd.DataFrame(
            [
                {
                    "College / Client": "",
                    "Location": "",
                    "Domain / Subject Area": ""
                }
            ]
        )

    for required_column in [
        "College / Client",
        "Location",
        "Domain / Subject Area"
    ]:
        if required_column not in df.columns:
            df[required_column] = ""

    return df[
        [
            "College / Client",
            "Location",
            "Domain / Subject Area"
        ]
    ]


def clean_experience_rows(dataframe):
    experience_details = []

    for _, row in dataframe.iterrows():

        organization = cleanup_dataframe_value(
            row.get(
                "Name of Organization",
                ""
            )
        )

        years_worked = cleanup_dataframe_value(
            row.get(
                "Years Worked",
                ""
            )
        )

        if organization:
            experience_details.append(
                {
                    "Name of Organization":
                        organization,

                    "Years Worked":
                        years_worked
                }
            )

    return experience_details


def clean_project_rows(dataframe):
    projects = []

    for _, row in dataframe.iterrows():

        college = cleanup_dataframe_value(
            row.get(
                "College / Client",
                ""
            )
        )

        location = cleanup_dataframe_value(
            row.get(
                "Location",
                ""
            )
        )

        subject = cleanup_dataframe_value(
            row.get(
                "Domain / Subject Area",
                ""
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

    return projects


def create_batch_zip(
    generated_profiles,
    output_type
):
    """
    Build one ZIP containing all successfully generated
    profiles.

    Word/
        CTxxxx_Name.docx

    PDF/
        CTxxxx_Name.pdf
    """

    buffer = BytesIO()

    with ZipFile(
        buffer,
        "w",
        ZIP_DEFLATED
    ) as zip_file:

        for item in generated_profiles:

            docx_path = item.get("docx")
            pdf_path = item.get("pdf")

            if (
                output_type in [
                    "Word",
                    "Word + PDF"
                ]
                and docx_path
            ):
                docx_path = Path(docx_path)

                if docx_path.exists():
                    zip_file.write(
                        docx_path,
                        arcname=(
                            "Word/"
                            + docx_path.name
                        )
                    )

            if (
                output_type in [
                    "PDF",
                    "Word + PDF"
                ]
                and pdf_path
            ):
                pdf_path = Path(pdf_path)

                if pdf_path.exists():
                    zip_file.write(
                        pdf_path,
                        arcname=(
                            "PDF/"
                            + pdf_path.name
                        )
                    )

    return buffer.getvalue()


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
    "Upload one or multiple resumes and generate "
    "Technical Trainer or Aptitude Trainer profiles together."
)

st.info(
    "This module is independent. It does not modify "
    "Trainers.xlsx, Projects.xlsx, or your existing "
    "profile-generation pages."
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
    selected_template = TECHNICAL_TEMPLATE
    output_dir = TECHNICAL_OUTPUT_DIR
else:
    selected_template = APTITUDE_TEMPLATE
    output_dir = APTITUDE_OUTPUT_DIR


if selected_template.exists():
    st.success(
        "Template available: "
        + selected_template.name
    )
else:
    st.error(
        "Template not found: "
        + str(selected_template)
    )


# =========================================================
# STEP 2 - MULTIPLE FILE UPLOAD
# =========================================================

st.markdown("---")

st.subheader(
    "Step 2: Upload Resumes"
)

uploaded_files = st.file_uploader(
    "Upload Trainer Resume PDFs",
    type=["pdf"],
    accept_multiple_files=True,
    help=(
        "You can select one PDF or multiple PDF resumes "
        "at the same time."
    )
)


if uploaded_files:

    st.caption(
        f"{len(uploaded_files)} resume(s) selected."
    )

    extract_button = st.button(
        "🔍 Extract All Resumes",
        type="primary"
    )

    if extract_button:

        batch_data = []
        extraction_errors = []

        progress = st.progress(0)

        total_files = len(uploaded_files)

        for index, uploaded_file in enumerate(
            uploaded_files,
            start=1
        ):

            try:
                pdf_bytes = (
                    uploaded_file.getvalue()
                )

                raw_text = extract_pdf_text(
                    pdf_bytes
                )

                if not raw_text.strip():
                    extraction_errors.append(
                        (
                            uploaded_file.name,
                            "No readable text found."
                        )
                    )

                    progress.progress(
                        index / total_files
                    )

                    continue

                parsed_data = parse_resume(
                    raw_text,
                    profile_type
                )

                photo_file = (
                    TEMP_DIR
                    / (
                        uuid.uuid4().hex
                        + ".png"
                    )
                )

                photo_path = (
                    extract_candidate_photo(
                        pdf_bytes,
                        str(photo_file)
                    )
                )

                parsed_data[
                    "Photo Path"
                ] = photo_path

                parsed_data[
                    "Profile Type"
                ] = profile_type

                parsed_data[
                    "Original File Name"
                ] = uploaded_file.name

                batch_data.append(
                    parsed_data
                )

            except Exception as error:
                extraction_errors.append(
                    (
                        uploaded_file.name,
                        str(error)
                    )
                )

            progress.progress(
                index / total_files
            )

        progress.empty()

        st.session_state[
            "batch_resume_profile_data"
        ] = batch_data

        st.session_state[
            "batch_profile_type"
        ] = profile_type

        st.session_state[
            "batch_generated_profiles"
        ] = []

        st.session_state[
            "batch_zip_bytes"
        ] = None

        st.session_state[
            "batch_output_type"
        ] = None

        if batch_data:
            st.success(
                f"{len(batch_data)} resume(s) "
                "extracted successfully."
            )

        if extraction_errors:

            st.warning(
                f"{len(extraction_errors)} resume(s) "
                "could not be extracted."
            )

            for file_name, message in extraction_errors:
                st.error(
                    f"{file_name}: {message}"
                )


# =========================================================
# GET BATCH DATA
# =========================================================

batch_data = st.session_state.get(
    "batch_resume_profile_data",
    []
)


# =========================================================
# REVIEW ALL EXTRACTED RESUMES
# =========================================================

if batch_data:

    if (
        st.session_state.get(
            "batch_profile_type"
        )
        != profile_type
    ):
        st.warning(
            "You changed the trainer type after extraction. "
            "Click Extract All Resumes again."
        )

        st.stop()

    st.markdown("---")

    st.subheader(
        "Step 3: Review / Edit All Profiles"
    )

    st.caption(
        "Each resume is shown separately below. "
        "Correct any extracted information before generating."
    )

    reviewed_candidates = []

    with st.form(
        "batch_resume_profile_form"
    ):

        for index, data in enumerate(
            batch_data
        ):

            original_name = data.get(
                "Original File Name",
                f"Resume {index + 1}"
            )

            extracted_name = data.get(
                "Name",
                ""
            )

            expander_title = (
                f"{index + 1}. "
                + (
                    extracted_name
                    if extracted_name
                    else original_name
                )
            )

            with st.expander(
                expander_title,
                expanded=(
                    index == 0
                )
            ):

                # =========================================
                # PHOTO
                # =========================================

                photo_path = data.get(
                    "Photo Path"
                )

                if (
                    photo_path
                    and Path(
                        photo_path
                    ).exists()
                ):
                    p1, p2 = st.columns(
                        [1, 4]
                    )

                    with p1:
                        st.image(
                            photo_path,
                            width=130
                        )

                    with p2:
                        st.success(
                            "Candidate photo detected."
                        )
                else:
                    st.warning(
                        "Candidate photo was not detected."
                    )

                # =========================================
                # BASIC DETAILS
                # =========================================

                st.markdown(
                    "#### Basic Details"
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
                        ),
                        key=f"name_{index}"
                    )

                    emp_id = st.text_input(
                        "Employee ID",
                        value=data.get(
                            "Emp ID",
                            ""
                        ),
                        placeholder="Example: CT0935",
                        key=f"emp_id_{index}"
                    )

                    st.text_input(
                        "Designation",
                        value=profile_type,
                        disabled=True,
                        key=f"designation_{index}"
                    )

                    qualification = (
                        st.text_input(
                            "Qualification",
                            value=data.get(
                                "Qualification",
                                ""
                            ),
                            key=f"qualification_{index}"
                        )
                    )

                    date_of_joining = (
                        st.text_input(
                            "Date of Joining",
                            value=data.get(
                                "Date of Joining",
                                ""
                            ),
                            placeholder="DD-MM-YYYY",
                            key=f"doj_{index}"
                        )
                    )

                with col2:

                    experience = (
                        st.text_input(
                            "Total Experience",
                            value=data.get(
                                "Experience",
                                ""
                            ),
                            key=f"experience_{index}"
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
                            ),
                            key=f"company_mail_{index}"
                        )
                    )

                    phone_number = (
                        st.text_input(
                            "Phone Number",
                            value=data.get(
                                "Phone Number",
                                ""
                            ),
                            key=f"phone_{index}"
                        )
                    )

                    st.text_input(
                        "Personal Email",
                        value=data.get(
                            "Personal Email",
                            ""
                        ),
                        disabled=True,
                        key=f"personal_email_{index}"
                    )

                    rating = st.selectbox(
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
                        ),
                        key=f"rating_{index}"
                    )

                st.text_input(
                    "LinkedIn",
                    value=data.get(
                        "LinkedIn",
                        ""
                    ),
                    disabled=True,
                    key=f"linkedin_{index}"
                )

                # =========================================
                # CORE SKILLS
                # =========================================

                st.markdown(
                    "#### Core Skills"
                )

                skills = st.text_area(
                    "Core Skills",
                    value=data.get(
                        "Skills",
                        ""
                    ),
                    height=100,
                    label_visibility="collapsed",
                    key=f"skills_{index}"
                )

                # =========================================
                # SUMMARY
                # =========================================

                st.markdown(
                    "#### Professional Summary"
                )

                summary = st.text_area(
                    "Professional Summary",
                    value=data.get(
                        "Summary",
                        ""
                    ),
                    height=180,
                    label_visibility="collapsed",
                    key=f"summary_{index}"
                )

                # =========================================
                # EXPERIENCE TABLE
                # =========================================

                st.markdown(
                    "#### Professional Experience"
                )

                experience_df = (
                    make_experience_dataframe(
                        data.get(
                            "Experience Details",
                            []
                        )
                    )
                )

                edited_experience = (
                    st.data_editor(
                        experience_df,
                        num_rows="dynamic",
                        hide_index=True,
                        use_container_width=True,
                        key=f"experience_editor_{index}",
                        column_config={
                            "Name of Organization":
                                st.column_config.TextColumn(
                                    "Name of Organization",
                                    width="large"
                                ),

                            "Years Worked":
                                st.column_config.TextColumn(
                                    "Years Worked",
                                    width="medium"
                                )
                        }
                    )
                )

                # =========================================
                # CERTIFICATIONS
                # =========================================

                st.markdown(
                    "#### Professional Certifications"
                )

                certifications = (
                    st.text_area(
                        "Professional Certifications",
                        value=data.get(
                            "Certifications",
                            ""
                        ),
                        height=130,
                        label_visibility="collapsed",
                        key=f"certifications_{index}"
                    )
                )

                # =========================================
                # HIGHLIGHTS
                # =========================================

                st.markdown(
                    "#### Professional Highlights"
                )

                highlights = (
                    st.text_area(
                        "Professional Highlights",
                        value=data.get(
                            "Professional Highlights",
                            ""
                        ),
                        height=170,
                        label_visibility="collapsed",
                        key=f"highlights_{index}"
                    )
                )

                # =========================================
                # DEFAULT TYPE-SPECIFIC VALUES
                # =========================================

                subjects_handled = ""
                exam_expertise = ""
                languages = ""

                leetcode = ""
                problems_done = ""
                other_profiles = ""

                # =========================================
                # APTITUDE
                # =========================================

                if profile_type == (
                    "Aptitude Trainer"
                ):

                    st.markdown(
                        "#### Subjects Handled"
                    )

                    subjects_handled = (
                        st.text_area(
                            "Subjects Handled",
                            value=data.get(
                                "Subjects Handled",
                                ""
                            ),
                            height=140,
                            label_visibility="collapsed",
                            key=f"subjects_{index}"
                        )
                    )

                    st.markdown(
                        "#### Exam / Placement Expertise"
                    )

                    exam_expertise = (
                        st.text_area(
                            "Exam / Placement Expertise",
                            value=data.get(
                                "Exam Placement Expertise",
                                ""
                            ),
                            height=140,
                            label_visibility="collapsed",
                            key=f"exam_expertise_{index}"
                        )
                    )

                    st.markdown(
                        "#### Languages"
                    )

                    languages = (
                        st.text_input(
                            "Languages",
                            value=data.get(
                                "Languages",
                                ""
                            ),
                            label_visibility="collapsed",
                            key=f"languages_{index}"
                        )
                    )

                # =========================================
                # TECHNICAL
                # =========================================

                else:

                    st.markdown(
                        "#### Competitive Coding Profiles"
                    )

                    leetcode = (
                        st.text_input(
                            "LeetCode Profile Link",
                            value=data.get(
                                "LeetCode Profile Link",
                                ""
                            ),
                            key=f"leetcode_{index}"
                        )
                    )

                    problems_done = (
                        st.text_input(
                            "No of Problems Solved",
                            value=data.get(
                                "No of Problems Done",
                                ""
                            ),
                            key=f"problems_{index}"
                        )
                    )

                    other_profiles = (
                        st.text_area(
                            "Other Profiles",
                            value=data.get(
                                "Other Profiles",
                                ""
                            ),
                            height=90,
                            key=f"other_profiles_{index}"
                        )
                    )

                # =========================================
                # TRAINING EXPERTISE
                # =========================================

                st.markdown(
                    "#### Training Expertise"
                )

                training_expertise = (
                    st.text_area(
                        "Training Expertise",
                        value=data.get(
                            "Training Expertise",
                            ""
                        ),
                        height=160,
                        label_visibility="collapsed",
                        key=f"training_expertise_{index}"
                    )
                )

                # =========================================
                # CORE COMPETENCIES
                # =========================================

                st.markdown(
                    "#### Core Competencies"
                )

                core_competencies = (
                    st.text_area(
                        "Core Competencies",
                        value=data.get(
                            "Core Competencies",
                            ""
                        ),
                        height=160,
                        label_visibility="collapsed",
                        key=f"core_competencies_{index}"
                    )
                )

                # =========================================
                # TRAINING PROJECTS
                # =========================================

                st.markdown(
                    "#### Training Projects"
                )

                project_df = (
                    make_projects_dataframe(
                        data.get(
                            "Training Projects",
                            []
                        )
                    )
                )

                edited_projects = (
                    st.data_editor(
                        project_df,
                        num_rows="dynamic",
                        hide_index=True,
                        use_container_width=True,
                        key=f"projects_editor_{index}"
                    )
                )

                # =========================================
                # STORE REVIEWED VALUES
                # =========================================

                reviewed_candidates.append(
                    {
                        "index":
                            index,

                        "photo_path":
                            photo_path,

                        "name":
                            name,

                        "emp_id":
                            emp_id,

                        "qualification":
                            qualification,

                        "date_of_joining":
                            date_of_joining,

                        "experience":
                            experience,

                        "company_mail":
                            company_mail,

                        "phone_number":
                            phone_number,

                        "rating":
                            rating,

                        "skills":
                            skills,

                        "summary":
                            summary,

                        "edited_experience":
                            edited_experience,

                        "certifications":
                            certifications,

                        "highlights":
                            highlights,

                        "subjects_handled":
                            subjects_handled,

                        "exam_expertise":
                            exam_expertise,

                        "languages":
                            languages,

                        "leetcode":
                            leetcode,

                        "problems_done":
                            problems_done,

                        "other_profiles":
                            other_profiles,

                        "training_expertise":
                            training_expertise,

                        "core_competencies":
                            core_competencies,

                        "edited_projects":
                            edited_projects,

                        "original_file_name":
                            original_name
                    }
                )

        # =================================================
        # OUTPUT FORMAT FOR ENTIRE BATCH
        # =================================================

        st.markdown("---")

        st.markdown(
            "### Output Format for All Profiles"
        )

        output_type = st.radio(
            "Generate",
            [
                "Word",
                "PDF",
                "Word + PDF"
            ],
            horizontal=True,
            key="batch_output_type_selector"
        )

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
                    "PDF conversion is not available: "
                    + pdf_status[
                        "method"
                    ]
                )

        generate_all_button = (
            st.form_submit_button(
                f"🚀 Generate All {len(batch_data)} Profiles",
                type="primary",
                use_container_width=True
            )
        )


    # =====================================================
    # GENERATE ALL PROFILES
    # =====================================================

    if generate_all_button:

        if not selected_template.exists():
            st.error(
                "Selected Word template does not exist."
            )
            st.stop()

        generated_profiles = []
        generation_errors = []

        used_base_names = set()

        progress = st.progress(0)

        total_candidates = len(
            reviewed_candidates
        )

        for position, candidate in enumerate(
            reviewed_candidates,
            start=1
        ):

            try:
                name = (
                    candidate[
                        "name"
                    ].strip()
                )

                if not name:
                    raise ValueError(
                        "Trainer name is missing."
                    )

                experience_details = (
                    clean_experience_rows(
                        candidate[
                            "edited_experience"
                        ]
                    )
                )

                projects = (
                    clean_project_rows(
                        candidate[
                            "edited_projects"
                        ]
                    )
                )

                final_data = {

                    "Name":
                        name,

                    "Emp ID":
                        candidate[
                            "emp_id"
                        ].strip(),

                    "Designation":
                        profile_type,

                    "Qualification":
                        candidate[
                            "qualification"
                        ].strip(),

                    "Date of Joining":
                        candidate[
                            "date_of_joining"
                        ].strip(),

                    "Experience":
                        candidate[
                            "experience"
                        ].strip(),

                    "Company Mail":
                        candidate[
                            "company_mail"
                        ].strip(),

                    "Phone Number":
                        candidate[
                            "phone_number"
                        ].strip(),

                    "Rating":
                        rating_to_stars(
                            candidate[
                                "rating"
                            ]
                        ),

                    "Skills":
                        candidate[
                            "skills"
                        ].strip(),

                    "Summary":
                        candidate[
                            "summary"
                        ].strip(),

                    "Certifications":
                        candidate[
                            "certifications"
                        ].strip(),

                    "Professional Highlights":
                        candidate[
                            "highlights"
                        ].strip(),

                    "Experience Details":
                        experience_details,

                    "Subjects Handled":
                        candidate[
                            "subjects_handled"
                        ].strip(),

                    "Exam Placement Expertise":
                        candidate[
                            "exam_expertise"
                        ].strip(),

                    "Languages":
                        candidate[
                            "languages"
                        ].strip(),

                    "Training Expertise":
                        candidate[
                            "training_expertise"
                        ].strip(),

                    "Core Competencies":
                        candidate[
                            "core_competencies"
                        ].strip(),

                    "LeetCode Profile Link":
                        candidate[
                            "leetcode"
                        ].strip(),

                    "No of Problems Done":
                        candidate[
                            "problems_done"
                        ].strip(),

                    "Other Profiles":
                        candidate[
                            "other_profiles"
                        ].strip(),

                    "Training Projects":
                        projects
                }

                trainer_name = safe_filename(
                    name
                )

                emp_id = candidate[
                    "emp_id"
                ].strip()

                if emp_id:
                    base_filename = (
                        safe_filename(
                            emp_id
                        )
                        + "_"
                        + trainer_name
                    )
                else:
                    base_filename = (
                        trainer_name
                    )

                original_base = base_filename
                duplicate_number = 2

                while (
                    base_filename.lower()
                    in used_base_names
                ):
                    base_filename = (
                        original_base
                        + "_"
                        + str(
                            duplicate_number
                        )
                    )

                    duplicate_number += 1

                used_base_names.add(
                    base_filename.lower()
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
                            candidate[
                                "photo_path"
                            ],

                        projects=
                            projects,

                        experience_details=
                            experience_details
                    )
                )

                record = {
                    "name":
                        name,

                    "docx":
                        generated_docx,

                    "pdf":
                        None
                }

                if output_type in [
                    "PDF",
                    "Word + PDF"
                ]:

                    generated_pdf = (
                        convert_docx_to_pdf(
                            generated_docx,
                            pdf_path
                        )
                    )

                    record[
                        "pdf"
                    ] = generated_pdf

                generated_profiles.append(
                    record
                )

            except Exception as error:
                generation_errors.append(
                    {
                        "Resume":
                            candidate.get(
                                "original_file_name",
                                ""
                            ),

                        "Name":
                            candidate.get(
                                "name",
                                ""
                            ),

                        "Error":
                            str(error)
                    }
                )

            progress.progress(
                position
                / total_candidates
            )

        progress.empty()

        st.session_state[
            "batch_generated_profiles"
        ] = generated_profiles

        st.session_state[
            "batch_output_type"
        ] = output_type

        if generated_profiles:

            zip_bytes = (
                create_batch_zip(
                    generated_profiles,
                    output_type
                )
            )

            st.session_state[
                "batch_zip_bytes"
            ] = zip_bytes

            st.success(
                f"{len(generated_profiles)} profile(s) "
                "generated successfully."
            )

        else:
            st.session_state[
                "batch_zip_bytes"
            ] = None

        if generation_errors:

            st.warning(
                f"{len(generation_errors)} profile(s) "
                "could not be generated."
            )

            st.dataframe(
                pd.DataFrame(
                    generation_errors
                ),
                hide_index=True,
                use_container_width=True
            )


# =========================================================
# STEP 4 - DOWNLOAD ALL
# =========================================================

generated_profiles = (
    st.session_state.get(
        "batch_generated_profiles",
        []
    )
)

zip_bytes = (
    st.session_state.get(
        "batch_zip_bytes"
    )
)

saved_output_type = (
    st.session_state.get(
        "batch_output_type"
    )
)


if generated_profiles:

    st.markdown("---")

    st.subheader(
        "Step 4: Download Generated Profiles"
    )

    result_rows = []

    for item in generated_profiles:

        result_rows.append(
            {
                "Trainer":
                    item.get(
                        "name",
                        ""
                    ),

                "Word":
                    (
                        "Generated"
                        if item.get(
                            "docx"
                        )
                        else ""
                    ),

                "PDF":
                    (
                        "Generated"
                        if item.get(
                            "pdf"
                        )
                        else ""
                    )
            }
        )

    st.dataframe(
        pd.DataFrame(
            result_rows
        ),
        hide_index=True,
        use_container_width=True
    )

    if zip_bytes:

        st.download_button(
            label=(
                "⬇️ Download All Profiles as ZIP"
            ),
            data=zip_bytes,
            file_name=(
                "Generated_Trainer_Profiles.zip"
            ),
            mime="application/zip",
            use_container_width=True
        )

    # -----------------------------------------------------
    # OPTIONAL INDIVIDUAL DOWNLOADS
    # -----------------------------------------------------

    with st.expander(
        "Individual Profile Downloads"
    ):

        for index, item in enumerate(
            generated_profiles
        ):

            st.markdown(
                f"**{index + 1}. "
                f"{item.get('name', 'Trainer')}**"
            )

            col_word, col_pdf = (
                st.columns(2)
            )

            docx_file = item.get(
                "docx"
            )

            if (
                saved_output_type
                in [
                    "Word",
                    "Word + PDF"
                ]
                and docx_file
            ):

                docx_file = Path(
                    docx_file
                )

                if docx_file.exists():

                    with col_word:

                        st.download_button(
                            "⬇️ Word",
                            data=read_file_bytes(
                                docx_file
                            ),
                            file_name=
                                docx_file.name,
                            mime=(
                                "application/"
                                "vnd.openxmlformats-"
                                "officedocument."
                                "wordprocessingml."
                                "document"
                            ),
                            key=(
                                f"download_word_"
                                f"{index}"
                            ),
                            use_container_width=True
                        )

            pdf_file = item.get(
                "pdf"
            )

            if (
                saved_output_type
                in [
                    "PDF",
                    "Word + PDF"
                ]
                and pdf_file
            ):

                pdf_file = Path(
                    pdf_file
                )

                if pdf_file.exists():

                    with col_pdf:

                        st.download_button(
                            "⬇️ PDF",
                            data=read_file_bytes(
                                pdf_file
                            ),
                            file_name=
                                pdf_file.name,
                            mime=(
                                "application/pdf"
                            ),
                            key=(
                                f"download_pdf_"
                                f"{index}"
                            ),
                            use_container_width=True
                        )


# =========================================================
# RAW EXTRACTED TEXT
# =========================================================

if batch_data:

    with st.expander(
        "View Raw Extracted Resume Text"
    ):

        for index, item in enumerate(
            batch_data,
            start=1
        ):

            st.markdown(
                f"### {index}. "
                + item.get(
                    "Original File Name",
                    "Resume"
                )
            )

            st.text(
                item.get(
                    "Raw Text",
                    ""
                )
            )

            st.markdown("---")
