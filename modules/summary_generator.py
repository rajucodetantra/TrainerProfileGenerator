from modules.technical_expertise import TechnicalExpertise


class SummaryGenerator:


    def generate(self, trainer):


        tech = TechnicalExpertise()


        # IMPORTANT:
        # Always use original skills
        skills = tech.extract_skills(
            trainer.get(
                "Raw Skills",
                ""
            )
        )



        designation = trainer.get(
            "Designation",
            "Technical Trainer"
        ).strip()



        experience = trainer.get(
            "Experience",
            "Not Available"
        ).strip()



        expertise = []



        for skill in skills:


            normalized = tech.normalize_skill(
                skill
            )


            if normalized not in expertise:

                expertise.append(
                    normalized
                )



        # Limit summary technology list

        expertise = expertise[:5]



        summary = []



        summary.append(

            f"An accomplished {designation} with {experience} of experience in delivering high-quality technical training and mentoring aspiring professionals."

        )



        if expertise:


            if len(expertise) == 1:

                skill_text = expertise[0]


            else:

                skill_text = (
                    ", ".join(expertise[:-1])
                    +
                    " and "
                    +
                    expertise[-1]
                )



            summary.append(

                f"Possesses strong expertise in {skill_text}."

            )



        summary.append(

            "Experienced in delivering instructor-led classroom and online training with a strong emphasis on hands-on learning, coding practices, and project-based education."

        )



        summary.append(

            "Skilled in curriculum delivery, student mentoring, technical assessments, project guidance, and preparing learners for academic excellence and industry careers."

        )



        # AI specific sentence

        ai_skills = [

            "Generative AI",

            "Machine Learning",

            "Artificial Intelligence"

        ]



        if any(

            skill in expertise

            for skill in ai_skills

        ):


            summary.append(

                "Actively integrates emerging technologies and real-world use cases into the learning experience."

            )



        summary.append(

            "Recognized for excellent communication, learner engagement, and the ability to simplify complex technical concepts into practical, easy-to-understand sessions."

        )



        return " ".join(summary)