import streamlit as st

from confluence_parser import parse_confluence
from ado_parser import parse_ado
from gemini_client import compare_documents
from feature_resolver import resolve_feature

st.set_page_config(
    page_title="Knowledge Drift Detector",
    layout="wide"
)

st.title("Knowledge Drift Detector")

st.write(
    "Upload a Confluence HTML export and an Azure DevOps Excel export "
    "for the same feature."
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    confluence_file = st.file_uploader(
        "Upload Confluence HTML",
        type=["html"]
    )

with col2:

    ado_file = st.file_uploader(
        "Upload ADO Excel",
        type=["xlsx"]
    )

if confluence_file and ado_file:

    success, confluence = parse_confluence(confluence_file)

    if not success:

        st.error(confluence["error"])
        st.stop()

    ##########################################
    # Parse ADO
    ##########################################

    success, ado = parse_ado(ado_file)

    if not success:

        st.error(ado["error"])
        st.stop()

    ##########################################
    # Validation Passed
    ##########################################

    st.success("Both artifacts parsed successfully.")

    st.divider()
    # with st.spinner("Generating AI comparision report"):
    #     success, drift = compare_documents(confluence,ado)

    # if success:
    #     st.subheader("AI Compare ")
    #     st.subheader("Executive Summary:")
    #     st.write(drift["executive_summary"])
            
    #     st.subheader("⚠ Knowledge Drifts")
    #     for knowledge_drift in drift["knowledge_drifts"]:
    #         # st.write(f"• {knowledge_drift{}}")
    #         st.write(f"**Area** -> {knowledge_drift['area']}")
    #         st.write(f"• {knowledge_drift['confluence']}")
    #         st.write(f"• {knowledge_drift['ado']}")
    #         st.write(f"**Impact** -> {knowledge_drift['impact']}")
            
    #         st.divider()

    #     st.subheader("✅ Suggested reviews for PM")
    #     for review in drift["manual_review"]:
    #         st.write(f"• {review}")

    #     quality = drift["analysis_quality"]

    #     st.subheader("📊 Analysis Quality")

    #     st.metric(
    #         "Confidence",
    #         quality["confidence"]
    #     )

    #     st.caption(quality["reason"])
    # else:
    #     st.error(f"Failed to generate AI summary. Error: {drift['error']}")
    
    # st.subheader("Raw data")
    # with st.expander("Structured json output from llm"):
    #     st.json(drift)


    ##########################################
    # Resolve Feature
    ##########################################

    success, match = resolve_feature(
        confluence,
        ado
    )

    if not success:

        st.error("Unable to match feature.")
        st.stop()

    st.success("Artifacts parsed successfully.")

    st.divider()

    col1, col2 = st.columns(2)

    ##########################################
    # Selecting ADO Feature based on match confidence
    ##########################################

    feature = None

    if match["confidence"] == "High":

        feature = match["selected_feature"]

        st.success(
            f"Automatically matched feature "
            f"(Confidence: {match['confidence']})"
        )

    else:

        st.warning(
            "Unable to confidently identify the correct feature."
        )

        options = []

        lookup = {}

        for candidate in match["candidate_features"]:

            title = (
                f"{candidate['feature']['title']} "
                f"(Score: {candidate['score']})"
            )

            options.append(title)

            lookup[title] = candidate["feature"]

        selected = st.radio(
            "Select the correct ADO Feature",
            options
        )

        feature = lookup[selected]
    
    ##########################################
    # Display Confluence and Matched ADO
    ##########################################

    with col1:

        st.subheader("Confluence")

        st.write("### Feature")

        st.write(confluence["title"])

        st.write(f"Sections: {len(confluence['sections'])}")

    with col2:
        st.subheader("Selected ADO Feature")

        st.write(feature["title"])

        st.write(f"Stories: {len(feature['stories'])}")


