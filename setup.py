#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the README file for the long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="recirc",
    version="0.1.0",
    author="LAJIidea",
    author_email="",
    description="A Python DSL for processor architecture description and hardware generation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/LAJIidea/Recirc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research", 
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Core dependencies
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
            "mypy",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ],
    },
    entry_points={
        "console_scripts": [
            "recirc=recirc.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)