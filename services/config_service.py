# services/config_service.py

import json
import os


class ConfigService:
    """
    Handles application configuration.
    Stores and manages settings using config.json
    """

    def __init__(self):

        self.config_file = "config.json"


        self.defaults = {

            # ==========================================
            # Application Information
            # ==========================================

            "application_name": "Trainer Profile Generator",

            "version": "1.0.0",


            # ==========================================
            # Company Information
            # ==========================================

            "company_name": "CodeTantra Tech Solutions Pvt. Ltd.",

            "company_address": "",

            "company_email": "",

            "company_phone": "",

            "logo": "data/logo.png",



            # ==========================================
            # Excel Configuration
            # ==========================================

            "excel_file": "data/Trainers.xlsx",

            "sheet_name": "Trainers",



            # ==========================================
            # Template Configuration
            # ==========================================

            "template_file":
                "templates/Trainer_Profile_Template.docx",



            # ==========================================
            # Image Configuration
            # ==========================================

            "image_folder": "data/CTImages",



            # ==========================================
            # Output Configuration
            # ==========================================

            "docx_output": "output/DOCX",

            "pdf_output": "output/PDF",



            # ==========================================
            # Profile Configuration
            # ==========================================

            "default_rating": 5,

            "default_output": "Both"

        }


        self.config = self.load()



    # ==================================================
    # LOAD CONFIGURATION
    # ==================================================

    def load(self):

        if not os.path.exists(self.config_file):

            self.save(
                self.defaults.copy()
            )

            return self.defaults.copy()


        try:

            with open(
                self.config_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)


        except Exception:

            data = self.defaults.copy()



        # Add missing configuration values

        for key, value in self.defaults.items():

            if key not in data:

                data[key] = value



        return data



    # ==================================================
    # SAVE CONFIGURATION
    # ==================================================

    def save(self, config):

        with open(
            self.config_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                config,
                file,
                indent=4
            )


        self.config = config



    # ==================================================
    # APPLICATION PROPERTIES
    # ==================================================

    @property
    def application_name(self):

        return self.config.get(
            "application_name",
            "Trainer Profile Generator"
        )


    @property
    def version(self):

        return self.config.get(
            "version",
            "1.0.0"
        )



    # ==================================================
    # COMPANY PROPERTIES
    # ==================================================

    @property
    def company_name(self):

        return self.config.get(
            "company_name",
            ""
        )


    @property
    def company_address(self):

        return self.config.get(
            "company_address",
            ""
        )


    @property
    def company_email(self):

        return self.config.get(
            "company_email",
            ""
        )


    @property
    def company_phone(self):

        return self.config.get(
            "company_phone",
            ""
        )


    @property
    def logo(self):

        return self.config.get(
            "logo",
            "data/logo.png"
        )



    # ==================================================
    # FILE PROPERTIES
    # ==================================================

    @property
    def excel_file(self):

        return self.config["excel_file"]


    @property
    def sheet_name(self):

        return self.config["sheet_name"]


    @property
    def template_file(self):

        return self.config["template_file"]


    @property
    def image_folder(self):

        return self.config["image_folder"]


    @property
    def docx_output(self):

        return self.config["docx_output"]


    @property
    def pdf_output(self):

        return self.config["pdf_output"]



    # ==================================================
    # PROFILE PROPERTIES
    # ==================================================

    @property
    def default_rating(self):

        return self.config["default_rating"]


    @property
    def default_output(self):

        return self.config["default_output"]



    # ==================================================
    # APPLICATION SETTERS
    # ==================================================

    def set_application_name(self, value):

        self.config["application_name"] = value

        self.save(self.config)



    def set_version(self, value):

        self.config["version"] = value

        self.save(self.config)



    # ==================================================
    # COMPANY SETTERS
    # ==================================================

    def set_company_name(self, value):

        self.config["company_name"] = value

        self.save(self.config)



    def set_company_address(self, value):

        self.config["company_address"] = value

        self.save(self.config)



    def set_company_email(self, value):

        self.config["company_email"] = value

        self.save(self.config)



    def set_company_phone(self, value):

        self.config["company_phone"] = value

        self.save(self.config)



    def set_logo(self, value):

        self.config["logo"] = value

        self.save(self.config)



    # ==================================================
    # FILE SETTERS
    # ==================================================

    def set_excel_file(self, value):

        self.config["excel_file"] = value

        self.save(self.config)



    def set_sheet_name(self, value):

        self.config["sheet_name"] = value

        self.save(self.config)



    def set_template_file(self, value):

        self.config["template_file"] = value

        self.save(self.config)



    def set_image_folder(self, value):

        self.config["image_folder"] = value

        self.save(self.config)



    def set_docx_output(self, value):

        self.config["docx_output"] = value

        self.save(self.config)



    def set_pdf_output(self, value):

        self.config["pdf_output"] = value

        self.save(self.config)



    # ==================================================
    # PROFILE SETTERS
    # ==================================================

    def set_default_rating(self, value):

        self.config["default_rating"] = value

        self.save(self.config)



    def set_default_output(self, value):

        if value not in [
            "Word",
            "PDF",
            "Both"
        ]:

            value = "Both"


        self.config["default_output"] = value

        self.save(self.config)



    # ==================================================
    # RESET CONFIGURATION
    # ==================================================

    def reset(self):

        self.save(
            self.defaults.copy()
        )