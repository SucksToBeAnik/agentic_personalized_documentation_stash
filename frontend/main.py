import streamlit as st
import requests
import time

st.set_page_config(page_title="Agentic Personalized Documentation Stash", page_icon="📄")
st.title("Agentic Personalized Documentation Stash")

# Sidebar with a form to add a new document
with st.sidebar:
    st.title("Add a new documetation to the stash")

    # Form for submitting new document
    with st.form("document_form"):
        st.write("Submit a new document")
        document_text = st.text_area("Document content")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if document_text:
                # Sending POST request with the document text
                response = requests.post("http://localhost:8000/documents/", json={"doc": document_text})
                if response.status_code == 201:
                    st.success("Document submitted successfully!")
                else:
                    st.error("Failed to submit the document.")

# Main content area where documents will be shown
with st.container():
    st.title("Documents")

    # Show loading spinner while fetching documents
    with st.spinner("Loading documents..."):
        response = requests.get("http://localhost:8000/documents/")

    if response.status_code == 200:
        documents = response.json()
        for document in documents:
            # Display each document in a card-like layout
            with st.expander(document["title"], expanded=False):
                st.markdown(f"**Summary:** {document['summary']}")
                st.markdown(f"**Tags:** {', '.join(document['tags'])}")
                st.markdown(f"**Category:** {document['category']}")
                st.text_area("Document content", document["document"], height=200, disabled=True)
    else:
        print(response)
        st.error("Failed to load documents.")
