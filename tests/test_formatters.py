import unittest
from utlis.formatters import (
    format_test_cases_for_display, 
    format_traditional_for_display,
    format_gherkin_for_display,
    format_json_output
)

class TestFormatters(unittest.TestCase):
    """Test cases for formatter functions"""
    
    def test_format_traditional_for_display(self):
        """Test formatting traditional test cases for display"""
        test_cases = [
            {
                "id": "TC001",
                "title": "User Login",
                "preconditions": "User is registered",
                "steps": "1. Enter username\n2. Enter password\n3. Click login",
                "expected_results": "User is logged in",
                "priority": "High"
            }
        ]
        
        formatted = format_traditional_for_display(test_cases)
        
        self.assertIn("Test Case ID: TC001", formatted)
        self.assertIn("Title: User Login", formatted)
        self.assertIn("Preconditions: User is registered", formatted)
    
    def test_format_gherkin_for_display(self):
        """Test formatting Gherkin test cases for display"""
        test_cases = [
            {
                "feature": "User Authentication",
                "scenario": "Successful Login",
                "given": "User is registered",
                "when": "User enters valid credentials",
                "then": "User is logged in",
                "and": ["User sees dashboard", "User session is created"]
            }
        ]
        
        formatted = format_gherkin_for_display(test_cases)
        
        self.assertIn("Feature: User Authentication", formatted)
        self.assertIn("Scenario: Successful Login", formatted)
        self.assertIn("Given: User is registered", formatted)
        self.assertIn("When: User enters valid credentials", formatted)
        self.assertIn("Then: User is logged in", formatted)
        self.assertIn("- User sees dashboard", formatted)
    
    def test_format_test_cases_for_display_empty(self):
        """Test formatting empty test cases list"""
        formatted = format_test_cases_for_display([], "traditional")
        self.assertEqual(formatted, "No test cases generated.")
    
    def test_format_json_output(self):
        """Test formatting test cases as JSON with metadata"""
        test_cases = [
            {
                "id": "TC001",
                "title": "User Login",
                "preconditions": "User is registered",
                "steps": "1. Enter username\n2. Enter password\n3. Click login",
                "expected_results": "User is logged in",
                "priority": "High"
            }
        ]
        
        metadata = {"format_type": "traditional", "generated_at": "2023-01-01T00:00:00"}
        formatted = format_json_output(test_cases, metadata)
        
        self.assertEqual(formatted["test_cases"], test_cases)
        self.assertEqual(formatted["count"], 1)
        self.assertEqual(formatted["metadata"], metadata)

if __name__ == "__main__":
    unittest.main()