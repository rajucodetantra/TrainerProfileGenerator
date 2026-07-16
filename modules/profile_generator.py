import re

class ProfileGenerator:

    def __init__(self):
        pass

    def _get_clean_skills_list(self, trainer):
        """Helper to return a clean, flat list of uppercase/title strings from raw skills input, stripping existing structural symbols."""
        raw_skills = str(trainer.get("Skills", "")).strip()
        if not raw_skills or raw_skills.lower() == "nan":
            return []
            
        clean_items = []
        # Aggressively remove formatting leftovers
        normalized = raw_skills.replace("■", ",").replace("●", ",").replace("•", ",").replace("💻", ",")
        for item in normalized.split(","):
            val = item.strip()
            if val and val.lower() != "nan":
                if val.lower() in ["dsa", "ai", "iot", "fdp", "crt", "llm", "dbms", "os"]:
                    clean_items.append(val.upper())
                elif val.lower() == "n8n":
                    clean_items.append("n8n")
                else:
                    clean_items.append(val.title())
        return clean_items

    def generate_core_skills(self, trainer):
        """Generates clean inline skills separated uniformly by spaces, no duplicate nested symbols."""
        skills = self._get_clean_skills_list(trainer)
        if not skills:
            return "N/A"
        return "   ".join([f"■ {item}" for item in skills])

    def generate_professional_summary(self, trainer):
        """Generates a third-person narrative summary without mid-sentence symbols."""
        name = str(trainer.get("Name", "The trainer")).strip()
        designation = str(trainer.get("Designation", "Technical Trainer")).strip()
        company = str(trainer.get("Company", "CodeTantra Tech Solutions Pvt. Ltd.")).strip()
        exp = str(trainer.get("Experience", "0 Years")).strip()
        
        skills = self._get_clean_skills_list(trainer)
        skills_sentence = ", ".join(skills) if skills else "various modern technologies"

        summary = f"An accomplished {designation} with {exp} of experience in delivering high-quality " \
                  f"technical training and mentoring aspiring professionals. Possesses strong expertise in {skills_sentence}. " \
                  f"Experienced in delivering instructor-led classroom and online training with a strong emphasis on " \
                  f"hands-on learning, coding practices, and project-based education. Skilled in curriculum delivery, " \
                  f"student mentoring, technical assessments, project guidance, and preparing learners for academic excellence " \
                  f"and industry careers. Recognized for excellent communication, learner engagement, and the ability to simplify " \
                  f"complex technical concepts into practical, easy-to-understand sessions."
        return summary

    def generate_technical_expertise(self, trainer):
        """Intelligently groups flat skills into standard corporate technical groupings."""
        skills = self._get_clean_skills_list(trainer)
        if not skills:
            return "N/A"

        categories = {
            "Programming Languages": [],
            "Computer Science Fundamentals": [],
            "Web Technologies": [],
            "AI, Automation & Advanced Technologies": []
        }

        for skill in skills:
            skill_lower = skill.lower()
            if skill_lower in ["java", "c", "python", "c++", "javascript", "typescript", "ruby", "go"]:
                categories["Programming Languages"].append(skill)
            elif any(x in skill_lower for x in ["dsa", "data structure", "algorithm", "oop", "object", "dbms", "os", "networking"]):
                if "dsa" in skill_lower or "data structure" in skill_lower:
                    categories["Computer Science Fundamentals"].append("Data Structures & Algorithms")
                elif "oop" in skill_lower or "object" in skill_lower:
                    categories["Computer Science Fundamentals"].append("Object-Oriented Programming")
                else:
                    categories["Computer Science Fundamentals"].append(skill)
            elif any(x in skill_lower for x in ["web", "full stack", "frontend", "backend", "react", "node", "html", "css"]):
                if "full stack" in skill_lower:
                    categories["Web Technologies"].append("Full Stack Web Development")
                else:
                    categories["Web Technologies"].append(skill)
            else:
                if "n8n" in skill_lower:
                    categories["AI, Automation & Advanced Technologies"].append("n8n Workflow Automation")
                elif "agentic" in skill_lower:
                    categories["AI, Automation & Advanced Technologies"].append("Agentic AI Architectures")
                elif "prompt" in skill_lower:
                    categories["AI, Automation & Advanced Technologies"].append("Prompt Engineering")
                else:
                    categories["AI, Automation & Advanced Technologies"].append(skill)

        output_blocks = []
        for cat_name, items in categories.items():
            if items:
                unique_items = list(dict.fromkeys(items))
                block = f"{cat_name}\n" + "\n".join([f"● {item}" for item in unique_items])
                output_blocks.append(block)

        return "\n\n".join(output_blocks) if output_blocks else "N/A"

    def generate_certifications(self, trainer):
        certs = str(trainer.get("Certifications", "")).strip()
        if not certs or certs.lower() in ["nan", "n/a", ""]:
            return "N/A"
        return "\n".join([item.strip() for item in certs.split(",") if item.strip()])

    def generate_competitive_programming(self, trainer):
        """Generates a cohesive competitive programming layout block."""
        leetcode = str(trainer.get("LeetCode Profile Link", "")).strip()
        problems = str(trainer.get("No of Problems Done", "")).strip()
        other = str(trainer.get("Other Profiles", "")).strip()

        lines = []
        if leetcode and leetcode.lower() != "nan":
            lines.append(f"Leetcode Profile: {leetcode}")
        if problems and problems.lower() != "nan":
            lines.append(f"No of Problems solved: {problems}")
        if other and other.lower() != "nan":
            lines.append(f"Other Profiles: {other}")

        return "\n".join(lines) if lines else "N/A"

    def generate_coding_profiles(self, trainer):
        profiles = str(trainer.get("Coding Profiles", "")).strip()
        if not profiles or profiles.lower() in ["nan", "n/a", ""]:
            return "N/A"
        return profiles

    def generate_training_expertise(self, trainer):
        skills = self._get_clean_skills_list(trainer)
        items = []
        for s in skills:
            if "dsa" in s.lower() or "data structure" in s.lower():
                items.extend(["• Data Structures & Algorithms", "• Problem Solving & Coding Practice"])
            elif "web" in s.lower() or "full stack" in s.lower():
                items.append("• Full Stack Development")
            elif s.lower() in ["n8n", "agentic ai", "prompt engineering"]:
                items.append(f"• {s}")
            else:
                items.append(f"• {s} Programming")
                
        items.extend([
            "• Mini Project Guidance & Development",
            "• Major Project Mentoring & Guidance",
            "• Technical Assessments & Mock Interviews",
            "• Student Mentoring & Project Guidance"
        ])
        return "\n".join(list(dict.fromkeys(items)))

    def generate_professional_highlights(self, trainer):
        highlights = [
            "• Delivered technical training programs across academic and industry environments.",
            "• Conducted hands-on sessions with practical coding exercises and real-world projects.",
            "• Mentored students in programming, project development, and technical skill enhancement.",
            "• Guided learners for coding assessments, technical interviews, and placement preparation.",
            "• Designed outcome-based learning activities to improve practical implementation skills.",
            "• Experienced in classroom, online, and hybrid training delivery."
        ]
        return "\n".join(highlights)

    def generate_core_competencies(self, trainer):
        competencies = [
            "• Technical Training",
            "• Curriculum Design",
            "• Student Mentoring",
            "• Faculty Development",
            "• Campus Training Programs",
            "• Assessment & Evaluation",
            "• Workshop Delivery",
            "• Learning Management Platforms"
        ]
        return "\n".join(competencies)

    def generate_training_projects(self, projects):
        """Builds formatted list of all active or completed project titles."""
        items = []
        if not projects:
            return "N/A"
            
        ongoing = projects.get("ongoing", [])
        completed = projects.get("completed", [])

        for p in ongoing:
            subj = p.get('Subject', '')
            col = p.get('College', '')
            if subj and col:
                items.append(f"• Ongoing: {subj} at {col}")
        for p in completed:
            subj = p.get('Subject', '')
            col = p.get('College', '')
            if subj and col:
                items.append(f"• Completed: {subj} at {col}")

        return "\n".join(items) if items else "N/A"