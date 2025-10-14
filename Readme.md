# QA Test Case Generator

A Streamlit application that generates test cases from requirements using Google's Gemini AI.

## Features

- Upload requirement documents (TXT, DOCX)
- Generate test cases in multiple formats (Traditional, Gherkin, Detailed)
- Export test cases to JSON, CSV, or Markdown
- Refine generated test cases with additional prompts

## Setup

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file based on `.env.example`
4. Add your Gemini API key to the `.env` file
5. Run the application: `streamlit run app.py`

## Usage

1. Upload a requirement document
2. Select test case format
3. Click "Generate Test Cases"
4. Review and refine if needed
5. Export the results