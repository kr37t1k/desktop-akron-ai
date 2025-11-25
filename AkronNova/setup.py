#!/usr/bin/env python3
"""
Setup script for AkronNova Desktop AI Companion
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="akronnova",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An animated desktop AI companion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/akronnova",
    packages=find_packages(where="src", include=["akronnova", "akronnova.*"]),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyQt5>=5.15.0",
        "requests>=2.25.0",
        "Pillow>=8.0.0",
        "pyaudio>=0.2.11",
        "SpeechRecognition>=3.8.0",
    ],
    entry_points={
        "console_scripts": [
            "akronnova=akronnova.main:main",
        ],
    },
)