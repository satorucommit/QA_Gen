# User Guide

## Getting Started

1. Install the required dependencies:
pip install -r requirements.txt


2. Set up your environment variables:
- Copy `.env.example` to `.env`
- Add your API keys to the `.env` file

3. Run the application:
streamlit run app.py


## Using the Application

### Step 1: Upload Requirements

1. Click on "Browse files" or drag and drop a requirements document
2. Supported formats: TXT, DOCX
3. Preview the content to ensure it's correct

### Step 2: Configure Generation

1. Select your preferred LLM provider (OpenAI or Anthropic)
2. Choose the test case format:
- Traditional: Standard test case format with ID, title, steps, etc.
- Gherkin: BDD format with Given/When/Then structure
- Detailed: Comprehensive format with additional fields
3. Adjust advanced settings if needed (temperature, max tokens)

### Step 3: Generate Test Cases

1. Click the "Generate Test Cases" button
2. Wait for the process to complete
3. Review the generated test cases

### Step 4: Refine (Optional)

1. If needed, provide feedback for refinement
2. Click "Refine Test Cases" to improve the results
3. Repeat until satisfied with the output

### Step 5: Export

1. Choose your preferred export format:
- JSON: Structured data format
- CSV: Tabular format for spreadsheets
- Markdown: Human-readable format
2. Click the corresponding export button
3. Download the generated file

## Tips for Best Results

- Provide clear and detailed requirements
- Include acceptance criteria when possible
- Use specific language rather than vague terms
- Break down complex requirements into smaller parts
- Review and refine the generated test cases for accuracy