import os
import pythoncom
import win32com.client


class PDFService:


    def __init__(self):
        pass


    def convert(
        self,
        docx_file,
        pdf_file
    ):

        word = None

        try:

            # Initialize COM for Streamlit thread
            pythoncom.CoInitialize()


            word = win32com.client.Dispatch(
                "Word.Application"
            )

            word.Visible = False


            doc = word.Documents.Open(
                os.path.abspath(docx_file)
            )


            doc.SaveAs(
                os.path.abspath(pdf_file),
                FileFormat=17
            )


            doc.Close()


            return True


        except Exception as e:

            raise e


        finally:


            if word:

                word.Quit()


            # Release COM
            pythoncom.CoUninitialize()