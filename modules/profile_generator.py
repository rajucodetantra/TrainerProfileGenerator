class ProfileGenerator:


    def generate_certifications(self, trainer):

        certifications = trainer.get(
            "Certifications",
            ""
        )


        if not certifications or str(certifications).strip() == "":

            return "N/A"


        return str(certifications)



    def generate_competitive_programming(self, trainer):

        platform = trainer.get(
            "LeetCode",
            ""
        )

        problems = trainer.get(
            "Problems Solved",
            ""
        )


        if not platform:

            return "N/A"


        output = []

        output.append(
            f"Platform : {platform}"
        )


        if problems:

            output.append(
                f"Problems Solved : {problems}"
            )


        return "\n".join(output)



    def generate_coding_profiles(self, trainer):


        profiles=[]


        profiles.append(
            f"GeeksforGeeks : {trainer.get('GeeksforGeeks','N/A')}"
        )


        profiles.append(
            f"HackerRank : {trainer.get('HackerRank','N/A')}"
        )


        profiles.append(
            f"CodeChef : {trainer.get('CodeChef','N/A')}"
        )


        return "\n".join(profiles)



    def generate_core_competencies(self, trainer):


        competencies = [

            "Technical Training",

            "Curriculum Design",

            "Student Mentoring",

            "Faculty Development",

            "Assessment & Evaluation",

            "Workshop Delivery",

            "Learning Management Systems"

        ]


        return "\n".join(
            f"• {item}"
            for item in competencies
        )



    def generate_professional_highlights(self, trainer):


        highlights=[]


        experience = trainer.get(
            "Experience",
            ""
        )


        if experience:

            highlights.append(
                f"{experience} of experience in technical training."
            )


        highlights.extend([

            "Delivered training programs across universities.",

            "Conducted workshops and faculty development programs.",

            "Mentored students in academic and industry projects.",

            "Guided learners through practical hands-on training.",

            "Experienced in outcome-based technical education."

        ])


        return "\n".join(
            f"• {item}"
            for item in highlights
        )