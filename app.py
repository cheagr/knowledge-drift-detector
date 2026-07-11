import streamlit as st

from confluence_parser import parse_confluence
from ado_parser import parse_ado
from gemini_client import compare_documents
from feature_resolver import resolve_feature
# from artifact_validator import validate_artifacts
from artifact_validator import (validate_uploads, validate_selected_feature)

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

    st.divider()

    ########################################
    # Validate the uploaded artifacts
    #######################################

    success, validation = validate_uploads(
        confluence,
        ado
    )

    if validation["errors"]:
        st.error("Artifact validation failed.")

        for error in validation["errors"]:
            st.error(error)

        st.stop()

    if validation["warnings"]:

        with st.expander("Artifact Validation Warnings"):

            for warning in validation["warnings"]:
                st.warning(warning)

    ##########################################
    # Resolve Feature to find match against the confluence
    ##########################################

    success, match = resolve_feature(
        confluence,
        ado
    )

    if not success:

        st.error("Unable to match feature.")
        st.stop()

    st.success("Both Artifacts parsed successfully. ADO hierarchy built")

    st.divider()

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
            f"""
            Multiple potential ADO Features matching the Confluence were found.
            The best automatic match had **{match['confidence']} confidence**
            (score: {match['score']}).

            Please select the correct feature before continuing.
            """
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
            options,
            index=None
        )

        if selected is None:
            st.stop()

        feature = lookup[selected]

    ##################################################
    # Validate stories under the selected feature
    ##################################################

    success, validation = validate_selected_feature(feature)

    if validation["errors"]:

        st.error("Selected Feature's validation failed.")

        for error in validation["errors"]:
            st.error(error)

        st.stop()

    if validation["warnings"]:

        with st.expander("Selected Feature Validation Warnings"):

            for warning in validation["warnings"]:
                st.warning(warning)
        
    ##########################################
    # Call LLM with confluence and selected feature 
    # Display AI report
    ##########################################

    with st.spinner("Generating AI comparision report"):
        success, drifts = compare_documents(confluence,feature)

    if success:
        st.subheader("AI Compare ")
        # st.json(drifts)
        # st.subheader("Executive Summary")
        # st.write(drift["executive_summary"])
            
        st.subheader("⚠ Knowledge Drifts")
        for drift in drifts["knowledge_drifts"]:
        
            st.write(f"### {drift['area']}")
    
            severity = drift["severity"]
            if severity == "High":
                st.write(f"### Severity :red[{drift['severity']}]")
            elif severity == "Medium":
                st.write(f"### Severity :orange[{drift['severity']}]")
            else:
                st.write(f"### Severity :yellow[{drift['severity']}]")

            st.write(f" • {drift['confluence']}")
            st.write(f" • {drift['ado']}")
            st.write("### Impact")
            st.write(drift['impact'])

            st.write("#### Evidence")
            st.write(f"**Confluence:** {drift['evidence']['confluence']}")
            st.write(f"**ADO:** {drift['evidence']['ado']}")
            
            st.divider()

        st.subheader("✅ Suggested reviews for PM")
        # manual_review = drift.get("manual_review", "Not Available")
        for review in drifts.get("manual_review", []):
            st.write(f"• {review}")

        quality = drifts.get("analysis_quality", "Unknown")

        st.subheader("📊 Analysis Quality")

        st.metric(
            "Confidence",
            quality["confidence"]
        )

        st.caption(quality["reason"])
    else:
        st.error(f"Failed to generate AI summary. Error: {drifts['error']}")
    

    ##########################################
    # Display Processed data
    ##########################################
    st.subheader("Raw data")
    with st.expander("Structured json output from llm"):
        st.json(drifts)

    with st.expander("Parsed artifacts data"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Confluence")
            st.write("### Feature")
            st.write(confluence["title"])
            st.write(f"Sections: {len(confluence['sections'])}")
            st.json(confluence)
        with col2:
            st.subheader("Selected ADO Feature")
            st.write(feature["title"])
            st.write(f"Stories: {len(feature['stories'])}")
            st.write("##ADO all raw data")
            st.json(ado)


