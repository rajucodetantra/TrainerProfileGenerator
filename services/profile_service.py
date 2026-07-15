import os
import re
import pandas as pd
from datetime import datetime

from modules.excel_reader import ExcelReader
from modules.word_generator import WordGenerator
from modules.summary_generator import SummaryGenerator
from modules.skills_formatter import SkillsFormatter
from modules.experience import Experience
from modules.rating import Rating
from modules.image_handler import ImageHandler
from modules.technical_expertise import TechnicalExpertise
from modules.training_expertise import TrainingExpertise
from modules.trainer_highlights import TrainerHighlights
from modules.professional_achievements import ProfessionalAchievements
from modules.profile_generator import ProfileGenerator

from services.config_service import ConfigService
from services.pdf_service import PDFService
from services.zip_service import ZipService

class ProfileService:

    def __init__(self):

        self.config = ConfigService()
        self.zip_service = ZipService()
        self.reader = ExcelReader(
            self.config.excel_file,
            self.config.sheet_name
        )

        self.summary_generator = SummaryGenerator()
        self.skills_formatter = SkillsFormatter()
        self.experience = Experience()
        self.rating = Rating()

        self.image_handler = ImageHandler(
            self.config.image_folder
        )

        self.technical = TechnicalExpertise()
        self.training = TrainingExpertise()
        self.highlights = TrainerHighlights()
        self.achievements = ProfessionalAchievements()
        self.profile = ProfileGenerator()

        self.pdf_service = PDFService()

        os.makedirs(
            self.config.docx_output,
            exist_ok=True
        )

        os.makedirs(
            self.config.pdf_output,
            exist_ok=True
        )

        os.makedirs(
            "logs",
            exist_ok=True
        )

    # -------------------------------------------------------

    def get_trainers(self):

        return self.reader.read_trainers()

    # -------------------------------------------------------

    def write_log(
        self,
        emp_id,
        trainer_name,
        status,
        output_file="",
        remarks=""
    ):

        log_file = "logs/generation_log.csv"

        row = pd.DataFrame([{

            "Date": datetime.now().strftime("%d-%m-%Y"),

            "Time": datetime.now().strftime("%H:%M:%S"),

            "Employee ID": emp_id,

            "Trainer Name": trainer_name,

            "Status": status,

            "Output File": output_file,

            "Remarks": remarks

        }])

        if os.path.exists(log_file):

            row.to_csv(
                log_file,
                mode="a",
                header=False,
                index=False
            )

        else:

            row.to_csv(
                log_file,
                index=False
            )

    # -------------------------------------------------------

    def prepare_trainer(
        self,
        trainer
    ):

        trainer = trainer.copy()

        trainer["Raw Skills"] = str(
            trainer.get(
                "Skills",
                ""
            )
        )

        trainer["Skills"] = self.skills_formatter.format(
            trainer
        )

        trainer["Experience"] = self.experience.calculate(
            trainer.get(
                "Date of Joining",
                ""
            )
        )

        trainer["Summary"] = self.summary_generator.generate(
            trainer
        )

        trainer["Technical Expertise"] = self.technical.generate(
            trainer
        )

        trainer["Training Expertise"] = self.training.generate(
            trainer
        )

        trainer["Rating"] = self.rating.get_rating(
            trainer.get(
                "Trainer Rating",
                self.config.default_rating
            )
        )

        trainer["Professional Highlights"] = (
            self.highlights.generate(
                trainer
            )
        )

        trainer["Professional Achievements"] = (
            self.achievements.generate(
                trainer
            )
        )

        trainer["Certifications"] = (
            self.profile.generate_certifications(
                trainer
            )
        )

        trainer["Competitive Programming"] = (
            self.profile.generate_competitive_programming(
                trainer
            )
        )

        trainer["Coding Profiles"] = (
            self.profile.generate_coding_profiles(
                trainer
            )
        )

        trainer["Core Competencies"] = (
            self.profile.generate_core_competencies(
                trainer
            )
        )

        trainer["Image"] = (
            self.image_handler.get_image_path(
                trainer["Emp ID"]
            )
        )

        return trainer

    # -------------------------------------------------------

    def generate_profile(
        self,
        trainer,
        generate_pdf=False
    ):

        trainer = self.prepare_trainer(
            trainer
        )

        emp_id = str(
            trainer["Emp ID"]
        ).strip()

        name = re.sub(
            r'[\\/:*?"<>|]',
            "",
            str(
                trainer["Name"]
            )
        )

        name = re.sub(
            r"\s+",
            " ",
            name
        ).strip()

        docx_file = os.path.join(
            self.config.docx_output,
            f"{emp_id}_{name}.docx"
        )

        pdf_file = os.path.join(
            self.config.pdf_output,
            f"{emp_id}_{name}.pdf"
        )

        try:

            generator = WordGenerator(
                self.config.template_file,
                trainer
            )

            generator.generate(
                docx_file
            )

            print("=" * 50)
            print("generate_pdf =", generate_pdf)
            print("DOCX :", docx_file)
            print("PDF  :", pdf_file)

            if generate_pdf:

                print("Calling PDFService.convert()")

                self.pdf_service.convert(
                    docx_file,
                    pdf_file
                )

                print("PDF Generated Successfully")

            print("=" * 50)

            if self.config.default_output == "PDF":

                if os.path.exists(docx_file):

                    os.remove(docx_file)

                    docx_file = ""

            self.write_log(
                emp_id,
                trainer["Name"],
                "SUCCESS",
                docx_file,
                ""
            )

            return {

            "success": True,

            "employee_id": emp_id,

            "trainer": trainer["Name"],

            "docx": docx_file,

            "pdf": pdf_file if generate_pdf else "",

            "message": "Generated Successfully"

            }

        except Exception as e:

            self.write_log(
                emp_id,
                trainer["Name"],
                "FAILED",
                "",
                str(e)
            )

            return {

                "success": False,

                "employee_id": emp_id,

                "trainer": trainer["Name"],

                "docx": "",

                "pdf": "",

                "message": str(e)

            }

    # -------------------------------------------------------

    def generate_profiles(
        self,
        trainers,
        progress_callback=None,
        generate_pdf=False
    ):

        results = []

        total = len(
            trainers
        )

        for index, (_, trainer) in enumerate(
            trainers.iterrows(),
            start=1
        ):

            result = self.generate_profile(
                trainer,
                generate_pdf
            )

            results.append(
                result
            )

            if progress_callback:

                progress_callback(
                    index,
                    total
                )

        return results
    # -------------------------------------------------------

    def get_trainer(
        self,
        emp_id
    ):

        trainers = self.get_trainers()

        trainer = trainers[
            trainers["Emp ID"]
            .astype(str)
            ==
            str(emp_id)
        ]

        if trainer.empty:

            return None

        return self.prepare_trainer(
            trainer.iloc[0]
        )

    # -------------------------------------------------------

    def search_trainers(
        self,
        keyword
    ):

        trainers = self.get_trainers()

        result = trainers[
            trainers.astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    keyword,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]

        return result

    # -------------------------------------------------------

    def get_skills(self):

        trainers = self.get_trainers()

        skills = []

        for value in trainers["Skills"].fillna(""):

            value = (
                str(value)
                .replace("//", ",")
                .replace("\n", ",")
            )

            for skill in value.split(","):

                skill = skill.strip()

                if skill:

                    skills.append(skill)

        return sorted(list(set(skills)))

    # -------------------------------------------------------

    def get_designations(self):

        trainers = self.get_trainers()

        if "Designation" not in trainers.columns:

            return []

        return sorted(
            trainers["Designation"]
            .dropna()
            .unique()
        )

    # -------------------------------------------------------

    def get_qualifications(self):

        trainers = self.get_trainers()

        if "Qualification" not in trainers.columns:

            return []

        return sorted(
            trainers["Qualification"]
            .dropna()
            .unique()
        )

    # -------------------------------------------------------

    def generate_all(
        self,
        progress_callback=None,
        generate_pdf=False
    ):

        trainers = self.get_trainers()

        return self.generate_profiles(
            trainers,
            progress_callback,
            generate_pdf
        )

    # -------------------------------------------------------

    def generate_single(
        self,
        emp_id,
        generate_pdf=False
    ):

        trainer = self.get_trainer(
            emp_id
        )

        if trainer is None:

            raise Exception(
                "Trainer Not Found."
            )

        return self.generate_profile(
            trainer,
            generate_pdf
        )

    # -------------------------------------------------------

    def generate_selected(
        self,
        emp_ids,
        progress_callback=None,
        generate_pdf=False
    ):

        trainers = self.get_trainers()

        trainers = trainers[
            trainers["Emp ID"]
            .astype(str)
            .isin(
                [str(x) for x in emp_ids]
            )
        ]

        return self.generate_profiles(
            trainers,
            progress_callback,
            generate_pdf
        )

    # -------------------------------------------------------

    def generate_by_skill(
        self,
        skill,
        progress_callback=None,
        generate_pdf=False
    ):

        trainers = self.get_trainers()

        trainers = trainers[
            trainers["Skills"]
            .fillna("")
            .str.contains(
                skill,
                case=False,
                na=False
            )
        ]

        return self.generate_profiles(
            trainers,
            progress_callback,
            generate_pdf
        )

    # -------------------------------------------------------

    def generate_by_designation(
        self,
        designation,
        progress_callback=None,
        generate_pdf=False
    ):

        trainers = self.get_trainers()

        trainers = trainers[
            trainers["Designation"]
            .fillna("")
            .str.lower()
            ==
            designation.lower()
        ]

        return self.generate_profiles(
            trainers,
            progress_callback,
            generate_pdf
        )

    # -------------------------------------------------------

    def generate_by_qualification(
        self,
        qualification,
        progress_callback=None,
        generate_pdf=False
    ):

        trainers = self.get_trainers()

        trainers = trainers[
            trainers["Qualification"]
            .fillna("")
            .str.lower()
            ==
            qualification.lower()
        ]

        return self.generate_profiles(
            trainers,
            progress_callback,
            generate_pdf
        )

    # -------------------------------------------------------

    def statistics(self):

        trainers = self.get_trainers()

        return {

            "total_trainers": len(trainers),

            "designations":
            trainers["Designation"].nunique()
            if "Designation" in trainers.columns
            else 0,

            "qualifications":
            trainers["Qualification"].nunique()
            if "Qualification" in trainers.columns
            else 0,

            "skills":
            len(
                self.get_skills()
            ),

            "images_folder":
            self.config.image_folder,

            "template":
            self.config.template_file,

            "excel":
            self.config.excel_file

        }

    # -------------------------------------------------------

    def output_summary(self):

        docx_count = 0
        pdf_count = 0

        if os.path.exists(
            self.config.docx_output
        ):

            docx_count = len([

                f

                for f in os.listdir(
                    self.config.docx_output
                )

                if f.lower().endswith(
                    ".docx"
                )

            ])

        if os.path.exists(
            self.config.pdf_output
        ):

            pdf_count = len([

                f

                for f in os.listdir(
                    self.config.pdf_output
                )

                if f.lower().endswith(
                    ".pdf"
                )

            ])

        return {

            "docx": docx_count,

            "pdf": pdf_count

        }
    # ----------------------------------------------------

    def create_docx_zip(self, files):

        zip_path = os.path.join(

        self.config.docx_output,

        "Trainer_Profiles_DOCX.zip"

        )

        return self.zip_service.create_zip(

            files,

            zip_path

        )

# ----------------------------------------------------

    def create_pdf_zip(self, files):

        zip_path = os.path.join(

        self.config.pdf_output,

        "Trainer_Profiles_PDF.zip"

        )

        return self.zip_service.create_zip(

            files,

            zip_path

        )