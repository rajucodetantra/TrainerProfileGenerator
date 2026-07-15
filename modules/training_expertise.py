from modules.technical_expertise import TechnicalExpertise


class TrainingExpertise:


    COURSE_MAP = {


        # Programming

        "python":
            "Python Programming",

        "java":
            "Java Programming",

        "c":
            "C Programming",

        "c++":
            "C++ Programming",



        # Computer Science

        "data structures & algorithms":
            "Data Structures & Algorithms",

        "competitive programming":
            "Competitive Programming",



        # Web Development

        "full stack web development":
            "Full Stack Web Development",

        "react":
            "React JS Development",

        "javascript":
            "JavaScript Development",



        # Database

        "mongodb":
            "MongoDB Database",

        "mysql":
            "SQL Database",



        # Cloud

        "aws":
            "Cloud Computing",

        "azure":
            "Cloud Computing",



        # AI

        "machine learning":
            "Machine Learning",

        "generative ai":
            "Generative AI",

        "langchain":
            "LLM Application Development"

    }



    def generate(self, trainer):


        tech = TechnicalExpertise()


        skills = tech.extract_skills(
            trainer.get(
                "Raw Skills",
                ""
            )
        )


        training = []



        # Technology based courses

        for skill in skills:


            normalized = tech.normalize_skill(
                skill
            )


            key = normalized.lower()



            if key in self.COURSE_MAP:


                training.append(
                    self.COURSE_MAP[key]
                )



        # Remove duplicates

        training = list(
            dict.fromkeys(training)
        )



        # Training responsibilities

        common_training = [


            "Mini Project Guidance & Development",

            "Major Project Mentoring & Guidance",

            "Problem Solving & Coding Practice",

            "Technical Assessments & Mock Interviews",

            "Student Mentoring & Project Guidance"

        ]



        training.extend(
            common_training
        )



        return "\n".join(

            f"● {item}"

            for item in training

        )