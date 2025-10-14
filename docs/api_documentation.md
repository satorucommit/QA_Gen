# API Documentation

## Core Classes

### LLMHandler

Handles interactions with Google's Gemini API.

#### Methods

##### `__init__(provider: str = "gemini")`
Initialize the LLM handler with Gemini.

**Parameters:**
- `provider`: LLM provider (only "gemini" is supported)

##### `generate_test_cases(requirements: str, format_type: str = "traditional", additional_instructions: str = "") -> Dict`
Generate test cases based on requirements using Gemini.

**Parameters:**
- `requirements`: The requirements text
- `format_type`: Format for test cases ("traditional", "gherkin", "detailed")
- `additional_instructions`: Additional instructions for refinement

**Returns:**
Dictionary containing generated test cases or error information.