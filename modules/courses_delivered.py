from modules.technical_expertise import TechnicalExpertise


class CoursesDelivered:

    COURSE_MAP = {
        "Java": "Java Programming",
        "Python": "Python Programming",
        "C": "C Programming",
        "C++": "C++ Programming",
        "C#": "C# Programming",
        "Data Structures & Algorithms": "Data Structures & Algorithms",
        "Object-Oriented Programming": "Object-Oriented Programming",
        "HTML": "HTML & CSS",
        "CSS": "HTML & CSS",
        "JavaScript": "JavaScript Programming",
        "React": "React.js Development",
        "Angular": "Angular Development",
        "Vue": "Vue.js Development",
        "Node.js": "Node.js Development",
        "Express.js": "Express.js Development",
        "Spring Boot": "Spring Boot Development",
        "Django": "Django Development",
        "Flask": "Flask Development",
        "FastAPI": "FastAPI Development",
        "Full Stack Web Development": "Full Stack Web Development",
        "MongoDB": "MongoDB Database",
        "MySQL": "MySQL Database",
        "Oracle": "Oracle Database",
        "SQL": "SQL Programming",
        "AWS": "AWS Cloud Computing",
        "Azure": "Microsoft Azure",
        "Docker": "Docker Fundamentals",
        "Kubernetes": "Kubernetes",
        "Machine Learning": "Machine Learning",
        "Deep Learning": "Deep Learning",
        "Generative AI": "Generative AI",
        "LangChain": "LangChain Development",
        "LangGraph": "LangGraph",
        "OpenAI": "OpenAI API Integration"
    }

    def generate(self, trainer):

        tech = TechnicalExpertise()
        skills = tech.extract_skills(trainer.get("Skills", ""))

        courses = []

        for skill in skills:

            if skill in self.COURSE_MAP:
                courses.append(self.COURSE_MAP[skill])

        # Remove duplicates
        courses = list(dict.fromkeys(courses))

        # Add broader courses automatically
        if "Java Programming" in courses and "Data Structures & Algorithms" not in courses:
            courses.append("Data Structures & Algorithms")

        if (
            "HTML & CSS" in courses
            or "JavaScript Programming" in courses
            or "React.js Development" in courses
        ):
            if "Web Development" not in courses:
                courses.append("Web Development")

        if (
            "Java Programming" in courses
            and "Web Development" in courses
        ):
            if "Full Stack Web Development" not in courses:
                courses.append("Full Stack Web Development")

        return "\n".join(f"● {course}" for course in courses)