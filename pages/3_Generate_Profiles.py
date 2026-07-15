import os
import pandas as pd
import streamlit as st

from services.profile_service import ProfileService

# -------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------

st.set_page_config(
    page_title="Generate Profiles",
    page_icon="📄",
    layout="wide"
)

service = ProfileService()

st.title("📄 Generate Trainer Profiles")

st.divider()

# -------------------------------------------------------
# LOAD TRAINERS
# -------------------------------------------------------

trainers = service.get_trainers()

# -------------------------------------------------------
# GENERATION MODE
# -------------------------------------------------------

generation_mode = st.radio(

    "Generation Type",

    [

        "All Trainers",

        "Single Trainer",

        "Selected Trainers",

        "By Skill",

        "By Qualification",

        "By Designation"

    ],

    horizontal=True

)

# -------------------------------------------------------
# OUTPUT FORMAT
# -------------------------------------------------------

output_format = st.radio(

    "Output Format",

    [

        "Word",

        "PDF",

        "Both"

    ],

    horizontal=True

)

generate_pdf = output_format in [

    "PDF",

    "Both"

]

service.config.set_default_output(output_format)

st.divider()

# -------------------------------------------------------
# VARIABLES
# -------------------------------------------------------

selected_emp = None

selected_trainers = None

selected_skill = None

selected_qualification = None

selected_designation = None

# -------------------------------------------------------
# ALL TRAINERS
# -------------------------------------------------------

if generation_mode == "All Trainers":

    st.info(

        f"Total Trainers : {len(trainers)}"

    )

# -------------------------------------------------------
# SINGLE TRAINER
# -------------------------------------------------------

elif generation_mode == "Single Trainer":

    trainers["Display"] = (

        trainers["Emp ID"].astype(str)

        + " - "

        + trainers["Name"]

    )

    selected_emp = st.selectbox(

        "Select Trainer",

        trainers["Display"]

    )

# -------------------------------------------------------
# SELECTED TRAINERS
# -------------------------------------------------------

elif generation_mode == "Selected Trainers":

    trainers["Display"] = (

        trainers["Emp ID"].astype(str)

        + " - "

        + trainers["Name"]

    )

    selected_trainers = st.multiselect(

        "Select Trainers",

        trainers["Display"]

    )

# -------------------------------------------------------
# BY SKILL
# -------------------------------------------------------

elif generation_mode == "By Skill":

    selected_skill = st.selectbox(

        "Select Skill",

        service.get_skills()

    )

# -------------------------------------------------------
# BY QUALIFICATION
# -------------------------------------------------------

elif generation_mode == "By Qualification":

    selected_qualification = st.selectbox(

        "Select Qualification",

        service.get_qualifications()

    )

# -------------------------------------------------------
# BY DESIGNATION
# -------------------------------------------------------

elif generation_mode == "By Designation":

    selected_designation = st.selectbox(

        "Select Designation",

        service.get_designations()

    )

st.divider()

# -------------------------------------------------------
# PROGRESS
# -------------------------------------------------------

progress_bar = st.progress(0)

status = st.empty()

summary = st.empty()

# -------------------------------------------------------
# CALLBACK
# -------------------------------------------------------

def update_progress(current, total):

    progress_bar.progress(

        current / total

    )

    status.info(

        f"Generating {current} of {total}"

    )
# -------------------------------------------------------
# GENERATE BUTTON
# -------------------------------------------------------

if st.button(

    "🚀 Generate Profiles",

    use_container_width=True

):

    try:

        # ---------------------------------------------
        # ALL TRAINERS
        # ---------------------------------------------

        if generation_mode == "All Trainers":

            results = service.generate_all(

                progress_callback=update_progress,

                generate_pdf=generate_pdf

            )

        # ---------------------------------------------
        # SINGLE TRAINER
        # ---------------------------------------------

        elif generation_mode == "Single Trainer":

            if selected_emp is None:

                st.warning(

                    "Please select a trainer."

                )

                st.stop()

            emp_id = selected_emp.split(" - ")[0]

            result = service.generate_single(

                emp_id,

                generate_pdf=generate_pdf

            )

            results = [

                result

            ]

            progress_bar.progress(1.0)

        # ---------------------------------------------
        # SELECTED TRAINERS
        # ---------------------------------------------

        elif generation_mode == "Selected Trainers":

            if not selected_trainers:

                st.warning(

                    "Please select one or more trainers."

                )

                st.stop()

            emp_ids = [

                item.split(" - ")[0]

                for item in selected_trainers

            ]

            results = service.generate_selected(

                emp_ids,

                progress_callback=update_progress,

                generate_pdf=generate_pdf

            )

        # ---------------------------------------------
        # BY SKILL
        # ---------------------------------------------

        elif generation_mode == "By Skill":

            results = service.generate_by_skill(

                selected_skill,

                progress_callback=update_progress,

                generate_pdf=generate_pdf

            )

        # ---------------------------------------------
        # BY QUALIFICATION
        # ---------------------------------------------

        elif generation_mode == "By Qualification":

            results = service.generate_by_qualification(

                selected_qualification,

                progress_callback=update_progress,

                generate_pdf=generate_pdf

            )

        # ---------------------------------------------
        # BY DESIGNATION
        # ---------------------------------------------

        else:

            results = service.generate_by_designation(

                selected_designation,

                progress_callback=update_progress,

                generate_pdf=generate_pdf

            )

        # ---------------------------------------------
        # SUCCESS / FAILED
        # ---------------------------------------------

        success = [

            item

            for item in results

            if item["success"]

        ]

        failed = [

            item

            for item in results

            if not item["success"]

        ]

        summary.success(

            f"""

Generation Completed

✅ Successful : {len(success)}

❌ Failed : {len(failed)}

"""

        )

        progress_bar.progress(1.0)

        # ---------------------------------------------
        # SUCCESS TABLE
        # ---------------------------------------------

        if success:

            st.subheader(

                "Generated Profiles"

            )

            success_df = pd.DataFrame([

                {

                    "Employee ID":

                    item["employee_id"],

                    "Trainer":

                    item["trainer"],

                    "DOCX":

                    item["docx"],

                    "PDF":

                    item["pdf"]

                }

                for item in success

            ])

            st.dataframe(

                success_df,

                use_container_width=True,

                hide_index=True

            )

        # ---------------------------------------------
        # FAILED TABLE
        # ---------------------------------------------

        if failed:

            st.subheader(

                "Failed Profiles"

            )

            failed_df = pd.DataFrame([

                {

                    "Employee ID":

                    item["employee_id"],

                    "Trainer":

                    item["trainer"],

                    "Reason":

                    item["message"]

                }

                for item in failed

            ])

            st.dataframe(

                failed_df,

                use_container_width=True,

                hide_index=True

            )
        # ---------------------------------------------
        # OUTPUT SUMMARY
        # ---------------------------------------------

        output = service.output_summary()

        st.divider()

        st.subheader(
            "Output Summary"
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "DOCX Files",
            output["docx"]
        )

        col2.metric(
            "PDF Files",
            output["pdf"]
        )

        # ---------------------------------------------
        # DOWNLOAD ZIP FILES
        # ---------------------------------------------

        st.divider()

        st.subheader(
            "Download Generated Profiles"
        )

        download_col1, download_col2 = st.columns(2)

        if output["docx"] > 0:

            zip_file = service.create_docx_zip()

            with open(
                zip_file,
                "rb"
            ) as file:

                download_col1.download_button(

                    label="📥 Download DOCX ZIP",

                    data=file,

                    file_name="DOCX_Profiles.zip",

                    mime="application/zip",

                    use_container_width=True

                )

        if output["pdf"] > 0:

            zip_file = service.create_pdf_zip()

            with open(
                zip_file,
                "rb"
            ) as file:

                download_col2.download_button(

                    label="📥 Download PDF ZIP",

                    data=file,

                    file_name="PDF_Profiles.zip",

                    mime="application/zip",

                    use_container_width=True

                )

        # ---------------------------------------------
        # OPEN OUTPUT FOLDER
        # ---------------------------------------------

        st.divider()

        if st.button(

            "📂 Open Output Folder",

            use_container_width=True

        ):

            output_folder = os.path.abspath(
                "output"
            )

            os.startfile(
                output_folder
            )

    except Exception as e:

        st.error(
            str(e)
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