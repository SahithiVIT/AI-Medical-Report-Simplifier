import streamlit as st
import fitz
import pytesseract
import requests
import pandas as pd
import json
import re
import tempfile

from PIL import Image
from google import genai


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Medical Report Simplifier",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Medical Report Simplifier")

st.write(
    "Upload your medical report and get a simple, "
    "easy-to-understand explanation."
)

st.warning(
    "⚠️ This application simplifies medical information. "
    "It does not provide diagnosis or treatment."
)


# --------------------------------------------------
# GEMINI API CONFIGURATION
# --------------------------------------------------

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL_NAME = "gemini-3.5-flash"


# --------------------------------------------------
# EXTRACT REPORT TEXT
# --------------------------------------------------

def extract_report_text(file_path, file_type):

    if file_type == "application/pdf":

        doc = fitz.open(file_path)

        final_text = ""

        for page_number, page in enumerate(doc):

            text = page.get_text("text").strip()

            # OCR for scanned PDF
            if len(text) < 50:

                pix = page.get_pixmap(dpi=300)

                image = Image.frombytes(
                    "RGB",
                    [pix.width, pix.height],
                    pix.samples
                )

                text = pytesseract.image_to_string(image)

            final_text += (
                f"\n--- PAGE {page_number + 1} ---\n"
            )

            final_text += text

        return final_text

    else:

        image = Image.open(file_path)

        return pytesseract.image_to_string(image)


# --------------------------------------------------
# MEDICAL TERMINOLOGY API
# --------------------------------------------------

def validate_medical_term(term):

    url = (
        "https://clinicaltables.nlm.nih.gov/"
        "api/conditions/v3/search"
    )

    params = {
        "terms": term,
        "maxList": 3
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data[0] > 0:
            return data[3]

    except Exception:
        return []

    return []


# --------------------------------------------------
# ANALYZE LAB VALUES
# --------------------------------------------------

def analyze_lab_values(results):

    analyzed_results = []

    for item in results:

        result = item.copy()

        try:

            value = float(item["value"])

            low = item.get("reference_low")
            high = item.get("reference_high")

            if low is not None and value < float(low):

                status = "LOW"

            elif high is not None and value > float(high):

                status = "HIGH"

            elif low is not None and high is not None:

                status = "NORMAL"

            else:

                status = "UNKNOWN"

        except Exception:

            status = "UNKNOWN"

        result["status"] = status

        analyzed_results.append(result)

    return analyzed_results


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

st.header("📄 Upload Medical Report")

uploaded_file = st.file_uploader(
    "Upload PDF, PNG, JPG or JPEG",
    type=["pdf", "png", "jpg", "jpeg"]
)


# --------------------------------------------------
# REPORT ANALYSIS
# --------------------------------------------------

if uploaded_file is not None:

    st.success("File uploaded successfully!")

    if st.button("🔍 Analyze Report"):

        with st.spinner("Analyzing medical report..."):

            try:

                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(
                    delete=False
                ) as temp_file:

                    temp_file.write(
                        uploaded_file.getvalue()
                    )

                    file_path = temp_file.name


                # Extract report text
                report_text = extract_report_text(
                    file_path,
                    uploaded_file.type
                )


                # ------------------------------------------
                # STRUCTURED MEDICAL DATA EXTRACTION
                # ------------------------------------------

                extraction_prompt = f"""
You are a medical document information extraction system.

Extract information ONLY from the report.

Return valid JSON using this format:

{{
    "report_type": "",
    "medical_terms": [],
    "lab_results": [
        {{
            "test_name": "",
            "value": "",
            "unit": "",
            "reference_low": null,
            "reference_high": null
        }}
    ]
}}

Rules:

1. Do not diagnose.
2. Do not invent values.
3. Use only information from the report.
4. Use only reference ranges printed in the report.
5. Return JSON only.

MEDICAL REPORT:

{report_text}
"""

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=extraction_prompt
                )

                raw_json = re.sub(
                    r"```json|```",
                    "",
                    response.text
                ).strip()

                medical_data = json.loads(raw_json)


                # ------------------------------------------
                # LAB VALUE ANALYSIS
                # ------------------------------------------

                lab_results = medical_data.get(
                    "lab_results",
                    []
                )

                analyzed_results = analyze_lab_values(
                    lab_results
                )


                # ------------------------------------------
                # MEDICAL TERMINOLOGY VALIDATION
                # ------------------------------------------

                medical_terms = medical_data.get(
                    "medical_terms",
                    []
                )

                validated_terms = {}

                for term in medical_terms:

                    validated_terms[term] = (
                        validate_medical_term(term)
                    )


                # ------------------------------------------
                # SIMPLE REPORT EXPLANATION
                # ------------------------------------------

                simplification_prompt = f"""
You are a medical report simplification assistant.

Explain the medical report in very simple language.

MEDICAL REPORT:

{report_text}

LAB ANALYSIS:

{json.dumps(analyzed_results, indent=2)}

MEDICAL TERMINOLOGY API RESULTS:

{json.dumps(validated_terms, indent=2)}

Rules:

1. Do not diagnose diseases.
2. Do not prescribe medicines.
3. Do not recommend treatment.
4. Explain medical terms simply.
5. Mention HIGH or LOW only from LAB ANALYSIS.
6. Do not exaggerate health risks.
7. Encourage discussion with a healthcare professional.

Create these sections:

REPORT OVERVIEW

LAB RESULT EXPLANATION

MEDICAL TERMS EXPLAINED

IMPORTANT DISCUSSION POINTS
"""

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=simplification_prompt
                )

                simple_report = response.text


                # ------------------------------------------
                # DOCTOR QUESTIONS
                # ------------------------------------------

                question_prompt = f"""
Based ONLY on the medical report and lab analysis,
generate 5 useful questions the patient can ask their doctor.

Do not diagnose.
Do not prescribe medicine.
Do not recommend treatment.

MEDICAL REPORT:

{report_text}

LAB ANALYSIS:

{json.dumps(analyzed_results, indent=2)}
"""

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=question_prompt
                )

                doctor_questions = response.text


                # ------------------------------------------
                # DISPLAY RESULTS
                # ------------------------------------------

                st.success(
                    "🎉 Report analyzed successfully!"
                )

                st.header("📊 Lab Results")

                if analyzed_results:

                    lab_df = pd.DataFrame(
                        analyzed_results
                    )

                    st.dataframe(
                        lab_df,
                        use_container_width=True
                    )

                else:

                    st.info(
                        "No structured lab values detected."
                    )


                st.header(
                    "🧠 Simple Report Explanation"
                )

                st.markdown(simple_report)


                st.header(
                    "❓ Questions to Ask Your Doctor"
                )

                st.markdown(doctor_questions)


                with st.expander(
                    "📄 View Extracted Report Text"
                ):

                    st.text(report_text)


                st.warning(
                    "⚠️ This tool simplifies medical "
                    "information and does not provide "
                    "medical diagnosis or treatment."
                )


            except Exception as error:

                st.error(
                    f"Error analyzing report: {error}"
                )
