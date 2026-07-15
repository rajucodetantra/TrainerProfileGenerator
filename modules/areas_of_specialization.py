from modules.technical_expertise import TechnicalExpertise


class AreasOfSpecialization:

    DOMAIN_MAP = {
        "Java": "Java Application Development",
        "Python": "Python Programming",
        "C": "Programming Fundamentals",
        "C++": "Object-Oriented Programming",
        "Data Structures & Algorithms": "Problem Solving & Algorithms",
        "Object-Oriented Programming": "Object-Oriented Design",
        "HTML": "Frontend Development",
        "CSS": "Frontend Development",
        "JavaScript": "Frontend Development",
        "React": "Modern Web Development",
        "Angular": "Modern Web Development",
        "Vue": "Modern Web Development",
        "Node.js": "Backend Development",
        "Express.js": "Backend Development",
        "Spring Boot": "Enterprise Application Development",
        "Django": "Backend Development",
        "Flask": "Backend Development",
        "FastAPI": "API Development",
        "MongoDB": "NoSQL Databases",
        "MySQL": "Relational Databases",
        "Oracle": "Database Management",
        "SQL": "Database Programming",
        "AWS": "Cloud Computing",
        "Azure": "Cloud Computing",
        "Docker": "Containerization",
        "Kubernetes": "Container Orchestration",
        "Machine Learning": "Artificial Intelligence",
        "Deep Learning": "Artificial Intelligence",
        "Generative AI": "Generative AI",
        "LangChain": "LLM Application Development",
        "LangGraph": "AI Agent Development",
        "OpenAI": "Generative AI Solutions"
    }

    def generate(self, trainer):

        tech = TechnicalExpertise()
        skills = tech.extract_skills(trainer.get("Skills", ""))

        domains = []

        for skill in skills:
            if skill in self.DOMAIN_MAP:
                domains.append(self.DOMAIN_MAP[skill])

        # Remove duplicates while preserving order
        domains = list(dict.fromkeys(domains))

        return "\n".join(f"● {domain}" for domain in domains)