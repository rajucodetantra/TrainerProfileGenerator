from docx import Document
from docx.shared import Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os


class WordGenerator:


    def __init__(self, template_path, trainer):

        self.template_path = template_path
        self.trainer = trainer



    def mask_phone(self, phone):

        phone = str(phone)

        phone = phone.replace("+91", "")
        phone = phone.replace("-", "")
        phone = phone.replace(" ", "")


        if len(phone) >= 3:

            return (
                "×" * (len(phone) - 3)
                +
                phone[-3:]
            )

        return phone



    def get_replacements(self):

        return {


            "{{Name}}":
                str(self.trainer.get("Name", "")),


            "{{Emp ID}}":
                str(self.trainer.get("Emp ID", "")),


            "{{Designation}}":
                str(self.trainer.get("Designation", "")),


            "{{Qualification}}":
                str(self.trainer.get("Qualification", "")),


            "{{Date of Joining}}":
                str(self.trainer.get("Date of Joining", "")),


            "{{Experience}}":
                str(self.trainer.get("Experience", "")),


            "{{Company Mail}}":
                str(self.trainer.get("Company Mail", "")),


            "{{Phone Number}}":
                self.mask_phone(
                    self.trainer.get(
                        "Phone Number",
                        ""
                    )
                ),


            "{{Rating}}":
                str(
                    self.trainer.get(
                        "Rating",
                        ""
                    )
                ),


            "{{Skills}}":
                str(
                    self.trainer.get(
                        "Skills",
                        ""
                    )
                ),


            "{{Summary}}":
                str(
                    self.trainer.get(
                        "Summary",
                        ""
                    )
                ),


            "{{Technical Expertise}}":
                str(
                    self.trainer.get(
                        "Technical Expertise",
                        ""
                    )
                ),


            "{{Training Expertise}}":
                str(
                    self.trainer.get(
                        "Training Expertise",
                        ""
                    )
                ),


            "{{Professional Highlights}}":
                str(
                    self.trainer.get(
                        "Professional Highlights",
                        ""
                    )
                ),


            "{{Professional Achievements}}":
                str(
                    self.trainer.get(
                        "Professional Achievements",
                        ""
                    )
                ),


            "{{Certifications}}":
                str(
                    self.trainer.get(
                        "Certifications",
                        ""
                    )
                ),


            "{{Competitive Programming}}":
                str(
                    self.trainer.get(
                        "Competitive Programming",
                        ""
                    )
                ),


            "{{Coding Profiles}}":
                str(
                    self.trainer.get(
                        "Coding Profiles",
                        ""
                    )
                ),


            "{{Core Competencies}}":
                str(
                    self.trainer.get(
                        "Core Competencies",
                        ""
                    )
                )

        }



    def replace_text(self, doc):

        replacements = self.get_replacements()


        # Paragraphs

        self.process_paragraphs(
            doc.paragraphs,
            replacements
        )


        # Tables

        for table in doc.tables:

            for row in table.rows:

                for cell in row.cells:

                    self.process_paragraphs(
                        cell.paragraphs,
                        replacements
                    )



    def process_paragraphs(
            self,
            paragraphs,
            replacements
    ):


        for paragraph in paragraphs:


            for key, value in replacements.items():


                if key in paragraph.text:


                    for run in paragraph.runs:


                        if key in run.text:


                            run.text = run.text.replace(
                                key,
                                value
                            )


                            # All inserted content black

                            run.font.color.rgb = RGBColor(
                                0,
                                0,
                                0
                            )



                    # ---------------------------------
                    # SUMMARY ONLY JUSTIFICATION
                    # ---------------------------------

                    if key == "{{Summary}}":

                        paragraph.alignment = (
                            WD_ALIGN_PARAGRAPH.JUSTIFY
                        )




    def add_image(self, doc):


        image_path = self.trainer.get(
            "Image"
        )


        if not image_path:

            return


        if not os.path.exists(image_path):

            return



        # Normal paragraph image

        for paragraph in doc.paragraphs:


            if "{{Image}}" in paragraph.text:


                paragraph.text = ""


                run = paragraph.add_run()


                run.add_picture(
                    image_path,
                    width=Inches(2.2)
                )


                return




        # Table image

        for table in doc.tables:


            for row in table.rows:


                for cell in row.cells:


                    if "{{Image}}" in cell.text:


                        cell.text = ""


                        run = (
                            cell.paragraphs[0]
                            .add_run()
                        )


                        run.add_picture(
                            image_path,
                            width=Inches(2.2)
                        )


                        return




    def generate(self, output_path):


        doc = Document(
            self.template_path
        )


        self.replace_text(
            doc
        )


        self.add_image(
            doc
        )


        doc.save(
            output_path
        )