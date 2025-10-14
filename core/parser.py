import json
import re
from typing import Dict, List, Any, Union

def parse_test_cases(content: str, format_type: str) -> List[Dict[str, Any]]:
    """
    Parse the generated test cases into a structured format
    
    Args:
        content: Raw content from LLM
        format_type: Format type (traditional, gherkin, detailed)
        
    Returns:
        List of structured test cases
    """
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