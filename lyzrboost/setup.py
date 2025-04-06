import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lyzrboost",
    version="0.1.0",
    author="Lyzr AI",
    author_email="example@lyzr.ai",
    description="A Python package to simplify orchestration and debugging of Lyzr AI agents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lyzr-ai/lyzrboost",
    project_urls={
        "Bug Tracker": "https://github.com/lyzr-ai/lyzrboost/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.1",
        "pyyaml>=5.4.1",
    ],
    entry_points={
        "console_scripts": [
            "lyzrboost=lyzrboost.cli.main:main",
        ],
    },
) 