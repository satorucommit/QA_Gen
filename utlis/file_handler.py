import os
import json
import pandas as pd
from typing import Dict, Any, Union, List
from docx import Document

def read_txt_file(file_path: str) -> str:
    """
    Read content from a text file
    
    Args:
        file_path: Path to the text file
        
    Returns:
        File content as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        raise Exception(f"Error reading text file: {str(e)}")

def read_docx_file(file_path: str) -> str:
    """
    Read content from a DOCX file
    
    Args:
        file_path: Path to the DOCX file
        
    Returns:
        File content as string
    """
    try:
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        raise Exception(f"Error reading DOCX file: {str(e)}")

def export_to_json(data: Union[Dict, List], file_path: str) -> str:
    """
    Export data to JSON file
    
    Args:
        data: Data to export
        file_path: Path to save the JSON file
        
    Returns:
        Path to the saved file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return file_path
    except Exception as e:
        raise Exception(f"Error exporting to JSON: {str(e)}")

def export_to_csv(data: List[Dict], file_path: str) -> str:
    """
    Export data to CSV file
    
    Args:
        data: List of dictionaries to export
        file_path: Path to save the CSV file
        
    Returns:
        Path to the saved file
    """
    try:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        return file_path
    except Exception as e:
        raise Exception(f"Error exporting to CSV: {str(e)}")

def export_to_md(data: Union[Dict, List], file_path: str, format_type: str = "traditional") -> str:
    """
    Export data to Markdown file
    
    Args:
        data: Data to export
        file_path: Path to save the Markdown file
        format_type: Format type for proper markdown rendering
        
    Returns:
        Path to the saved file
    """
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

def ensure_output_dir(output_dir: str = "output") -> str:
    """
    Ensure the output directory exists
    
    Args:
        output_dir: Path to the output directory
        
    Returns:
        Path to the output directory
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir