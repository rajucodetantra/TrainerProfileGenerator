import re

class SkillsFormatter:

    def __init__(self):
        # Master list of normalized skills matching the enterprise profile ecosystem
        self.normalization_map = {
            "n8n": "N8N",
            "agentic ai": "Agentic AI",
            "agentic intelligence": "Agentic AI",
            "prompt engineering": "Prompt Engineering",
            "java": "Java",
            "c": "C",
            "c++": "C++",
            "python": "Python",
            "javascript": "JavaScript",
            "data structures & algorithms": "Data Structures & Algorithms",
            "dsa": "Data Structures & Algorithms",
            "full stack web development": "Full Stack Web Development",
            "full stack": "Full Stack Web Development",
            "mongodb": "MongoDB",
            "mysql": "MySQL",
            "sql": "SQL"
        }

    def extract_skills(self, skill_text):
        """
        Splits and isolates skill names cleanly regardless of whether they are 
        separated by commas, slashes, newlines, or tabs.
        """
        if not skill_text or not isinstance(skill_text, str):
            return []
            
        # Strip off any historical legacy decoration characters first
        cleaned = skill_text.replace("■", ",").replace("●", ",")
        
        # Replace common split characters with commas, then split
        cleaned = cleaned.replace("//", ",").replace("\n", ",")
        parts = cleaned.split(",")
        
        extracted = []
        for part in parts:
            # Handle secondary spacing splits if multiple skills are separated by large gaps or tabs
            sub_parts = re.split(r'\s{2,}', part.strip())
            for sub_part in sub_parts:
                item = sub_part.strip()
                if item:
                    extracted.append(item)
                    
        return extracted

    def normalize_skill(self, skill):
        """Maps varying raw strings to their official title configurations"""
        if not skill:
            return ""
        key = skill.lower().strip()
        return self.normalization_map.get(key, skill.strip())

    def format(self, trainer):
        """
        Main formatter loop that guarantees every isolated skill is 
        cleanly separated and preceded by a bullet symbol (■).
        """
        raw_skills = trainer.get("Raw Skills", trainer.get("Skills", ""))
        extracted = self.extract_skills(raw_skills)
        
        formatted_skills = []
        for skill in extracted:
            normalized = self.normalize_skill(skill)
            if normalized and normalized not in formatted_skills:
                formatted_skills.append(normalized)
                
        if not formatted_skills:
            return ""

        # Joins every skill in the list with a leading bullet and exact consistent spacing
        return "    ".join(f"■ {skill}" for skill in formatted_skills)