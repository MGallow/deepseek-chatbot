"""Setup script for deepseek_chatbot package."""

from setuptools import setup, find_packages

# Read the contents of README.md file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="deepseek-chatbot",
    version="0.1.0",
    description="A Streamlit-based chatbot for interacting with DeepSeek-V3 "
    "language model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="youremail@example.com",
    url="https://github.com/yourusername/deepseek-chatbot",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "deepseek-cli=deepseek_chatbot.cli:main",
            "deepseek-chat=deepseek_chatbot.app:run_app",
        ],
    },
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pre-commit>=3.0.0",
        ]
    },
    include_package_data=True,
)
