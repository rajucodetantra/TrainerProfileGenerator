import os
import time

import streamlit as st

from services.word_pdf_service import WordPDFService
from services.zip_service import ZipService
from services.download_service import DownloadService
from services.file_utils import FileUtils
from services.logger import Logger


# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title="Word to PDF",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Word to PDF Converter")
st.markdown("---")

st.write(
    """
Convert one or more Microsoft Word (.docx) files into PDF documents
while preserving the original filenames.
"""
)

# --------------------------------------------------------
# Folders
# --------------------------------------------------------

OUTPUT_FOLDER = "output/pdf"
ZIP_FOLDER = "output/zip"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ZIP_FOLDER, exist_ok=True)

# --------------------------------------------------------
# Services
# --------------------------------------------------------

service = WordPDFService()
zip_service = ZipService()
logger = Logger()

# --------------------------------------------------------
# Upload Files
# --------------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload Word File(s)",
    type=["docx"],
    accept_multiple_files=True
)

# --------------------------------------------------------
# Display Uploaded Files
# --------------------------------------------------------

if uploaded_files:

    st.success(
        f"{len(uploaded_files)} file(s) selected."
    )

    st.subheader("Selected Files")

    total_size = 0

    for i, file in enumerate(uploaded_files, start=1):

        total_size += file.size

        st.write(
            f"{i}. 📄 {file.name} "
            f"({FileUtils.readable_size(file.size)})"
        )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Files Selected",
            len(uploaded_files)
        )

    with col2:

        st.metric(
            "Total Size",
            FileUtils.readable_size(total_size)
        )

    st.info(
        "Original filenames will be preserved after conversion."
    )

    st.markdown("")

    # --------------------------------------------------------
    # Convert Button
    # --------------------------------------------------------

    if st.button(
        "🚀 Convert to PDF",
        use_container_width=True
    ):

        start_time = time.time()

        logger.info(
            "Word to PDF conversion started."
        )

        # Remove previous output files

        for folder in [OUTPUT_FOLDER, ZIP_FOLDER]:

            if os.path.exists(folder):

                for file in os.listdir(folder):

                    path = os.path.join(folder, file)

                    if os.path.isfile(path):

                        os.remove(path)

        progress = st.progress(0)

        status = st.empty()

        results = []

        total_files = len(uploaded_files)
        # --------------------------------------------------------
        # Convert Files
        # --------------------------------------------------------

        for index, uploaded_file in enumerate(uploaded_files):

            status.write(
                f"Converting **{uploaded_file.name}**..."
            )

            logger.info(
                f"Converting {uploaded_file.name}"
            )

            result = service.convert_files(
                [uploaded_file],
                OUTPUT_FOLDER
            )[0]

            results.append(result)

            progress.progress(
                (index + 1) / total_files
            )

        progress.empty()
        status.empty()

        elapsed = FileUtils.execution_time(
            start_time
        )

        logger.info(
            f"Conversion completed in {elapsed} seconds."
        )

        st.markdown("---")

        st.subheader("Conversion Summary")

        success = 0
        failed = 0

        for result in results:

            if result["success"]:

                success += 1

                st.success(
                    f"""
✅ {os.path.basename(result['output'])}

Size : {FileUtils.file_size(result['output'])}
"""
                )

                logger.info(
                    f"Created {result['output']}"
                )

            else:

                failed += 1

                logger.error(
                    result["error"]
                )

                st.error(
                    f"""
❌ {os.path.basename(result['input'])}

{result['error']}
"""
                )

        st.markdown("---")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Converted",
                success
            )

        with col2:

            st.metric(
                "Failed",
                failed
            )

        with col3:

            st.metric(
                "Time",
                f"{elapsed} sec"
            )

        successful_files = [

            r["output"]

            for r in results

            if r["success"]

        ]

        # --------------------------------------------------------
        # Single PDF
        # --------------------------------------------------------

        if len(successful_files) == 1:

            pdf_path = successful_files[0]

            download_path = DownloadService.save_to_downloads(
                pdf_path
            )

            st.success(
                f"""
PDF automatically saved to

{download_path}
"""
            )

            with open(pdf_path, "rb") as file:

                st.download_button(

                    label="⬇ Download PDF Again",

                    data=file.read(),

                    file_name=os.path.basename(pdf_path),

                    mime="application/pdf",

                    use_container_width=True

                )

        # --------------------------------------------------------
        # Multiple PDFs
        # --------------------------------------------------------

        elif len(successful_files) > 1:

            zip_path = os.path.join(

                ZIP_FOLDER,

                "Converted_PDFs.zip"

            )

            if os.path.exists(zip_path):

                os.remove(zip_path)

            zip_service.create_zip(

                successful_files,

                zip_path

            )

            download_path = DownloadService.save_to_downloads(

                zip_path

            )

            st.success(
                f"""
ZIP automatically saved to

{download_path}
"""
            )

            with open(zip_path, "rb") as file:

                st.download_button(

                    label="⬇ Download ZIP Again",

                    data=file.read(),

                    file_name="Converted_PDFs.zip",

                    mime="application/zip",

                    use_container_width=True

                )
# --------------------------------------------------------
# Notes
# --------------------------------------------------------

st.markdown("---")

with st.expander("ℹ Notes", expanded=False):

    st.markdown("""
### Features

- Convert one or more Microsoft Word (.docx) files to PDF.
- Preserves the original filename.
- Supports batch conversion.
- Automatically saves the converted file(s) to the **Windows Downloads** folder.
- Provides a **Download Again** button.
- Displays:
  - File size
  - Number of converted files
  - Failed files
  - Conversion time
- Creates a ZIP archive automatically when multiple PDFs are generated.
- Progress bar during conversion.
- Detailed logging using `logger.py`.

---

### Requirements

- Microsoft Word must be installed.
- Windows Operating System.
- Python packages:
  - pywin32
  - streamlit

---

### Output

**Single File**

Resume.docx

↓

Resume.pdf

Automatically saved to:

`C:\\Users\\<username>\\Downloads\\`

---

**Multiple Files**

Resume1.docx

Resume2.docx

↓

Converted_PDFs.zip

Automatically saved to:

`C:\\Users\\<username>\\Downloads\\`
""")