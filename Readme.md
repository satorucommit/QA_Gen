# QA Test Case Generator

A Streamlit application that generates test cases from requirements using Google's Gemini AI.

## Features

- Upload requirement documents (TXT, DOCX)
- Generate test cases in multiple formats (Traditional, Gherkin, Detailed)
- Export test cases to JSON, CSV, or Markdown
- Refine generated test cases with additional prompts

## Prerequisites

- Python 3.8+
- Google Gemini API key

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   python run.py
   ```
2. Open your browser to the displayed URL (typically `http://localhost:8501`)
3. Upload a requirement document
4. Select test case format
5. Click "Generate Test Cases"
6. Review, refine, and export results

## Supported Formats

- **Traditional**: Standard test case format
- **Gherkin**: Behavior-driven development format
- **Detailed**: Comprehensive test case format

## License

MIT
