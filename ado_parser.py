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
            "features": [...],
            "orphan_stories": [...]
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

    ###########################################
    # Build Feature Dictionary
    ###########################################

    features = {}

    feature_rows = df[
        df["Work Item Type"].astype(str).str.lower() == "feature"
    ]

    if feature_rows.empty:

        return False, {
            "error": "No Feature work items found."
        }

    for _, row in feature_rows.iterrows():

        ticket_id = normalize_value(row["Ticket ID"])

        features[ticket_id] = {

            "ticket_id": ticket_id,

            "title": normalize_value(row["Title"]),

            "description": normalize_value(row["Description"]),

            "status": normalize_value(row["State"]),

            "stories": []

        }

    ###########################################
    # Attach Stories
    ###########################################

    orphan_stories = []

    story_rows = df[
        df["Work Item Type"].astype(str).str.lower() == "story"
    ]

    if story_rows.empty:

        return False, {
            "error": "No Story work items found."
        }

    for _, row in story_rows.iterrows():

        story = {

            "ticket_id": normalize_value(row["Ticket ID"]),

            "title": normalize_value(row["Title"]),

            "description": normalize_value(row["Description"]),

            "acceptance_criteria": normalize_value(
                row["Acceptance Criteria"]
            ),

            "status": normalize_value(row["State"])

        }

        parent_id = normalize_value(row["Parent"])

        if parent_id in features:

            features[parent_id]["stories"].append(story)

        else:

            orphan_stories.append(story)

    ###########################################
    # Return
    ###########################################

    return True, {

        "features": list(features.values()),

        "orphan_stories": orphan_stories

    }