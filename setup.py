# setup.py
from setuptools import setup, find_packages

setup(
    name="zennix",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "typer",
        "groq",
        "setuptools"
    ],
    entry_points={
        'console_scripts': [
            'zennix=zennix.cli:main',
        ],
    },
)
