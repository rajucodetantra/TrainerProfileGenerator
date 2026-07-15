from modules.technical_expertise import TechnicalExpertise


class KeyStrengths:

    def generate(self, trainer):

        tech = TechnicalExpertise()
        skills = tech.extract_skills(trainer.get("Skills", ""))

        strengths = []

        programming = any(
            s.lower() in [
                "java", "python", "c", "c++", "c#",
                "javascript", "typescript", "go", "php"
            ]
            for s in skills
        )

        web = any(
            any(k in s.lower() for k in [
                "html", "css", "react", "angular",
                "vue", "node", "spring",
                "django", "flask", "full stack"
            ])
            for s in skills
        )

        database = any(
            any(k in s.lower() for k in [
                "mysql", "mongodb", "oracle",
                "postgres", "sql"
            ])
            for s in skills
        )

        ai = any(
            any(k in s.lower() for k in [
                "machine learning", "deep learning",
                "langchain", "langgraph",
                "gen ai", "openai", "rag"
            ])
            for s in skills
        )

        cloud = any(
            any(k in s.lower() for k in [
                "aws", "azure", "gcp",
                "docker", "kubernetes",
                "jenkins"
            ])
            for s in skills
        )

        if programming:
            strengths.append("Strong programming and problem-solving skills")

        if web:
            strengths.append("Expertise in modern web application development")

        if database:
            strengths.append("Strong database design and data management knowledge")

        if ai:
            strengths.append("Hands-on experience with Artificial Intelligence and Generative AI")

        if cloud:
            strengths.append("Knowledge of Cloud Computing and DevOps practices")

        strengths.extend([
            "Excellent classroom presentation and communication skills",
            "Project-based and outcome-driven training approach",
            "Student mentoring and technical guidance",
            "Curriculum planning and instructional design",
            "Coding assessment and interview preparation",
            "Continuous learning and technology upskilling"
        ])

        # Remove duplicates while preserving order
        strengths = list(dict.fromkeys(strengths))

        return "\n".join(f"● {item}" for item in strengths)