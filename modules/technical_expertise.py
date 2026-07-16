import re
from modules.skills_formatter import SkillsFormatter

class TechnicalExpertise:

    def __init__(self):
        self.formatter = SkillsFormatter()
        # Explicit mapping structure matching professional layouts
        self.categories_map = {
            "Automation & AI": ["N8N", "Agentic AI", "Prompt Engineering"],
            "Programming Languages": ["Java", "C", "C++", "Python", "JavaScript"],
            "Computer Science Fundamentals": ["Data Structures & Algorithms", "Competitive Coding", "Competitive Programming"],
            "Web Technologies": ["Full Stack Web Development", "HTML", "CSS", "JavaScript"],
            "Database Technologies": ["MongoDB", "MySQL", "SQL"]
        }

    def extract_skills(self, skill_text):
        """Maintains backward compatibility for other modules leveraging this method"""
        return self.formatter.extract_skills(skill_text)

    def normalize_skill(self, skill):
        """Maintains backward compatibility for other modules leveraging this method"""
        return self.formatter.normalize_skill(skill)

    def generate(self, trainer):
        # Extract and normalize the structured list cleanly
        raw_skills = trainer.get("Raw Skills", trainer.get("Skills", ""))
        extracted = self.extract_skills(raw_skills)
        skills_list = [self.normalize_skill(s) for s in extracted]
        
        output_lines = []
        categorized_skills = set()
        
        # Group fields dynamically into matching categories
        for category, matching_skills in self.categories_map.items():
            found_skills = [s for s in skills_list if s in matching_skills]
            if found_skills:
                output_lines.append(category)
                for fs in found_skills:
                    output_lines.append(f"● {fs}")
                    categorized_skills.add(fs)
                    
        # Fallback category handler for uncategorized skills
        other_skills = [s for s in skills_list if s not in categorized_skills]
        if other_skills:
            output_lines.append("Other Technologies")
            for os_skill in other_skills:
                output_lines.append(f"● {os_skill}")
                
        return "\n".join(output_lines)