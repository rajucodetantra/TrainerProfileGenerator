import os
import streamlit as st
import pandas as pd

from services.profile_service import ProfileService
from modules.word_generator import WordGenerator
from modules.project_extractor import ProjectExtractor

# -------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------
st.set_page_config(
    page_title="Search Trainer",
    page_icon="🔍",
    layout="wide"
)

service = ProfileService()
project_extractor = ProjectExtractor("data/Projects.xlsx")

st.title("🔍 Search Trainer")
st.divider()

# -------------------------------------------------------
# DATA LOADING
# -------------------------------------------------------
try:
    trainers = service.get_trainers()
except Exception as e:
    st.error(f"Failed to load trainers dataset: {str(e)}")
    st.stop()

# -------------------------------------------------------
# SEARCH FILTERS SETUP
# -------------------------------------------------------
search_type = st.selectbox(
    "Search By",
    ["Employee ID", "Trainer Name", "Designation", "Qualification", "Skills"]
)

column_map = {
    "Employee ID": "Emp ID",
    "Trainer Name": "Name",
    "Designation": "Designation",
    "Qualification": "Qualification",
    "Skills": "Skills"
}

column = column_map[search_type]
search = st.text_input(f"Enter {search_type}")

filtered = trainers.copy()
if search.strip():
    filtered = filtered[
        filtered[column].astype(str).str.contains(search, case=False, na=False)
    ]

st.success(f"{len(filtered)} trainer(s) discovered")
if filtered.empty:
    st.warning("No tracking records match the current parameters.")
    st.stop()

filtered["Display"] = filtered["Emp ID"].astype(str) + " - " + filtered["Name"].astype(str)
selected = st.selectbox("Select Trainer", filtered["Display"])
emp_id_raw = selected.split(" - ")[0].strip()

try:
    trainer = service.get_trainer(emp_id_raw)
except Exception as e:
    st.error(f"Error fetching profile context metrics: {str(e)}")
    st.stop()

st.divider()

# -------------------------------------------------------
# PRESENTATION INTERFACE (TWO COLUMNS)
# -------------------------------------------------------
left, right = st.columns([1, 2])

with left:
    st.subheader("Trainer Details")
    image = trainer.get("Image", "")
    if image and os.path.exists(image):
        st.image(image, width=180)

    fields = [
        ("Employee ID", "Emp ID"),
        ("Name", "Name"),
        ("Designation", "Designation"),
        ("Qualification", "Qualification"),
        ("Experience", "Experience"),
        ("Company Mail", "Company Mail"),
        ("Phone Number", "Phone Number"),
        ("Trainer Rating", "Rating")
    ]
    for label, key in fields:
        val = str(trainer.get(key, "")).strip()
        if val and val.lower() != "nan":
            st.write(f"**{label}**")
            st.write(val)

with right:
    st.subheader(trainer.get("Name", "Trainer Profile"))

    sections = [
        ("💻 Core Skills", "Skills"),
        ("📝 Professional Summary", "Summary"),
        ("⚙ Technical Expertise", "Technical Expertise"),
        ("⭐ Professional Certifications", "Certifications"),
        ("📈 Competitive Programming", "Competitive Programming"),
        ("🔗 Professional Coding Profiles", "Coding Profiles"),
        ("🎯 Training Expertise", "Training Expertise"),
        ("🎖 Professional Highlights", "Professional Highlights"),
        ("🤝 Core Competencies", "Core Competencies")
    ]

    for title, key in sections:
        content = str(trainer.get(key, "")).strip()
        if content and content.lower() not in ["nan", "", "n/a", "none"]:
            st.markdown(f"### {title}")
            st.write(content)

    # --- INJECT PROJECTS VIA RECONCILED EMP ID FORMATTING ---
    target_id = str(trainer.get("Emp ID", emp_id_raw)).strip()
    if target_id.isdigit():
        lookup_id = f"CT{int(target_id):04d}"
    else:
        lookup_id = target_id if target_id.startswith("CT") else f"CT{target_id}"

    project_data = project_extractor.get_trainer_projects(lookup_id)

    if project_data["ongoing"] or project_data["completed"]:
        st.markdown("### 📊 Training Projects")

        if project_data["ongoing"]:
            st.markdown("#### ⏳ Ongoing Project(s)")
            df_ongoing = pd.DataFrame(project_data["ongoing"])
            df_ongoing.columns = ["S.No", "College", "Place", "Subject", "From", "To"]
            st.table(df_ongoing.set_index("S.No"))

        if project_data["completed"]:
            st.markdown("#### ✅ Completed Projects")
            df_completed = pd.DataFrame(project_data["completed"])
            df_completed.columns = ["S.No", "College", "Place", "Subject", "From", "To"]
            st.dataframe(df_completed.set_index("S.No"), use_container_width=True)

st.divider()

# -------------------------------------------------------
# INTEGRATED EXPORT ACTIONS
# -------------------------------------------------------
c1, c2, c3, c4 = st.columns(4)
safe_name = str(trainer.get("Name", "Trainer")).replace(" ", "_")
emp_id_str = str(trainer.get("Emp ID", "0000"))

if c1.button("👁 Preview Profile", use_container_width=True):
    st.success("JSON Configuration Structure Checked")
    st.json({k: trainer.get(v, "") for k, v in column_map.items()})

try:
    word_gen = WordGenerator(service.config.template_file, trainer)
    word_bytes = word_gen.generate_bytes()
    c2.download_button(
        label="📄 Download Word",
        data=word_bytes,
        file_name=f"{emp_id_str}_{safe_name}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )
except Exception as e:
    c2.error(f"Word Generation Failure: {str(e)}")

try:
    result_pdf = service.generate_single(trainer.get("Emp ID"), output_format="PDF")
    if result_pdf.get("success") and os.path.exists(result_pdf.get("pdf", "")):
        with open(result_pdf["pdf"], "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
        c3.download_button(
            label="📕 Download PDF",
            data=pdf_bytes,
            file_name=f"{emp_id_str}_{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
except Exception as e:
    c3.error(f"PDF Pipeline Error: {str(e)}")

try:
    result_both = service.generate_single(trainer.get("Emp ID"), output_format="Both")
    if result_both.get("success"):
        paths = [result_both.get(f, "") for f in ["docx", "pdf"] if result_both.get(f, "") and os.path.exists(result_both.get(f, ""))]
        if paths:
            zip_path = service.create_docx_zip(paths)
            with open(zip_path, "rb") as zf:
                c4.download_button(
                    label="📦 Download Both (ZIP)",
                    data=zf.read(),
                    file_name=f"{emp_id_str}_{safe_name}_Profiles.zip",
                    mime="application/zip",
                    use_container_width=True
                )
except Exception as e:
    pass