import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("Warning: .env file not found. Please create one based on .env.example")
    
    # Check if Gemini API key is set
    if not os.getenv("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY not found in environment variables")
    
    # Run the Streamlit application
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()