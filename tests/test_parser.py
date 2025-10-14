import unittest
from core.parser import parse_test_cases, parse_traditional_format, parse_gherkin_format, parse_detailed_format

class TestParser(unittest.TestCase):
    """Test cases for parser functions"""
    
    def test_parse_traditional_format(self):
        """Test parsing traditional format test cases"""
        content = """
        Test Case ID: TC001
        Test Case Title: User Login
        Preconditions: User is registered
        Test Steps: 1. Enter username 2. Enter password 3. Click login
        Expected Results: User is logged in
        Priority: High
        
        Test Case ID: TC002
        Test Case Title: User Logout
        Preconditions: User is logged in
        Test Steps: 1. Click logout button
        Expected Results: User is logged out
        Priority: Medium
        """
        
        test_cases = parse_traditional_format(content)
        
        self.assertEqual(len(test_cases), 2)
        self.assertEqual(test_cases[0]["id"], "TC001")
        self.assertEqual(test_cases[0]["title"], "User Login")
        self.assertEqual(test_cases[1]["id"], "TC002")
        self.assertEqual(test_cases[1]["title"], "User Logout")
    
    def test_parse_gherkin_format(self):
        """Test parsing Gherkin format test cases"""
        content = """
        Feature: User Authentication
        
        Scenario: Successful Login
        Given User is registered
        When User enters valid credentials
        Then User is logged in
        And User sees dashboard
        
        Scenario: Failed Login
        Given User is registered
        When User enters invalid credentials
        Then User sees error message
        """
        
        test_cases = parse_gherkin_format(content)
        
        self.assertEqual(len(test_cases), 2)
        self.assertEqual(test_cases[0]["scenario"], "Successful Login")
        self.assertEqual(test_cases[1]["scenario"], "Failed Login")
    
    def test_parse_detailed_format(self):
        """Test parsing detailed format test cases"""
        content = """
        Test Case ID: TC001
        Test Case Title: User Login
        Test Objective: Verify user can login with valid credentials
        Preconditions: User is registered
        Test Data: Valid username and password
        Test Steps: 1. Enter username 2. Enter password 3. Click login
        Expected Results: User is logged in
        Postconditions: User session is created
        Priority: High
        Test Type: Functional
        """
        
        test_cases = parse_detailed_format(content)
        
        self.assertEqual(len(test_cases), 1)
        self.assertEqual(test_cases[0]["id"], "TC001")
        self.assertEqual(test_cases[0]["title"], "User Login")
        self.assertEqual(test_cases[0]["objective"], "Verify user can login with valid credentials")
    
    def test_parse_test_cases_unsupported_format(self):
        """Test parsing with unsupported format"""
        content = "Some test case content"
        test_cases = parse_test_cases(content, "unsupported")
        
        self.assertEqual(len(test_cases), 1)
        self.assertEqual(test_cases[0]["raw_content"], content)

if __name__ == "__main__":
    unittest.main()