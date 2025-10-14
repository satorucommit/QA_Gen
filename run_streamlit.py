import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("Warning: .env file not found. Please create one with your GEMINI_API_KEY")
    
    # Run the Streamlit application
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()