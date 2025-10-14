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