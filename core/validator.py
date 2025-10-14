import re
from typing import Dict, List, Any

def validate_requirements(requirements: str) -> Dict[str, Any]:
    """
    Validate the requirements text
    
    Args:
        requirements: The requirements text to validate
        
    Returns:
        Dictionary with validation result and message
    """
    if not requirements or not requirements.strip():
        return {"valid": False, "message": "Requirements text is empty"}
    
    if len(requirements) < 50:
        return {"valid": False, "message": "Requirements text is too short to generate meaningful test cases"}
    
    if len(requirements) > 10000:
        return {"valid": False, "message": "Requirements text is too long. Please keep it under 10,000 characters"}
    
    return {"valid": True, "message": "Requirements are valid"}

def validate_format(format_type: str, supported_formats: List[str]) -> Dict[str, Any]:
    """
    Validate the format type
    
    Args:
        format_type: The format type to validate
        supported_formats: List of supported formats
        
    Returns:
        Dictionary with validation result and message
    """
    if not format_type:
        return {"valid": False, "message": "Format type is required"}
    
    if format_type.lower() not in [f.lower() for f in supported_formats]:
        return {"valid": False, "message": f"Unsupported format. Supported formats: {', '.join(supported_formats)}"}
    
    return {"valid": True, "message": "Format is valid"}

def validate_refinement_feedback(feedback: str) -> Dict[str, Any]:
    """
    Validate the refinement feedback
    
    Args:
        feedback: The feedback text to validate
        
    Returns:
        Dictionary with validation result and message
    """
    if not feedback or not feedback.strip():
        return {"valid": False, "message": "Feedback text is empty"}
    
    if len(feedback) < 10:
        return {"valid": False, "message": "Feedback is too short to provide meaningful refinement"}
    
    if len(feedback) > 1000:
        return {"valid": False, "message": "Feedback is too long. Please keep it under 1,000 characters"}
    
    return {"valid": True, "message": "Feedback is valid"}