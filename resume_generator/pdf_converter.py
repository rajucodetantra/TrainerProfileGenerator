import os
import shutil
import subprocess
from pathlib import Path


# =========================================================
# MAIN FUNCTION
# =========================================================

def convert_docx_to_pdf(
    docx_path,
    pdf_path=None
):
    """
    Convert generated Word document to PDF.

    Supports:

    1. Windows local system
       - Uses docx2pdf
       - Microsoft Word should be installed

    2. Streamlit Cloud / Linux
       - Uses LibreOffice
       - libreoffice should be available
         through packages.txt
    """

    docx_path = Path(
        docx_path
    ).resolve()

    # -----------------------------------------------------
    # Check Word file
    # -----------------------------------------------------

    if not docx_path.exists():

        raise FileNotFoundError(
            f"Word file not found: "
            f"{docx_path}"
        )

    # -----------------------------------------------------
    # Create PDF path automatically
    # -----------------------------------------------------

    if pdf_path is None:

        pdf_path = (
            docx_path.with_suffix(
                ".pdf"
            )
        )

    pdf_path = Path(
        pdf_path
    ).resolve()

    pdf_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # =====================================================
    # WINDOWS LOCAL SYSTEM
    # =====================================================

    if os.name == "nt":

        return _convert_windows(
            docx_path,
            pdf_path
        )

    # =====================================================
    # STREAMLIT CLOUD / LINUX
    # =====================================================

    return _convert_libreoffice(
        docx_path,
        pdf_path
    )


# =========================================================
# WINDOWS CONVERSION
# =========================================================

def _convert_windows(
    docx_path,
    pdf_path
):
    """
    Convert Word to PDF using docx2pdf.

    docx2pdf internally uses Microsoft Word,
    so Word should be installed on Windows.
    """

    try:

        from docx2pdf import convert

    except ImportError:

        raise RuntimeError(
            "docx2pdf is not installed.\n"
            "Add docx2pdf to requirements.txt."
        )

    try:

        convert(
            str(docx_path),
            str(pdf_path)
        )

    except Exception as error:

        raise RuntimeError(
            "PDF conversion failed on Windows.\n\n"
            "Microsoft Word must be installed "
            "on the computer.\n\n"
            f"Details: {error}"
        )

    # -----------------------------------------------------
    # Confirm generated PDF
    # -----------------------------------------------------

    if not pdf_path.exists():

        raise RuntimeError(
            "Word file was generated, but "
            "the PDF file was not created."
        )

    return str(pdf_path)


# =========================================================
# LIBREOFFICE CONVERSION
# =========================================================

def _convert_libreoffice(
    docx_path,
    pdf_path
):
    """
    Convert Word to PDF using LibreOffice.

    Intended mainly for:

    - Streamlit Cloud
    - Linux
    - Servers without Microsoft Word
    """

    libreoffice = (
        shutil.which("libreoffice")
        or shutil.which("soffice")
    )

    if not libreoffice:

        raise RuntimeError(
            "LibreOffice is not installed.\n\n"
            "For Streamlit Cloud, create "
            "packages.txt in the project root "
            "and add:\n\n"
            "libreoffice"
        )

    # -----------------------------------------------------
    # LibreOffice generates the PDF using the
    # original DOCX filename.
    # -----------------------------------------------------

    output_directory = (
        pdf_path.parent
    )

    command = [
        libreoffice,
        "--headless",
        "--convert-to",
        "pdf",
        "--outdir",
        str(output_directory),
        str(docx_path)
    ]

    try:

        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120
        )

    except subprocess.TimeoutExpired:

        raise RuntimeError(
            "PDF conversion timed out."
        )

    except Exception as error:

        raise RuntimeError(
            f"LibreOffice conversion error: "
            f"{error}"
        )

    # -----------------------------------------------------
    # Check command result
    # -----------------------------------------------------

    if process.returncode != 0:

        error_message = (
            process.stderr
            or process.stdout
            or "Unknown LibreOffice error"
        )

        raise RuntimeError(
            "LibreOffice PDF conversion failed.\n\n"
            + error_message
        )

    # -----------------------------------------------------
    # LibreOffice output filename
    # -----------------------------------------------------

    generated_pdf = (
        output_directory
        / (
            docx_path.stem
            + ".pdf"
        )
    )

    if not generated_pdf.exists():

        raise RuntimeError(
            "LibreOffice completed, but "
            "the PDF file was not found."
        )

    # -----------------------------------------------------
    # If requested filename is different,
    # rename generated PDF.
    # -----------------------------------------------------

    if (
        generated_pdf.resolve()
        != pdf_path.resolve()
    ):

        if pdf_path.exists():

            pdf_path.unlink()

        generated_pdf.rename(
            pdf_path
        )

    return str(pdf_path)


# =========================================================
# CHECK PDF SUPPORT
# =========================================================

def get_pdf_conversion_status():
    """
    Used by Streamlit page to check whether
    PDF conversion is available.

    Returns dictionary like:

    {
        "available": True,
        "method": "Microsoft Word"
    }
    """

    # -----------------------------------------------------
    # Windows
    # -----------------------------------------------------

    if os.name == "nt":

        try:

            import docx2pdf

            return {
                "available": True,
                "method": (
                    "Microsoft Word / docx2pdf"
                )
            }

        except ImportError:

            return {
                "available": False,
                "method": (
                    "docx2pdf not installed"
                )
            }

    # -----------------------------------------------------
    # Linux / Streamlit Cloud
    # -----------------------------------------------------

    libreoffice = (
        shutil.which("libreoffice")
        or shutil.which("soffice")
    )

    if libreoffice:

        return {
            "available": True,
            "method": "LibreOffice"
        }

    return {
        "available": False,
        "method": (
            "LibreOffice not installed"
        )
    }