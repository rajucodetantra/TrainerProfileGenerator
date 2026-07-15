import re

from modules.skills_database import SKILL_CATEGORIES


class TechnicalExpertise:


    def extract_skills(self, skill_text):

        if not skill_text:
            return []


        skill_text = str(skill_text)


        # Convert separators

        skill_text = re.sub(
            r'//|/|;|\||\n|\r',
            ',',
            skill_text
        )


        skills = []


        for skill in skill_text.split(","):

            skill = skill.strip()

            if skill:

                skills.append(skill)


        return list(
            dict.fromkeys(skills)
        )



    def normalize_skill(self, skill):


        mapping = {


            # Programming

            "python":
                "Python",

            "java":
                "Java",

            "c":
                "C",

            "c++":
                "C++",


            # DSA

            "dsa":
                "Data Structures & Algorithms",

            "data structures":
                "Data Structures & Algorithms",

            "data structures and algorithms":
                "Data Structures & Algorithms",



            # Competitive Programming

            "competitive coding":
                "Competitive Programming",

            "competetive coding":
                "Competitive Programming",

            "competitive programming":
                "Competitive Programming",



            # Full Stack

            "python full stack":
                "Full Stack Web Development",

            "full stack":
                "Full Stack Web Development",



            # Web

            "javascript":
                "JavaScript",

            "js":
                "JavaScript",

            "html":
                "HTML",

            "css":
                "CSS",



            # Database

            "mongodb":
                "MongoDB",

            "mysql":
                "MySQL",

            "sql":
                "SQL",



            # Cloud

            "aws":
                "AWS",

            "azure":
                "Azure",

            "git":
                "Git",

            "github":
                "GitHub",


            # AI

            "gen ai":
                "Generative AI",

            "generative ai":
                "Generative AI",

            "machine learning":
                "Machine Learning"

        }


        key = skill.lower().strip()


        return mapping.get(
            key,
            skill.strip()
        )



    def generate(self, trainer):


        raw_skills = trainer.get(
            "Raw Skills",
            ""
        )


        skills = self.extract_skills(
            raw_skills
        )


        normalized_skills = []


        for skill in skills:

            normalized_skills.append(
                self.normalize_skill(skill)
            )


        normalized_skills = list(
            dict.fromkeys(
                normalized_skills
            )
        )



        categorized = {}



        for skill in normalized_skills:


            found = False



            for category, values in SKILL_CATEGORIES.items():


                values_lower = [

                    v.lower()
                    for v in values

                ]


                if skill.lower() in values_lower:


                    categorized.setdefault(
                        category,
                        []
                    ).append(skill)


                    found = True

                    break



            if not found:


                categorized.setdefault(
                    "Other Technologies",
                    []
                ).append(skill)



        output = ""



        for category, skills in categorized.items():


            output += category + "\n"



            for skill in skills:

                output += (
                    f"● {skill}\n"
                )


            output += "\n"



        return output.strip()