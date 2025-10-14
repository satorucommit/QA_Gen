# QA Test Case Generator

A Streamlit application that generates test cases from requirements using Google's Gemini AI.

## Features

- Upload requirement documents (TXT, DOCX)
- Generate test cases in multiple formats (Traditional, Gherkin, Detailed)
- Export test cases to JSON, CSV, or Markdown
- Refine generated test cases with additional prompts

## Prerequisites

- Python 3.8+ (Recommended: Python 3.11 for best compatibility)
- Google Gemini API key

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
4. Edit the `.env` file and add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Usage

You can run the application in two ways:

### Option 1: Using the original application

1. Run the application:
   ```bash
   python run.py
   ```

### Option 2: Using the new streamlined application (recommended)

1. Run the streamlined application:
   ```bash
   python run_streamlit.py
   ```

2. Open your browser to the displayed URL (typically `http://localhost:8501`)

Both options will open your browser to the application. From there:

1. Upload a requirement document
2. Select test case format
3. Click "Generate Test Cases"
4. Review, refine, and export results

## Environment Variables

- `GEMINI_API_KEY` (required): Your Google Gemini API key
- `DEFAULT_TEST_CASE_FORMAT` (optional): Default format for test cases (traditional, gherkin, detailed)

## Supported Formats

- **Traditional**: Standard test case format
- **Gherkin**: Behavior-driven development format
- **Detailed**: Comprehensive test case format

## Python Version Compatibility

This project has been tested with Python 3.8 through 3.12. For Python 3.13+ users, ensure you're using compatible package versions as specified in requirements.txt.

## License

MIT