import re
from difflib import SequenceMatcher


def tokenize(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9 ]", " ", text)

    return text.split()


def extract_phase(text):

    match = re.search(r"phase\s*(\d+)", text.lower())

    if match:
        return match.group(1)

    return None


def fuzzy_similarity(a, b):

    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


def calculate_score(confluence_title, ado_title):

    score = 0

    #######################################
    # Exact match
    #######################################

    if confluence_title.lower().strip() == ado_title.lower().strip():

        return 100

    #######################################
    # Fuzzy similarity
    #######################################

    similarity = fuzzy_similarity(
        confluence_title,
        ado_title
    )

    score += similarity * 40

    #######################################
    # Keyword overlap
    #######################################

    c_words = set(tokenize(confluence_title))

    a_words = set(tokenize(ado_title))

    common = c_words.intersection(a_words)

    score += len(common) * 10

    #######################################
    # Phase match
    #######################################

    c_phase = extract_phase(confluence_title)

    a_phase = extract_phase(ado_title)

    if c_phase and a_phase:

        if c_phase == a_phase:

            score += 30

    return min(round(score), 100)


def confidence(score):

    if score >= 90:
        return "High"

    if score >= 70:
        return "Medium"

    return "Low"


def resolve_feature(confluence, ado):

    candidates = []

    title = confluence["title"]

    for feature in ado["features"]:

        score = calculate_score(
            title,
            feature["title"]
        )

        candidates.append({

            "feature": feature,

            "score": score

        })

    candidates.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    best = candidates[0]

    return True, {

        "selected_feature": best["feature"],

        "score": best["score"],

        "confidence": confidence(best["score"]),

        "candidate_features": candidates

    }