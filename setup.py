from setuptools import setup, find_packages

setup(
    name="qa-test-case-generator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.29.0",
        "google-generativeai==0.3.2",
        "python-docx==1.1.0",
        "pandas>=2.2.0",
        "python-dotenv==1.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A Streamlit application that generates test cases from requirements using Google's Gemini AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/qa-test-case-generator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)