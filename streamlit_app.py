import streamlit as st
import os
import sys
import time
import json
import re
import uuid
from datetime import datetime
from typing import Dict, List, Any, Union
import pandas as pd

# Try to import required modules, with fallbacks for missing dependencies
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    st.warning("Google Generative AI (Gemini) not available. Please install google-generativeai.")

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configuration
SUPPORTED_FORMATS = ["traditional", "gherkin", "detailed"]
SUPPORTED_FILE_TYPES = ["txt", "docx"]
SUPPORTED_EXPORT_FORMATS = ["json", "csv", "md"]
PAGE_TITLE = "QA Test Case Generator"
PAGE_ICON = "🧪"

# Initialize session state
def initialize_session_state():
    """Initialize session state variables"""
    if 'requirements' not in st.session_state:
        st.session_state.requirements = None
    if 'test_cases' not in st.session_state:
        st.session_state.test_cases = None
    if 'format_type' not in st.session_state:
        st.session_state.format_type = "traditional"
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = None

# UI Components
def render_header():
    """Render the application header"""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title(f"{PAGE_ICON} {PAGE_TITLE}")
    st.markdown("Generate comprehensive test cases from requirements using AI")
    st.divider()

def render_sidebar():
    """Render the sidebar with configuration options"""
    with st.sidebar:
        st.header("Configuration")
        
        # Test Case Format Selection
        format_type = st.selectbox(
            "Test Case Format",
            ["Traditional", "Gherkin", "Detailed"],
            index=0
        )
        
        # Advanced Settings
        with st.expander("Advanced Settings"):
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.1
            )
            
            max_tokens = st.slider(
                "Max Tokens",
                min_value=500,
                max_value=4000,
                value=2000,
                step=100
            )
        
        return {
            "format_type": format_type.lower(),
            "temperature": temperature,
            "max_tokens": max_tokens
        }

def render_file_upload():
    """Render the file upload component"""
    st.header("Upload Requirements")
    
    uploaded_file = st.file_uploader(
        "Upload a requirements document",
        type=SUPPORTED_FILE_TYPES,
        help=f"Supported formats: {', '.join(SUPPORTED_FILE_TYPES).upper()}"
    )
    
    if uploaded_file is not None:
        # Display file info
        file_details = {
            "Filename": uploaded_file.name,
            "File type": uploaded_file.type,
            "File size": f"{uploaded_file.size / 1024:.2f} KB"
        }
        
        st.json(file_details)
        
        # Extract and display content
        with st.expander("Preview Content"):
            content = extract_text_from_upload(uploaded_file)
            st.text(truncate_text(content, 500))
            
            if len(content) > 500:
                st.caption(f"Showing first 500 characters of {len(content)} total")
        
        return content
    
    return None

def render_generation_button():
    """Render the generate button"""
    generate_button = st.button(
        "Generate Test Cases",
        type="primary",
        use_container_width=True
    )
    
    return generate_button

def render_loading_indicator():
    """Render loading indicator during generation"""
    with st.spinner("Generating test cases... This may take a moment."):
        time.sleep(1)  # Small delay to ensure spinner appears
        return True

def render_test_cases(test_cases: List[Dict[str, Any]], format_type: str):
    """Render the generated test cases"""
    st.header("Generated Test Cases")
    
    if not test_cases:
        st.warning("No test cases were generated. Please check your requirements and try again.")
        return
    
    # Display test cases count
    st.success(f"Generated {len(test_cases)} test case(s)")
    
    # Display test cases
    formatted_content = format_test_cases_for_display(test_cases, format_type)
    st.markdown(formatted_content)
    
    return test_cases

def render_refinement_section():
    """Render the refinement section"""
    st.header("Refine Test Cases")
    
    with st.expander("Refine Generated Test Cases"):
        feedback = st.text_area(
            "Provide feedback for refinement",
            placeholder="E.g., Add more edge cases, clarify step 3, etc.",
            height=100
        )
        
        refine_button = st.button(
            "Refine Test Cases",
            type="secondary"
        )
        
        return feedback, refine_button

def render_export_section(test_cases: List[Dict[str, Any]], format_type: str):
    """Render the export section"""
    st.header("Export Test Cases")
    
    if not test_cases:
        st.info("No test cases to export")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export as JSON", type="secondary", use_container_width=True):
            output_dir = ensure_output_dir()
            filename = f"test_cases_{get_timestamp()}.json"
            filepath = os.path.join(output_dir, filename)
            
            json_data = format_json_output(test_cases, {
                "format_type": format_type,
                "generated_at": datetime.now().isoformat()
            })
            
            export_to_json(json_data, filepath)
            st.success(f"Test cases exported to {filepath}")
            st.download_button(
                label="Download JSON",
                data=json.dumps(json_data, indent=2),
                file_name=filename,
                mime="application/json"
            )
    
    with col2:
        if st.button("Export as CSV", type="secondary", use_container_width=True):
            output_dir = ensure_output_dir()
            filename = f"test_cases_{get_timestamp()}.csv"
            filepath = os.path.join(output_dir, filename)
            
            export_to_csv(test_cases, filepath)
            st.success(f"Test cases exported to {filepath}")
            
            # Provide download button
            with open(filepath, "r") as file:
                st.download_button(
                    label="Download CSV",
                    data=file.read(),
                    file_name=filename,
                    mime="text/csv"
                )
    
    with col3:
        if st.button("Export as Markdown", type="secondary", use_container_width=True):
            output_dir = ensure_output_dir()
            filename = f"test_cases_{get_timestamp()}.md"
            filepath = os.path.join(output_dir, filename)
            
            export_to_md(test_cases, filepath, format_type)
            st.success(f"Test cases exported to {filepath}")
            
            # Provide download button
            with open(filepath, "r") as file:
                st.download_button(
                    label="Download Markdown",
                    data=file.read(),
                    file_name=filename,
                    mime="text/markdown"
                )

def render_error_message(error: str):
    """Render error message"""
    st.error(f"An error occurred: {error}")

def render_success_message(message: str):
    """Render success message"""
    st.success(message)

# Utility Functions
def generate_unique_id(prefix: str = "TC") -> str:
    """Generate a unique ID with prefix"""
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{unique_id}"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file saving"""
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'[-\s]+', '_', filename)
    return filename.strip()

def get_timestamp() -> str:
    """Get current timestamp as string"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def extract_text_from_upload(uploaded_file) -> str:
    """Extract text from uploaded file"""
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    
    if file_extension == ".txt":
        return uploaded_file.read().decode("utf-8")
    elif file_extension == ".docx":
        if not DOCX_AVAILABLE:
            raise ValueError("DOCX support not available. Please install python-docx.")
        doc = Document(uploaded_file)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def ensure_output_dir(output_dir: str = "output") -> str:
    """Ensure the output directory exists"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# Formatters
def format_test_cases_for_display(test_cases: List[Dict[str, Any]], format_type: str) -> str:
    """Format test cases for display in the UI"""
    if not test_cases:
        return "No test cases generated."
    
    if format_type.lower() == "gherkin":
        return format_gherkin_for_display(test_cases)
    else:
        return format_traditional_for_display(test_cases)

def format_traditional_for_display(test_cases: List[Dict[str, Any]]) -> str:
    """Format traditional test cases for display"""
    formatted = []
    
    for tc in test_cases:
        formatted.append(f"**Test Case ID:** {tc.get('id', 'N/A')}")
        formatted.append(f"**Title:** {tc.get('title', 'N/A')}")
        
        if 'objective' in tc:
            formatted.append(f"**Objective:** {tc.get('objective', 'N/A')}")
        
        formatted.append(f"**Preconditions:** {tc.get('preconditions', 'N/A')}")
        
        if 'test_data' in tc:
            formatted.append(f"**Test Data:** {tc.get('test_data', 'N/A')}")
        
        formatted.append(f"**Test Steps:** {tc.get('steps', 'N/A')}")
        formatted.append(f"**Expected Results:** {tc.get('expected_results', 'N/A')}")
        
        if 'postconditions' in tc:
            formatted.append(f"**Postconditions:** {tc.get('postconditions', 'N/A')}")
        
        formatted.append(f"**Priority:** {tc.get('priority', 'N/A')}")
        
        if 'test_type' in tc:
            formatted.append(f"**Test Type:** {tc.get('test_type', 'N/A')}")
        
        formatted.append("---")
    
    return "\n\n".join(formatted)

def format_gherkin_for_display(test_cases: List[Dict[str, Any]]) -> str:
    """Format Gherkin test cases for display"""
    formatted = []
    
    for tc in test_cases:
        formatted.append(f"**Feature:** {tc.get('feature', 'N/A')}")
        formatted.append(f"**Scenario:** {tc.get('scenario', 'N/A')}")
        formatted.append(f"**Given:** {tc.get('given', 'N/A')}")
        formatted.append(f"**When:** {tc.get('when', 'N/A')}")
        formatted.append(f"**Then:** {tc.get('then', 'N/A')}")
        
        if tc.get('and'):
            formatted.append("**And:**")
            for step in tc.get('and', []):
                formatted.append(f"- {step}")
        
        formatted.append("---")
    
    return "\n\n".join(formatted)

def format_json_output(test_cases: List[Dict[str, Any]], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """Format test cases as JSON with metadata"""
    output = {
        "test_cases": test_cases,
        "count": len(test_cases)
    }
    
    if metadata:
        output["metadata"] = metadata
    
    return output

# File Handlers
def export_to_json(data: Union[Dict, List], file_path: str) -> str:
    """Export data to JSON file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return file_path
    except Exception as e:
        raise Exception(f"Error exporting to JSON: {str(e)}")

def export_to_csv(data: List[Dict], file_path: str) -> str:
    """Export data to CSV file"""
    try:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        return file_path
    except Exception as e:
        raise Exception(f"Error exporting to CSV: {str(e)}")

def export_to_md(data: Union[Dict, List], file_path: str, format_type: str = "traditional") -> str:
    """Export data to Markdown file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            if format_type.lower() == "gherkin":
                file.write("# Test Cases (Gherkin Format)\n\n")
                for tc in data:
                    file.write(f"## Feature: {tc.get('feature', 'N/A')}\n\n")
                    file.write(f"### Scenario: {tc.get('scenario', 'N/A')}\n\n")
                    file.write(f"**Given:** {tc.get('given', 'N/A')}\n\n")
                    file.write(f"**When:** {tc.get('when', 'N/A')}\n\n")
                    file.write(f"**Then:** {tc.get('then', 'N/A')}\n\n")
                    
                    if tc.get('and'):
                        file.write("**And:**\n")
                        for step in tc.get('and', []):
                            file.write(f"- {step}\n")
                        file.write("\n")
                    
                    file.write("---\n\n")
            else:
                # Traditional or detailed format
                file.write("# Test Cases\n\n")
                for tc in data:
                    file.write(f"## {tc.get('title', 'N/A')}\n\n")
                    
                    for key, value in tc.items():
                        if key != 'title':
                            file.write(f"**{key.replace('_', ' ').title()}:** {value}\n\n")
                    
                    file.write("---\n\n")
        
        return file_path
    except Exception as e:
        raise Exception(f"Error exporting to Markdown: {str(e)}")

# Validation Functions
def validate_requirements(requirements: str) -> Dict[str, Any]:
    """Validate the requirements text"""
    if not requirements or not requirements.strip():
        return {"valid": False, "message": "Requirements text is empty"}
    
    if len(requirements) < 50:
        return {"valid": False, "message": "Requirements text is too short to generate meaningful test cases"}
    
    if len(requirements) > 10000:
        return {"valid": False, "message": "Requirements text is too long. Please keep it under 10,000 characters"}
    
    return {"valid": True, "message": "Requirements are valid"}

def validate_refinement_feedback(feedback: str) -> Dict[str, Any]:
    """Validate the refinement feedback"""
    if not feedback or not feedback.strip():
        return {"valid": False, "message": "Feedback text is empty"}
    
    if len(feedback) < 10:
        return {"valid": False, "message": "Feedback is too short to provide meaningful refinement"}
    
    if len(feedback) > 1000:
        return {"valid": False, "message": "Feedback is too long. Please keep it under 1,000 characters"}
    
    return {"valid": True, "message": "Feedback is valid"}

# Prompt Templates
def get_system_prompt(format_type: str) -> str:
    """Get the system prompt based on format type"""
    
    base_prompt = """You are a QA expert with years of experience in software testing. 
    Your task is to analyze requirements and generate comprehensive test cases."""
    
    if format_type.lower() == "traditional":
        return f"""{base_prompt}
        
        Generate test cases in the traditional format with the following fields:
        - Test Case ID
        - Test Case Title
        - Preconditions
        - Test Steps
        - Expected Results
        - Priority
        """
    
    elif format_type.lower() == "gherkin":
        return f"""{base_prompt}
        
        Generate test cases in Gherkin format (BDD) with the following structure:
        - Feature
        - Scenario
        - Given (preconditions)
        - When (actions)
        - Then (expected results)
        - And (additional steps or results)
        """
    
    elif format_type.lower() == "detailed":
        return f"""{base_prompt}
        
        Generate detailed test cases with the following fields:
        - Test Case ID
        - Test Case Title
        - Test Objective
        - Preconditions
        - Test Data
        - Test Steps
        - Expected Results
        - Postconditions
        - Priority
        - Test Type
        """
    
    return base_prompt

def get_user_prompt(requirements: str, format_type: str, additional_instructions: str = "") -> str:
    """Get the user prompt for generating test cases"""
    
    prompt = f"""Please analyze the following requirements and generate comprehensive test cases in {format_type} format:
    
    Requirements:
    {requirements}
    
    """
    
    if additional_instructions:
        prompt += f"""
        Additional Instructions:
        {additional_instructions}
        """
    
    prompt += """
    Please ensure the test cases cover:
    - Happy path scenarios
    - Edge cases
    - Error handling
    - Boundary conditions
    """
    
    return prompt

def get_refinement_prompt(original_test_cases: str, feedback: str) -> str:
    """Get the prompt for refining test cases"""
    
    return f"""Please refine the following test cases based on the feedback provided:
    
    Original Test Cases:
    {original_test_cases}
    
    Feedback:
    {feedback}
    
    Please provide the refined test cases while maintaining the same format.
    """

# LLM Handler
class LLMHandler:
    """Handler for LLM API interactions with Gemini"""
    
    def __init__(self, provider: str = "gemini"):
        self.provider = provider.lower()
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Gemini client"""
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not found in environment variables")
        
        if not GEMINI_AVAILABLE:
            raise ValueError("Google Generative AI (Gemini) not available. Please install google-generativeai.")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.client = genai.GenerativeModel('gemini-2.0-flash')
    
    def generate_test_cases(
        self, 
        requirements: str, 
        format_type: str = "traditional",
        additional_instructions: str = ""
    ) -> Dict:
        """
        Generate test cases based on requirements using Gemini
        
        Args:
            requirements: The requirements text
            format_type: Format for test cases (traditional, gherkin, detailed)
            additional_instructions: Additional instructions for refinement
            
        Returns:
            Dictionary containing generated test cases
        """
        system_prompt = get_system_prompt(format_type)
        user_prompt = get_user_prompt(requirements, format_type, additional_instructions)
        
        try:
            # Combine system and user prompts for Gemini
            combined_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            # Generate content with Gemini
            response = self.client.generate_content(combined_prompt)
            content = response.text
            
            # Parse the response
            return {"content": content, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}

# Parser Functions
def parse_test_cases(content: str, format_type: str) -> List[Dict[str, Any]]:
    """Parse the generated test cases into a structured format"""
    if format_type.lower() == "traditional":
        return parse_traditional_format(content)
    elif format_type.lower() == "gherkin":
        return parse_gherkin_format(content)
    elif format_type.lower() == "detailed":
        return parse_detailed_format(content)
    else:
        return [{"raw_content": content}]

def parse_traditional_format(content: str) -> List[Dict[str, Any]]:
    """Parse traditional format test cases"""
    test_cases = []
    
    # Split by test case ID pattern
    tc_pattern = r'(Test Case ID:\s*(.+?))(?=Test Case ID:|$)'
    matches = re.findall(tc_pattern, content, re.DOTALL)
    
    for match in matches:
        tc_content = match[0]
        tc_id = match[1].strip()
        
        # Extract other fields
        title = extract_field(tc_content, "Test Case Title")
        preconditions = extract_field(tc_content, "Preconditions")
        steps = extract_field(tc_content, "Test Steps")
        expected_results = extract_field(tc_content, "Expected Results")
        priority = extract_field(tc_content, "Priority")
        
        test_cases.append({
            "id": tc_id,
            "title": title,
            "preconditions": preconditions,
            "steps": steps,
            "expected_results": expected_results,
            "priority": priority
        })
    
    return test_cases

def parse_gherkin_format(content: str) -> List[Dict[str, Any]]:
    """Parse Gherkin format test cases"""
    test_cases = []
    
    # Split by Feature
    feature_pattern = r'Feature:\s*(.+?)(?=Feature:|$)'
    feature_matches = re.findall(feature_pattern, content, re.DOTALL)
    
    for feature_content in feature_matches:
        feature = feature_content.strip()
        
        # Extract scenarios
        scenario_pattern = r'Scenario:\s*(.+?)(?=Scenario:|Feature:|$)'
        scenario_matches = re.findall(scenario_pattern, feature_content, re.DOTALL)
        
        for scenario_content in scenario_matches:
            scenario = scenario_content.strip()
            
            # Extract Gherkin steps
            given = extract_gherkin_step(scenario, "Given")
            when = extract_gherkin_step(scenario, "When")
            then = extract_gherkin_step(scenario, "Then")
            and_steps = extract_gherkin_step(scenario, "And", multiple=True)
            
            test_cases.append({
                "feature": feature.split('\n')[0].strip(),
                "scenario": scenario.split('\n')[0].strip(),
                "given": given,
                "when": when,
                "then": then,
                "and": and_steps
            })
    
    return test_cases

def parse_detailed_format(content: str) -> List[Dict[str, Any]]:
    """Parse detailed format test cases"""
    test_cases = []
    
    # Split by test case ID pattern
    tc_pattern = r'(Test Case ID:\s*(.+?))(?=Test Case ID:|$)'
    matches = re.findall(tc_pattern, content, re.DOTALL)
    
    for match in matches:
        tc_content = match[0]
        tc_id = match[1].strip()
        
        # Extract all fields
        title = extract_field(tc_content, "Test Case Title")
        objective = extract_field(tc_content, "Test Objective")
        preconditions = extract_field(tc_content, "Preconditions")
        test_data = extract_field(tc_content, "Test Data")
        steps = extract_field(tc_content, "Test Steps")
        expected_results = extract_field(tc_content, "Expected Results")
        postconditions = extract_field(tc_content, "Postconditions")
        priority = extract_field(tc_content, "Priority")
        test_type = extract_field(tc_content, "Test Type")
        
        test_cases.append({
            "id": tc_id,
            "title": title,
            "objective": objective,
            "preconditions": preconditions,
            "test_data": test_data,
            "steps": steps,
            "expected_results": expected_results,
            "postconditions": postconditions,
            "priority": priority,
            "test_type": test_type
        })
    
    return test_cases

def extract_field(content: str, field_name: str) -> str:
    """Extract a specific field from content"""
    pattern = rf'{field_name}:\s*(.+?)(?=\n[A-Z][a-z]+:|$)'
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else ""

def extract_gherkin_step(content: str, step_type: str, multiple: bool = False) -> Union[str, List[str]]:
    """Extract Gherkin steps from content"""
    if multiple:
        pattern = rf'{step_type}\s+(.+?)(?=\n(?:Given|When|Then|And|Scenario|Feature):|$)'
        matches = re.findall(pattern, content, re.DOTALL)
        return [match.strip() for match in matches]
    else:
        pattern = rf'{step_type}\s+(.+?)(?=\n(?:Given|When|Then|And|Scenario|Feature):|$)'
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else ""

# Main Application
def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Render UI components
    render_header()
    
    # Check for API key
    if not GEMINI_API_KEY:
        st.warning("⚠️ Gemini API key not found!")
        st.info("Please set your GEMINI_API_KEY in a `.env` file:")
        st.code("GEMINI_API_KEY=your_actual_api_key_here")
        st.stop()
    
    # Render sidebar with configuration
    config = render_sidebar()
    st.session_state.format_type = config["format_type"]
    
    # File upload section
    requirements = render_file_upload()
    if requirements:
        st.session_state.requirements = requirements
    
    # Generation section
    if st.session_state.requirements:
        # Validate requirements
        validation_result = validate_requirements(st.session_state.requirements)
        
        if validation_result["valid"]:
            # Generate button
            if render_generation_button():
                # Show loading indicator
                render_loading_indicator()
                
                try:
                    # Initialize LLM handler
                    handler = LLMHandler(provider="gemini")
                    
                    # Generate test cases
                    result = handler.generate_test_cases(
                        requirements=st.session_state.requirements,
                        format_type=st.session_state.format_type
                    )
                    
                    if result["success"]:
                        # Parse the generated content
                        st.session_state.generated_content = result["content"]
                        st.session_state.test_cases = parse_test_cases(
                            result["content"], 
                            st.session_state.format_type
                        )
                        
                        # Display success message
                        render_success_message("Test cases generated successfully!")
                    else:
                        # Display error message
                        render_error_message(result["error"])
                
                except Exception as e:
                    # Display error message
                    render_error_message(str(e))
        else:
            # Display validation error
            render_error_message(validation_result["message"])
    
    # Display test cases if available
    if st.session_state.test_cases:
        st.write(f"Debug: test_cases length = {len(st.session_state.test_cases)}")
        render_test_cases(st.session_state.test_cases, st.session_state.format_type)
        
        # Refinement section
        feedback, refine_button = render_refinement_section()
        
        if refine_button and feedback:
            # Validate feedback
            validation_result = validate_refinement_feedback(feedback)
            
            if validation_result["valid"]:
                try:
                    # Show loading indicator
                    render_loading_indicator()
                    
                    # Initialize LLM handler
                    handler = LLMHandler(provider="gemini")
                    
                    # Refine test cases
                    refinement_prompt = get_refinement_prompt(
                        st.session_state.generated_content, 
                        feedback
                    )
                    
                    result = handler.generate_test_cases(
                        requirements=refinement_prompt,
                        format_type=st.session_state.format_type
                    )
                    
                    if result["success"]:
                        # Parse the refined content
                        st.session_state.generated_content = result["content"]
                        st.session_state.test_cases = parse_test_cases(
                            result["content"], 
                            st.session_state.format_type
                        )
                        
                        # Display success message
                        render_success_message("Test cases refined successfully!")
                        
                        # Rerun to update the display
                        st.rerun()
                    else:
                        # Display error message
                        render_error_message(result["error"])
                
                except Exception as e:
                    # Display error message
                    render_error_message(str(e))
            else:
                # Display validation error
                render_error_message(validation_result["message"])
        
        # Export section
        render_export_section(st.session_state.test_cases, st.session_state.format_type)

# Run the application
if __name__ == "__main__":
    main()