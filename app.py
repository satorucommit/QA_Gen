import streamlit as st
import os
from datetime import datetime

# Import modules
from config.settings import (
    SUPPORTED_FORMATS, 
    SUPPORTED_FILE_TYPES, 
    SUPPORTED_EXPORT_FORMATS
)
from core.llm_handler import LLMHandler
from core.parser import parse_test_cases
from core.validator import validate_requirements, validate_format, validate_refinement_feedback
from utlis.file_handler import ensure_output_dir
from ui.components import (
    render_header,
    render_sidebar,
    render_file_upload,
    render_generation_button,
    render_loading_indicator,
    render_test_cases,
    render_refinement_section,
    render_export_section,
    render_error_message,
    render_success_message
)

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

# Main application
def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Render UI components
    render_header()
    
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
                    from core.prompt_templates import get_refinement_prompt
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