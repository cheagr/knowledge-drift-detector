

"""
Prompt Builder

"""


def build_compare_prompt(confluence, ado) -> str:
    """
    Builds the prompt sent to Gemini.

    Parameters
    ----------
    feature_report : dict
        Structured output generated from the business rule engine.

    Returns
    -------
    str
        Prompt ready for Gemini.
    """

    prompt = f"""
        You are an experienced Technical Product Manager working on enterprise banking systems.

        You are comparing:

        1. Confluence functional specification.
        2. Azure DevOps implementation details.

        Identify knowledge drift.

        Rules

        • Only compare supplied information.
        • Do not invent missing functionality.
        • Do not assume implementation.
        • Ignore wording differences that preserve identical meaning.
        • Focus on behavioural differences.
        • Highlight missing validations.
        • Highlight missing acceptance criteria.
        • Highlight missing implementation details.
        • Highlight documentation that appears outdated.

        Confluence:
        {confluence}

        Azure DevOps:
        {ado}
    """
    # print(f"Prompt from builder: {prompt}")
    return prompt.strip()