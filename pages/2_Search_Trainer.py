import os
import streamlit as st
import pandas as pd

from services.profile_service import ProfileService

# -------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------

st.set_page_config(
    page_title="Search Trainer",
    page_icon="🔍",
    layout="wide"
)

service = ProfileService()

st.title("🔍 Search Trainer")

st.divider()

# -------------------------------------------------------
# LOAD TRAINERS
# -------------------------------------------------------

try:

    trainers = service.get_trainers()

except Exception as e:

    st.error(str(e))

    st.stop()

# -------------------------------------------------------
# SEARCH TYPE
# -------------------------------------------------------

search_type = st.selectbox(

    "Search By",

    [

        "Employee ID",

        "Trainer Name",

        "Designation",

        "Qualification",

        "Skills"

    ]

)

column_map = {

    "Employee ID": "Emp ID",

    "Trainer Name": "Name",

    "Designation": "Designation",

    "Qualification": "Qualification",

    "Skills": "Skills"

}

column = column_map[search_type]

search = st.text_input(

    f"Enter {search_type}"

)

# -------------------------------------------------------
# SEARCH
# -------------------------------------------------------

filtered = trainers.copy()

if search.strip():

    filtered = filtered[

        filtered[column]

        .astype(str)

        .str.contains(

            search,

            case=False,

            na=False

        )

    ]

st.success(

    f"{len(filtered)} trainer(s) found"

)

if filtered.empty:

    st.warning(

        "No trainer found."

    )

    st.stop()

# -------------------------------------------------------
# SELECT TRAINER
# -------------------------------------------------------

filtered["Display"] = (

    filtered["Emp ID"]

    .astype(str)

    +

    " - "

    +

    filtered["Name"]

)

selected = st.selectbox(

    "Select Trainer",

    filtered["Display"]

)

emp_id = selected.split(" - ")[0]

trainer = service.get_trainer(

    emp_id

)

st.divider()

left, right = st.columns(

    [1, 2]

)

# -------------------------------------------------------
# LEFT SIDE
# -------------------------------------------------------

with left:

    st.subheader("Trainer Details")

    image = trainer.get("Image", "")

    if image and os.path.exists(image):

        st.image(

            image,

            width=180

        )

    st.write(

        "**Employee ID**"

    )

    st.write(

        trainer.get(

            "Emp ID",

            ""

        )

    )

    st.write(

        "**Name**"

    )

    st.write(

        trainer.get(

            "Name",

            ""

        )

    )

    st.write(

        "**Designation**"

    )

    st.write(

        trainer.get(

            "Designation",

            ""

        )

    )

    st.write(

        "**Qualification**"

    )

    st.write(

        trainer.get(

            "Qualification",

            ""

        )

    )

    st.write(

        "**Experience**"

    )

    st.write(

        trainer.get(

            "Experience",

            ""

        )

    )

    st.write(

        "**Rating**"

    )

    st.write(

        trainer.get(

            "Trainer Rating",

            ""

        )

    )
# -------------------------------------------------------
# RIGHT SIDE
# -------------------------------------------------------

with right:

    st.subheader(

        trainer.get(

            "Name",

            ""

        )

    )

    # --------------------------------------------

    st.markdown(

        "### 💻 Core Skills"

    )

    st.write(

        trainer.get(

            "Skills",

            ""

        )

    )

    # --------------------------------------------

    st.markdown(

        "### 📝 Professional Summary"

    )

    st.write(

        trainer.get(

            "Summary",

            ""

        )

    )

    # --------------------------------------------

    st.markdown(

        "### ⚙ Technical Expertise"

    )

    st.write(

        trainer.get(

            "Technical Expertise",

            ""

        )

    )

    # --------------------------------------------

    st.markdown(

        "### 🎯 Training Expertise"

    )

    st.write(

        trainer.get(

            "Training Expertise",

            ""

        )

    )

    # --------------------------------------------

    st.markdown(

        "### ⭐ Professional Highlights"

    )

    st.write(

        trainer.get(

            "Professional Highlights",

            ""

        )

    )

    # --------------------------------------------

    st.markdown(

        "### 🤝 Core Competencies"

    )

    st.write(

        trainer.get(

            "Core Competencies",

            ""

        )

    )

st.divider()

# -------------------------------------------------------
# ACTION BUTTONS
# -------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

preview_clicked = c1.button(

    "👁 Preview Profile",

    use_container_width=True

)

word_clicked = c2.button(

    "📄 Generate Word",

    use_container_width=True

)

pdf_clicked = c3.button(

    "📕 Generate PDF",

    use_container_width=True

)

both_clicked = c4.button(

    "📦 Generate Both",

    use_container_width=True

)

# -------------------------------------------------------
# PREVIEW
# -------------------------------------------------------

if preview_clicked:

    st.success(

        "Trainer Preview"

    )

    preview = {

        "Employee ID": trainer.get(

            "Emp ID",

            ""

        ),

        "Name": trainer.get(

            "Name",

            ""

        ),

        "Designation": trainer.get(

            "Designation",

            ""

        ),

        "Qualification": trainer.get(

            "Qualification",

            ""

        ),

        "Experience": trainer.get(

            "Experience",

            ""

        ),

        "Skills": trainer.get(

            "Skills",

            ""

        ),

        "Summary": trainer.get(

            "Summary",

            ""

        )

    }

    st.json(preview)
# -------------------------------------------------------
# GENERATE WORD
# -------------------------------------------------------

if word_clicked:

    try:

        result = service.generate_single(

            trainer["Emp ID"],

            generate_pdf=False

        )

        if result["success"]:

            st.success(

                "Word Profile Generated Successfully."

            )

            if result["docx"]:

                st.code(

                    result["docx"]

                )

        else:

            st.error(

                result["message"]

            )

    except Exception as e:

        st.error(

            str(e)

        )

# -------------------------------------------------------
# GENERATE PDF
# -------------------------------------------------------

if pdf_clicked:

    try:

        service.config.set_default_output(

            "PDF"

        )

        result = service.generate_single(

            trainer["Emp ID"],

            generate_pdf=True

        )

        if result["success"]:

            st.success(

                "PDF Profile Generated Successfully."

            )

            if result["pdf"]:

                st.code(

                    result["pdf"]

                )

        else:

            st.error(

                result["message"]

            )

    except Exception as e:

        st.error(

            str(e)

        )

# -------------------------------------------------------
# GENERATE BOTH
# -------------------------------------------------------

if both_clicked:

    try:

        service.config.set_default_output(

            "Both"

        )

        result = service.generate_single(

            trainer["Emp ID"],

            generate_pdf=True

        )

        if result["success"]:

            st.success(

                "Word & PDF Profiles Generated Successfully."

            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(

                    "**DOCX File**"

                )

                st.code(

                    result["docx"]

                )

            with col2:

                st.write(

                    "**PDF File**"

                )

                st.code(

                    result["pdf"]

                )

        else:

            st.error(

                result["message"]

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