import streamlit as st
from pypdf import PdfReader, PdfWriter
from io import BytesIO
import zipfile


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Split PDF",
    page_icon="✂️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main-title {
    font-size: 48px;
    font-weight: 700;
    color: #26344A;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 20px;
    color: #34495E;
    margin-bottom: 25px;
}

.section-line {
    border-top: 1px solid #D9DEE7;
    margin: 25px 0;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">✂️ Split PDF</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-line"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload a PDF file and create multiple separate PDFs from it.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# UPLOAD PDF
# ============================================================

st.subheader("Upload PDF")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"],
    help="Maximum file size: 200 MB"
)


# ============================================================
# PARSE PAGE RANGE
# ============================================================

def parse_page_range(page_range, total_pages):

    selected_pages = []

    parts = page_range.replace(" ", "").split(",")

    for part in parts:

        if "-" in part:

            values = part.split("-")

            if len(values) != 2:
                raise ValueError(
                    f"Invalid range: {part}"
                )

            start = int(values[0])
            end = int(values[1])

            if start < 1 or end > total_pages:
                raise ValueError(
                    f"Pages must be between 1 and {total_pages}"
                )

            if start > end:
                raise ValueError(
                    f"Invalid range: {part}"
                )

            for page in range(start, end + 1):
                selected_pages.append(page)

        else:

            page = int(part)

            if page < 1 or page > total_pages:
                raise ValueError(
                    f"Page {page} does not exist. "
                    f"PDF has {total_pages} pages."
                )

            selected_pages.append(page)

    # Remove duplicate pages
    selected_pages = list(dict.fromkeys(selected_pages))

    return selected_pages


# ============================================================
# MAIN APPLICATION
# ============================================================

if uploaded_file is not None:

    try:

        pdf_reader = PdfReader(uploaded_file)

        total_pages = len(pdf_reader.pages)

        st.success(
            f"PDF uploaded successfully — "
            f"{total_pages} page(s)"
        )

        st.markdown('<div class="section-line"></div>',
                    unsafe_allow_html=True)

        # ====================================================
        # MULTIPLE SPLITS
        # ====================================================

        st.subheader("Create Multiple Splits")

        st.write(
            f"Enter different page ranges for each output PDF. "
            f"Available pages: **1–{total_pages}**"
        )

        # ----------------------------------------------------
        # Number of splits
        # ----------------------------------------------------

        number_of_splits = st.number_input(
            "Number of PDF files to create",
            min_value=1,
            max_value=20,
            value=2,
            step=1
        )

        st.markdown("### Define Page Ranges")

        split_ranges = []

        for i in range(int(number_of_splits)):

            col1, col2 = st.columns([1, 3])

            with col1:

                st.write(
                    f"**Split {i + 1}**"
                )

            with col2:

                page_range = st.text_input(
                    f"Pages for Split {i + 1}",
                    placeholder="Example: 1-5 or 1,3,5-7",
                    key=f"split_range_{i}"
                )

                split_ranges.append(page_range)

        # ====================================================
        # FILE NAMES
        # ====================================================

        st.markdown("### Output File Names")

        file_names = []

        for i in range(int(number_of_splits)):

            file_name = st.text_input(
                f"File name for Split {i + 1}",
                value=f"split_{i + 1}.pdf",
                key=f"file_name_{i}"
            )

            # Make sure .pdf exists
            if not file_name.lower().endswith(".pdf"):
                file_name += ".pdf"

            file_names.append(file_name)

        # ====================================================
        # CREATE SPLITS
        # ====================================================

        st.markdown('<div class="section-line"></div>',
                    unsafe_allow_html=True)

        if st.button(
            "✂️ Create All PDFs",
            type="primary",
            use_container_width=True
        ):

            generated_files = []

            errors = []

            # ------------------------------------------------
            # Validate and generate every split
            # ------------------------------------------------

            for i in range(int(number_of_splits)):

                page_range = split_ranges[i].strip()

                if not page_range:

                    errors.append(
                        f"Split {i + 1}: Page range is empty."
                    )

                    continue

                try:

                    selected_pages = parse_page_range(
                        page_range,
                        total_pages
                    )

                    writer = PdfWriter()

                    for page_number in selected_pages:

                        writer.add_page(
                            pdf_reader.pages[page_number - 1]
                        )

                    output_pdf = BytesIO()

                    writer.write(output_pdf)

                    output_pdf.seek(0)

                    generated_files.append({
                        "name": file_names[i],
                        "data": output_pdf.getvalue(),
                        "pages": selected_pages
                    })

                except Exception as e:

                    errors.append(
                        f"Split {i + 1}: {str(e)}"
                    )

            # =================================================
            # DISPLAY ERRORS
            # =================================================

            if errors:

                st.error("Some splits could not be created:")

                for error in errors:

                    st.write(
                        f"• {error}"
                    )

            # =================================================
            # DISPLAY GENERATED FILES
            # =================================================

            if generated_files:

                st.markdown(
                    '<div class="section-line"></div>',
                    unsafe_allow_html=True
                )

                st.subheader(
                    f"Generated {len(generated_files)} PDF(s)"
                )

                # ------------------------------------------------
                # Individual downloads
                # ------------------------------------------------

                for index, pdf_file in enumerate(
                    generated_files
                ):

                    col1, col2 = st.columns(
                        [3, 1]
                    )

                    with col1:

                        pages_text = ", ".join(
                            map(
                                str,
                                pdf_file["pages"]
                            )
                        )

                        st.write(
                            f"📄 **{pdf_file['name']}**"
                        )

                        st.caption(
                            f"Pages: {pages_text}"
                        )

                    with col2:

                        st.download_button(
                            label="⬇️ Download",
                            data=pdf_file["data"],
                            file_name=pdf_file["name"],
                            mime="application/pdf",
                            key=f"download_{index}"
                        )

                # =================================================
                # CREATE ZIP FILE
                # =================================================

                st.markdown(
                    '<div class="section-line"></div>',
                    unsafe_allow_html=True
                )

                st.subheader(
                    "Download All"
                )

                zip_buffer = BytesIO()

                with zipfile.ZipFile(
                    zip_buffer,
                    "w",
                    zipfile.ZIP_DEFLATED
                ) as zip_file:

                    for pdf_file in generated_files:

                        zip_file.writestr(
                            pdf_file["name"],
                            pdf_file["data"]
                        )

                zip_buffer.seek(0)

                st.download_button(
                    label="📦 Download All PDFs as ZIP",
                    data=zip_buffer.getvalue(),
                    file_name="split_pdfs.zip",
                    mime="application/zip",
                    use_container_width=True
                )

    except Exception as e:

        st.error(
            f"Unable to read the PDF: {str(e)}"
        )


# ============================================================
# NOTES
# ============================================================

st.markdown(
    '<div class="section-line"></div>',
    unsafe_allow_html=True
)

with st.expander("ℹ️ Notes"):

    st.markdown("""
    ### How to use

    1. Upload one PDF.
    2. Select how many PDF files you want to create.
    3. Enter the page range for each split.
    4. Give each output file a name.
    5. Click **Create All PDFs**.
    6. Download each PDF separately or download everything as a ZIP.

    ### Examples

    **Example 1**

    ```text
    Split 1 → 1-5
    Split 2 → 6-10
    Split 3 → 11-15
    ```

    **Example 2**

    ```text
    Split 1 → 1,3,5
    Split 2 → 2,4,6
    Split 3 → 7-10
    ```

    The original PDF is never modified.
    """)