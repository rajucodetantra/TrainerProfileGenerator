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
        "group discussions",
        "gd practice"
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
        "campus placements"
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
# DATE RANGE PATTERN FOR EXPERIENCE
# =========================================================

MONTH_PATTERN = (
    r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|"
    r"Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
    r"Aug(?:ust)?|Sep(?:tember)?|Sept|Oct(?:ober)?|"
    r"Nov(?:ember)?|Dec(?:ember)?)"
)

YEAR_PATTERN = r"(?:['’]?\d{2}|(?:19|20)\d{2})"

DATE_RANGE_PATTERN = re.compile(
    rf"(?:{MONTH_PATTERN}\s*)?"
    rf"{YEAR_PATTERN}"
    rf"\s*(?:-|–|—|to|at)\s*"
    rf"(?:"
    rf"(?:{MONTH_PATTERN}\s*)?"
    rf"{YEAR_PATTERN}"
    rf"|Present|Current|Now)",
    re.IGNORECASE
)


# =========================================================
# BASIC HELPERS
# =========================================================

def clean_lines(text):

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

    result = []
    seen = set()

    for item in items:

        item = str(item).strip()

        if not item:
            continue

        key = item.lower()

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

    return value in SECTION_HEADINGS


# =========================================================
# SECTION EXTRACTION
# =========================================================

def extract_section(lines, headings):

    if isinstance(headings, str):
        headings = [headings]

    headings = [
        heading.upper()
        for heading in headings
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

    for line in lines[:15]:

        candidate = line.strip()
        lower = candidate.lower()

        if not candidate:
            continue

        if "@" in candidate:
            continue

        if "http" in lower:
            continue

        if "trainer" in lower:
            continue

        if lower in [
            "resume",
            "curriculum vitae",
            "cv",
            "profile"
        ]:
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

            return re.sub(
                r"\s+",
                " ",
                match.group(0)
            ).strip()

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
# ORGANIZATION DETECTION
# =========================================================

def looks_like_organization(line):

    lower = line.lower()

    organization_words = [
        "college",
        "university",
        "institute",
        "academy",
        "school",
        "centre",
        "center",
        "pvt",
        "private limited",
        "solutions",
        "technologies",
        "technology",
        "bank",
        "finance",
        "consulting",
        "staffing",
        "spiders",
        "qspiders",
        "freelance",
        "company",
        "corporation",
        "services",
        "limited",
        "ltd"
    ]

    return any(
        word in lower
        for word in organization_words
    )


# =========================================================
# EXPERIENCE TABLE EXTRACTION
# =========================================================

def extract_experience_details(lines):
    """
    Extract organization and employment period.

    Output format:

    [
        {
            "Name of Organization": "...",
            "Years Worked": "2023 - 2024"
        }
    ]

    If organization cannot be identified safely,
    that row is ignored.
    """

    experience_text = extract_section(
        lines,
        [
            "PROFESSIONAL EXPERIENCE",
            "WORK EXPERIENCE",
            "EXPERIENCE",
            "EMPLOYMENT HISTORY"
        ]
    )

    if not experience_text:
        return []

    exp_lines = clean_lines(
        experience_text
    )

    results = []
    seen = set()

    for index, line in enumerate(
        exp_lines
    ):

        date_match = DATE_RANGE_PATTERN.search(
            line
        )

        if not date_match:
            continue

        date_range = (
            date_match.group(0)
            .strip()
        )

        organization = ""

        # -------------------------------------------------
        # Check same line after removing date range
        # -------------------------------------------------

        without_date = (
            line[:date_match.start()]
            + " "
            + line[date_match.end():]
        )

        without_date = (
            without_date
            .strip(" |-–—")
            .strip()
        )

        if looks_like_organization(
            without_date
        ):

            # If role | organization format exists,
            # prefer likely organization part.
            parts = re.split(
                r"\||\s+-\s+",
                without_date
            )

            for part in reversed(parts):

                part = part.strip()

                if looks_like_organization(
                    part
                ):

                    organization = part
                    break

            if not organization:
                organization = without_date

        # -------------------------------------------------
        # Search previous lines
        # -------------------------------------------------

        if not organization:

            start = max(
                0,
                index - 3
            )

            for previous_index in range(
                index - 1,
                start - 1,
                -1
            ):

                previous_line = (
                    exp_lines[
                        previous_index
                    ]
                )

                if looks_like_organization(
                    previous_line
                ):

                    organization = (
                        previous_line
                        .strip("•●▪■*- ")
                        .strip()
                    )

                    break

        # -------------------------------------------------
        # Search next lines
        # -------------------------------------------------

        if not organization:

            end = min(
                len(exp_lines),
                index + 3
            )

            for next_index in range(
                index + 1,
                end
            ):

                next_line = (
                    exp_lines[
                        next_index
                    ]
                )

                if looks_like_organization(
                    next_line
                ):

                    organization = (
                        next_line
                        .strip("•●▪■*- ")
                        .strip()
                    )

                    break

        if not organization:
            continue

        organization = re.sub(
            r"\s+",
            " ",
            organization
        ).strip()

        key = (
            organization.lower(),
            date_range.lower()
        )

        if key in seen:
            continue

        seen.add(key)

        results.append(
            {
                "Name of Organization":
                    organization,

                "Years Worked":
                    date_range
            }
        )

    return results


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

            if DEGREE_PATTERN.search(
                line
            ):

                return line.strip()

    for line in lines:

        if DEGREE_PATTERN.search(
            line
        ):

            if len(line) <= 140:
                return line.strip()

    return ""


# =========================================================
# KEYWORDS
# =========================================================

def contains_keyword(
    text,
    keyword
):

    text_lower = text.lower()

    keyword_lower = (
        keyword.lower()
    )

    if len(keyword) <= 4:

        return bool(
            re.search(
                r"\b"
                + re.escape(
                    keyword_lower
                )
                + r"\b",
                text_lower
            )
        )

    return keyword_lower in text_lower


def find_keywords(
    text,
    mapping
):

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

    return unique_list(
        found
    )


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

        return section.replace(
            "|",
            ", "
        ).strip()

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

            found.append(
                language
            )

    return ", ".join(
        found
    )


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

    for line in clean_lines(
        section
    ):

        cleaned = line.lstrip(
            "•●▪■*- "
        ).strip()

        if cleaned:

            result.append(
                "● " + cleaned
            )

    return "\n".join(
        result
    )


# =========================================================
# PROFESSIONAL SUMMARY AS BULLET POINTS
# =========================================================

def extract_summary(lines):
    """
    Extract Professional Summary and convert
    every point into a bullet.

    The generated Word profile will therefore
    contain bullet points instead of one large
    paragraph.
    """

    section = extract_section(
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

    if not section:
        return ""

    source_lines = clean_lines(
        section
    )

    # -----------------------------------------------------
    # If resume already has bullet points,
    # preserve those points.
    # -----------------------------------------------------

    existing_bullets = []

    for line in source_lines:

        if line.startswith(
            (
                "•",
                "●",
                "▪",
                "■",
                "-",
                "*"
            )
        ):

            cleaned = line.lstrip(
                "•●▪■*- "
            ).strip()

            if cleaned:

                existing_bullets.append(
                    cleaned
                )

    if existing_bullets:

        return "\n".join(
            "● " + point
            for point in existing_bullets
        )

    # -----------------------------------------------------
    # Otherwise join wrapped lines and split into
    # meaningful sentences.
    # -----------------------------------------------------

    full_summary = " ".join(
        source_lines
    )

    sentences = re.split(
        r"(?<=[.!?])\s+"
        r"(?=[A-Z])",
        full_summary
    )

    points = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        if len(sentence) < 10:
            continue

        points.append(
            sentence
        )

    # -----------------------------------------------------
    # If sentence splitting fails, use clean lines.
    # -----------------------------------------------------

    if len(points) <= 1:

        points = []

        for line in source_lines:

            cleaned = line.lstrip(
                "•●▪■*- "
            ).strip()

            if cleaned:

                points.append(
                    cleaned
                )

    points = unique_list(
        points
    )

    return "\n".join(
        "● " + point
        for point in points
    )


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

    for line in clean_lines(
        experience
    ):

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
        "● " + point
        for point in highlights
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
# PROBLEMS SOLVED
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
        unique_list(
            result
        )
    )


# =========================================================
# TRAINING PROJECTS
# =========================================================

def extract_training_projects(
    lines,
    profile_type
):

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

    lines = clean_lines(
        text
    )

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

    experience_details = (
        extract_experience_details(
            lines
        )
    )


    # =====================================================
    # APTITUDE TRAINER
    # =====================================================

    if profile_type == "Aptitude Trainer":

        aptitude_subjects = (
            find_keywords(
                text,
                APTITUDE_SUBJECTS
            )
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
    # CORE SKILLS
    #
    # IMPORTANT:
    # Add square bullet BEFORE THE FIRST SKILL ALSO.
    # =====================================================

    if all_skills:

        formatted_skills = (
            "■ "
            + " ■ ".join(
                all_skills
            )
        )

    else:

        formatted_skills = ""


    # =====================================================
    # FINAL DATA
    # =====================================================

    data = {

        "Name":
            extract_name(
                lines
            ),

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


        # =================================================
        # CORE SKILLS
        # =================================================

        "Skills":
            formatted_skills,


        # =================================================
        # SUMMARY - NOW BULLET POINTS
        # =================================================

        "Summary":
            summary,


        "Certifications":
            certifications,

        "Professional Highlights":
            highlights,


        # =================================================
        # EXPERIENCE TABLE DATA
        # =================================================

        "Experience Details":
            experience_details,


        # =================================================
        # APTITUDE FIELDS
        # =================================================

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


        # =================================================
        # TRAINING
        # =================================================

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


        # =================================================
        # TECHNICAL FIELDS
        # =================================================

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


        # =================================================
        # TRAINING PROJECTS
        # =================================================

        "Training Projects":
            extract_training_projects(
                lines,
                profile_type
            ),


        # =================================================
        # RAW PDF TEXT
        # =================================================

        "Raw Text":
            text
    }

    return data