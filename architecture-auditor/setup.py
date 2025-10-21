#!/usr/bin/env python3
"""
Architecture Auditor Pro - Enterprise Setup Configuration
Professional code quality and architecture analysis tool
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from VERSION file
version_file = Path(__file__).parent / "VERSION"
with open(version_file, "r", encoding="utf-8") as f:
    version = f.read().strip()

# Read long description from README
readme_file = Path(__file__).parent / "README.md"
with open(readme_file, "r", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
with open(requirements_file, "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="architecture-auditor-pro",
    version=version,
    description="Enterprise-Grade Architecture & Clean Code Analysis Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Juan José Sáez",
    author_email="juanjovip2490@gmail.com",
    url="https://github.com/juanjovip2490/architecture-auditor",
    project_urls={
        "Documentation": "https://github.com/juanjovip2490/architecture-auditor/blob/main/enterprise-architecture-patterns.html",
        "Source Code": "https://github.com/juanjovip2490/architecture-auditor",
        "Bug Tracker": "https://github.com/juanjovip2490/architecture-auditor/issues",
        "Clean Code Reference": "https://github.com/juanjovip2490/CLEAN-CODE-AND-ARCHITECTURES",
    },
    packages=find_packages(exclude=["tests*", "docs*"]),
    py_modules=["src.architecture_auditor", "src.report_generator"],
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "isort>=5.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "pylint>=2.6",
        ],
        "enterprise": [
            "pandas>=1.3.0",
            "matplotlib>=3.3.0",
            "jinja2>=3.0.0",
            "pyyaml>=5.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "architecture-auditor=src.architecture_auditor:main",
            "audit-pro=src.architecture_auditor:main",
            "generate-report=src.report_generator:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Environment :: Console",
        "Natural Language :: English",
        "Natural Language :: Spanish",
    ],
    keywords=[
        "code-quality", "architecture", "clean-code", "static-analysis",
        "software-engineering", "design-patterns", "solid-principles",
        "technical-debt", "code-review", "enterprise", "auditor",
        "robert-martin", "uncle-bob", "mvc", "hexagonal-architecture"
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        "": [
            "*.json",
            "*.html",
            "*.md",
            "*.txt",
            "config/*.json",
            "rules/*.json",
            "templates/*.html",
        ],
    },
    zip_safe=False,
    platforms=["any"],
)