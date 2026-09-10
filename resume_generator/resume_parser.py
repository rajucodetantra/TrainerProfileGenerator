import re


# =========================================================
# SECTION HEADINGS
# =========================================================

SECTION_HEADINGS = [
    "PROFESSIONAL SUMMARY",
    "EXECUTIVE SUMMARY",
    "PROFILE SUMMARY",
    "SUMMARY",
    "ABOUT ME",
    "CAREER OBJECTIVE",
    "OBJECTIVE",

    "PROFESSIONAL EXPERIENCE",
    "WORK EXPERIENCE",
    "EXPERIENCE",
    "EMPLOYMENT HISTORY",

    "EDUCATION",
    "EDUCATIONAL QUALIFICATION",
    "ACADEMIC QUALIFICATION",
    "ACADEMIC DETAILS",
    "QUALIFICATION",

    "CORE SKILLS",
    "KEY SKILLS",
    "SKILLS & TOOLS",
    "SKILLS",
    "TECHNICAL SKILLS",

    "CERTIFICATIONS",
    "CERTIFICATION",

    "ACHIEVEMENTS",
    "ACHIEVEMENT",
    "AWARDS",

    "LANGUAGES",
    "LANGUAGE",

    "PROJECTS",
    "TRAINING PROJECTS"
]


# =========================================================
# APTITUDE SUBJECTS
# =========================================================

APTITUDE_SUBJECTS = {
    "Quantitative Aptitude": [
        "quantitative aptitude",
        "quant aptitude"
    ],

    "Logical Reasoning": [
        "logical reasoning",
        "reasoning ability"
    ],

    "Verbal Ability": [
        "verbal ability",
        "verbal aptitude"
    ],

    "Data Interpretation": [
        "data interpretation"
    ],

    "Vedic Maths": [
        "vedic maths",
        "vedic mathematics"
    ],

    "Speed Maths": [
        "speed maths",
        "speed mathematics"
    ],

    "Soft Skills": [
        "soft skills",
        "personality development"
    ],

    "Communication Skills": [
        "communication skills",
        "communication training"
    ],

    "Interview Preparation": [
        "interview preparation",
        "interview training",
        "mock interview",
        "mock interviews"
    ],

    "Group Discussion": [
        "group discussion",
        "gd practice",
        "group discussions"
    ],

    "Placement Aptitude": [
        "placement aptitude",
        "placement preparation"
    ],

    "Campus Recruitment Training": [
        "campus recruitment training",
        "campus recruitment",
        "crt"
    ]
}


# =========================================================
# TECHNICAL SUBJECTS
# =========================================================

TECHNICAL_SUBJECTS = {
    "Python": [
        "python programming",
        "python"
    ],

    "Java": [
        "core java",
        "java programming",
        "java"
    ],

    "C Programming": [
        "c programming",
        "c language"
    ],

    "C++": [
        "c++"
    ],

    "Data Structures": [
        "data structures",
        "data structure",
        "dsa"
    ],

    "Python with DSA": [
        "python with dsa",
        "dsa using python"
    ],

    "Java with DSA": [
        "java with dsa",
        "dsa using java"
    ],

    "SQL": [
        "mysql",
        "sql"
    ],

    "Power BI": [
        "power bi"
    ],

    "Git": [
        "github",
        "git"
    ],

    "Python Full Stack": [
        "python full stack",
        "full stack python"
    ],

    "Java Full Stack": [
        "java full stack",
        "full stack java"
    ],

    "Web Development": [
        "web development",
        "html",
        "css",
        "javascript"
    ],

    "Generative AI": [
        "generative ai",
        "gen ai",
        "genai"
    ],

    "Prompt Engineering": [
        "prompt engineering"
    ]
}


# =========================================================
# EXAM / PLACEMENT EXPERTISE
# =========================================================

EXAM_EXPERTISE = {
    "Campus Recruitment Training": [
        "campus recruitment",
        "campus placement",
        "placement training",
        "crt"
    ],

    "Campus Placements": [
        "campus placements",
        "campus placement"
    ],

    "CAT": [
        "cat"
    ],

    "GRE": [
        "gre"
    ],

    "SSC CGL": [
        "ssc cgl"
    ],

    "Government Exams": [
        "government exams",
        "government exam"
    ],

    "Competitive Exams": [
        "competitive exams",
        "competitive exam"
    ],

    "Entrance Tests": [
        "entrance tests",
        "entrance test",
        "entrance exams",
        "entrance exam"
    ],

    "Banking Exams": [
        "banking exams",
        "banking exam",
        "bank exams"
    ],

    "Placement Assessments": [
        "placement assessment",
        "placement assessments",
        "placement test",
        "placement tests"
    ],

    "Interview Preparation": [
        "interview preparation",
        "mock interview",
        "mock interviews"
    ],

    "Resume Building": [
        "resume building",
        "resume preparation"
    ]
}


# =========================================================
# CORE COMPETENCIES
# =========================================================

CORE_COMPETENCIES = {
    "Training Delivery": [
        "training delivery",
        "delivering training",
        "delivered training"
    ],

    "Student Mentoring": [
        "student mentoring",
        "mentoring students",
        "mentored students"
    ],

    "Curriculum Development": [
        "curriculum development",
        "curriculum design"
    ],

    "Assessment & Evaluation": [
        "assessment",
        "evaluation",
        "mock tests",
        "mock test"
    ],

    "Workshop Delivery": [
        "workshop",
        "workshops",
        "bootcamp",
        "bootcamps"
    ],

    "Classroom Management": [
        "classroom management"
    ],

    "Placement Training": [
        "placement training",
        "placement preparation"
    ],

    "Faculty Development": [
        "faculty development"
    ],

    "Content Development": [
        "content development",
        "content creation",
        "lesson planning",
        "study guides"
    ],

    "Interview Training": [
        "interview training",
        "interview preparation"
    ],

    "Career Guidance": [
        "career guidance",
        "career counselling",
        "career counseling"
    ],

    "Campus Training Programs": [
        "campus training",
        "campus recruitment"
    ]
}


# =========================================================
# DEGREE PATTERN
# =========================================================

DEGREE_PATTERN = re.compile(
    r"\b("
    r"B\.?\s*Tech|"
    r"B\.?\s*E\.?|"
    r"M\.?\s*Tech|"
    r"M\.?\s*E\.?|"
    r"MCA|"
    r"MBA|"
    r"BCA|"
    r"B\.?\s*Sc|"
    r"M\.?\s*Sc|"
    r"Bachelor(?:'s)?|"
    r"Master(?:'s)?"
    r")\b",
    re.IGNORECASE
)


# =========================================================
# BASIC HELPERS
# =========================================================

def clean_lines(text):
    """
    Convert extracted PDF text into clean lines.
    """

    cleaned = []

    for line in text.splitlines():

        line = re.sub(
            r"\s+",
            " ",
            line
        ).strip()

        if line:
            cleaned.append(line)

    return cleaned


def unique_list(items):
    """
    Remove duplicates while maintaining order.
    """

    result = []
    seen = set()

    for item in items:

        key = item.lower().strip()

        if key not in seen:

            seen.add(key)
            result.append(item)

    return result


def normalize_heading(line):

    return (
        line.strip()
        .upper()
        .rstrip(":")
    )


def is_known_heading(line):

    value = normalize_heading(line)

    for heading in SECTION_HEADINGS:

        if value == heading:
            return True

    return False


# =========================================================
# SECTION EXTRACTION
# =========================================================

def extract_section(lines, headings):
    """
    Extract content below a heading until
    the next known section heading.
    """

    if isinstance(headings, str):

        headings = [headings]

    headings = [
        item.upper()
        for item in headings
    ]

    start_index = None

    for index, line in enumerate(lines):

        current = normalize_heading(line)

        if current in headings:

            start_index = index + 1
            break

    if start_index is None:
        return ""

    result = []

    for line in lines[start_index:]:

        if is_known_heading(line):
            break

        result.append(line)

    return "\n".join(result).strip()


# =========================================================
# NAME
# =========================================================

def extract_name(lines):
    """
    Usually candidate name appears within
    the first few lines of the resume.
    """

    skip_words = [
        "resume",
        "curriculum vitae",
        "trainer",
        "professional summary",
        "executive summary",
        "profile",
        "phone",
        "email",
        "linkedin",
        "chennai",
        "hyderabad",
        "india"
    ]

    for line in lines[:15]:

        candidate = line.strip()

        lower = candidate.lower()

        if not candidate:
            continue

        if "@" in candidate:
            continue

        if "http" in lower:
            continue

        if any(
            word == lower
            for word in skip_words
        ):
            continue

        if "trainer" in lower:
            continue

        if DEGREE_PATTERN.search(candidate):
            continue

        digits = re.sub(
            r"\D",
            "",
            candidate
        )

        if len(digits) >= 8:
            continue

        if len(candidate) > 70:
            continue

        # Candidate names normally contain
        # mostly letters, dots and spaces
        if re.fullmatch(
            r"[A-Za-z.\s'-]+",
            candidate
        ):

            return candidate.strip()

    return ""


# =========================================================
# EMAIL
# =========================================================

def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+\-]+"
        r"@[A-Za-z0-9.\-]+"
        r"\.[A-Za-z]{2,}",
        text
    )

    if match:
        return match.group(0)

    return ""


# =========================================================
# PHONE
# =========================================================

def extract_phone(text):

    patterns = [
        r"(?:\+91[\s\-]?)?[6-9]\d{9}",

        r"(?:\+91[\s\-]?)?"
        r"[6-9](?:[\s\-]?\d){9}"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            phone = match.group(0)

            phone = re.sub(
                r"\s+",
                " ",
                phone
            )

            return phone.strip()

    return ""


# =========================================================
# LINKEDIN
# =========================================================

def extract_linkedin(text):

    match = re.search(
        r"https?://(?:www\.)?"
        r"linkedin\.com/[^\s|]+",
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(0).rstrip(
            ".,);"
        )

    return ""


# =========================================================
# EXPERIENCE
# =========================================================

def extract_experience(text):
    """
    Extract values like:
    4 years
    5+ years
    over 6 years
    12 years of experience
    """

    patterns = [
        r"(?:over\s+)?"
        r"\d+(?:\.\d+)?"
        r"\s*\+?\s*years",

        r"\d+(?:\.\d+)?"
        r"\s*\+?\s*yrs"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(0).strip()

    return ""


# =========================================================
# QUALIFICATION
# =========================================================

def extract_qualification(lines):

    education_section = extract_section(
        lines,
        [
            "EDUCATION",
            "EDUCATIONAL QUALIFICATION",
            "ACADEMIC QUALIFICATION",
            "ACADEMIC DETAILS",
            "QUALIFICATION"
        ]
    )

    if education_section:

        education_lines = clean_lines(
            education_section
        )

        for line in education_lines:

            if DEGREE_PATTERN.search(line):

                return line.strip()

    # Fallback: search entire resume
    for line in lines:

        if DEGREE_PATTERN.search(line):

            if len(line) <= 140:
                return line.strip()

    return ""


# =========================================================
# KEYWORD DETECTION
# =========================================================

def contains_keyword(text, keyword):

    text_lower = text.lower()
    keyword_lower = keyword.lower()

    # Short terms like CAT, GRE, SQL, Git
    # should use word boundaries.
    if len(keyword) <= 4:

        pattern = (
            r"\b"
            + re.escape(keyword_lower)
            + r"\b"
        )

        return bool(
            re.search(
                pattern,
                text_lower
            )
        )

    return keyword_lower in text_lower


def find_keywords(text, mapping):

    found = []

    for display_name, keywords in (
        mapping.items()
    ):

        for keyword in keywords:

            if contains_keyword(
                text,
                keyword
            ):

                found.append(
                    display_name
                )

                break

    return unique_list(found)


# =========================================================
# LANGUAGES
# =========================================================

def extract_languages(lines):

    section = extract_section(
        lines,
        [
            "LANGUAGES",
            "LANGUAGE"
        ]
    )

    if section:

        section = section.replace(
            "|",
            ", "
        )

        section = re.sub(
            r"\s*,\s*",
            ", ",
            section
        )

        return section.strip()

    full_text = " ".join(
        lines
    ).lower()

    known_languages = [
        "English",
        "Telugu",
        "Hindi",
        "Tamil",
        "Kannada",
        "Malayalam"
    ]

    found = []

    for language in known_languages:

        if re.search(
            r"\b"
            + re.escape(
                language.lower()
            )
            + r"\b",
            full_text
        ):

            found.append(language)

    return ", ".join(found)


# =========================================================
# CERTIFICATIONS
# =========================================================

def extract_certifications(lines):

    section = extract_section(
        lines,
        [
            "CERTIFICATIONS",
            "CERTIFICATION"
        ]
    )

    if not section:
        return ""

    result = []

    for line in clean_lines(section):

        cleaned = line.lstrip(
            "•●▪■*- "
        ).strip()

        if cleaned:

            result.append(
                "● " + cleaned
            )

    return "\n".join(result)


# =========================================================
# PROFESSIONAL HIGHLIGHTS
# =========================================================

def extract_highlights(lines):

    achievements = extract_section(
        lines,
        [
            "ACHIEVEMENTS",
            "ACHIEVEMENT",
            "AWARDS"
        ]
    )

    if achievements:

        result = []

        for line in clean_lines(
            achievements
        ):

            cleaned = line.lstrip(
                "•●▪■*- "
            ).strip()

            if cleaned:

                result.append(
                    "● " + cleaned
                )

        return "\n".join(
            result[:8]
        )

    # Fallback:
    # pick useful training statements
    experience = extract_section(
        lines,
        [
            "PROFESSIONAL EXPERIENCE",
            "WORK EXPERIENCE",
            "EXPERIENCE"
        ]
    )

    if not experience:
        return ""

    keywords = [
        "trained",
        "delivered",
        "conducted",
        "mentored",
        "developed",
        "coordinated",
        "placement",
        "workshop",
        "students",
        "recognized",
        "author",
        "improved",
        "facilitated"
    ]

    highlights = []

    for line in clean_lines(experience):

        lower = line.lower()

        if any(
            word in lower
            for word in keywords
        ):

            cleaned = line.lstrip(
                "•●▪■*- "
            ).strip()

            if cleaned:

                highlights.append(
                    cleaned
                )

        if len(highlights) >= 6:
            break

    highlights = unique_list(
        highlights
    )

    return "\n".join(
        "● " + item
        for item in highlights
    )


# =========================================================
# LEETCODE
# =========================================================

def extract_leetcode(text):

    match = re.search(
        r"https?://(?:www\.)?"
        r"leetcode\.com/[^\s|]+",
        text,
        re.IGNORECASE
    )

    if match:

        return match.group(0).rstrip(
            ".,);"
        )

    return ""


# =========================================================
# NUMBER OF PROBLEMS SOLVED
# =========================================================

def extract_problem_count(text):

    patterns = [
        r"(\d+)\s+problems?\s+solved",

        r"problems?\s+solved"
        r"\s*[:\-]?\s*(\d+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

    return ""


# =========================================================
# OTHER CODING PROFILES
# =========================================================

def extract_other_profiles(text):

    urls = re.findall(
        r"https?://[^\s|]+",
        text
    )

    result = []

    for url in urls:

        lower = url.lower()

        if "linkedin.com" in lower:
            continue

        if "leetcode.com" in lower:
            continue

        result.append(
            url.rstrip(
                ".,);"
            )
        )

    return "\n".join(
        unique_list(result)
    )


# =========================================================
# PROFESSIONAL SUMMARY
# =========================================================

def extract_summary(lines):

    return extract_section(
        lines,
        [
            "PROFESSIONAL SUMMARY",
            "EXECUTIVE SUMMARY",
            "PROFILE SUMMARY",
            "SUMMARY",
            "ABOUT ME",
            "CAREER OBJECTIVE",
            "OBJECTIVE"
        ]
    )


# =========================================================
# TRAINING PROJECTS
# =========================================================

def extract_training_projects(
    lines,
    profile_type
):
    """
    Safely attempts to find colleges /
    universities mentioned in training
    experience.

    Location is intentionally left blank
    unless it is clearly available.

    User can edit this later before profile
    generation.
    """

    experience_section = extract_section(
        lines,
        [
            "PROFESSIONAL EXPERIENCE",
            "WORK EXPERIENCE",
            "EXPERIENCE"
        ]
    )

    if not experience_section:
        return []

    experience_lines = clean_lines(
        experience_section
    )

    institution_words = [
        "college",
        "university",
        "institute",
        "academy"
    ]

    projects = []
    seen = set()

    for line in experience_lines:

        lower = line.lower()

        if not any(
            word in lower
            for word in institution_words
        ):
            continue

        cleaned = line.lstrip(
            "•●▪■*- "
        ).strip()

        if len(cleaned) < 5:
            continue

        key = cleaned.lower()

        if key in seen:
            continue

        seen.add(key)

        projects.append(
            {
                "College / Client":
                    cleaned,

                "Location":
                    "",

                "Domain / Subject Area":
                    ""
            }
        )

        if len(projects) >= 30:
            break

    return projects


# =========================================================
# MAIN PARSER
# =========================================================

def parse_resume(
    text,
    profile_type
):
    """
    Main function called by Streamlit.

    profile_type must be:
        Technical Trainer
        Aptitude Trainer
    """

    lines = clean_lines(text)

    summary = extract_summary(
        lines
    )

    certifications = (
        extract_certifications(
            lines
        )
    )

    highlights = (
        extract_highlights(
            lines
        )
    )

    competencies = find_keywords(
        text,
        CORE_COMPETENCIES
    )


    # =====================================================
    # APTITUDE TRAINER
    # =====================================================

    if profile_type == "Aptitude Trainer":

        aptitude_subjects = find_keywords(
            text,
            APTITUDE_SUBJECTS
        )

        additional_technical = (
            find_keywords(
                text,
                TECHNICAL_SUBJECTS
            )
        )

        exams = find_keywords(
            text,
            EXAM_EXPERTISE
        )

        all_skills = unique_list(
            aptitude_subjects
            + additional_technical
        )

        training_expertise = (
            unique_list(
                aptitude_subjects
                + exams
            )
        )

        subjects_handled = (
            aptitude_subjects
        )


    # =====================================================
    # TECHNICAL TRAINER
    # =====================================================

    else:

        technical_subjects = (
            find_keywords(
                text,
                TECHNICAL_SUBJECTS
            )
        )

        all_skills = (
            technical_subjects
        )

        training_expertise = (
            technical_subjects
        )

        subjects_handled = []

        exams = []


    # =====================================================
    # CREATE FINAL DATA DICTIONARY
    # =====================================================

    data = {

        # ---------------------------------------------
        # Basic Information
        # ---------------------------------------------

        "Name":
            extract_name(lines),

        "Emp ID":
            "",

        "Designation":
            profile_type,

        "Qualification":
            extract_qualification(
                lines
            ),

        "Date of Joining":
            "",

        "Experience":
            extract_experience(
                text
            ),

        "Company Mail":
            "",

        "Phone Number":
            extract_phone(
                text
            ),

        "Personal Email":
            extract_email(
                text
            ),

        "LinkedIn":
            extract_linkedin(
                text
            ),

        "Rating":
            "",


        # ---------------------------------------------
        # Main Profile
        # ---------------------------------------------

        "Skills":
            " ■ ".join(
                all_skills
            ),

        "Summary":
            summary,

        "Certifications":
            certifications,

        "Professional Highlights":
            highlights,


        # ---------------------------------------------
        # Aptitude Fields
        # ---------------------------------------------

        "Subjects Handled":
            "\n".join(
                "● " + item
                for item in subjects_handled
            ),

        "Exam Placement Expertise":
            "\n".join(
                "● " + item
                for item in exams
            ),

        "Languages":
            extract_languages(
                lines
            ),


        # ---------------------------------------------
        # Common Training Fields
        # ---------------------------------------------

        "Training Expertise":
            "\n".join(
                "● " + item
                for item in training_expertise
            ),

        "Core Competencies":
            "\n".join(
                "● " + item
                for item in competencies
            ),


        # ---------------------------------------------
        # Technical Trainer Fields
        # ---------------------------------------------

        "LeetCode Profile Link":
            extract_leetcode(
                text
            ),

        "No of Problems Done":
            extract_problem_count(
                text
            ),

        "Other Profiles":
            extract_other_profiles(
                text
            ),


        # ---------------------------------------------
        # Projects / Colleges
        # ---------------------------------------------

        "Training Projects":
            extract_training_projects(
                lines,
                profile_type
            ),


        # ---------------------------------------------
        # Keep raw resume text for checking
        # ---------------------------------------------

        "Raw Text":
            text
    }

    return data