import os
import shutil
import streamlit as st
from services.zip_service import ZipService
from services.pdf_word_service import PDFWordService

zip_service = ZipService()
st.set_page_config(
    page_title="PDF to Word",
    page_icon="📑",
    layout="wide"
)

st.title("📑 PDF to Word Converter")
st.markdown("---")

st.write(
    "Convert one or more PDF files into editable Microsoft Word (.docx) documents."
)

OUTPUT_FOLDER = "output/docx"
ZIP_FOLDER = "output/zip"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ZIP_FOLDER, exist_ok=True)

service = PDFWordService()

uploaded_files = st.file_uploader(
    "Upload PDF File(s)",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    st.success(f"{len(uploaded_files)} file(s) selected.")

    st.subheader("Selected Files")

    for file in uploaded_files:
        st.write(f"📄 {file.name}")

    st.markdown("")

    if st.button("🚀 Convert to Word", use_container_width=True):

        # Clear previous output
        for folder in [OUTPUT_FOLDER, ZIP_FOLDER]:

            if os.path.exists(folder):

                for file in os.listdir(folder):

                    path = os.path.join(folder, file)

                    if os.path.isfile(path):
                        os.remove(path)

        progress = st.progress(0)
        status = st.empty()

        results = []

        total = len(uploaded_files)

        for index, uploaded_file in enumerate(uploaded_files):

            status.write(f"Converting **{uploaded_file.name}**...")

            result = service.convert_files(
                [uploaded_file],
                OUTPUT_FOLDER
            )[0]

            results.append(result)

            progress.progress((index + 1) / total)

        progress.empty()
        status.empty()

        st.markdown("---")
        st.subheader("Conversion Summary")

        success = 0
        failed = 0

        for result in results:

            if result["success"]:

                success += 1

                st.success(
                    f"✅ {os.path.basename(result['output'])}"
                    
                )

            else:

                failed += 1

                st.error(
                    f"❌ {os.path.basename(result['input'])}\n\n{result['error']}"
                )

        st.markdown("---")

        col1, col2 = st.columns(2)

        col1.metric("Converted", success)
        col2.metric("Failed", failed)

        successful_files = [
            r["output"]
            for r in results
            if r["success"]
        ]

        # Single File Download
        if len(successful_files) == 1:

            docx_path = successful_files[0]

            with open(docx_path, "rb") as file:

                st.download_button(
                    label="⬇ Download Word File",
                    data=file,
                    file_name=os.path.basename(docx_path),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )

        # Multiple Files Download
        elif len(successful_files) > 1:

            zip_path = os.path.join(
                ZIP_FOLDER,
                "Converted_Word_Files.zip"
            )

            if os.path.exists(zip_path):
                os.remove(zip_path)

            zip_service.create_zip(
                successful_files,
                zip_path
            )

            with open(zip_path, "rb") as file:

                st.download_button(
                    label="⬇ Download ZIP",
                    data=file,
                    file_name="Converted_Word_Files.zip",
                    mime="application/zip",
                    use_container_width=True
                )

st.markdown("---")

with st.expander("ℹ Notes"):

    st.markdown(
        """
### Features

- Supports multiple PDF files.
- Preserves original file names.
- Output format is **.docx**.
- If multiple files are converted, they are downloaded as a ZIP archive.

### Supported Input

- PDF (.pdf)

### Output

- Microsoft Word (.docx)
"""
    )