import os
import time
import streamlit as st

from services.pdf_merge_service import PDFMergeService
from services.download_service import DownloadService
from services.file_utils import FileUtils
from services.logger import Logger

st.set_page_config(
    page_title="Combine PDF",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Combine PDF Files")
st.markdown("---")

st.write(
    "Upload two or more PDF files and merge them into a single PDF."
)

OUTPUT_FOLDER = "output/merged"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

service = PDFMergeService()
logger = Logger()

# ----------------------------------------------------------
# Upload Files
# ----------------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload PDF Files",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    # Initialize session state
    if (
        "pdf_order" not in st.session_state
        or len(st.session_state.pdf_order) != len(uploaded_files)
    ):
        st.session_state.pdf_order = uploaded_files.copy()

    st.success(
        f"{len(st.session_state.pdf_order)} PDF file(s) selected."
    )

    st.subheader("Selected Files")

    # ----------------------------------------------------------
    # Reordering
    # ----------------------------------------------------------

    for i in range(len(st.session_state.pdf_order)):

        file = st.session_state.pdf_order[i]

        c1, c2, c3 = st.columns([8,1,1])

        with c1:

            st.write(
                f"📄 {file.name} ({FileUtils.readable_size(file.size)})"
            )

        with c2:

            if i > 0:

                if st.button("⬆", key=f"up{i}"):

                    st.session_state.pdf_order[i-1], st.session_state.pdf_order[i] = (
                        st.session_state.pdf_order[i],
                        st.session_state.pdf_order[i-1]
                    )

                    st.rerun()

        with c3:

            if i < len(st.session_state.pdf_order)-1:

                if st.button("⬇", key=f"down{i}"):

                    st.session_state.pdf_order[i+1], st.session_state.pdf_order[i] = (
                        st.session_state.pdf_order[i],
                        st.session_state.pdf_order[i+1]
                    )

                    st.rerun()

    st.markdown("---")

    # Reset uploaded file pointers before counting pages
    for pdf in st.session_state.pdf_order:
        pdf.seek(0)

    total_pages = service.get_total_pages(
        st.session_state.pdf_order
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Files Selected",
            len(st.session_state.pdf_order)
        )

    with col2:

        st.metric(
            "Total Pages",
            total_pages
        )

    st.info(
        "PDFs will be merged in the above order."
    )

    # ----------------------------------------------------------

    if st.button(
        "📚 Combine PDFs",
        use_container_width=True
    ):

        start = time.time()

        output_pdf = os.path.join(
            OUTPUT_FOLDER,
            "CTCombined.pdf"
        )

        if os.path.exists(output_pdf):
            os.remove(output_pdf)

        logger.info("Starting PDF Merge")

        progress = st.progress(0)

        progress.progress(25)

        # Reset uploaded file pointers before merging
        for pdf in st.session_state.pdf_order:
            pdf.seek(0)

        result = service.merge_files(
            st.session_state.pdf_order,
            OUTPUT_FOLDER
        )

        progress.progress(100)

        progress.empty()

        elapsed = FileUtils.execution_time(start)

        st.markdown("---")

        if result["success"]:

            logger.info("PDF Merge Completed")

            

            st.success("PDFs combined successfully.")

            col1, col2 = st.columns(2)

            try:
                download_path = DownloadService.save_to_downloads(
                    result["output"]
                )
            except Exception:
            # Streamlit Cloud/Linux doesn't have a Windows Downloads folder
                download_path = "Downloaded using the button below."

            with col1:

                st.metric(
                    "Pages",
                    result["pages"]
                )

            with col2:

                st.metric(
                    "Time",
                    f"{elapsed} sec"
                )

            st.info(
                f"File Size : {FileUtils.file_size(result['output'])}"
            )

            st.success(download_path)

            with open(result["output"], "rb") as pdf:

                st.download_button(
                    label="⬇ Download Again",
                    data=pdf,
                    file_name="CTCombined.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        else:

            logger.error(result["error"])

            st.error(result["error"])

st.markdown("---")

with st.expander("ℹ Notes"):

    st.markdown(
        """
### Features

- Merge unlimited PDF files.
- Reorder files using ▲ ▼ buttons.
- Shows total pages.
- Shows file sizes.
- Shows processing time.
- Automatically saves the merged PDF to the Windows Downloads folder.
- Download button is also provided.
- Output file name is **CTCombined.pdf**.
"""
    )