import os
import json
from typing import Dict, List, Optional, Union
import google.generativeai as genai
from config.settings import GEMINI_API_KEY

class LLMHandler:
    """Handler for LLM API interactions with Gemini"""
    
    def __init__(self, provider: str = "gemini"):
        self.provider = provider.lower()
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Gemini client"""
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key not found in environment variables")
        
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
        from core.prompt_templates import get_system_prompt, get_user_prompt
        
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