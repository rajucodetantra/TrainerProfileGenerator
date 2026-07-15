from modules.technical_expertise import TechnicalExpertise


class ProfessionalAchievements:

    def generate(self, trainer):

        tech = TechnicalExpertise()
        skills = tech.extract_skills(trainer.get("Skills", ""))

        achievements = []

        skill_count = len(skills)

        # Technology-specific achievements
        if any(s.lower() in ["java", "python", "c", "c++"] for s in skills):
            achievements.append(
                "Successfully delivered programming courses with a strong emphasis on practical implementation and coding standards."
            )

        if any("full stack" in s.lower() or "react" in s.lower() or "spring" in s.lower() for s in skills):
            achievements.append(
                "Facilitated end-to-end application development training through real-world projects."
            )

        if any("mongodb" in s.lower() or "mysql" in s.lower() or "sql" in s.lower() for s in skills):
            achievements.append(
                "Guided learners in database design, optimization, and application integration."
            )

        if any(x in s.lower() for s in skills for x in ["machine learning", "gen ai", "langchain", "openai"]):
            achievements.append(
                "Designed and delivered industry-oriented AI and Generative AI learning experiences."
            )

        # General achievements
        achievements.extend([
            "Mentored students in academic and industry-oriented projects.",
            "Prepared learners for coding assessments, technical interviews, and placement drives.",
            "Designed engaging hands-on laboratory sessions to enhance practical learning.",
            "Continuously upgraded technical knowledge to align training with current industry trends.",
            "Maintained high learner engagement through interactive and outcome-based teaching methodologies."
        ])

        # Add a personalized achievement based on breadth of skills
        if skill_count >= 10:
            achievements.append(
                "Demonstrated versatility by delivering training across multiple technologies and domains."
            )

        # Remove duplicates
        achievements = list(dict.fromkeys(achievements))

        return "\n".join(f"● {item}" for item in achievements)
