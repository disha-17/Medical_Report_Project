
import streamlit as st
import fitz
import re

st.set_page_config(
    page_title="Medical Report Simplifier",
    page_icon="📄"
)

st.title("Medical Report Simplifier")
st.write("Upload a medical report PDF to understand its terms.")

def simplify_report(text):
    explanations = {
        "hemoglobin":
            "Hemoglobin is a protein in red blood cells that carries oxygen.",
        "platelet count":
            "Platelets help blood clot and stop bleeding.",
        "white blood cell count":
            "White blood cells help the body fight infections.",
        "reference range":
            "A reference range shows values commonly expected by the laboratory."
    }

    results = []

    for term, explanation in explanations.items():
        if term in text.lower():
            results.append(
                "**" + term.title() + ":** " + explanation
            )

    if not results:
        results.append("No known medical terms were found.")

    return results


def check_numbers(original, simplified):
    original_numbers = re.findall(
        r"\b\d+(?:\.\d+)?\b", original
    )
    simplified_numbers = re.findall(
        r"\b\d+(?:\.\d+)?\b", simplified
    )

    return [
        number for number in simplified_numbers
        if number not in original_numbers
    ]


uploaded_file = st.file_uploader(
    "Choose a medical report PDF",
    type=["pdf"]
)

if uploaded_file is not None:
    if st.button("Simplify Medical Report"):
        try:
            with fitz.open(
                stream=uploaded_file.getvalue(),
                filetype="pdf"
            ) as pdf:
                original_text = "\n".join(
                    page.get_text() for page in pdf
                )

            if not original_text.strip():
                st.warning(
                    "No selectable text found. "
                    "This PDF may be scanned."
                )
            else:
                explanations = simplify_report(original_text)
                simplified_text = "\n".join(
                    item.replace("**", "")
                    for item in explanations
                )

                st.subheader("Simplified Explanation")
                for item in explanations:
                    st.markdown(item)

                st.subheader("Basic Number Check")
                warnings = check_numbers(
                    original_text, simplified_text
                )

                if warnings:
                    st.warning(
                        "Numbers not found in original report: "
                        + ", ".join(warnings)
                    )
                else:
                    st.success(
                        "No unsupported numbers detected."
                    )

                with st.expander("View Original Report Text"):
                    st.text(original_text)

                st.caption(
                    "Educational prototype only. "
                    "This tool does not diagnose medical conditions "
                    "or guarantee that explanations are correct."
                )

        except Exception as error:
            st.error("Could not read this PDF: " + str(error))
