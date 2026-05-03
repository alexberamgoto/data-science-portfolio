#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="spark-bigdata-project",
    version="1.0.0",
    author="Alexis Djekounmian",
    description="Big Data project for social media events analysis using Spark, Kafka, and HDFS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexberamgoto/spark-bigdata-project",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pyspark==3.5.0",
        "kafka-python==2.0.2",
        "pandas==2.0.3",
        "numpy==1.24.3",
        "pyarrow==12.0.1",
        "pyyaml==6.0",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.0",
            "black==23.7.0",
            "flake8==6.0.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
)
