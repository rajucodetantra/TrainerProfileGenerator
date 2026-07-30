import os
import gc
import time
import platform
import subprocess

IS_WINDOWS = platform.system() == "Windows"

if IS_WINDOWS:
    import pythoncom
    import win32com.client


class PDFService:
    """
    Production-ready PDF conversion service.

    Features
    --------
    ✓ Microsoft Word COM conversion
    ✓ LibreOffice fallback
    ✓ Automatic retries
    ✓ Proper COM cleanup
    ✓ Handles temporary file locking
    """

    def __init__(self, retries=3, retry_delay=2):
        self.retries = retries
        self.retry_delay = retry_delay

    # ----------------------------------------------------------
    # LibreOffice Converter
    # ----------------------------------------------------------

    def _convert_via_libreoffice(self, abs_docx, out_dir, abs_pdf):

        commands = []

        if IS_WINDOWS:
            commands.extend([
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
            ])

        commands.extend([
            "soffice",
            "libreoffice"
        ])

        for cmd in commands:

            try:

                subprocess.run(
                    [
                        cmd,
                        "--headless",
                        "--convert-to",
                        "pdf",
                        "--outdir",
                        out_dir,
                        abs_docx
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True
                )

                if os.path.exists(abs_pdf):
                    return True

            except Exception:
                continue

        return False

    # ----------------------------------------------------------
    # Microsoft Word COM Converter
    # ----------------------------------------------------------

    def _convert_via_word(self, abs_docx, abs_pdf):

        pythoncom.CoInitialize()

        word = None
        document = None

        try:

            word = win32com.client.DispatchEx("Word.Application")

            word.Visible = False
            word.DisplayAlerts = 0

            document = word.Documents.Open(
                abs_docx,
                ReadOnly=True
            )

            document.SaveAs(
                abs_pdf,
                FileFormat=17
            )

            document.Close(False)
            document = None

            word.Quit()
            word = None

            pythoncom.CoUninitialize()

            gc.collect()

            return os.path.exists(abs_pdf)

        finally:

            try:
                if document:
                    document.Close(False)
            except:
                pass

            try:
                if word:
                    word.Quit()
            except:
                pass

            try:
                pythoncom.CoUninitialize()
            except:
                pass

            document = None
            word = None

            gc.collect()

    # ----------------------------------------------------------
    # Wait until DOCX is unlocked
    # ----------------------------------------------------------

    def _wait_until_unlocked(self, filename, timeout=10):

        start = time.time()

        while True:

            try:
                with open(filename, "rb"):
                    return True

            except PermissionError:

                if time.time() - start > timeout:
                    return False

                time.sleep(0.5)

    # ----------------------------------------------------------
    # Public Convert Function
    # ----------------------------------------------------------

    def convert(self, docx_file, pdf_file):

        abs_docx = os.path.abspath(docx_file)
        abs_pdf = os.path.abspath(pdf_file)

        out_dir = os.path.dirname(abs_pdf)

        if not os.path.exists(abs_docx):
            raise FileNotFoundError(
                f"DOCX file not found:\n{abs_docx}"
            )

        os.makedirs(out_dir, exist_ok=True)

        last_error = None

        for attempt in range(1, self.retries + 1):

            try:

                if not self._wait_until_unlocked(abs_docx):
                    raise PermissionError(
                        "DOCX file is locked."
                    )

                if IS_WINDOWS:

                    if self._convert_via_word(abs_docx, abs_pdf):

                        if os.path.exists(abs_pdf):
                            return True

                if self._convert_via_libreoffice(
                    abs_docx,
                    out_dir,
                    abs_pdf
                ):

                    if os.path.exists(abs_pdf):
                        return True

                raise RuntimeError(
                    "Conversion completed but PDF not created."
                )

            except Exception as e:

                last_error = e

                print(
                    f"[PDF Attempt {attempt}/{self.retries}] {e}"
                )

                gc.collect()

                time.sleep(self.retry_delay)

        raise RuntimeError(
            f"""
PDF Conversion Failed

DOCX :
{abs_docx}

PDF :
{abs_pdf}

Reason :
{last_error}
"""
        )