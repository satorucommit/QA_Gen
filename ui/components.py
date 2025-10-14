import streamlit as st
import time
import os
from typing import Dict, Any, List, Callable
from datetime import datetime

def render_header():
    """Render the application header"""
    st.set_page_config(
        page_title="QA Test Case Generator",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🧪 QA Test Case Generator")
    st.markdown("Generate comprehensive test cases from requirements using Google's Gemini AI")
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
        type=["txt", "docx"],
        help="Supported formats: TXT, DOCX"
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
            from utlis.helpers import extract_text_from_upload, truncate_text
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
    from utlis.formatters import format_test_cases_for_display
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
            from utlis.file_handler import ensure_output_dir, export_to_json
            from utlis.helpers import sanitize_filename, get_timestamp
            
            output_dir = ensure_output_dir()
            filename = f"test_cases_{get_timestamp()}.json"
            filepath = os.path.join(output_dir, filename)
            
            from utlis.formatters import format_json_output
            metadata = {
                "format_type": format_type,
                "generated_at": datetime.now().isoformat()
            }
            json_data = format_json_output(test_cases, metadata)
            
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
            from utlis.file_handler import ensure_output_dir, export_to_csv
            from utlis.helpers import sanitize_filename, get_timestamp
            
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
            from utlis.file_handler import ensure_output_dir, export_to_md
            from utlis.helpers import sanitize_filename, get_timestamp
            
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