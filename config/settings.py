import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Default Settings
DEFAULT_LLM_PROVIDER = "gemini"
DEFAULT_TEST_CASE_FORMAT = os.getenv("DEFAULT_TEST_CASE_FORMAT", "traditional")

# Supported Formats
SUPPORTED_FORMATS = ["traditional", "gherkin", "detailed"]
SUPPORTED_FILE_TYPES = ["txt", "docx"]
SUPPORTED_EXPORT_FORMATS = ["json", "csv", "md"]

# UI Configuration
PAGE_TITLE = "QA Test Case Generator"
PAGE_ICON = "🧪"