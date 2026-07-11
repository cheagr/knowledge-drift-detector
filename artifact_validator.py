def validate_uploads(confluence, ado):
    """
    Validate uploaded artifacts before feature resolution.

    For Confluence:
    1. Should have a title that is to be matched with feature in ADO extract
    2. Should have at least 3 sections that explains/defines the specs

    For ADO:
    1. There should be at least one FEATURE available
    2. There be a feature available to select/match against the confluence
    3. The selected feature should have at least 1 story
    4. Each story under selected feature should have a Title, Desc and Acceptance Criteria

    """

    errors = []
    warnings = []

    ##################################################
    # Confluence
    ##################################################
    if not confluence.get("title"):
        errors.append("Confluence feature title not found.")

    if not confluence.get("sections"):
        errors.append("No sections found in Confluence page.")

    elif len(confluence["sections"]) < 3:
        warnings.append(
            "Confluence contains very few sections."
        )

    ##################################################
    # ADO
    ##################################################

    if not ado.get("features"):
        errors.append("No Features found in ADO extract.")

    elif len(ado["features"]) > 1:
        warnings.append(
            f"{len(ado['features'])} Features detected in ADO extract."
        )

    if ado["orphan_stories"]:
        warnings.append(
            f"{len(ado['orphan_stories'])} orphan Stories detected."
        )

    ##################################################

    return True, {

        "errors": errors,

        "warnings": warnings

    }


def validate_selected_feature(feature):
    """
    Validate only the feature selected for comparison.
    """

    errors = []
    warnings = []

    ##################################################
    # Feature
    ##################################################

    if feature is None:

        errors.append("No ADO Feature selected.")

        return True, {

            "errors": errors,

            "warnings": warnings

        }

    ##################################################
    # Stories
    ##################################################

    if len(feature["stories"]) == 0:

        errors.append(
            "Selected Feature contains no Stories."
        )

    elif len(feature["stories"]) == 1:

        warnings.append(
            "Selected Feature contains only one Story."
        )

    titles = set()

    for story in feature["stories"]:
        if not story["title"]:

            errors.append(
                f"Story {story['ticket_id']} has no title."
            )

        if not story["description"]:

            warnings.append(
                f"Story {story['ticket_id']} has no description."
            )

        if not story["acceptance_criteria"]:

            warnings.append(
                f"Story {story['ticket_id']} has no Acceptance Criteria."
            )

        if story["title"] in titles:

            warnings.append(
                f"Duplicate Story title: {story['title']}"
            )

        titles.add(story["title"])

    ##################################################

    return True, {

        "errors": errors,

        "warnings": warnings

    }