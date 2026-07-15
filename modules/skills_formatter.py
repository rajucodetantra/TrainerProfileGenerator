import re


class SkillsFormatter:


    def extract_skills(self, skill_text):

        if not skill_text:
            return []


        skill_text = str(skill_text)


        # Convert different separators into comma

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



        # Remove duplicates

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


            "cpp":
                "C++",



            # DSA

            "dsa":
                "DSA",

            "data structures":
                "DSA",

            "data structures and algorithms":
                "DSA",

            "data structures & algorithms":
                "DSA",



            # Competitive Programming

            "competitive coding":
                "Competitive Programming",

            "competetive coding":
                "Competitive Programming",

            "competitive programming":
                "Competitive Programming",



            # Web

            "python full stack":
                "Python Full Stack",

            "full stack":
                "Full Stack Development",


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
                "GitHub"

        }


        key = skill.lower().strip()


        return mapping.get(
            key,
            skill.title()
        )



    def format(self, trainer):


        raw_skills = trainer.get(
            "Raw Skills",
            trainer.get(
                "Skills",
                ""
            )
        )


        skills = self.extract_skills(
            raw_skills
        )


        formatted = []


        for skill in skills:

            formatted.append(
                self.normalize_skill(skill)
            )



        formatted = list(
            dict.fromkeys(formatted)
        )


        return "    ".join(
            f"■ {skill}"
            for skill in formatted
        )