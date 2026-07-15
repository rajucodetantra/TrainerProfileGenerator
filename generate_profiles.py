import streamlit as st
import pandas as pd

from services.profile_service import ProfileService

st.set_page_config(
    page_title="Generate Profiles",
    page_icon="📄",
    layout="wide"
)

service = ProfileService()

st.title("📄 Generate Trainer Profiles")

st.divider()

trainers = service.get_trainers()

# -------------------------------------------------------
# Generation Mode
# -------------------------------------------------------

generation_mode = st.radio(

    "Generate Profiles",

    [

        "All Trainers",

        "Selected Trainers",

        "Search Trainer",

        "By Skill"

    ],

    horizontal=True

)

st.divider()

# -------------------------------------------------------
# Output Format
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

st.divider()

selected_trainers = None

selected_skill = None

search_emp = None

# -------------------------------------------------------
# ALL
# -------------------------------------------------------

if generation_mode == "All Trainers":

    st.info(

        f"Total Trainers : {len(trainers)}"

    )

# -------------------------------------------------------
# SELECTED
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
# SEARCH
# -------------------------------------------------------

elif generation_mode == "Search Trainer":

    search_emp = st.text_input(

        "Employee ID"

    )

# -------------------------------------------------------
# SKILL
# -------------------------------------------------------

elif generation_mode == "By Skill":

    skills = service.get_skills()

    selected_skill = st.selectbox(

        "Technology",

        skills

    )

st.divider()

progress = st.progress(0)

status = st.empty()

summary = st.empty()

# -------------------------------------------------------
# CALLBACK
# -------------------------------------------------------

def update_progress(current, total):

    progress.progress(

        current / total

    )

    status.info(

        f"Generating {current} of {total}"

    )
# -------------------------------------------------------
# Generate Button
# -------------------------------------------------------

if st.button(
    "🚀 Generate Profiles",
    use_container_width=True
):

    try:

        # ---------------------------------------------
        # Generate All
        # ---------------------------------------------

        if generation_mode == "All Trainers":

            results = service.generate_all(
                progress_callback=update_progress,
                generate_pdf=generate_pdf
            )

        # ---------------------------------------------
        # Generate Selected
        # ---------------------------------------------

        elif generation_mode == "Selected Trainers":

            if not selected_trainers:

                st.warning(
                    "Please select at least one trainer."
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
        # Generate Search
        # ---------------------------------------------

        elif generation_mode == "Search Trainer":

            if not search_emp:

                st.warning(
                    "Please enter Employee ID."
                )

                st.stop()

            result = service.generate_single(

                search_emp,

                generate_pdf=generate_pdf

            )

            results = [result]

            progress.progress(1.0)

        # ---------------------------------------------
        # Generate By Skill
        # ---------------------------------------------

        else:

            results = service.generate_by_skill(

                selected_skill,

                progress_callback=update_progress,

                generate_pdf=generate_pdf

            )

        # ---------------------------------------------
        # Summary
        # ---------------------------------------------

        success = [

            r

            for r in results

            if r["success"]

        ]

        failed = [

            r

            for r in results

            if not r["success"]

        ]

        summary.success(

            f"""
Generation Completed

✅ Success : {len(success)}

❌ Failed : {len(failed)}
"""
        )

        progress.progress(1.0)

        # ---------------------------------------------
        # Success Table
        # ---------------------------------------------

        if success:

            st.subheader(
                "Generated Profiles"
            )

            success_df = pd.DataFrame([

                {

                    "Employee ID": r["employee_id"],

                    "Trainer": r["trainer"],

                    "DOCX": r["docx"],

                    "PDF": r["pdf"]

                }

                for r in success

            ])

            st.dataframe(

                success_df,

                use_container_width=True

            )

        # ---------------------------------------------
        # Failed Table
        # ---------------------------------------------

        if failed:

            st.subheader(
                "Failed Profiles"
            )

            failed_df = pd.DataFrame([

                {

                    "Employee ID": r["employee_id"],

                    "Trainer": r["trainer"],

                    "Reason": r["message"]

                }

                for r in failed

            ])

            st.dataframe(

                failed_df,

                use_container_width=True

            )

        # ---------------------------------------------
        # Output Summary
        # ---------------------------------------------

        output = service.output_summary()

        st.divider()

        col1, col2 = st.columns(2)

        col1.metric(

            "DOCX Files",

            output["docx"]

        )

        col2.metric(

            "PDF Files",

            output["pdf"]

        )

    except Exception as e:

        st.error(str(e))