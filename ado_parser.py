import pandas as pd


REQUIRED_COLUMNS = [
    "Ticket ID",
    "Work Item Type",
    "Title",
    "Description",
    "Acceptance Criteria",
    "Parent",
    "State"
]


def normalize_value(value):
    """
    Convert NaN to empty string and strip whitespace.
    """

    if pd.isna(value):
        return ""

    return str(value).strip()


def parse_ado(uploaded_file):
    """
    Parses an Azure DevOps Excel export.

    Returns

    Success:
        (
            True,
            {
                "feature_title": "...",
                "stories": [...]
            }
        )

    Failure:
        (
            False,
            {
                "error": "..."
            }
        )
    """

    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

    except Exception as ex:

        return False, {
            "error": f"Unable to read ADO Excel.\n\n{str(ex)}"
        }

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]

    if missing:

        return False, {
            "error": f"Missing required columns in ADO extract:\n\n{', '.join(missing)}"
        }

    df = df.fillna("")

    stories = []

    feature_title = ""

    # Find Feature

    feature_rows = df[
        df["Work Item Type"].astype(str).str.lower() == "feature"
    ]

    if len(feature_rows) == 0:

        return False, {
            "error": "No Feature ticket found."
        }

    feature_title = normalize_value(
        feature_rows.iloc[0]["Title"]
    )

    # Parse Stories

    story_rows = df[
        df["Work Item Type"].astype(str).str.lower() == "story"
    ]

    if len(story_rows) == 0:

        return False, {
            "error": "No Story tickets found."
        }

    for _, row in story_rows.iterrows():

        stories.append(

            {
                "ticket_id": normalize_value(row["Ticket ID"]),
                "title": normalize_value(row["Title"]),
                "description": normalize_value(row["Description"]),
                "acceptance_criteria": normalize_value(
                    row["Acceptance Criteria"]
                ),
                "status": normalize_value(row["State"])
            }

        )

    return True, {

        "feature_title": feature_title,

        "stories": stories

    }