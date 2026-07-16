import os
import io
import zipfile
import streamlit as st
from services.profile_service import ProfileService

# -------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------
st.set_page_config(page_title="Generate Profiles", page_icon="📄", layout="wide")
service = ProfileService()

st.title("📄 Generate Trainer Profiles")
st.divider()

# Persistent State
if "docx_zip" not in st.session_state: st.session_state.docx_zip = None
if "pdf_zip" not in st.session_state: st.session_state.pdf_zip = None
if "gen_success" not in st.session_state: st.session_state.gen_success = False

# -------------------------------------------------------
# 1. TRAINER SELECTION
# -------------------------------------------------------
st.subheader("Trainers Selection")
gen_mode = st.radio("Select Mode", ["All Trainers", "Single Trainer", "Multiple Trainers", "Search Trainer"], horizontal=True)

selected_data = None
if gen_mode == "Single Trainer":
    selected_data = st.selectbox("Select a Trainer", service.get_trainer_display_list())
elif gen_mode == "Multiple Trainers":
    selected_data = st.multiselect("Select Multiple Trainers", service.get_trainer_display_list())
elif gen_mode == "Search Trainer":
    keyword = st.text_input("Enter name, skill, or ID to search")
    if keyword:
        search_df = service.search_trainers(keyword)
        if not search_df.empty:
            search_list = (search_df["Emp ID"].astype(str) + " - " + search_df["Name"]).tolist()
            selected_data = st.multiselect("Select from Results", search_list, default=search_list)
        else:
            st.info("No trainers found.")

# -------------------------------------------------------
# 2. FILE TYPE
# -------------------------------------------------------
st.subheader("Type of File")
out_format = st.radio("Select Format", ["Word", "PDF", "Both"], horizontal=True)

st.divider()

# -------------------------------------------------------
# 3. DOWNLOAD AREA (ALWAYS VISIBLE)
# -------------------------------------------------------
st.subheader("📥 Download Center")
c1, c2 = st.columns(2)

c1.download_button(
    "📥 Download Word ZIP", data=st.session_state.docx_zip or b"", 
    file_name="Word_Profiles.zip", mime="application/zip", 
    use_container_width=True, disabled=(st.session_state.docx_zip is None)
)
c2.download_button(
    "📥 Download PDF ZIP", data=st.session_state.pdf_zip or b"", 
    file_name="PDF_Profiles.zip", mime="application/zip", 
    use_container_width=True, disabled=(st.session_state.pdf_zip is None)
)

st.divider()

# -------------------------------------------------------
# 4. GENERATE ENGINE
# -------------------------------------------------------
if st.button("🚀 Generate Profiles", use_container_width=True, type="primary"):
    def get_id(val): return str(val).split(" - ")[0]
    
    with st.spinner("Processing..."):
        try:
            results = []
            if gen_mode == "All Trainers":
                results = service.generate_all(output_format=out_format)
            elif gen_mode == "Single Trainer":
                results = [service.generate_single(get_id(selected_data), output_format=out_format)]
            elif gen_mode in ["Multiple Trainers", "Search Trainer"]:
                results = service.generate_selected([get_id(x) for x in selected_data], output_format=out_format)
            
            success = [r for r in results if r.get('success')]
            
            # Pack DOCX
            if out_format in ["Word", "Both"]:
                paths = [r["docx"] for r in success if r.get("docx") and os.path.exists(r["docx"])]
                if paths:
                    buf = io.BytesIO()
                    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
                        for p in paths: z.write(p, os.path.basename(p))
                    st.session_state.docx_zip = buf.getvalue()
            
            # Pack PDF
            if out_format in ["PDF", "Both"]:
                paths = [r["pdf"] for r in success if r.get("pdf") and os.path.exists(r["pdf"])]
                if paths:
                    buf = io.BytesIO()
                    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
                        for p in paths: z.write(p, os.path.basename(p))
                    st.session_state.pdf_zip = buf.getvalue()
                else:
                    st.error("No PDF files created. Check server logs/dependencies.")

            st.session_state.gen_success = True
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")