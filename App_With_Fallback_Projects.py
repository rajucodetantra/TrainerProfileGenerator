"""
App_With_Fallback_Projects.py

Purpose
-------
Run the existing Streamlit project WITHOUT changing any existing .py file.

Behavior
--------
1. Existing trainer projects are used exactly as they are.
2. If a trainer has no saved projects, 5 projects are selected from:
       data/CTProjects.xlsx
3. The fallback projects are stable for each Employee ID.
4. Existing Home.py and pages remain unchanged.

How to run
----------
    streamlit run App_With_Fallback_Projects.py

Required file
-------------
    data/CTProjects.xlsx

Expected CTProjects.xlsx columns
--------------------------------
    S.No
    College / Client
    Location
    Domain / Subject Area
"""

from pathlib import Path
import hashlib
import os
import runpy
import sys

import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
FALLBACK_FILE = DATA_DIR / "CTProjects.xlsx"
HOME_FILE = BASE_DIR / "Home.py"


# ============================================================
# FALLBACK PROJECT HELPERS
# ============================================================

EMPTY_PROJECT_MESSAGES = {
    "",
    "project allocation not yet done",
    "project allocation not yet done.",
    "no projects",
    "no project",
    "no projects found",
    "no project found",
    "n/a",
    "na",
    "none",
}


def _clean_text(value):
    """Convert Excel values safely to clean strings."""
    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass

    return str(value).strip()


def _has_real_project_data(value):
    """
    Detect whether the original project result actually contains project data.
    Works with dicts, lists, tuples, pandas DataFrames, Series and strings.
    """

    if value is None:
        return False

    if isinstance(value, pd.DataFrame):
        if value.empty:
            return False

        cleaned = value.dropna(how="all")
        return not cleaned.empty

    if isinstance(value, pd.Series):
        return not value.dropna().empty

    if isinstance(value, dict):
        if not value:
            return False

        # Project extractor commonly returns:
        # {"ongoing": [...], "completed": [...]}
        project_keys = [
            "ongoing",
            "completed",
            "ongoing_projects",
            "completed_projects",
            "projects",
        ]

        found_project_key = False

        for key in project_keys:
            if key in value:
                found_project_key = True
                if _has_real_project_data(value[key]):
                    return True

        if found_project_key:
            return False

        # Generic dictionary fallback
        return any(_has_real_project_data(v) for v in value.values())

    if isinstance(value, (list, tuple, set)):
        return any(_has_real_project_data(v) for v in value)

    if isinstance(value, str):
        text = value.strip().lower()

        if text in EMPTY_PROJECT_MESSAGES:
            return False

        if "project allocation not yet done" in text:
            return False

        return bool(text)

    return True


def _stable_seed(emp_id):
    """
    Produce a repeatable seed.
    Same Employee ID -> same five fallback projects.
    """
    text = str(emp_id).strip().upper()
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def _load_fallback_pool():
    """Load and validate data/CTProjects.xlsx."""

    if not FALLBACK_FILE.exists():
        return pd.DataFrame()

    try:
        df = pd.read_excel(
            FALLBACK_FILE,
            sheet_name="Projects"
        )
    except ValueError:
        # If the sheet was renamed, use first sheet.
        df = pd.read_excel(FALLBACK_FILE)

    required = [
        "College / Client",
        "Location",
        "Domain / Subject Area",
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            "CTProjects.xlsx is missing required column(s): "
            + ", ".join(missing)
        )

    df = df.copy()

    for col in required:
        df[col] = df[col].apply(_clean_text)

    # Remove blank/incomplete rows
    df = df[
        (df["College / Client"] != "")
        & (df["Location"] != "")
        & (df["Domain / Subject Area"] != "")
    ].copy()

    # Remove exact duplicate project rows
    df = df.drop_duplicates(
        subset=[
            "College / Client",
            "Location",
            "Domain / Subject Area",
        ]
    )

    return df.reset_index(drop=True)


def _five_fallback_rows(emp_id):
    """Return five deterministic fallback project records."""

    df = _load_fallback_pool()

    if df.empty:
        return []

    count = min(5, len(df))

    sample = df.sample(
        n=count,
        random_state=_stable_seed(emp_id)
    ).reset_index(drop=True)

    rows = []

    for index, row in sample.iterrows():
        college = _clean_text(row["College / Client"])
        location = _clean_text(row["Location"])
        subject = _clean_text(row["Domain / Subject Area"])

        # Include both your new Excel column names and the aliases
        # commonly expected by the existing profile generator.
        rows.append(
            {
                "S.No": index + 1,

                "College / Client": college,
                "College": college,

                "Location": location,
                "Place": location,

                "Domain / Subject Area": subject,
                "Subject": subject,

                # Kept blank because CTProjects.xlsx has only 4 fields.
                "From": "",
                "To": "",

                "Status": "Completed",
            }
        )

    return rows


def _fallback_project_dict(emp_id):
    """
    Structure normally used by ProjectExtractor / ProfileGenerator.
    All fallback rows are treated as Completed Projects.
    """
    return {
        "ongoing": [],
        "completed": _five_fallback_rows(emp_id),
    }


def _fallback_markdown(emp_id):
    """
    Final display safety-net.
    Used only if the normal formatter still returns an empty project section.
    """

    rows = _five_fallback_rows(emp_id)

    if not rows:
        return "Project allocation not yet done."

    lines = [
        "#### ✅ Completed Projects",
        "",
        "| S.No | College / Client | Location | Domain / Subject Area |",
        "|---:|---|---|---|",
    ]

    for row in rows:
        college = row["College / Client"].replace("|", "/")
        location = row["Location"].replace("|", "/")
        subject = row["Domain / Subject Area"].replace("|", "/")

        lines.append(
            f"| {row['S.No']} | {college} | {location} | {subject} |"
        )

    return "\n".join(lines)


# ============================================================
# PATCH 1:
# PROJECT EXTRACTOR
#
# Existing trainers -> untouched.
# Empty trainer projects -> 5 fallback projects.
# ============================================================

def _patch_project_extractor():

    try:
        from modules.project_extractor import ProjectExtractor
    except Exception as exc:
        print(
            "[Fallback Projects] Could not import ProjectExtractor:",
            exc
        )
        return

    # Avoid wrapping the method again during Streamlit reruns.
    if getattr(
        ProjectExtractor,
        "_ct_fallback_patch_applied",
        False
    ):
        return

    original_method = ProjectExtractor.get_trainer_projects

    def patched_get_trainer_projects(self, emp_id, *args, **kwargs):

        original_projects = original_method(
            self,
            emp_id,
            *args,
            **kwargs
        )

        # If actual projects exist, DO NOT touch them.
        if _has_real_project_data(original_projects):
            return original_projects

        fallback = _fallback_project_dict(emp_id)

        # If CTProjects.xlsx is unavailable/empty,
        # preserve original behavior.
        if not fallback["completed"]:
            return original_projects

        return fallback

    ProjectExtractor.get_trainer_projects = patched_get_trainer_projects
    ProjectExtractor._ct_fallback_patch_applied = True


# ============================================================
# PATCH 2:
# PROFILE SERVICE SAFETY NET
#
# If the existing formatter still produces:
# "Project allocation not yet done."
# replace only the final displayed Training Projects section.
# ============================================================

def _patch_profile_service():

    try:
        from services.profile_service import ProfileService
    except Exception:
        # Some versions of the project may keep ProfileService elsewhere.
        # Patch 1 is normally sufficient, so silently continue.
        return

    if getattr(
        ProfileService,
        "_ct_fallback_patch_applied",
        False
    ):
        return

    original_prepare = ProfileService.prepare_trainer

    def patched_prepare_trainer(self, trainer, *args, **kwargs):

        prepared = original_prepare(
            self,
            trainer,
            *args,
            **kwargs
        )

        if not isinstance(prepared, dict):
            return prepared

        project_text = prepared.get("Training Projects", "")

        if _has_real_project_data(project_text):
            return prepared

        emp_id = prepared.get(
            "Emp ID",
            trainer.get("Emp ID", "")
            if isinstance(trainer, dict)
            else ""
        )

        markdown = _fallback_markdown(emp_id)

        if "project allocation not yet done" not in markdown.lower():
            prepared["Training Projects"] = markdown

        return prepared

    ProfileService.prepare_trainer = patched_prepare_trainer
    ProfileService._ct_fallback_patch_applied = True


# ============================================================
# APPLY PATCHES BEFORE EXISTING APP IS EXECUTED
# ============================================================

def _apply_fallback_system():

    if not FALLBACK_FILE.exists():
        print(
            "\n[Fallback Projects] WARNING:\n"
            f"File not found: {FALLBACK_FILE}\n"
            "Add CTProjects.xlsx inside the data folder.\n"
        )

    _patch_project_extractor()
    _patch_profile_service()


# ============================================================
# RUN EXISTING HOME.PY
# ============================================================

def _run_existing_app():

    if not HOME_FILE.exists():
        raise FileNotFoundError(
            f"Existing Home.py was not found at:\n{HOME_FILE}"
        )

    # Keep imports and relative file paths behaving exactly
    # as they do when Home.py is run normally.
    os.chdir(BASE_DIR)

    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))

    # Execute the existing Home.py after fallback patching.
    runpy.run_path(
        str(HOME_FILE),
        run_name="__main__"
    )


_apply_fallback_system()
_run_existing_app()
