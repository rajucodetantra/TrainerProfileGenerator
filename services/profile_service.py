import os
import re
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from modules.excel_reader import ExcelReader
from modules.word_generator import WordGenerator
from modules.summary_generator import SummaryGenerator
from modules.skills_formatter import SkillsFormatter
from modules.experience import Experience
from modules.rating import Rating
from modules.image_handler import ImageHandler
from modules.training_expertise import TrainingExpertise
from modules.trainer_highlights import TrainerHighlights
from modules.professional_achievements import ProfessionalAchievements
from modules.profile_generator import ProfileGenerator
from modules.project_extractor import ProjectExtractor

from services.config_service import ConfigService
from services.pdf_service import PDFService
from services.zip_service import ZipService

class ProfileService:
    def __init__(self):
        self.config = ConfigService()
        self.zip_service = ZipService()
        self.reader = ExcelReader(self.config.excel_file, self.config.sheet_name)
        self.summary_generator = SummaryGenerator()
        self.skills_formatter = SkillsFormatter()
        self.experience = Experience()
        self.rating = Rating()
        self.image_handler = ImageHandler(self.config.image_folder)
        self.training = TrainingExpertise()
        self.highlights = TrainerHighlights()
        self.achievements = ProfessionalAchievements()
        self.profile = ProfileGenerator()
        project_file = "data/Projects.xlsx" if os.path.exists("data/Projects.xlsx") else "Projects.xlsx"
        self.project_extractor = ProjectExtractor(project_file)
        self.pdf_service = PDFService()
        os.makedirs(self.config.docx_output, exist_ok=True)
        os.makedirs(self.config.pdf_output, exist_ok=True)
        os.makedirs("logs", exist_ok=True)

    def get_trainers(self): return self.reader.read_trainers()

    def write_log(self, emp_id, trainer_name, status, output_file="", remarks=""):
        log_file = "logs/generation_log.csv"
        row = pd.DataFrame([{"Date": datetime.now().strftime("%d-%m-%Y"), "Time": datetime.now().strftime("%H:%M:%S"), "Employee ID": emp_id, "Trainer Name": trainer_name, "Status": status, "Output File": output_file, "Remarks": remarks}])
        if os.path.exists(log_file): row.to_csv(log_file, mode="a", header=False, index=False)
        else: row.to_csv(log_file, index=False)

    def _normalize_emp_id(self, raw_id):
        clean_id = str(raw_id).strip()
        if clean_id.isdigit(): return f"CT{int(clean_id):04d}"
        digits = "".join(filter(str.isdigit, clean_id))
        return f"CT{int(digits):04d}" if digits else clean_id

    def prepare_trainer(self, trainer):
        trainer = trainer.copy()
        trainer["Emp ID"] = self._normalize_emp_id(trainer.get("Emp ID", ""))
        
        # --- Adjusted Date Logic ---
        raw_doj = trainer.get("Date of Joining")
        if raw_doj:
            doj_dt = pd.to_datetime(raw_doj)
            adjusted_doj = doj_dt - relativedelta(years=1)
            trainer["Date of Joining"] = adjusted_doj.strftime("%d-%m-%Y")
            trainer["Experience"] = self.experience.calculate(adjusted_doj)
        else:
            trainer["Date of Joining"] = ""
            trainer["Experience"] = "0 Years 0 Months"

        trainer["Skills"] = self.skills_formatter.format(trainer)
        trainer["Summary"] = self.summary_generator.generate(trainer)
        trainer["LeetCode Profile Link"] = str(trainer.get("LeetCode Profile Link", "")).strip()
        trainer["No of Problems Done"] = str(trainer.get("No of Problems Done", "")).strip()
        trainer["Other Profiles"] = str(trainer.get("Other Profiles", "")).strip()
        
        projects = self.project_extractor.get_trainer_projects(trainer["Emp ID"])
        trainer["Training Projects"] = self.profile.generate_training_projects(projects)
        trainer["Technical Expertise"] = self.profile.generate_technical_expertise(trainer)
        trainer["Training Expertise"] = self.training.generate(trainer)
        trainer["Rating"] = self.rating.get_rating(trainer.get("Trainer Rating", self.config.default_rating))
        trainer["Professional Highlights"] = self.highlights.generate(trainer)
        trainer["Professional Achievements"] = self.achievements.generate(trainer)
        trainer["Certifications"] = self.profile.generate_certifications(trainer)
        trainer["Competitive Programming"] = self.profile.generate_competitive_programming(trainer)
        trainer["Coding Profiles"] = self.profile.generate_coding_profiles(trainer)
        trainer["Core Competencies"] = self.profile.generate_core_competencies(trainer)
        
        raw_img_path = self.image_handler.get_image_path(trainer["Emp ID"])
        trainer["Image"] = raw_img_path.replace("\\", "/").replace("\n", "").strip() if raw_img_path else ""

        # Clean all remaining fields
        trainer = self.clean_trainer_data(trainer)

        return trainer

    def generate_profile(self, trainer, generate_pdf=False, output_format="Word"):
        trainer = self.prepare_trainer(trainer)
        emp_id = str(trainer["Emp ID"]).strip()
        name = re.sub(r'[\\/:*?"<>|]', "", str(trainer["Name"]))
        name = re.sub(r"\s+", " ", name).strip()
        docx_file = os.path.join(self.config.docx_output, f"{emp_id}_{name}.docx")
        pdf_file = os.path.join(self.config.pdf_output, f"{emp_id}_{name}.pdf")
        try:
            generator = WordGenerator(self.config.template_file, trainer)
            generator.generate(docx_file)
            if generate_pdf: self.pdf_service.convert(docx_file, pdf_file)
            if (output_format == "PDF" or self.config.default_output == "PDF") and os.path.exists(docx_file):
                os.remove(docx_file)
                docx_file = ""
            self.write_log(emp_id, trainer["Name"], "SUCCESS", docx_file if docx_file else pdf_file, "")
            return {"success": True, "employee_id": emp_id, "trainer": trainer["Name"], "docx": docx_file, "pdf": pdf_file if generate_pdf else "", "message": "Generated Successfully"}
        except Exception as e:
            self.write_log(emp_id, trainer["Name"], "FAILED", "", str(e))
            return {"success": False, "employee_id": emp_id, "trainer": trainer["Name"], "docx": "", "pdf": "", "message": str(e)}

    def generate_profiles(self, trainers, progress_callback=None, output_format="Word"):
        results = []
        total = len(trainers)
        generate_pdf = output_format in ["PDF", "Both"]
        for index, (_, trainer) in enumerate(trainers.iterrows(), start=1):
            results.append(self.generate_profile(trainer, generate_pdf=generate_pdf, output_format=output_format))
            if progress_callback: progress_callback(index, total)
        return results

    def get_trainer(self, emp_id):
        trainers = self.get_trainers()
        normalized_target = self._normalize_emp_id(emp_id)
        trainer = trainers[(trainers["Emp ID"].astype(str) == str(emp_id)) | (trainers["Emp ID"].astype(str).apply(self._normalize_emp_id) == normalized_target)]
        return self.prepare_trainer(trainer.iloc[0]) if not trainer.empty else None

    def search_trainers(self, keyword):
        trainers = self.get_trainers()
        return trainers[trainers.astype(str).apply(lambda row: row.str.contains(keyword, case=False, na=False).any(), axis=1)]

    def get_skills(self):
        trainers = self.get_trainers()
        skills = []
        for value in trainers["Skills"].fillna(""):
            for skill in str(value).replace("//", ",").replace("\n", ",").split(","):
                if skill.strip(): skills.append(skill.strip())
        return sorted(list(set(skills)))

    def get_designations(self): return sorted(self.get_trainers()["Designation"].dropna().unique()) if "Designation" in self.get_trainers().columns else []
    def get_qualifications(self): return sorted(self.get_trainers()["Qualification"].dropna().unique()) if "Qualification" in self.get_trainers().columns else []
    def generate_all(self, progress_callback=None, output_format="Word"): return self.generate_profiles(self.get_trainers(), progress_callback, output_format)
    def generate_single(self, emp_id, output_format="Word"): 
        trainer = self.get_trainer(emp_id)
        if trainer is None: raise Exception("Trainer Not Found.")
        return self.generate_profile(trainer, generate_pdf=output_format in ["PDF", "Both"], output_format=output_format)

    def generate_selected(self, emp_ids, progress_callback=None, output_format="Word"):
        trainers = self.get_trainers()
        str_emp_ids = [self._normalize_emp_id(x) for x in emp_ids]
        return self.generate_profiles(trainers[trainers["Emp ID"].astype(str).apply(self._normalize_emp_id).isin(str_emp_ids)], progress_callback, output_format)

    def generate_by_skill(self, skill, progress_callback=None, output_format="Word"): return self.generate_profiles(self.get_trainers()[self.get_trainers()["Skills"].fillna("").str.contains(skill, case=False, na=False)], progress_callback, output_format)
    def generate_by_designation(self, designation, progress_callback=None, output_format="Word"): return self.generate_profiles(self.get_trainers()[self.get_trainers()["Designation"].fillna("").str.lower() == designation.lower()], progress_callback, output_format)
    def generate_by_qualification(self, qualification, progress_callback=None, output_format="Word"): return self.generate_profiles(self.get_trainers()[self.get_trainers()["Qualification"].fillna("").str.lower() == qualification.lower()], progress_callback, output_format)
    
    def statistics(self):
        t = self.get_trainers()
        return {"total_trainers": len(t), "designations": t["Designation"].nunique() if "Designation" in t.columns else 0, "qualifications": t["Qualification"].nunique() if "Qualification" in t.columns else 0, "skills": len(self.get_skills()), "images_folder": self.config.image_folder, "template": self.config.template_file, "excel": self.config.excel_file}

    def output_summary(self):
        d = len([f for f in os.listdir(self.config.docx_output) if f.lower().endswith(".docx")]) if os.path.exists(self.config.docx_output) else 0
        p = len([f for f in os.listdir(self.config.pdf_output) if f.lower().endswith(".pdf")]) if os.path.exists(self.config.pdf_output) else 0
        return {"docx": d, "pdf": p}

    def create_docx_zip(self, files): return self.zip_service.create_zip(files, os.path.join(self.config.docx_output, "Trainer_Profiles_DOCX.zip"))
    def create_pdf_zip(self, files): return self.zip_service.create_zip(files, os.path.join(self.config.pdf_output, "Trainer_Profiles_PDF.zip"))
    def get_trainer_display_list(self): return (self.get_trainers()["Emp ID"].astype(str) + " - " + self.get_trainers()["Name"]).tolist()
    def clean_trainer_data(self, trainer):
        """
        Replace NaN / NA / N/A / None with blank strings.
        This keeps Word and PDF clean without changing the Excel file.
        """

        INVALID_VALUES = {
        "nan",
        "NaN",
        "NA",
        "N/A",
        "None",
        "none",
        "null",
        "NULL",
        "<NA>"
        }

        for key in trainer.index:

            value = trainer[key]

            # Handle pandas NaN
            if pd.isna(value):
                trainer[key] = ""
                continue

            value = str(value).strip()

            if value == "" or value in INVALID_VALUES:
                trainer[key] = ""
            else:
                trainer[key] = value

        return trainer