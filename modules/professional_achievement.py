
from modules.technical_expertise import TechnicalExpertise


class ProfessionalAchievements:


    def generate(self, trainer):


        tech = TechnicalExpertise()


        skills = tech.extract_skills(

            trainer.get(
                "Raw Skills",
                ""
            )

        )


        achievements = []



        # Programming based

        if any(

            skill.lower() in [

                "java",
                "python",
                "c",
                "c++"

            ]

            for skill in skills

        ):


            achievements.append(

                "Successfully developed learners' programming and problem-solving capabilities through structured technical training."

            )



        # Full stack based

        if any(

            "full stack" in skill.lower()

            or "react" in skill.lower()

            or "spring" in skill.lower()

            for skill in skills

        ):


            achievements.append(

                "Supported learners in building application development skills through practical software projects."

            )



        # AI based

        if any(

            "ai" in skill.lower()

            or "machine learning" in skill.lower()

            or "langchain" in skill.lower()

            for skill in skills

        ):


            achievements.append(

                "Introduced learners to emerging technologies through industry-relevant AI and modern application development practices."

            )



        # General achievements


        achievements.extend([


            "Contributed to improving learner technical skills through structured and outcome-driven training programs.",


            "Supported students in achieving academic excellence and career readiness.",


            "Maintained continuous knowledge enhancement aligned with evolving industry technologies."


        ])




        # Remove duplicates

        achievements = list(

            dict.fromkeys(

                achievements

            )

        )



        return "\n".join(

            f"● {item}"

            for item in achievements

        )