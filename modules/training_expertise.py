import re
from modules.skills_formatter import SkillsFormatter

class TrainingExpertise:

    COURSE_MAP = {
        "python": "Python Programming",
        "java": "Java Programming",
        "c": "C Programming",
        "c++": "C++ Programming",
        "data structures & algorithms": "Data Structures & Algorithms",
        "competitive programming": "Competitive Programming",
        "full stack web development": "Full Stack Web Development",
        "react": "React JS Development",
        "javascript": "JavaScript Development",
        "mongodb": "MongoDB Database",
        "mysql": "SQL Database",
        "aws": "Cloud Computing",
        "azure": "Cloud Computing",
        "machine learning": "Machine Learning",
        "generative ai": "Generative AI",
        "langchain": "LLM Application Development",
        "n8n": "N8N Workflow Automation",
        "agentic ai": "Agentic AI Engineering",
        "prompt engineering": "Prompt Engineering & GenAI"
    }

    def __init__(self):
        self.formatter = SkillsFormatter()

    def generate(self, trainer):
        raw_skills = trainer.get("Raw Skills", trainer.get("Skills", ""))
        
        # Clean up legacy decoration run artifacts safely if they exist
        if isinstance(raw_skills, str):
            raw_skills = raw_skills.replace("■", "").replace("●", "")
            
        extracted = self.formatter.extract_skills(raw_skills)
        training = []

        for skill in extracted:
            normalized = self.formatter.normalize_skill(skill)
            key = normalized.lower().strip()

            if key in self.COURSE_MAP:
                training.append(self.COURSE_MAP[key])
            else:
                training.append(f"{normalized} Training")

        # De-duplicate entries cleanly
        training = list(dict.fromkeys(training))

        common_training = [
            "Mini Project Guidance & Development",
            "Major Project Mentoring & Guidance",
            "Problem Solving & Coding Practice",
            "Technical Assessments & Mock Interviews",
            "Student Mentoring & Project Guidance"
        ]

        training.extend(common_training)

        return "\n".join(f"● {item}" for item in training)