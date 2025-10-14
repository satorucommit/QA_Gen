# System Architecture

## Overview

The QA Test Case Generator is a web application built with Streamlit that leverages Large Language Models (LLMs) to generate test cases from requirements documents.

## Components

### Frontend (Streamlit UI)
- Main application interface
- File upload component
- Test case display
- Export functionality

### Core Logic
- **LLM Handler**: Manages interactions with LLM APIs (OpenAI, Anthropic)
- **Parser**: Parses LLM responses into structured test cases
- **Validator**: Validates inputs and outputs
- **Prompt Templates**: Manages prompt engineering for different formats

### Utilities
- **File Handler**: Handles file reading and writing operations
- **Formatters**: Formats test cases for display and export
- **Helpers**: General utility functions

### Data
- Sample requirements for testing
- Test case templates
- Example outputs

## Data Flow

1. User uploads a requirements document
2. File content is extracted and validated
3. User selects test case format and LLM provider
4. System generates appropriate prompt
5. LLM processes the prompt and returns test cases
6. Parser structures the test cases
7. Formatted test cases are displayed to the user
8. User can refine or export the test cases

## Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **LLM Integration**: OpenAI API, Anthropic API
- **File Processing**: python-docx
- **Data Handling**: pandas
- **Environment Management**: python-dotenv