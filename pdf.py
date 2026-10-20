
import streamlit as st
from pypdf import PdfReader
import io

# Page configuration
st.set_page_config(
    page_title="PDF Text Extractor",
    page_icon="📄",
    layout="wide"
)

# App title
st.title("📄 PDF Text Extractor")
st.write("Upload a PDF file to extract and display its text.")

# Upload PDF
uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:
    try:
        # Read the uploaded PDF
        pdf_bytes = io.BytesIO(uploaded_file.getvalue())
        pdf_reader = PdfReader(pdf_bytes)

        st.success("PDF uploaded successfully!")

        st.write(f"**Total pages:** {len(pdf_reader.pages)}")

        # Extract text from all pages
        extracted_text = ""

        for page_number, page in enumerate(pdf_reader.pages, start=1):
            page_text = page.extract_text() or ""

            extracted_text += (
                f"\n--- Page {page_number} ---\n"
                f"{page_text}\n"
            )

        # Display extracted text
        st.subheader("Extracted PDF Text")

        if extracted_text.strip():
            st.text_area(
                "PDF Content",
                value=extracted_text,
                height=450
            )

            # Download extracted text
            st.download_button(
                label="📥 Download Text File",
                data=extracted_text,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
        else:
            st.warning(
                "No selectable text found. "
                "This PDF may contain scanned images. "
                "OCR is required to extract text from images."
            )

    except Exception as e:
        st.error(f"Could not read the PDF: {e}")
