from setuptools import setup

setup(
    name="githelper",
    version="0.1",
    py_modules=["githelper"],
    entry_points={
        "console_scripts": [
            "githelper = githelper:main",
        ],
    },
    author="aalbrightpdx",
    description="Friendly Git assistant for staging, committing, and pushing safely.",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
    ],
    python_requires=">=3.6",
)

