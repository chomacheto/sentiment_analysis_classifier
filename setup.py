#!/usr/bin/env python3
"""
Setup script for sentiment analysis classifier CLI.
"""

from setuptools import setup, find_packages

setup(
    name="sentiment-analysis-classifier",
    version="0.1.0",
    description="Sentiment Analysis Classifier using ML",
    author="Developer",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "torch>=2.8.0,<3.0.0",
        "transformers>=4.56.0,<5.0.0",
        "click>=8.1.0,<9.0.0",
        "pydantic>=2.11.0,<3.0.0",
        "structlog>=25.4.0,<26.0.0",
    ],
    entry_points={
        "console_scripts": [
            "sentiment-cli=apps.ml_pipeline.cli:cli",
        ],
    },
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
