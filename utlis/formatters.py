import json
from typing import Dict, List, Any, Union

def format_test_cases_for_display(test_cases: List[Dict[str, Any]], format_type: str) -> str:
    """
    Format test cases for display in the UI
    
    Args:
        test_cases: List of test case dictionaries
        format_type: Format type (traditional, gherkin, detailed)
        
    Returns:
        Formatted string for display
    """
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

def format_test_cases_for_export(test_cases: List[Dict[str, Any]], format_type: str) -> Union[List[Dict], str]:
    """
    Format test cases for export
    
    Args:
        test_cases: List of test case dictionaries
        format_type: Format type (traditional, gherkin, detailed)
        
    Returns:
        Formatted data for export
    """
    if format_type.lower() == "gherkin":
        # For Gherkin, we might want to convert to a more structured format
        return test_cases
    else:
        # For traditional and detailed, return as is
        return test_cases

def format_json_output(test_cases: List[Dict[str, Any]], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Format test cases as JSON with metadata
    
    Args:
        test_cases: List of test case dictionaries
        metadata: Additional metadata to include
        
    Returns:
        Formatted JSON structure
    """
    output = {
        "test_cases": test_cases,
        "count": len(test_cases)
    }
    
    if metadata:
        output["metadata"] = metadata
    
    return output