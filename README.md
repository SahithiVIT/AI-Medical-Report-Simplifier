# 🧠 AI Medical Report Simplifier

AI Medical Report Simplifier is an AI-powered web application that converts complex medical lab reports into simple and easy-to-understand language.

The application extracts medical information, analyzes lab values using the reference ranges provided in the report, explains medical terminology, and generates useful questions that users can discuss with healthcare professionals.

---

## 🌐 Live Demo

🚀 Try the deployed application:

https://ai-medical-report-simplifier-kbgvceawxr4qbsajio4k7i.streamlit.app/

---

## 💻 GitHub Repository

View the complete source code:

https://github.com/SahithiVIT/AI-Medical-Report-Simplifier

---

## 🚀 Features

- 📄 Upload medical reports in PDF, PNG, JPG, or JPEG format
- 🔍 Extract text using PDF parsing and OCR
- 🧠 Extract structured medical information using Generative AI
- 📊 Analyze HIGH, LOW, NORMAL, and UNKNOWN lab values
- 🔌 Validate medical terminology using the NIH/NLM Clinical Tables API
- ✨ Simplify complex medical terms into easy language
- ❓ Generate useful questions to ask a doctor
- 🌐 Interactive web application using Streamlit

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Gemini API
- Google GenAI SDK
- PyMuPDF
- Tesseract OCR
- NIH/NLM Clinical Tables API
- Pandas
- REST APIs
- Google Colab
- GitHub

---

## 🔄 Project Workflow

Medical Report Upload

↓

PDF Parsing / OCR

↓

Structured Medical Data Extraction

↓

Lab Value Analysis

↓

Medical Terminology API Validation

↓

AI-Based Report Simplification

↓

Doctor Question Generation

↓

Streamlit Web Interface

---

## 📊 Lab Value Analysis

The application extracts lab test values and compares them only with the reference ranges provided in the uploaded medical report.

Python-based logic classifies lab results as:

- HIGH
- LOW
- NORMAL
- UNKNOWN

The application does not independently define medical reference ranges.

---

## 🤖 AI Integration

The Gemini API is used to:

- Extract structured medical information
- Convert medical report data into JSON format
- Simplify complex medical terminology
- Generate easy-to-understand report explanations
- Generate useful questions for doctor discussions

The AI is instructed not to diagnose diseases or prescribe treatment.

---

## 🔌 Healthcare API Integration

The project integrates the NIH/NLM Clinical Tables API.

The API is used to search and validate medical terminology extracted from uploaded medical reports.

---

## 🔍 OCR and PDF Processing

PyMuPDF is used to extract text from text-based PDF reports.

For scanned medical reports and images, Tesseract OCR is used for text extraction.

### Supported Formats

- PDF
- PNG
- JPG
- JPEG

---

## 📁 Project Structure

AI-Medical-Report-Simplifier/

- app.py
- Medical_Report_Simplifier.ipynb
- requirements.txt
- packages.txt
- README.md

### app.py

Contains the complete Streamlit web application and AI processing pipeline.

### Medical_Report_Simplifier.ipynb

Google Colab notebook used for project development, testing, and experimentation.

### requirements.txt

Contains the required Python libraries.

### packages.txt

Contains the Tesseract OCR system dependency required for deployment.

---

## ▶️ Run the Project Locally

Clone the repository:

    git clone https://github.com/SahithiVIT/AI-Medical-Report-Simplifier.git

Open the project folder:

    cd AI-Medical-Report-Simplifier

Install dependencies:

    pip install -r requirements.txt

Run the Streamlit application:

    streamlit run app.py

---

## 🔐 Gemini API Configuration

Create a `.streamlit` folder.

Inside the folder, create:

    secrets.toml

Add your Gemini API key:

    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

Never upload API keys to GitHub.

---

## 📓 Google Colab Notebook

The project includes a Google Colab notebook for development and testing.

File:

    Medical_Report_Simplifier.ipynb

The notebook demonstrates:

- Medical report upload
- PDF text extraction
- OCR
- Structured medical information extraction
- Lab value analysis
- NIH/NLM API integration
- AI report simplification
- Doctor question generation

---

## 💡 Example Workflow

A user uploads a medical laboratory report.

The system extracts lab values such as:

- Hemoglobin
- White Blood Cell Count
- Platelet Count
- Fasting Blood Glucose
- Serum Creatinine
- TSH

The application compares extracted values with the reference ranges printed in the report.

Example:

    Hemoglobin: 10.5 g/dL
    Reference Range: 12.0 - 16.0 g/dL
    Status: LOW

The AI then explains the report in simple language and generates questions the user can discuss with a healthcare professional.

---

## ⚠️ Disclaimer

This application is developed for educational and informational purposes only.

It simplifies medical report information and does not provide medical diagnosis, treatment, or medical advice.

Users should discuss medical reports and health concerns with a qualified healthcare professional.



