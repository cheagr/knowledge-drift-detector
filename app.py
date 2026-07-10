import streamlit as st

from confluence_parser import parse_confluence
from ado_parser import parse_ado
from gemini_client import compare_documents

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
    with st.spinner("Generating AI comparision report"):
        success, drift = compare_documents(confluence,ado)

    if success:
        st.subheader("AI Compare ")
        st.subheader("Executive Summary:")
        st.write(drift["executive_summary"])
            
        st.subheader("⚠ Knowledge Drifts")
        for knowledge_drift in drift["knowledge_drifts"]:
            # st.write(f"• {knowledge_drift{}}")
            st.write(f"**Area** -> {knowledge_drift['area']}")
            st.write(f"• {knowledge_drift['confluence']}")
            st.write(f"• {knowledge_drift['ado']}")
            st.write(f"**Impact** -> {knowledge_drift['impact']}")
            
            st.divider()

        st.subheader("✅ Suggested reviews for PM")
        for review in drift["manual_review"]:
            st.write(f"• {review}")

        quality = drift["analysis_quality"]

        st.subheader("📊 Analysis Quality")

        st.metric(
            "Confidence",
            quality["confidence"]
        )

        st.caption(quality["reason"])
    else:
        st.error(f"Failed to generate AI summary. Error: {drift['error']}")
    
    st.subheader("Raw data")
    with st.expander("Structured json output from llm"):
        st.json(drift)
    with st.expander("Confluence and ADO parsed data"):
        ##########################################
        # Parse Confluence
        ##########################################

        col1, col2 = st.columns(2)

        ##########################################
        # Confluence Preview
        ##########################################

        with col1:

            st.subheader("Confluence")

            st.write("### Feature")

            st.write(confluence["title"])

            st.write("### Sections")

            st.write(len(confluence["sections"]))

            st.json(confluence)

        ##########################################
        # ADO Preview
        ##########################################

        with col2:

            st.subheader("ADO")

            st.write("### Feature")

            st.write(ado["feature_title"])

            st.write("### Stories")

            st.write(len(ado["stories"]))

            st.json(ado)


