"""
Setup configuration for Project Lexora
Enables installation with: pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="project-lexora",
    version="1.0.0",
    author="Chandan Malakar",
    author_email="your-email@example.com",
    description="RAG + LLM Chatbot for IT Act and Cyber Crime Law",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/askchandan/Project-Lexora",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pypdf>=3.0.0",
        "langchain>=1.0.0",
        "langchain-chroma>=0.1.0",
        "langchain-community>=0.0.0",
        "langchain-core>=0.1.0",
        "langchain-openai>=0.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lexora-populate=scripts.populate_database:main",
            "lexora-query=scripts.query:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
