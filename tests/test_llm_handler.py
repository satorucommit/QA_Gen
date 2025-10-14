import unittest
from unittest.mock import patch, MagicMock
from core.llm_handler import LLMHandler

class TestLLMHandler(unittest.TestCase):
    """Test cases for LLMHandler class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.handler = LLMHandler(provider="gemini")
    
    @patch('core.llm_handler.genai.configure')
    @patch('core.llm_handler.genai.GenerativeModel')
    def test_gemini_initialization(self, mock_model, mock_configure):
        """Test Gemini client initialization"""
        handler = LLMHandler(provider="gemini")
        mock_configure.assert_called_once()
        mock_model.assert_called_once_with('gemini-pro')
    
    def test_unsupported_provider(self):
        """Test error handling for unsupported provider"""
        with self.assertRaises(ValueError):
            LLMHandler(provider="unsupported")
    
    @patch('core.llm_handler.genai.configure')
    @patch('core.llm_handler.genai.GenerativeModel')
    def test_generate_test_cases_gemini(self, mock_model, mock_configure):
        """Test test case generation with Gemini"""
        # Mock the Gemini response
        mock_response = MagicMock()
        mock_response.text = "Test case content"
        
        mock_client = MagicMock()
        mock_client.generate_content.return_value = mock_response
        mock_model.return_value = mock_client
        
        handler = LLMHandler(provider="gemini")
        result = handler.generate_test_cases("Test requirements", "traditional")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["content"], "Test case content")
    
    @patch('core.llm_handler.genai.configure')
    @patch('core.llm_handler.genai.GenerativeModel')
    def test_generate_test_cases_error(self, mock_model, mock_configure):
        """Test error handling in test case generation"""
        # Mock an exception
        mock_client = MagicMock()
        mock_client.generate_content.side_effect = Exception("API error")
        mock_model.return_value = mock_client
        
        handler = LLMHandler(provider="gemini")
        result = handler.generate_test_cases("Test requirements", "traditional")
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)

if __name__ == "__main__":
    unittest.main()