import os
import io
import zipfile
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
# CORE STATE PERSISTENCE (Fixes Streamlit Rerun Bug)
# -------------------------------------------------------
if "generation_results" not in st.session_state:
    st.session_state.generation_results = None
if "run_executed" not in st.session_state:
    st.session_state.run_executed = False
if "docx_zip_bytes" not in st.session_state:
    st.session_state.docx_zip_bytes = None
if "pdf_zip_bytes" not in st.session_state:
    st.session_state.pdf_zip_bytes = None

# -------------------------------------------------------
# LOAD TRAINERS
# -------------------------------------------------------
trainers = service.get_trainers()

# -------------------------------------------------------
# SIDEBAR / CONFIGURATION CONTROLS
# -------------------------------------------------------
with st.sidebar:
    st.header("Settings")
    generation_mode = st.radio(
        "Generation Type",
        ["All Trainers", "Single Trainer", "Selected Trainers", "By Skill", "By Qualification", "By Designation"]
    )
    
    output_format = st.radio(
        "Output Format",
        ["Word", "PDF", "Both"]
    )

if hasattr(service.config, "set_default_output"):
    service.config.set_default_output(output_format)

# -------------------------------------------------------
# FILTER SELECTION UI
# -------------------------------------------------------
selected_emp = None
selected_trainers = None
selected_skill = None
selected_qualification = None
selected_designation = None

if generation_mode == "All Trainers":
    st.info(f"📊 Total Trainers Found: {len(trainers)}")

elif generation_mode == "Single Trainer":
    trainers["Display"] = trainers["Emp ID"].astype(str) + " - " + trainers["Name"]
    selected_emp = st.selectbox("Select Trainer", trainers["Display"])

elif generation_mode == "Selected Trainers":
    trainers["Display"] = trainers["Emp ID"].astype(str) + " - " + trainers["Name"]
    selected_trainers = st.multiselect("Select Trainers", trainers["Display"])

elif generation_mode == "By Skill":
    selected_skill = st.selectbox("Select Skill", service.get_skills())

elif generation_mode == "By Qualification":
    selected_qualification = st.selectbox("Select Qualification", service.get_qualifications())

elif generation_mode == "By Designation":
    selected_designation = st.selectbox("Select Designation", service.get_designations())

st.divider()

# -------------------------------------------------------
# STATIC PERMANENT DOWNLOAD AREA (Always Visible)
# -------------------------------------------------------
st.subheader("📥 Action Center & Downloads")
download_col1, download_col2 = st.columns(2)

# These buttons are always rendered right here on the page layout, so they can never disappear.
download_col1.download_button(
    label="📥 Download DOCX ZIP Package",
    data=st.session_state.docx_zip_bytes if st.session_state.docx_zip_bytes else b"",
    file_name="DOCX_Profiles.zip",
    mime="application/zip",
    use_container_width=True,
    disabled=(st.session_state.docx_zip_bytes is None),
    key="docx_zip_action"
)

download_col2.download_button(
    label="📥 Download PDF ZIP Package",
    data=st.session_state.pdf_zip_bytes if st.session_state.pdf_zip_bytes else b"",
    file_name="PDF_Profiles.zip",
    mime="application/zip",
    use_container_width=True,
    disabled=(st.session_state.pdf_zip_bytes is None),
    key="pdf_zip_action"
)

st.divider()

# -------------------------------------------------------
# PROGRESS AND ENGINE TRIGGER
# -------------------------------------------------------
progress_bar = st.progress(0)
status = st.empty()

def update_progress(current, total):
    progress_bar.progress(current / total)
    status.info(f"Processing Profile {current} of {total}...")

if st.button("🚀 Run Profile Generator Engine", use_container_width=True, type="primary"):
    # Clear old byte caches on new runs
    st.session_state.docx_zip_bytes = None
    st.session_state.pdf_zip_bytes = None
    st.session_state.run_executed = False
    
    try:
        results = []

        if generation_mode == "All Trainers":
            results = service.generate_all(progress_callback=update_progress, output_format=output_format)
        elif generation_mode == "Single Trainer":
            if selected_emp is None:
                st.warning("Please select a valid trainer targeting vector.")
                st.stop()
            emp_id = selected_emp.split(" - ")[0]
            result = service.generate_single(emp_id, output_format=output_format)
            results = [result]
        elif generation_mode == "Selected Trainers":
            if not selected_trainers:
                st.warning("No trainers highlighted for rendering targets.")
                st.stop()
            emp_ids = [item.split(" - ")[0] for item in selected_trainers]
            results = service.generate_selected(emp_ids, progress_callback=update_progress, output_format=output_format)
        elif generation_mode == "By Skill":
            results = service.generate_by_skill(selected_skill, progress_callback=update_progress, output_format=output_format)
        elif generation_mode == "By Qualification":
            results = service.generate_by_qualification(selected_qualification, progress_callback=update_progress, output_format=output_format)
        else:
            results = service.generate_by_designation(selected_designation, progress_callback=update_progress, output_format=output_format)

        st.session_state.generation_results = results
        success = [item for item in results if item["success"]]

        # --- PROCESS IN-MEMORY DOCX ZIP ---
        docx_paths = [item["docx"] for item in success if item.get("docx") and os.path.exists(item["docx"])]
        if docx_paths:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for path in docx_paths:
                    zf.write(path, arcname=os.path.basename(path))
            st.session_state.docx_zip_bytes = zip_buffer.getvalue()

        # --- PROCESS IN-MEMORY PDF ZIP ---
        pdf_paths = [item["pdf"] for item in success if item.get("pdf") and os.path.exists(item["pdf"])]
        if pdf_paths:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for path in pdf_paths:
                    zf.write(path, arcname=os.path.basename(path))
            st.session_state.pdf_zip_bytes = zip_buffer.getvalue()

        st.session_state.run_executed = True
        progress_bar.progress(1.0)
        status.empty()
        st.rerun()  # Instantly update button states to 'Active'

    except Exception as e:
        st.error(f"Engine Crash Context: {str(e)}")

# -------------------------------------------------------
# POST-RUN DATA VIEWS
# -------------------------------------------------------
if st.session_state.run_executed and st.session_state.generation_results:
    results = st.session_state.generation_results
    success = [item for item in results if item["success"]]
    failed = [item for item in results if not item["success"]]

    st.success(f"Execution Summary: Successfully Compiled {len(success)} profiles. (Failed: {len(failed)})")

    if success:
        st.subheader("Generated Records Log")
        st.dataframe(
            pd.DataFrame([{
                "ID": item["employee_id"], 
                "Trainer Name": item["trainer"], 
                "DOCX Link": item["docx"] if item["docx"] else "Skipped", 
                "PDF Link": item["pdf"] if item["pdf"] else "Failed/Missing Engine"
            } for item in success]), 
            use_container_width=True, hide_index=True
        )

    if failed:
        st.subheader("Failed Pipeline Exceptions")
        st.dataframe(
            pd.DataFrame([{"ID": item["employee_id"], "Name": item["trainer"], "Error Message": item["message"]} for item in failed]), 
            use_container_width=True, hide_index=True
        )

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.divider()
st.caption("Trainer Profile Generator | CodeTantra Tech Solutions Pvt. Ltd.")