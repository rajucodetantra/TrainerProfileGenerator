class TrainerHighlights:


    def generate(self, trainer):

        highlights = []


        skills = trainer.get(
            "Skills",
            ""
        )


        highlights.append(
            "Delivered technical training programs across academic and industry environments."
        )

        highlights.append(
            "Conducted hands-on sessions with practical coding exercises and real-world projects."
        )

        highlights.append(
            "Mentored students in programming, project development, and technical skill enhancement."
        )

        highlights.append(
            "Guided learners for coding assessments, technical interviews, and placement preparation."
        )

        highlights.append(
            "Designed outcome-based learning activities to improve practical implementation skills."
        )

        highlights.append(
            "Experienced in classroom, online, and hybrid training delivery."
        )


        return "\n".join(
            f"● {item}"
            for item in highlights
        )