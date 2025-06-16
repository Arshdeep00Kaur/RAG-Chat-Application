import streamlit as st
from pathlib import Path
from chat import chat_with_pdf
from indexing import run_indexing
import sys
import tempfile

st.markdown("""
    <style>
    .stApp {
        background-color: #fdf5e6; /* Light beige */
    }
    </style>
""", unsafe_allow_html=True)

st.title("GenieDocs")
uploaded_pdf=st.file_uploader("Upload your pdf here...",type="pdf")


if uploaded_pdf is not None:
    st.success("pdf uploaded")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_pdf.read())
        pdf_path = tmp_file.name

    if st.button("📚 Prepare this PDF"):
        with st.spinner("Indexing PDF..."):
            run_indexing(pdf_path)
        st.success("✅ PDF processed and indexed!")

    query = st.text_input("🔎 Ask a question about the PDF")

    if query:
        with st.spinner("Generating answer..."):
            response = chat_with_pdf(query)
        st.markdown("### 🤖 Answer")
        st.write(response)

    
  