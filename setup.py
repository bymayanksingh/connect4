from setuptools import setup, find_packages

setup(
    name="connect4",
    version="2.0.0",
    description="Production-grade Connect 4 engine, AI algorithms, and visualizer.",
    author="Mayank Singh",
    author_email="mayank.singh081997@gmail.com",
    packages=find_packages(include=["connect4", "connect4.*"]),
    python_requires=">=3.9",
    install_requires=[
        "pygame>=2.0.0",
        "numpy>=1.20.0",
        "event-bus>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "connect4=connect4.cli:main",
        ],
    },
)
