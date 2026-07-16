import re
from modules.technical_expertise import TechnicalExpertise

class SummaryGenerator:

    def __init__(self):
        # Instantiate inside init to follow module configuration patterns safely
        self.tech = TechnicalExpertise()

    def generate(self, trainer):
        # 1. Safely grab raw skills falling back to standard "Skills" if "Raw Skills" is missing
        raw_skills = trainer.get("Raw Skills", trainer.get("Skills", ""))
        
        # Strip away legacy punctuation artifacts if they got injected into the string pipeline
        if isinstance(raw_skills, str):
            raw_skills = raw_skills.replace("■", "").replace("●", "")

        skills = self.tech.extract_skills(raw_skills)

        designation = trainer.get("Designation", "Technical Trainer").strip()
        experience = trainer.get("Experience", "Not Available").strip()

        expertise = []
        for skill in skills:
            normalized = self.tech.normalize_skill(skill)
            if normalized not in expertise:
                expertise.append(normalized)

        # Cap list lengths strictly to keep the sentence density balanced
        expertise = expertise[:5]

        summary = []

        # Sentence 1: Designation & Years of Experience
        summary.append(
            f"An accomplished {designation} with {experience} of experience in delivering high-quality "
            f"technical training and mentoring aspiring professionals."
        )

        # Sentence 2: Clean Comma-Separated Skills String
        if expertise:
            if len(expertise) == 1:
                skill_text = expertise[0]
            elif len(expertise) == 2:
                skill_text = f"{expertise[0]} and {expertise[1]}"
            else:
                # Proper grammatical join including Oxford comma before the ultimate conjunction
                skill_text = ", ".join(expertise[:-1]) + f", and {expertise[-1]}"

            summary.append(f"Possesses strong expertise in {skill_text}.")

        # Sentence 3 & 4: Delivery styles and capabilities
        summary.append(
            "Experienced in delivering instructor-led classroom and online training with a strong emphasis on "
            "hands-on learning, coding practices, and project-based education."
        )

        summary.append(
            "Skilled in curriculum delivery, student mentoring, technical assessments, project guidance, and "
            "preparing learners for academic excellence and industry careers."
        )

        # Sentence 5: AI Specific Trigger expansion (Includes Agentic AI, Prompt Engineering, and N8N)
        ai_skills = [
            "Generative AI", 
            "Machine Learning", 
            "Artificial Intelligence", 
            "Agentic AI", 
            "Prompt Engineering", 
            "N8N"
        ]

        if any(skill in expertise for skill in ai_skills):
            summary.append(
                "Actively integrates emerging technologies and real-world use cases into the learning experience."
            )

        # Sentence 6: Evaluation communication wrapper
        summary.append(
            "Recognized for excellent communication, learner engagement, and the ability to simplify complex "
            "technical concepts into practical, easy-to-understand sessions."
        )

        # Final pass: Join items cleanly and ensure no accidental spaces remain
        combined_summary = " ".join(summary)
        return re.sub(r"\s+", " ", combined_summary).strip()