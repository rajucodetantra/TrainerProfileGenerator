import os
import streamlit as st

from services.pdf_split_service import PDFSplitService


# --------------------------------------------------------
# Page Configuration
# --------------------------------------------------------

st.set_page_config(
    page_title="Split PDF",
    page_icon="✂️",
    layout="wide"
)

st.title("✂️ Split PDF")
st.markdown("---")

st.write(
    "Upload a PDF file and extract any page range into a new PDF."
)

# --------------------------------------------------------
# Output Folder
# --------------------------------------------------------

OUTPUT_FOLDER = "output/split"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --------------------------------------------------------
# Service
# --------------------------------------------------------

service = PDFSplitService()

# --------------------------------------------------------
# Upload PDF
# --------------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# --------------------------------------------------------
# Process
# --------------------------------------------------------

if uploaded_file is not None:

    total_pages = service.get_total_pages(uploaded_file)

    st.success("PDF loaded successfully.")

    st.metric(
        "Total Pages",
        total_pages
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        start_page = st.number_input(
            "From Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1
        )

    with col2:

        end_page = st.number_input(
            "To Page",
            min_value=1,
            max_value=total_pages,
            value=total_pages,
            step=1
        )

    st.info(
        f"Selected Pages : {start_page} → {end_page}"
    )

    if start_page > end_page:

        st.error("Starting page cannot be greater than ending page.")

    else:

        st.markdown("")

        if st.button(
            "✂ Split PDF",
            use_container_width=True
        ):

            progress = st.progress(0)

            progress.progress(25)

            result = service.split_pdf(
                uploaded_file,
                int(start_page),
                int(end_page),
                OUTPUT_FOLDER
            )

            progress.progress(100)

            progress.empty()

            st.markdown("---")

            if result["success"]:

                st.success("PDF split successfully.")

                st.metric(
                    "Pages Extracted",
                    result["pages"]
                )

                with open(result["output"], "rb") as pdf:

                    st.download_button(
                        label="⬇ Download Split PDF",
                        data=pdf.read(),
                        file_name=os.path.basename(result["output"]),
                        mime="application/pdf",
                        use_container_width=True
                    )

            else:

                st.error(result["error"])

# --------------------------------------------------------
# Notes
# --------------------------------------------------------

st.markdown("---")

with st.expander("ℹ Notes", expanded=False):

    st.markdown("""
### Features

- Extract any page range from a PDF.
- Preserves original page quality.
- Supports all standard PDF files.
- Output filename format:
  - `OriginalFile_Pages_1_5.pdf`
- Fast processing using **pypdf**.

---

### Steps

1. Upload a PDF.
2. View the total pages.
3. Enter the starting page.
4. Enter the ending page.
5. Click **Split PDF**.
6. Download the extracted PDF.

---

### Example

Input:

Report.pdf

Pages:

1 2 3 4 5 6 7 8 9 10

Selected Range:

3 → 7

Output:

Report_Pages_3_7.pdf
""")