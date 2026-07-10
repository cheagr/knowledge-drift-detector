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

    st.divider()

    ##########################################
    # Parse Confluence
    ##########################################

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

